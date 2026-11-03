"""RAG · 第 5 课 · 配套脚本：相似度的三把尺子——点积、余弦、欧氏。

对应第 5 课「三把尺子」「尺子怎么选」两节。用几个手写的二维向量演示：
  1. 同一对向量，三把尺子读出三个不同的东西
  2. 同一组候选，换尺子就换名次（谁被长度骗了，一目了然）
  3. 归一化之后，点积和余弦给出完全一样的名次（数学上等价）

⚠ 向量是手写的玩具（二维），真的嵌入是几百上千维——但【尺子在量什么】一模一样。

运行：  python exercises/rag/0005-similarity-metrics.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

import math

# 问题向量
Q = (1.0, 0.0)

# 四个候选段的向量（手写，故意安排了不同的方向和长度）
CANDS = {
    "段 A": (1.2, 0.0),   # 方向和问题完全一致，长度适中
    "段 B": (3.0, 1.5),   # 方向偏了，但长度很长
    "段 C": (0.5, 0.5),   # 方向偏 45 度，长度短
    "段 D": (0.0, 2.0),   # 方向垂直，完全无关
}


def dot(a, b):
    """点积：对应分量相乘再相加 = |a||b|cosθ。方向和长度都参与。"""
    return sum(x * y for x, y in zip(a, b))


def cosine(a, b):
    """余弦：点积除以两个长度。只剩方向，长度被除掉了。"""
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot(a, b) / (na * nb)


def euclidean(a, b):
    """欧氏：直线距离。方向和长度都参与，而且长度差会被放大。"""
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def normalize(v):
    n = math.sqrt(sum(x * x for x in v))
    return tuple(x / n for x in v)


print("[1] 同一对向量，三把尺子各在量什么（问题 Q=(1,0) vs 各段）")
print(f"    {'':6s}{'点积↑大好':>12s}{'余弦↑大好':>12s}{'欧氏↓小好':>12s}   向量")
for name, v in CANDS.items():
    print(f"    {name:6s}{dot(Q, v):12.3f}{cosine(Q, v):12.3f}{euclidean(Q, v):12.3f}   {v}")
print()
print("    读数说明：")
print("      · 段 B 点积最高（3.000）——【但它方向是偏的】，是长度把分数抬了上去。")
print("      · 段 A 余弦最高（1.000）——方向和问题完全一致，长度不影响余弦。")
print("      · 段 B 欧氏最远（2.500）——直线距离里，长度差被如实记账。")

print("\n" + "=" * 72)
print("[2] 同一组候选，换尺子就换名次")
print("=" * 72)
by_dot = sorted(CANDS, key=lambda n: -dot(Q, CANDS[n]))
by_cos = sorted(CANDS, key=lambda n: -cosine(Q, CANDS[n]))
by_euc = sorted(CANDS, key=lambda n: euclidean(Q, CANDS[n]))
print("    点积榜（大→小）：", " > ".join(by_dot))
print("    余弦榜（大→小）：", " > ".join(by_cos))
print("    欧氏榜（近→远）：", " > ".join(by_euc))
print()
print("    → 三个榜的冠军不一样：【点积选了段 B，余弦和欧氏选了段 A】。")
print("    → 变化最大的是段 B：点积第 1、余弦第 2、欧氏垫底——同一个向量，")
print("      三把尺子给出三种待遇，分歧全在【长度算不算数】上。")
print("    → 段 D 方向垂直，点积和余弦都给 0 分：方向不对的段，")
print("      「越大越好」的两把尺子都不会救它。")

print("\n" + "=" * 72)
print("[3] 归一化之后：点积 ≡ 余弦")
print("=" * 72)
normed = {n: normalize(v) for n, v in CANDS.items()}
print("    把每个向量缩到长度 1，再比：")
for name, v in normed.items():
    short = tuple(round(x, 3) for x in v)
    print(f"    {name:6s} 归一化后 {str(short):24s} 点积={dot(Q, v):.3f}")
print()
print("    名次：", " > ".join(sorted(normed, key=lambda n: -dot(Q, normed[n]))), "（和余弦榜完全一样）")
print("    所以工具里看到「余弦」和「归一化点积」两种说法，【是同一件事】。")

print("\n" + "=" * 72)
print("[4] 尺子怎么选：跟模型走")
print("=" * 72)
print("    没有「最准」的尺子，只有【和嵌入模型训练时一致】的尺子：")
print("    · all-MiniLM-L6-v2   训练用的是余弦   → 索引就用余弦")
print("    · msmarco-bert-base-dot-v5  训练用点积 → 索引就用点积")
print("    用错了会怎样：模型学出来的「像」，和你排名用的「像」不是一个定义。")
print()
print("    带走三条：")
print("      ① 点积看方向×长度，余弦只看方向，欧氏看直线距离（含长度）。")
print("      ② 换尺子＝换名次，所以【尺子跟模型走】，不跟心情走。")
print("      ③ 归一化点积和余弦是一回事——别当成两种方法去调参。")
