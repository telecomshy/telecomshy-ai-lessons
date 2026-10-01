"""LLM 底层 · 第 1 课 配套脚本：「按百分比抽一个」到底是怎么抽的。

对应进阶版 Q9。它不碰模型内部，只做最后那一步「挑字」：
    原始分(logits) -> [采样参数都在这儿动手] -> 挑出一个 token
你会看到四个旋钮各自在改什么：
    temperature  换算百分比之前，先把所有分数除以 T（调「锐度」）
    top_k        只留分数最高的 k 个，其余直接出局
    top_p        从高到低累加百分比，加够 p 就停，剩下的出局
    seed         让「抽」这个动作可复现

⚠ 起点那五个原始分是手编的（挑了五个「下一个字」的候选）。
  真实模型的候选是整个词表（十几万个），但「挑」的规则一模一样。

运行：  python exercises/llm/0001-sampling-params.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

import random

# ============ 起点：一张已经打好的分表（logits） ============
# 这就是模型最后吐出来的那张「每个候选各得多少原始分」的表。
CANDIDATES = ["好", "冷", "坏", "差", "热"]
LOGITS = [2.469, 1.595, 1.192, 0.796, 0.414]

E = 2.718281828


# ============ 小工具 ============
def to_percent(scores):
    """把一堆任意分数换算成百分比（加起来 = 100%）。这一步叫 softmax。"""
    biggest = max(scores)
    exps = [pow(E, s - biggest) for s in scores]
    total = sum(exps)
    return [e / total for e in exps]


def line(title, probs, alive=None):
    """一行打完：每个候选的百分比；被砍掉的标成 ✗。"""
    print("      " + title)
    for c, p in zip(CANDIDATES, probs):
        mark = "  " if (alive is None or alive[c]) else "✗ "
        print(f"        {mark}「{c}」 {p * 100:5.1f}%")


def keep_top_k(probs, k):
    """top_k：只留分数（这里等价于百分比）最高的 k 个。"""
    order = sorted(range(len(probs)), key=lambda i: probs[i], reverse=True)
    alive = {c: False for c in CANDIDATES}
    for i in order[:k]:
        alive[CANDIDATES[i]] = True
    return alive


def keep_top_p(probs, p):
    """top_p（核采样）：从高到低累加，加够 p 就停。留下的那个集合叫「核」。"""
    order = sorted(range(len(probs)), key=lambda i: probs[i], reverse=True)
    alive = {c: False for c in CANDIDATES}
    acc = 0.0
    for i in order:
        alive[CANDIDATES[i]] = True
        acc += probs[i]
        if acc >= p:
            break
    return alive


def renorm(probs, alive):
    """砍完之后重新换算百分比（剩下的加起来还是 100%）。"""
    total = sum(p for c, p in zip(CANDIDATES, probs) if alive[c])
    return [p / total if alive[c] else 0.0 for c, p in zip(CANDIDATES, probs)]


def draw(probs, n, seed):
    """按百分比抽 n 次，统计各候选被抽中的次数。"""
    rng = random.Random(seed)
    hits = {c: 0 for c in CANDIDATES}
    for _ in range(n):
        hits[rng.choices(CANDIDATES, weights=probs, k=1)[0]] += 1
    return hits


def show_hits(hits, n):
    print("        " + "   ".join(f"「{c}」{h / n * 100:4.1f}%" for c, h in hits.items()))


# ============ [1] 起点 ============
print("[1] 起点：模型吐出来的那张分表（logits，原始分）")
for c, s in zip(CANDIDATES, LOGITS):
    print(f"      「{c}」 {s:.3f}")
print("      ——到这一步为止，模型的工作已经结束了。下面全是「怎么挑」。")

# ============ [2] temperature ============
print("\n[2] 旋钮① temperature：换算百分比之前，先把所有分数除以 T")
print("      （除以 T 只改「差距有多悬殊」，不改谁高谁低的名次）")
for t in [0.2, 0.5, 1.0, 2.0]:
    scaled = [s / t for s in LOGITS]
    probs = to_percent(scaled)
    print(f"      T = {t:<4} 换算后的百分比：")
    print("        " + "   ".join(f"「{c}」{p * 100:4.1f}%" for c, p in zip(CANDIDATES, probs)))
print("      看「好」这一列：T 越小 -> 一家独大；T 越大 -> 越接近平均。")

# ============ [3] T 推到头 ============
print("\n[3] 把 T 推到头会怎样？")
greedy = CANDIDATES[LOGITS.index(max(LOGITS))]
print(f"      T -> 0 时百分比会塌成一个点，于是「按百分比抽」退化成「永远挑最高分」")
print(f"            -> 「{greedy}」。这种挑法叫【贪心 greedy】，不是采样。")
print("      T = 1 时分数原样不动，换算出来的就是模型给的那个分布本身。")

# ============ [4] top_k ============
print("\n[4] 旋钮② top_k：只留分数最高的 k 个，其余直接出局（不看百分比攒到多少）")
base = to_percent(LOGITS)
for k in [1, 2, 3]:
    alive = keep_top_k(base, k)
    kept = [c for c in CANDIDATES if alive[c]]
    print(f"      k = {k}  留下 {len(kept)} 个：{'、'.join('「' + c + '」' for c in kept)}"
          f"   砍掉 {len(CANDIDATES) - len(kept)} 个")

# ============ [5] top_p ============
print("\n[5] 旋钮③ top_p（核采样）：从高到低累加百分比，加够 p 就停")
print("      （留下的那个集合叫「核 nucleus」——它有多大，由分布自己的形状决定）")
order = sorted(range(len(CANDIDATES)), key=lambda i: base[i], reverse=True)
print("        从高到低累加：" + "   ".join(
    f"「{CANDIDATES[i]}」{base[i] * 100:.1f}%" for i in order))
for p in [0.6, 0.8, 0.95]:
    alive = keep_top_p(base, p)
    kept = [c for c in CANDIDATES if alive[c]]
    acc = sum(base[CANDIDATES.index(c)] for c in kept)
    print(f"      p = {p}  留下 {len(kept)} 个：{'、'.join('「' + c + '」' for c in kept)}"
          f"   （累计 {acc * 100:.1f}%）")
print("      对比 top_k：k 是「按个数砍」，p 是「按攒够多少砍」。")
print("      分布尖的时候 p 自动少留几个，分布平的时候 p 自动多留几个——这正是它比 top_k 好用的地方。")
print("      注意 p = 0.95：连累加到底都攒不够，于是谁也没被砍——p 只砍「尾巴」，不会硬砍。")

# ============ [6] 顺序 ============
print("\n[6] 叠着用：通行顺序是 先温度 -> 再 top_k -> 再 top_p -> 最后抽")
t = 0.7
k = 4
p = 0.9
probs = to_percent([s / t for s in LOGITS])
line(f"① 温度 T = {t} 之后：", probs)
alive = keep_top_k(probs, k)
probs = renorm(probs, alive)
line(f"② 再 top_k = {k} 之后（砍完重新换算百分比）：", probs, alive)
alive = keep_top_p(probs, p)
probs = renorm(probs, alive)
line(f"③ 再 top_p = {p} 之后：", probs, alive)
print("      ② 是 top_k 按「个数」砍掉「热」，③ 是 top_p 按「攒够多少」再砍掉「差」。")
print("      两把刀各砍各的，叠着用的时候，起作用的往往是更紧的那把。")

# ============ [7] seed ============
print("\n[7] 旋钮④ seed：让「抽」这个动作可复现")
flat = to_percent(LOGITS)
for s in [7, 7, 8]:
    rng = random.Random(s)
    picks = "".join(rng.choices(CANDIDATES, weights=flat, k=6))
    print(f"      seed = {s}  连抽 6 次：{picks}")
print("      seed 相同 -> 抽出来的序列一模一样；seed 不同 -> 序列不同。")
print("      （种子固定的是「抽」这一步的运气，不是模型算出来的分。）")

# ============ [8] 实测分布 ============
print("\n[8] 每种旋钮各抽 2000 次，看真实的落点分布（种子固定，你我看到同一份）")
N = 2000
for label, pr in [
    ("T = 0.5（偏尖）          ", to_percent([s / 0.5 for s in LOGITS])),
    ("T = 1.0（模型原分布）    ", to_percent(LOGITS)),
    ("T = 2.0（偏平）          ", to_percent([s / 2.0 for s in LOGITS])),
]:
    print(f"      {label}")
    show_hits(draw(pr, N, seed=42), N)
alive = keep_top_p(to_percent(LOGITS), 0.7)
pr = renorm(to_percent(LOGITS), alive)
print("      T = 1.0 + top_p = 0.7（只留下「好」「冷」，其余三个永远抽不到）")
show_hits(draw(pr, N, seed=42), N)

print("\n一句话收尾：模型只负责给出那张分表；")
print("【怎么挑】由你随请求传的采样参数决定，【真正在挑】的是跑模型的那个推理引擎。")
