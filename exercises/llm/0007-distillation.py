"""LLM 底层 · 第 7 课 配套脚本：蒸馏搬的是「答案的分布」，不是「答案」。

这一课只讲一件事：教一个小模型时，【你给它什么】决定了它能学会什么。

第 0 课那种训练方式只给「正确答案」（谁对就给 1 分，其他都是 0）。
Hinton 那篇蒸馏论文的做法不一样：它要小模型去【对齐老师那一整张概率表】。
为什么值得多花这个力气？因为非答案那几个字上的分数，不是噪声——
它记着「如果我错了，更可能错成哪个」。那套排序就是老师的泛化方式。

这个脚本用一份能真跑的小实验把它测出来：
  · 造两份语料，【故意让老师见过的数据和学生手上的数据给出不同的排序】
  · 老师在大语料上正常训练，量出它真正学到的分布
  · 三种教法训练三个学生，只给不同的「目标」：
      A 正确答案（one-hot）      —— 学生学到的是小语料自己的频率
      B 老师的答案（只搬 argmax） —— 丢光排序，还得到一个过度自信的学生
      C 老师的整张分布（真蒸馏）  —— 精确复现老师的分布与排序
  · 量三件事：离老师有多远 / 尾部排序和老师一致吗 / 有多过度自信

只用 Python 标准库，离线能跑。数字是实跑出来的。

运行：  python exercises/llm/0007-distillation.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

import math

# ---- 玩具设定：只有一个上下文，模型要在 5 个候选字里挑下一个 ----
CAND = ["晴", "雨", "风", "云", "霜"]

# 两份语料都是「一句话 = 上下文 + 下一个字」。刻意造得让两者【排序不同】：
#   老师那份：雨 的比重最大（雨 > 风 > 云 > 霜）
#   学生那份：云 的比重最大（云 > 雨 > 风 > 霜）
# 于是「雨比云更可能」这件事，只存在于老师的分布里，学生自己的数据里没有。
RICH = [("晴", 60), ("雨", 18), ("风", 10), ("云", 7), ("霜", 5)]      # 共 100 句
POOR = [("晴", 30), ("雨", 5), ("风", 5), ("云", 6), ("霜", 4)]        # 共 50 句

STEPS = 6000
LR = 0.5
E = 2.718281828


def softmax(scores, t=1.0):
    """把分数换算成百分比（t 是温度：越大越平）。这一步叫 softmax。"""
    z = [s / t for s in scores]
    m = max(z)
    exps = [pow(E, v - m) for v in z]
    total = sum(exps)
    return [e / total for e in exps]


def train(target, steps=STEPS, lr=LR):
    """训一个只会「接下一个字」的玩具模型，直到它的分布对上 target。

    这就是第 0 课那套「出题 -> 扣分 -> 拧一点点」，只不过换成在概率空间里拧。
    唯一的信息就是 target：你给它什么，它就学到什么。
    """
    w = [0.0] * len(CAND)
    for _ in range(steps):
        p = softmax(w)
        for i in range(len(CAND)):
            w[i] -= lr * (p[i] - target[i])
    return softmax(w)


def onehot(idx):
    t = [0.0] * len(CAND)
    t[idx] = 1.0
    return t


def corpus_target(corpus):
    """把一份语料变成频率表——这正是「只给正确答案」训练所能学到的极限。"""
    total = sum(n for _, n in corpus)
    t = [0.0] * len(CAND)
    for ch, n in corpus:
        t[CAND.index(ch)] = n / total
    return t


def tv(p, q):
    """总变差距离：两行概率表差多少。0 = 完全一样，1 = 毫无重叠。"""
    return 0.5 * sum(abs(a - b) for a, b in zip(p, q))


def tail_order(dist):
    """只看非第一名那几个字，从大到小排——这才是「排序信息」。"""
    idx = sorted(range(len(dist)), key=lambda i: -dist[i])
    return [CAND[i] for i in idx[1:]]


def tail_spread(dist):
    """尾部里最大和最小的差。差 = 0 意味着几个字完全并列，根本谈不上排序。"""
    tail = sorted(dist)[:len(dist) - 1]
    return max(tail) - min(tail)


def tail_verdict(dist, teacher, eps=0.001):
    """尾部排序和老师一致吗。

    ⚠ 必须先挡掉「全并列」：几个非答案都是 0 时，排序是任意的，
      而 Python 的稳定排序会把它按 CAND 的原顺序排出来——那不是「对了」，
      是压根没有信息。上一版就是在这里静默假通过的。
    """
    if tail_spread(dist) < eps:
        return "并列"
    return "对" if tail_order(dist) == tail_order(teacher) else "错"


def dwidth(s):
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


def pad(s, w):
    return s + " " * max(0, w - dwidth(s))


def lpad(s, w):
    return " " * max(0, w - dwidth(s)) + s


def show(label, dist):
    print(f"      {pad(label, 30)}"
          + "".join(lpad(f"{c} {d * 100:.1f}%", 12) for c, d in zip(CAND, dist)))


# ============ [1] 两份语料，排序故意相反 ============
print("[1] 先造两份语料。它们故意排得【不一样】——这是本脚本的关键")
print(f"      {'来源':<12}{'规模':>6}" + "".join(f"{lpad(c, 8)}" for c in CAND) + "   尾部排序（非第一名）")
for label, corpus in [("老师见过的", RICH), ("学生手上的", POOR)]:
    t = corpus_target(corpus)
    print(f"      {pad(label, 12)}{lpad(str(sum(n for _, n in corpus)), 6)}"
          + "".join(f"{lpad(f'{d * 100:.0f}%', 8)}" for d in t)
          + "   " + " > ".join(tail_order(t)))
print("      ——老师说「雨比云更可能」，学生自己的数据说「云比雨更可能」。")
print("        所以「雨 > 风 > 云 > 霜」这个排序，只存在于老师的分布里。")

# ============ [2] 老师真的训一遍 ============
rich_t = corpus_target(RICH)
teacher = train(rich_t)
print("\n[2] 老师：在 100 句语料上正常训练（只给正确答案）。训完量一下它学到什么")
show("老师（实测）", teacher)
print(f"      尾部排序：{' > '.join(tail_order(teacher))}")
print(f"      和语料频率差 {tv(teacher, rich_t):.4f} —— 收敛得很干净。")

# ============ [3] 三种教法，三个学生 ============
poor_t = corpus_target(POOR)
top = max(range(len(CAND)), key=lambda i: teacher[i])

student_a = train(poor_t)                    # A：正确答案（one-hot），也就是第 0 课那种
student_b = train(onehot(top))               # B：只搬老师的答案
student_c = train(teacher)                   # C：老师的整张分布 = 真蒸馏

print("\n[3] 三个学生，骨架一样、步数一样，只有「你给它什么」不同")
print(f"      {pad('教法', 34)}{lpad('离老师多远', 11)}{lpad('尾部排序', 10)}"
      f"{lpad('尾部差距', 11)}{lpad('第一名多自信', 13)}")
rows = []
for label, s in [("A 正确答案（one-hot）", student_a),
                 ("B 只搬老师的答案（argmax）", student_b),
                 ("C 搬老师的整张分布（蒸馏）", student_c)]:
    d = tv(s, teacher)
    verdict = tail_verdict(s, teacher)
    spread = tail_spread(s)
    conf = s[max(range(len(CAND)), key=lambda i: s[i])]
    rows.append((label, s, d, verdict, spread, conf))
    print(f"      {pad(label, 34)}{lpad(f'{d:.3f}', 11)}{lpad(verdict, 10)}"
          f"{lpad(f'{spread * 100:.1f} pp', 11)}{lpad(f'{conf * 100:.0f}%', 13)}")
print(f"      （老师自己的尾部差距是 {tail_spread(teacher) * 100:.1f} pp）")

print()
for label, s, *_ in rows:
    show(f"  {label}", s)

# ============ [4] 三条结论 ============
print("\n[4] 三条要看懂的")
a, b, c = rows[0], rows[1], rows[2]
print(f"      A 离老师 {a[2]:.3f}，尾部排序{a[3]}（差距只有 {a[4] * 100:.1f} pp）。")
print("        它学到的是【学生自己那份小语料的频率】——语料里没有的东西，它学不到。")
print(f"      B 离老师 {b[2]:.3f}，尾部{b[3]}，第一名拿了 {b[5] * 100:.0f}%。")
print("        这是最糟的一档：整套排序全丢了，还额外得到一个【过度自信】的学生。")
print("        「只搬老师的答案」听起来像蒸馏，其实不是。")
print(f"      C 离老师 {c[2]:.3f}，尾部排序{c[3]}，差距 {c[4] * 100:.1f} pp——和老师一样。")
print("        它没有见过老师那份语料，只是照着那 5 个数反复拧，就复现了老师的排序。")
print("        ——被搬过来的不是答案，是【泛化方式】。")

# ============ [5] 温度：为什么要把分布调软 ============
print("\n[5] 那为什么要【加热】老师（temperature）？看尾部就明白了")
print(f"      {'温度':<10}" + "".join(f"{lpad(c, 8)}" for c in CAND) + "   尾部排序")
for t in (0.5, 1.0, 3.0, 8.0):
    hot = softmax([math.log(max(p, 1e-12)) for p in teacher], t=t)
    print(f"      {pad(str(t), 10)}" + "".join(f"{lpad(f'{d * 100:.1f}%', 8)}" for d in hot)
          + "   " + " > ".join(tail_order(hot)))
print("      ——注意这个玩具里【排序】四种温度下都没变（雨>风>云>霜）。")
print("        真正被温度改变的是【尾部之间的差距】：")
print("          0.5 档：尾部挤成 7.9% / 2.4% / 1.2% / 0.6%——四个数已经快贴成一条线；")
print("                 （这个玩具只有 5 个候选，再挤也挤不到 0；真实词表是几万量级，")
print("                  所以实际训练里尾部会被压得更狠，这是要留意的方向。）")
print("          8.0 档：尾部被抹平到 20.7% / 19.2% / 18.4% / 17.6%——谁大谁小也看不清了。")
print("        所以温度是【两头都不能要】：太低压掉尾部，太高抹平尾部。")
print("        Hinton 那篇的原话：蒸馏就是「把 softmax 的温度往上抬，")
print("        直到老师给出一组足够软的目标」。而且直接对齐 logit 只是它的特例。")
print("        这也正是第 1 课那个 temperature —— 同一个旋钮，训练和生成两头都在用。")

# ============ [6] 和量化对照 ============
print("\n[6] 收尾：它和第 5 课的量化是两件事")
print("      量化：改【怎么存】——每个数占几个字节。模型学到的东西一个没动。")
print("      蒸馏：改【从哪来】——老师的分布当目标。模型学到的东西变了。")
print("      所以顺序是先蒸馏变小、再量化压小：")
print("        先让它学会（小模型 + 完整分布），再让它变轻（4 bit + 挑着压）。")
print("      反过来做，等于把一个本来就没学好的模型再压一遍。")
print()
print("      最后一句必须说清楚：这一整套只解决【能力从哪来】，")
print("      不解决【能力够不够用】。R1 论文自己就写了：")
print("      它的结构化输出能力【不如现有模型】，而且【没法调用工具】。")
print("      所以推理强的小模型，不等于能当好 agent —— 该测的还是要测。")