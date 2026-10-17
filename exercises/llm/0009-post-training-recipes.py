"""LLM 底层 · 第 9 课 配套脚本：换扣分单，换学法。

对应正文第 2～4 节。同一个学生、同一道题、同样的训练量，只换「扣分单」
（= 学习目标），看学完的表差在哪。这是教学模拟器，不是真训练——但每一步
的算法都是真的：
  - 表格式扣分单（人标答案 / 老师范文 / 老师概率表）：朝目标表插值；
  - 数字式扣分单（奖励分 / 对错一比特）：只知道「这次好还是不好」，
    只能把尾部的分挪一点给正确答案（尾部谁大谁小，它一个字没提）；
  - 偏好式扣分单（A 比 B 好）：只把两者差距拉开，别的字一动不动。

故意让学生的尾部排序一开始就是**错的**（它觉得「雨＞霜＞云＞风」，老师说「雨＞风＞云＞霜」）：
谁能把尾部也教对，一眼就能看出来。

关键看一件事：扣分单给的是【一整张表】，还是【一句话】。
给表的教得细，给一句话的教得粗。

跑法：python exercises/llm/0009-post-training-recipes.py
"""

# ---------- 设定 ----------

WORDS = ["晴", "雨", "风", "云", "霜"]        # 明天天气的五个候选字
STUDENT = [30.0, 25.0, 10.0, 15.0, 20.0]       # 学生练之前：非答案区错排成「雨＞霜＞云＞风」
TEACHER = [60.0, 18.0, 10.0, 7.0, 5.0]         # 老师的概率表：非答案区是「雨＞风＞云＞霜」
ANSWER = 0                                     # 正确答案是「晴」
RIGHT_TAIL = "雨＞风＞云＞霜"                   # 老师的尾部排序（除答案外的全部）

STEPS = 200          # 表格式扣分单的训练步数
LR = 0.05            # 每步补掉差距的 5%
COARSE_STEPS = 200   # 数字式 / 偏好式扣分单的轮数
NUDGE = 0.01         # 数字式：每轮把尾部剩余的 1% 挪给答案
PAIR_STEP = 0.5      # 偏好式：每轮把 0.5 个点从「输家」挪给「赢家」


def towards_table(start, target, steps, lr):
    """朝目标表插值：每步把差距补掉 lr 这么多。"""
    cur = start[:]
    for _ in range(steps):
        cur = [c + lr * (t - c) for c, t in zip(cur, target)]
    return cur


def towards_answer_by_nudge(start, steps, rate):
    """数字式扣分单：只知道「该往答案那边挪」，每轮把尾部剩余的 rate 挪给答案。
    尾部谁大谁小一个字没提，所以各字之间的比例原样不动。"""
    cur = start[:]
    for _ in range(steps):
        tail_total = sum(cur) - cur[ANSWER]
        if tail_total < 0.01:
            break
        move = tail_total * rate
        for i in range(len(cur)):
            if i != ANSWER:
                cur[i] -= cur[i] / tail_total * move
        cur[ANSWER] += move
    return cur


def preference_pair(start, steps, step, win, lose):
    """偏好式扣分单：只说「win 比 lose 好」，每轮把两者差距拉开一点，
    其余的字不碰——它只知道这一对谁好。"""
    cur = start[:]
    for _ in range(steps):
        if cur[lose] <= 0.1:
            break
        cur[win] += step
        cur[lose] -= step
    return cur


def tail_order(table):
    tail = sorted(range(1, len(table)), key=lambda i: -table[i])
    return "＞".join(WORDS[i] for i in tail)


def tail_ok(table):
    return "对上了" if tail_order(table) == RIGHT_TAIL else "没对上"

def show(name, table, note):
    body = "  ".join(f"{w} {v:5.1f}%" for w, v in zip(WORDS, table))
    print(f"{name:<20} {body}")
    print(f"{'':<20} 尾部 {tail_order(table)}（要 {RIGHT_TAIL} 才算学到）→ {note}")


print("同一道题「明天什么天气」，同一个学生，同样的训练量。")
print(f"练之前        {'  '.join(f'{w} {v:5.1f}%' for w, v in zip(WORDS, STUDENT))}"
      f"   尾部 {tail_order(STUDENT)}（错的）")
print(f"老师那张表    {'  '.join(f'{w} {v:5.1f}%' for w, v in zip(WORDS, TEACHER))}"
      f"   尾部 {RIGHT_TAIL}（目标）")
print()
print("=" * 92)
print("一、表格式扣分单：给的是一整张表，教得最细")
print("=" * 92)

one_hot = [0.0] * len(WORDS)
one_hot[ANSWER] = 100.0

sft = towards_table(STUDENT, one_hot, STEPS, LR)
show("① 人标答案（SFT）", sft,
     "答案记住了；尾部全压成 0，谁大谁小再也没法说——不是排对排错，是没了")

from_teacher_text = towards_table(STUDENT, one_hot, STEPS, LR)   # 范文是老师写的，落到目标上还是「答案那一个字」
show("② 老师范文（照范文背）", from_teacher_text,
     "和 ① 逐位一模一样：练法同一个，只换了范文的作者")

soft = towards_table(STUDENT, TEACHER, STEPS, LR)
show("③ 老师概率表（蒸馏）", soft,
     "答案学到了，连错的尾部也被老师掰正了：「猜错会错成什么样」整个搬了过来")

print()
print("=" * 92)
print("二、一句话式扣分单：只给一个数、或一句偏好，教得粗")
print("=" * 92)

nudge = towards_answer_by_nudge(STUDENT, COARSE_STEPS, NUDGE)
show("④ 奖励一个数（RLHF）", nudge,
     "只知道「这次好」，往答案挪了一截；尾部谁大谁小它一个字没提，错的原样留着")

pref = preference_pair(STUDENT, COARSE_STEPS, PAIR_STEP, ANSWER, 1)
show("⑤ 偏好一对（DPO）", pref,
     "只拉开「晴 vs 雨」，风云霜一动不动——扣分单里只有这一对的信息")

print()
print("=" * 92)
print("三、排个名（两个指标：第一名学到了吗、尾部跟老师对上了吗）")
print("=" * 92)
ranked = [
    ("③ 老师概率表", soft),
    ("① 人标答案", sft),
    ("② 老师范文", from_teacher_text),
    ("④ 奖励一个数", nudge),
    ("⑤ 偏好一对", pref),
]
print(f"{'教法':<18}{'第一名':>8}{'尾部对上老师':>14}{'离老师多远':>12}")
for name, table in ranked:
    dist = sum(abs(a - b) for a, b in zip(table, TEACHER)) / 2
    print(f"{name:<18}{table[ANSWER]:>7.1f}%{tail_ok(table):>15}{dist:>11.3f}")

print()
print("[看输出三件事]")
print("1) ① 和 ② 完全一样——「照答案练」就是「照答案练」，范文是人写的还是老师写的，")
print("   只改变它叫什么名字（SFT 还是蒸馏），不改变学出来的东西。")
print("2) ③ 是唯一尾部对上老师的：扣分单给的是整张表，连「猜错会错成什么样」都在里面。")
print("3) ④⑤ 的尾部还是错的：扣分单只给一个数、或一句偏好，那几个字的讲究根本不在教材里。")
print("   这就是「扣分单给一句话，就只能学个大概」——不是模型笨，是教材里没写。")
