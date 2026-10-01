"""LLM 底层 · 第 1 课 配套脚本：一台玩具级的「下一个 token」流水线。

它把整条链走一遍，每一步都打印出来——注意流动的始终是「向量」（就是一串数字）：
  token -> 变成向量 -> 注意力(看一眼前文) -> 残差(留一份原来的)
        -> FFN(自己再加工) -> 打分 -> 换算成百分比 -> 采样

⚠ 所有数字都是手编的、故意很小，只为让你看清「流程」。
  真实模型：向量几千个数、几十层、词表十几万，而且整句是一起并行算的。
  这里只做 1 层，FFN 也是极度简化的，所以结果本身没有实际意义。

运行：  python exercises/llm/0001-tiny-attention.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

import random

# ============ 准备：这台玩具模型认识的东西 ============
TOKENS = ["天", "气", "很"]          # 已经写出来的 3 个 token
CANDIDATES = ["好", "差", "冷"]       # 词表里，下一个 token 的候选

# 每个 token 的「此刻的理解」：4 维向量（就是 4 个数的一串，手编）
X = {
    "天": [1.0, 0.0, 0.0, 0.5],
    "气": [0.8, 0.6, 0.0, 0.4],
    "很": [0.2, 0.1, 1.0, 0.0],
}

# 真实模型里，Q/K/V 是用三套「学出来的换算规则」从 X 算出来的。
# 这里为了短，直接把算好的结果摆出来。
Q = {"很": [1.0, 0.0]}                                    # 只有当前 token 需要 Q
K = {"天": [0.5, 0.1], "气": [0.9, 0.2], "很": [0.2, 0.0]}
V = {"天": [1.0, 0.0, 0.0, 0.2],
     "气": [0.8, 0.6, 0.0, 0.3],
     "很": [0.0, 0.2, 0.5, 0.0]}

# FFN（自己再加工）：一个极简的「一进一出小加工器」
W1 = [[0.5, 0.1, 0.0, 0.0],
      [0.0, 0.6, 0.1, 0.0],
      [0.1, 0.0, 0.4, 0.1],
      [0.0, 0.1, 0.0, 0.7]]
W2 = [[0.8, 0.0, 0.0, 0.0],
      [0.0, 0.8, 0.0, 0.0],
      [0.0, 0.0, 0.8, 0.0],
      [0.0, 0.0, 0.0, 0.8]]

# 「去词表里打分」的那张大表：4 个数的一串 -> 每个候选的原始分
W_OUT = {"好": [1.0, 0.5, 0.5, 0.2],
         "差": [0.2, 0.3, 0.1, 0.5],
         "冷": [0.3, 0.2, 0.6, 0.4]}


# ============ 小工具 ============
def dot(a, b):
    """比相似度：两串数字逐位相乘，再加起来。越大越像。"""
    return sum(x * y for x, y in zip(a, b))


def dot_steps(a, b):
    """把上面那步算式摊开，方便肉眼看。"""
    return " + ".join(f"{x}×{y}" for x, y in zip(a, b))


def matvec(matrix, vector):
    return [dot(row, vector) for row in matrix]


def ffn(vector):
    """一个「一进一出的小加工器」：调一调这串数字。"""
    hidden = [max(0.0, v) for v in matvec(W1, vector)]
    return matvec(W2, hidden)


def to_percent(scores):
    """把一堆任意分数换算成百分比（加起来 = 100%）。这一步叫 softmax。"""
    biggest = max(scores)
    exps = [pow(2.718281828, s - biggest) for s in scores]
    total = sum(exps)
    return [e / total for e in exps]


def show(v):
    return "[" + ", ".join(f"{x:.3f}" for x in v) + "]"


# ============ 走一遍流水线 ============
CUR = TOKENS[-1]                 # 当前 token = 最后一个已经写出来的
DIM = len(X[CUR])

print(f"已经写出来的 token：{' '.join(TOKENS)}")
print(f"当前要往前推进的是：{CUR}")

print(f"\n[1] 举 Query：{CUR} 拿出自己的提问向量 {Q[CUR]}")

print("\n[2] 和每个 Key 比相似度（逐位相乘再相加；越大越相关）")
scores = []
for t in TOKENS:
    s = dot(Q[CUR], K[t])
    scores.append(s)
    print(f"      「{t}」: {dot_steps(Q[CUR], K[t])} = {s:.3f}")

print("\n[3] 把分数换算成百分比（softmax），这组百分比就是「权重」")
weights = to_percent(scores)
for t, w in zip(TOKENS, weights):
    print(f"      「{t}」: {w:.3f}  = {w * 100:.1f}%")

print("\n[4] 按权重把每个 Value 加起来（这一步就是「交流」）")
attn = [0.0] * DIM
for t, w in zip(TOKENS, weights):
    for i in range(DIM):
        attn[i] += w * V[t][i]
print("      = " + " + ".join(f"{w:.3f}×{V[t]}" for t, w in zip(TOKENS, weights)))
print("      = " + show(attn) + "   <- 还是一串数字，但已经「看过前文」")

print(f"\n[5] 残差：把「{CUR}」原来的向量也加回来（别把自己弄丢了）")
x_mid = [a + b for a, b in zip(X[CUR], attn)]
print(f"      {show(attn)} + {X[CUR]} = {show(x_mid)}")

print("\n[6] FFN：自己再加工一道（真实模型里是一个小加工器）")
ffn_out = ffn(x_mid)
x_out = [a + b for a, b in zip(x_mid, ffn_out)]
print(f"      FFN 输出 = {show(ffn_out)}")
print(f"      再加回自己（第二处残差）= {show(x_out)}")
print("      （真实模型会把 [1]~[6] 重复几十层，这里只做 1 层）")

print("\n[7] 打分（logits）：拿最终向量去词表里逐个对分")
logits = [dot(W_OUT[c], x_out) for c in CANDIDATES]
for c, s in zip(CANDIDATES, logits):
    print(f"      「{c}」: {s:.3f}")

print("\n[8] 换算成百分比（softmax）")
probs = to_percent(logits)
for c, p in zip(CANDIDATES, probs):
    print(f"      「{c}」: {p * 100:.1f}%")

print("\n[9] 采样：按百分比抽一个（像按比例抽奖）")
random.seed(7)
pick = random.choices(CANDIDATES, weights=probs, k=1)[0]
print(f"      -> 「{pick}」")
print(f"\n到这里，那串数字才终于变回一个字：「{pick}」")
print("（多跑几次会抽到不同的字——这就是「采样」。若每次都取最高分，叫「贪心」。）")
