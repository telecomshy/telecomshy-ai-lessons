"""LLM 底层 · 第 5 课 配套脚本：把模型权重「压小」，看看压掉的是什么。

这一课只讲一件事：量化省的是【搬运量】，所以它只救 decode，不救 prefill。

量化 = 换一种存法。把每个权重从 float32（占 4 字节）改成低精度整数
（4 bit 只占 0.5 字节），体积跟着变小，模型每吐一个字要搬的货也跟着变少。

但你马上会看到两个反直觉的事实：
  1. 数字变小不等于「随便压」——要用一把合适的尺子，误差小很多
  2. 压得越狠，模型能力真的会掉（第 0 课那个玩具模型的扣分会变差）

你会看到六件事：
  1. float32 -> int8：体积掉到 1/4，但一把尺子量整张表，小数全被压扁
  2. 误差出在哪：绝对误差到处都差不多，差的是「相对自己量级」的大小
  3. 换三种尺子（整表 / 每列 / 每 32 个一组）—— 误差和体积的取舍
  4. 压到 4 bit：bit 减半，误差大约翻倍
  5. 算笔账：连刻度本身的开销算进去，每个权重实际占几个字节
     （算出来的 8.5 / 4.5，和 llama.cpp 官方公布的数字对得上）
  6. 能力掉没掉：把第 0 课训练出来的玩具模型压一遍，看平均扣分

运行：  python exercises/llm/0005-quantization.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

import math
import random

VOCAB = ["天", "气", "很", "好", "冷", "差", "雨"]
CORPUS_A = ["天气很好", "天气很冷", "天气很差", "雨天很好", "雨天很冷", "雨天很差"]

ROWS, COLS = 8, 512          # 假权重表：8 行 x 512 列 = 4096 个数
GROUP = 32                   # 「每 32 个数一把尺子」


# ============ 小工具 ============
def to_percent(scores):
    biggest = max(scores)
    exps = [pow(2.718281828, s - biggest) for s in scores]
    total = sum(exps)
    return [e / total for e in exps]


def loss_of(row, y):
    """一道题扣多少分（扣分 = -log(正确答案拿到的百分比)）。"""
    return -math.log(to_percent(row)[VOCAB.index(y)])


def average_loss(W, pairs):
    return sum(loss_of(W[x], y) for x, y in pairs) / len(pairs)


def dwidth(s):
    """中文按两格宽算，不然表格对不齐。"""
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


def pad(s, width):
    return s + " " * max(0, width - dwidth(s))


def lpad(s, width):
    return " " * max(0, width - dwidth(s)) + s


# ============ 第 0 课那个玩具模型（这里只借用它的训练过程） ============
def train_toy(epochs=1200, seed=7, lr=0.2):
    """和第 0 课一模一样的训练：出题 -> 作答 -> 扣分 -> 拧一点点。"""
    rng = random.Random(seed)
    W = {a: [rng.uniform(-1.0, 1.0) for _ in VOCAB] for a in VOCAB}
    pairs = [(a, b) for s in CORPUS_A for a, b in zip(s, s[1:])]
    for _ in range(epochs):
        rng.shuffle(pairs)
        for x, y in pairs:
            probs = to_percent(W[x])
            for i, p in enumerate(probs):
                W[x][i] -= lr * (p - (1.0 if VOCAB[i] == y else 0.0))
    return W, pairs


# ============ 量化：核心就是「一把尺子 + 取整」 ============
def build_scales(values, bits, per, cols):
    """决定「谁跟谁共用一把尺子」。共用得越细，误差越小、刻度越占地方。

    返回与 values 等长的列表，第 i 项就是第 i 个数用的那把尺子。
    """
    limit = 2 ** (bits - 1) - 1          # 8 bit -> 127；4 bit -> 7

    if per == "tensor":
        m = max(abs(v) for v in values)
        return [m / limit] * len(values)

    if per == "column":
        # values 按行平铺，每 cols 个数是一行；真实矩阵里就是「每个输入通道一把」
        tops = [max(abs(v) for v in values[c::cols]) for c in range(cols)]
        return [tops[i % cols] / limit for i in range(len(values))]

    scales = []
    for start in range(0, len(values), GROUP):
        block = values[start:start + GROUP]
        scales.extend([max(abs(v) for v in block) / limit] * len(block))
    return scales


def quantize(values, bits, per, cols=COLS):
    """把一组 float32 的数压成低精度整数，再乘回刻度（假装没压过）。

    这就是量化的全部数学：找一把尺子，量出格子有多粗，
    每个数按格子取整。取整这一步丢掉的，就是误差。
    """
    limit = 2 ** (bits - 1) - 1
    scales = build_scales(values, bits, per, cols)
    out = []
    for v, s in zip(values, scales):
        q = max(-limit - 1, min(limit, round(v / s)))   # 夹在量程内，再取整
        out.append(q * s)                               # 这一格代表多少，乘回去
    return out


def report(values, restored, cols=COLS):
    """三个数：最大误差、平均误差，以及「一半的列相对自己量级差多少」。

    第三个用中位数，因为少数离群列会把平均值撑得看不出差别。
    """
    errs = [abs(a - b) for a, b in zip(values, restored)]
    rows = len(values) // cols
    rels = []
    for c in range(cols):
        idxs = [r * cols + c for r in range(rows)]
        top = max(abs(values[i]) for i in idxs)
        rels.append(sum(errs[i] for i in idxs) / len(idxs) / top)
    rels.sort()
    return max(errs), sum(errs) / len(errs), rels[len(rels) // 2]


def bits_per_weight(bits, n, group_size=None):
    """每个权重实际占几个 bit —— 刻度本身也要存，所以比 bits 略大。

    真实做法里刻度用 float16（2 字节）存，这里照抄。
    """
    if group_size is None:
        return bits + 2 * 8 / n              # 整表一把尺子：开销可忽略
    return bits + 2 * 8 / group_size         # 每组一把：多出 2 字节 / 组


# ============ [1] 一张假权重表 ============
print("[1] 先造一张「假权重表」，它代表真实模型里几十亿个数中的一个矩阵")
rng = random.Random(11)
base = [rng.gauss(0.0, 1.0) for _ in range(ROWS * COLS)]
# 关键设定：少数几列的数值明显比别的大（真实权重矩阵里就是这样，
# 少数通道承担了大部分信息量）
outlier_cols = [7, 42, 130, 300, 411]
for c in outlier_cols:
    for r in range(ROWS):
        base[r * COLS + c] *= 12.0

col_scale = [max(abs(base[r * COLS + c]) for r in range(ROWS)) for c in range(COLS)]
plain = sorted(col_scale[:7] + col_scale[8:42])
print(f"      形状 {ROWS} 行 x {COLS} 列 = {ROWS * COLS} 个权重")
print(f"      绝大多数列的量级中位数 = {plain[len(plain) // 2]:.3f}")
print("      但有几列特别大：")
for c in outlier_cols:
    print(f"        第 {c:3d} 列，最大值 = {col_scale[c]:6.2f}")
print("      ——一把尺子量全表，量程被这几列吃光了，其余列全被压扁。")

# ============ [2] float32 -> int8 ============
fp32_bytes = ROWS * COLS * 4
i8 = quantize(base, 8, per="tensor")
print("\n[2] 换一种存法：float32 -> int8（一把尺子量整张表）")
print(f"      float32：每个权重 32 bit = 4 字节 -> 全表 {fp32_bytes} 字节")
print(f"      int8   ：每个权重  8 bit = 1 字节 -> 全表 {ROWS * COLS + 4} 字节（含 4 字节刻度）")
print(f"      体积掉到 {(ROWS * COLS + 4) / fp32_bytes:.1%}，但每个数只能落在 "
      f"{max(abs(v) for v in base) / 127:.4f} 的格子里")
mx, avg, rel = report(base, i8)
print(f"      最大误差 {mx:.4f}，平均误差 {avg:.4f}，"
      f"一半的列相对自己量级差 {rel:.1%}")

# ============ [3] 误差来自哪 ============
print("\n[3] 误差出在哪：绝对误差到处都差不多，差的是「相对自己量级」")
print(f"      {'列':>5}{'这一列最大值':>14}{'平均绝对误差':>14}{'相对误差':>10}")
for c in [0, 1, 2, 42, 130]:
    idxs = [r * COLS + c for r in range(ROWS)]
    top = max(abs(base[i]) for i in idxs)
    err = sum(abs(base[i] - i8[i]) for i in idxs) / len(idxs)
    print(f"      {c:>5}{top:>14.3f}{err:>14.4f}{err / top:>9.1%}")
print("      ——绝对误差都是 0.06 上下，一模一样；可是除以自己量级，")
print("         普通列差 3~4%，大列只差 0.2%。被压扁的是小数，不是大数。")

# ============ [4][5] 换三种尺子，8 bit 与 4 bit ============
SCHEMES = [("整表一把尺子", "tensor", None),
           ("每列一把尺子", "column", None),
           (f"每 {GROUP} 个一把", "group", GROUP)]

for step, bits in enumerate((8, 4), start=4):
    head = ("换三种尺子：共用得越细，误差越小、刻度越占地方" if bits == 8
            else "再压：4 bit，每一格是上一档的两倍宽")
    print(f"\n[{step}] {head}（{bits} bit）")
    print(f"      {pad('方案', 22)}{lpad('最大误差', 11)}{lpad('平均误差', 11)}"
          f"{lpad('一半的列相对误差', 17)}{lpad('实际 bit/权重', 16)}")
    for label, per, gs in SCHEMES:
        r = quantize(base, bits, per=per)
        mx, avg, rel = report(base, r)
        bpw = bits_per_weight(bits, ROWS * COLS, gs)
        print(f"      {pad(label, 22)}{lpad(f'{mx:.4f}', 11)}{lpad(f'{avg:.4f}', 11)}"
              f"{lpad(f'{rel:.2%}', 17)}{lpad(f'{bpw:.3f}', 16)}")
    if bits == 8:
        print("      ——整表一把差 3.4%，细分之后掉到 0.2% 上下：一个数量级。")
        print("      ——注意「每列一把」反而比「每 32 个一把」更准。这不是脚本算错：")
        print("         这张表里每一列的量级本来就一样，所以按列切正好切在量级边界上；")
        print("         而 32 个一组会把 32 个不同量级的列混进一把尺子里。")
        print("         真实权重矩阵里同一列内部的量级并不整齐，所以才轮到「每 32 个一组」")
        print("         （llama.cpp 的老格式就叫 Q4_0）这种折中。")
    else:
        print("      ——4 bit 的格子太粗：整表一把已经差 45%，细分之后也只剩 3%。")

print("\n[5b] 对比 8 bit 与 4 bit（都用「每 32 个一把」）")
for bits in (8, 4):
    r = quantize(base, bits, per="group")
    mx, avg, rel = report(base, r)
    print(f"      {bits} bit：最大误差 {mx:.4f}，平均误差 {avg:.4f}，"
          f"一半的列相对自己量级差 {rel:.2%}，"
          f"实际 {bits_per_weight(bits, ROWS * COLS, GROUP):.3f} bit/权重")
print("      ——bit 减半，误差大约翻倍。这条曲线就是「省多少 vs 掉多少」的取舍。")

# ============ [6] 真实模型的账 ============
print("\n[6] 换成真实模型的账：一个 8B 参数的模型，各种存法各占多大")
print(f"      {pad('存法', 26)}{lpad('每个权重', 11)}{lpad('8B 模型体积', 15)}{lpad('相对 float32', 15)}")
n_params = 8_000_000_000
ref = n_params * 4 / 1e9
for label, bits, gs in [("float32", 32, None), ("float16", 16, None),
                        ("int8", 8, None),
                        (f"int4（每 {GROUP} 个一把尺子）", 4, GROUP)]:
    gb = n_params * bits / 8 / 1e9 + (n_params / gs * 2 / 1e9 if gs else 0)
    print(f"      {pad(label, 26)}{lpad(f'{bits} bit', 11)}{lpad(f'{gb:.1f} GB', 15)}"
          f"{lpad(f'{gb / ref:.1%}', 15)}")
print("      ——这就是「8B 模型能塞进普通笔记本」的账。")
print(f"      ——刻度开销已经算进去了：4 bit 那行是 {bits_per_weight(4, n_params, GROUP):.2f}，"
      f"不是 4.00；8 bit 那行是 {bits_per_weight(8, n_params, GROUP):.2f}。")
print("         llama.cpp 官方公布的实测值是 8.5008 和 4.5，一模一样（课里会用到）。")

# ============ [7] 能力掉没掉 ============
print("\n[7] 最要紧的一问：压完，模型还能不能用？拿第 0 课那个玩具模型试")
W, pairs = train_toy()
flat = [v for row in W.values() for v in row]      # 7 x 7 = 49 个权重


def restore_toy(bits):
    # 每 len(VOCAB) 个数一把尺子——玩具表是 7x7，「列」就是 7 个下一字候选
    r = quantize(flat, bits, per="column", cols=len(VOCAB))
    out, i = {}, 0
    for ch in VOCAB:
        out[ch] = r[i:i + len(VOCAB)]
        i += len(VOCAB)
    return out


def show_row(label, Wd):
    print(f"      {label}看「很」：" + "  ".join(
        f"「{b}」{p * 100:5.1f}%" for b, p in zip(VOCAB, to_percent(Wd["很"]))))


base_loss = average_loss(W, pairs)
show_row("float32 ", W)
print(f"      float32（没压）    平均扣分 {base_loss:.4f}")
for bits in (8, 4):
    Q = restore_toy(bits)
    d = average_loss(Q, pairs) - base_loss
    print(f"      int{bits}（每行一把）  平均扣分 {average_loss(Q, pairs):.4f}   变化 {d:+.4f}")
    show_row(f"int{bits:<7}", Q)
print("      ——int8 扣分几乎没动（+0.0003），int4 也只差 0.0023。看「很」那一行，")
print("         四个候选的百分比基本照旧，连排序都没变。")
print("      ——别急着把它读成「量化不掉能力」。这个玩具只有 18 道题、7 个候选字，")
print("         「能力」只有一个刻度，太粗了。真模型上能力是用几万道题测的，")
print("         那里掉一点就是掉分数——所以各家论文都要跑一整套 benchmark 才敢下结论。")

# ============ [8] 收尾 ============
print("\n[8] 一句话")
print("      量化不改模型【学到了什么】，只改【每个数占几个字节】——")
print("      而模型每吐一个字都要把整张权重表搬一遍，所以字节少了，decode 就快了。")
print("      代价是每个数只能落在格子上：格子越粗，模型越糊。")
print("      （真模型上有专门的算法挑格子：AWQ 说「保护 1% 关键的权重就够了」，")
print("       GPTQ 用二阶信息逐个补偿；llama.cpp 的 K-quant 用 256 个数一个超块摊平刻度开销。）")