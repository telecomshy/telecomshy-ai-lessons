"""LLM 底层 · 第 0 课 配套脚本：让一个玩具「学」会接下一个字。

这一课只讲一件事：模型里的数字（权重）是【怎么被训练调出来的】。
人写好的只是骨架（神经网络）；这一步训练，才把数字填进去。

玩具的身体被故意简化到只剩一张表（真实模型是几十层矩阵，那是第 1 课的事），
但【训练的方式一模一样】：出题 -> 作答 -> 算扣分 -> 往少扣分的方向拧一点点。

你会看到四件事：
  1. 损失一路往下掉 —— 它在「变好」
  2. 被拧的就是那张表 —— 那就是模型的【权重】
  3. 扣分停在 0.6 不再降 —— 那不是它笨，是语料本身就有多种答案
  4. 语料里有什么，它就信什么 —— 换一份语料，学出来的东西就不一样

运行：  python exercises/llm/0000-how-models-learn.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

import math
import random

E = 2.718281828
LR = 0.2          # 每次拧多少（拧猛了会把之前学会的冲掉）
EPOCHS = 1200     # 把整份考题来回做几遍

VOCAB = ["天", "气", "很", "好", "冷", "差", "雨"]

# 两份语料，差别只有一个：「很」后面跟什么
CORPUS_A = ["天气很好", "天气很冷", "天气很差", "雨天很好", "雨天很冷", "雨天很差"]
CORPUS_B = ["天气很冷", "雨天很冷", "天气很冷", "雨天很冷", "天气很冷", "雨天很冷"]


# ============ 小工具 ============
def to_percent(scores):
    """把一堆任意分数换算成百分比（加起来 = 100%）。这一步叫 softmax。"""
    biggest = max(scores)
    exps = [pow(E, s - biggest) for s in scores]
    total = sum(exps)
    return [e / total for e in exps]


def make_pairs(sentences):
    """把句子拆成考题：每一对相邻的字就是一道「看前一个，猜下一个」。"""
    out = []
    for s in sentences:
        for a, b in zip(s, s[1:]):
            out.append((a, b))
    return out


def show_row(W, x):
    """打印「模型看 x 时，给每个字打多少分」的百分比。"""
    probs = to_percent([W[x][b] for b in VOCAB])
    print("      " + "   ".join(f"「{b}」{p * 100:5.1f}%" for b, p in zip(VOCAB, probs)))


def loss_of(W, x, y):
    """一道题扣多少分：真实那个字得到的百分比越低，扣得越多（扣分 = -log(百分比)）。"""
    probs = to_percent([W[x][b] for b in VOCAB])
    return -math.log(probs[VOCAB.index(y)])


def average_loss(W, pairs):
    """整份考题的平均扣分。满分是 0，越大越差。"""
    return sum(loss_of(W, x, y) for x, y in pairs) / len(pairs)


def train(sentences, seed=7, epochs=EPOCHS):
    """训练 = 反复：出题 -> 作答 -> 算扣分 -> 拧那张表。"""
    rng = random.Random(seed)
    # 那张表就是这个模型全部的「权重」：W[上一个字][下一个字] = 该给多少分
    W = {a: {b: rng.uniform(-1.0, 1.0) for b in VOCAB} for a in VOCAB}
    pairs = make_pairs(sentences)
    history = []
    for _ in range(epochs):
        rng.shuffle(pairs)
        for x, y in pairs:
            probs = to_percent([W[x][b] for b in VOCAB])
            # 往哪拧：给真实那个字加一点分，给别的字减一点分
            for b, p in zip(VOCAB, probs):
                want = 1.0 if b == y else 0.0
                W[x][b] -= LR * (p - want)
        history.append(average_loss(W, pairs))
    return W, history, pairs


# ============ [1] 出题 ============
print("[1] 训练语料：6 句话。答案不用人标——句子自己带着下一个字")
for s in CORPUS_A:
    print(f"      {s}")
print(f"      拆成 {len(make_pairs(CORPUS_A))} 道考题：（天→气）（气→很）（很→好）（雨→天）…")

# ============ [2] 训练前 ============
print("\n[2] 训练前：让模型看「很」，它给每个字打多少分")
W0, _, pairs = train(CORPUS_A, epochs=0)
show_row(W0, "很")
print(f"      平均扣分 = {average_loss(W0, pairs):.3f}   （满分 0，越大越差）")
print("      ——纯随机，看不出任何规律。")

# ============ [3] 训练 ============
print("\n[3] 开始训练：每一遍 = 把 18 道考题全做一遍，每题都拧一点点")
W1, hist, pairs = train(CORPUS_A)
for ep in [0, 49, 199, 599, EPOCHS - 1]:
    print(f"      第 {ep + 1:4d} 遍   平均扣分 {hist[ep]:.3f}")
print("      ——扣分一路往下掉，就是在「变好」。")

# ============ [4] 训练后 ============
print("\n[4] 训练后：再让模型看两个字")
print("      看「很」")
show_row(W1, "很")
print("      看「天」")
show_row(W1, "天")
print("      ——「很」后面三个都在三成上下：因为语料里「很」后面三种都出现过，而且一样多。")
print("      ——「天」后面是五五开：一半跟「气」（天气很…），一半跟「很」（雨天很…）。")
print("      ——它学的不是「道理」，是【语料里的统计规律】；它给的不是答案，是【一张百分比表】。")

# ============ [5] 扣分停在哪 ============
print("\n[5] 扣分最后停在 0.599 就不降了——那不是它笨")
for x in ["天", "气", "很"]:
    sub = [(a, b) for a, b in pairs if a == x]
    avg = sum(loss_of(W1, a, b) for a, b in sub) / len(sub)
    print(f"      看「{x}」的那 {len(sub)} 道题，平均每题扣 {avg:.3f}")
print("      ——「气」后面永远是「很」，所以能扣到 0。")
print("      ——「天」后面有两种答案，「很」后面有三种。再聪明也只能按比例猜，")
print("         所以那两组最好也得扣 0.69 / 1.10——这部分扣不掉，是语料本身的不确定性。")

# ============ [6] 换语料 ============
print("\n[6] 换一份语料再训一遍：「很」后面永远是「冷」")
for s in CORPUS_B:
    print(f"      {s}")
W2, _, pairs2 = train(CORPUS_B)
print("      看「很」")
show_row(W2, "很")
print(f"      平均扣分 = {average_loss(W2, pairs2):.3f}")
print("      ——语料里有什么，它就信什么。语料没写过的，它不会。")

# ============ [7] 收尾 ============
print("\n[7] 一句话")
print("      训练 = 出题（文本自带答案）-> 作答 -> 算扣分 -> 往少扣分的方向拧一点点 -> 重复几百亿次。")
print("      被拧的那些数，就是模型的【权重】。真实模型有几十亿个，但拧的方式一模一样。")
print("      （这个玩具只有一张表；真实模型是几十层矩阵——那是第 1 课的事。）")
print("      （它只管【像不像】，不管【对不对】：一段胡话只要写得够像，同样是高分。）")
