"""LLM 底层 · 第 2 课 配套脚本：为什么"前缀的字不用回头看前面"是错的。

一个很容易想到、但**是错的**想法：
    "第 1 轮不就是为了预测第一个字吗？前面那些字只要把 k、v 提供出来就行，
     它们自己**不用**回头看前面的字、不用算自己的注意力。"

本脚本用一个 4 层的玩具模型把这件事算给你看：
    让中间某个字"不回头看前面"，然后量一量**最后一个位置**的最终向量变了多少。

⚠ 所有数字都是手编的、故意很小，只为看清「依赖关系」，不是真实性能。
  运行：  python exercises/llm/0002-why-all-positions.py
  Windows 终端若中文乱码：先执行  chcp 65001
"""

import math
import random

random.seed(11)                 # 固定随机数，每次跑结果一样，方便对照

D = 4                          # 每个向量 4 个数
LAYERS = 4                     # 4 层
TOKENS = ["天", "气", "很"]      # 已写出来的 3 个 token
CANDIDATES = ["好", "差", "冷"]   # 下一个 token 的候选

# 第 0 层：刚查完嵌入表时，每个 token 的「此刻的理解」
X = {
    "天": [1.0, 0.0, 0.0, 0.5],
    "气": [0.8, 0.6, 0.0, 0.4],
    "很": [0.2, 0.1, 1.0, 0.0],
}


# ============ 小工具 ============
def matvec(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def rand_mat(rows, cols, scale):
    return [[round(random.uniform(-scale, scale), 3) for _ in range(cols)]
            for _ in range(rows)]


def softmax(scores):
    m = max(scores)
    e = [math.exp(s - m) for s in scores]
    t = sum(e)
    return [x / t for x in e]


def show(v):
    return "[" + ", ".join(f"{x:+.3f}" for x in v) + "]"


def linf(a, b):
    """两个向量差多少（取差得最大的那一维）"""
    return max(abs(x - y) for x, y in zip(a, b))


# **每一层都有自己的一套参数**——这正是整个现象的来源
LAYER_W = [{
    "Wq": rand_mat(D, 2, 0.7), "Wk": rand_mat(D, 2, 0.7), "Wv": rand_mat(D, D, 0.7),
    "W1": rand_mat(D, D, 0.5), "W2": rand_mat(D, D, 0.5),
} for _ in range(LAYERS)]
W_OUT = {c: rand_mat(1, D, 0.4)[0] for c in CANDIDATES}


def attention(layer_in, w, blind):
    """算所有位置的注意力。blind = 哪个位置「假装不回头看前面」。"""
    q = {t: matvec(w["Wq"], layer_in[t]) for t in TOKENS}
    k = {t: matvec(w["Wk"], layer_in[t]) for t in TOKENS}
    v = {t: matvec(w["Wv"], layer_in[t]) for t in TOKENS}
    out = {}
    for idx, t in enumerate(TOKENS):
        seen = [t] if idx == blind else TOKENS[:idx + 1]   # [t] = 只看自己 ← 那个错想法
        scores = [sum(a * b for a, b in zip(q[t], k[u])) / math.sqrt(len(q[t]))
                  for u in seen]
        wts = softmax(scores)
        out[t] = [sum(wt * v[u][i] for wt, u in zip(wts, seen)) for i in range(D)]
    return out


def ffn(vec, w):
    return matvec(w["W2"], [max(0.0, v) for v in matvec(w["W1"], vec)])


def forward(blind=None, upto=None):
    """跑到第 upto 层，返回 (最后一个位置的向量, 对词表各词的原始分)。"""
    cur = dict(X)
    for w in LAYER_W[:upto]:
        att = attention(cur, w, blind)
        # 残差 → FFN → 残差：这行数字被改写后，下一层才拿它投影出 k、v
        cur = {t: [a + b for a, b in zip(cur[t], att[t])] for t in TOKENS}
        cur = {t: [a + b for a, b in zip(cur[t], ffn(cur[t], w))] for t in TOKENS}
    last = cur["很"]
    return last, {c: sum(a * b for a, b in zip(W_OUT[c], last)) for c in CANDIDATES}


if __name__ == "__main__":
    print(f"3 个 token：{'  '.join(TOKENS)}    共 {LAYERS} 层")
    print("盯的是**最后一个位置**（「很」那一行）的最终向量和对下一个字的预测。\n")

    base_vec, base_log = forward()

    print("=" * 66)
    print("让某个字「不回头看前面」，看最后一个位置偏了多少")
    print("=" * 66)
    for i, t in enumerate(TOKENS[:-1]):
        v, lg = forward(blind=i)
        d = linf(base_vec, v)
        dl = max(abs(lg[c] - base_log[c]) for c in CANDIDATES)
        extra = "（它本来就没有「前面」可看）" if d < 1e-9 else ""
        print(f"  若「{t}」不回头看：最终向量最大差 {d:.4f}，原始分最大差 {dl:.4f}  {extra}")
    print()
    print(f"  正常时最后一个位置的向量 = {show(base_vec)}")
    print(f"  对下一个字的原始分        = "
          + "   ".join(f"「{c}」{base_log[c]:+.3f}" for c in CANDIDATES))
    p = softmax([base_log[c] for c in CANDIDATES])
    print("  换算成百分比              = "
          + "   ".join(f"「{c}」{p[i]*100:5.1f}%" for i, c in enumerate(CANDIDATES)))
    print()

    print("=" * 66)
    print("关键：这个偏差会**一层一层放大**")
    print("=" * 66)
    print("  （让「气」不回头看，每跑完一层就量一次最后一个位置的向量偏差）\n")
    for L in range(1, LAYERS + 1):
        ref, _ = forward(upto=L)
        v, _ = forward(blind=1, upto=L)
        print(f"    跑完第 {L} 层    偏差 {linf(ref, v):.4f}")
    print()
    print("=" * 66)
    print()
    print("看到了吗：")
    print()
    print("  【最关键的一行是「跑完第 1 层 偏差 0.0000」】")
    print("    位置 2 在第 1 层明明变了，可最后那个位置**一点没受影响**。")
    print("    因为第 1 层里，位置 3 读的是位置 2 的 k、v——而那两个数是从**第 0 层")
    print("    的嵌入**投影出来的，还没混进位置 2 的注意力结果。")
    print()
    print("    位置 2 的注意力结果要到**第 2 层**才被位置 3 读到（那时候它的 k、v")
    print("    是从「第 1 层改写后的那行数字」投影的）。偏差就是从这一层开始冒出来的。")
    print()
    print("  这就是为什么**前缀位置一个都省不掉**：它们的注意力结果不是终点，")
    print("  而是**下游每一层都要接着用的原料**。")
    print()
    print("  位置 1 那行是 0.0000，是因为它**本来就没有「前面」可看**——")
    print("    这正好反证了：影响不是凭空来的，而是它的注意力真的被用掉了。")
    print()
    print("所以：")
    print("  · 要算出最后一个位置的预测，**前面每个位置、每一层的注意力都得算**——")
    print("    一个都省不掉。")
    print("  · 真正只算最后一个位置的，只有**最后那一步「打分」**（对词表对分）。")
    print("    前面每个位置也各自出了个预测，但推理时没人要，**那才是被丢掉的部分**。")
