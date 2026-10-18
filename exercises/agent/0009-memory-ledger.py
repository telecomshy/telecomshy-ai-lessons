"""Agent 篇 · 第 9 课 配套脚本：给 agent 的长期记忆「建台账」。

一段固定对话（三周里用户改了两次主意）过一遍记忆台账：
  1. 提取：流水账变成一条条记忆（类型 + 时间 + 状态）
  2. 四个决定：记新 / 改旧 / 推翻 / 不管
  3. 过期：改口的旧条目标「已过期」，不删——将来还能回答「她当时爱坐哪」
  4. 取回：只把「有效」的条目塞回上下文

真实系统里，第 1 步由 LLM 做（见 Mem0 论文的提取阶段）；这里用手写规则，
让你把注意力放在「账怎么记」上。不调 API，纯离线。

运行：  python exercises/agent/0009-memory-ledger.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

import sys
import unicodedata


def dpad(s, width):
    """按显示宽度补齐（中文算 2 格），让表格在终端里对齐。"""
    used = sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)
    return s + " " * max(0, width - used)

# ---- 固定对话：(日期, 说话内容) ----
DIALOGUE = [
    ("3/01", "用户：我一般坐东航。"),
    ("3/01", "用户：座位记得要靠窗。"),
    ("3/08", "用户：上次那趟 620 的不错，以后订票先查它。"),
    ("3/15", "用户：最近都走虹桥，浦东太远了。"),
    ("3/20", "用户：我现在爱坐走道了，靠窗那个不算了啊。"),
    ("3/21", "用户：今天天气真不错。"),
    ("3/22", "用户：帮我订明天去北京的票。"),
]

# ---- 手写规则版「提取器」：每条流水账抽出什么记忆 ----
# (抽出的记忆, 类型, 动作)  类型：事实 / 经历 / 做法    动作：记新 / 改旧 / 推翻 / 不管
EXTRACTOR = {
    "3/01 我一般坐东航。":
        ("常坐东航", "事实", "记新"),
    "3/01 座位记得要靠窗。":
        ("偏好靠窗座位", "事实", "记新"),
    "3/08 上次那趟 620 的不错，以后订票先查它。":
        ("订票先查东航 620 那趟", "做法", "记新"),
    "3/15 最近都走虹桥，浦东太远了。":
        ("出发走虹桥（浦东太远）", "事实", "改旧"),   # 并进「出行偏好」，不是全新一条
    "3/20 我现在爱坐走道了，靠窗那个不算了啊。":
        ("偏好走道座位", "事实", "推翻"),             # 推翻 3/01 的「靠窗」
    "3/21 今天天气真不错。":
        ("", "", "不管"),                            # 一次性闲聊，不值得记
    "3/22 帮我订明天去北京的票。":
        ("", "", "不管"),                            # 这是任务，不是要记的事
}


def main():
    print("=" * 60)
    print("记忆台账演示：流水账 -> 一条条记忆 -> 四个决定")
    print("=" * 60)

    ledger = []      # 台账：(编号, 内容, 类型, 时间, 状态)
    next_id = 1

    print("\n[第一步] 逐条过对话，程序对每句话做个决定：\n")
    for date, text in DIALOGUE:
        key = f"{date} {text[3:]}"
        memory, kind, action = EXTRACTOR[key]
        print(f"  {date} {text}")

        if action == "不管":
            print(f"    -> 决定：不管（这条不进台账）\n")
            continue

        if action == "记新":
            ledger.append([next_id, memory, kind, date, "有效"])
            print(f"    -> 决定：记新。写进台账 #{next_id}（{kind}）\n")
            next_id += 1

        elif action == "改旧":
            # 找到同类旧条目，把新信息并进去（不是新起一条）
            for row in ledger:
                if row[2] == kind and row[4] == "有效":
                    row[1] = row[1] + "；" + memory
                    row[3] = date
                    print(f"    -> 决定：改旧。并进台账 #{row[0]}（{kind}）\n")
                    break

        elif action == "推翻":
            # 旧条目标「已过期」，留底不删；新条目写进来
            for row in ledger:
                if row[2] == kind and row[4] == "有效" and "靠窗" in row[1]:
                    row[4] = "已过期"
                    print(f"    -> 决定：推翻。台账 #{row[0]} 标「已过期」（留底不删）")
                    break
            ledger.append([next_id, memory, kind, date, "有效"])
            print(f"    -> 并写进台账 #{next_id}（{kind}）\n")
            next_id += 1

    print("\n[第二步] 台账长这样：\n")
    print(f"  {dpad('编号', 6)}{dpad('类型', 8)}{dpad('内容', 34)}{dpad('时间', 8)}状态")
    for row in ledger:
        print(f"  {dpad('#' + str(row[0]), 6)}{dpad(row[2], 8)}{dpad(row[1], 34)}{dpad(row[3], 8)}{row[4]}")

    print("\n[第三步] 取回：只把「有效」的条目塞回上下文\n")
    query = "帮她订明天去北京的票"
    hits = [row for row in ledger if row[4] == "有效"]
    print(f"  任务：{query}")
    print(f"  取回 {len(hits)} 条有效记忆：")
    for row in hits:
        print(f"    - [{row[2]}] {row[1]}")

    expired = [row for row in ledger if row[4] == "已过期"]
    if expired:
        print(f"\n  没取回的：{len(expired)} 条已过期。它们不干扰今天的事，")
        print("  但问「她以前爱坐哪」时还能答——这就是「标过期」比「直接删」多出来的好处。")

    print("\n" + "=" * 60)
    print("收尾一句：记忆不是存下来就完了。存得干净、管得住过期、")
    print("取回得准——三件都做对，长期记忆才是加分项。")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
