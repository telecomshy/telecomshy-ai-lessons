"""Agent 原理篇 · 第 6 课 配套脚本：给「你正在用的 harness」做个零件盘点。

核心公式：**Agent = Model + Harness**
harness ＝ 模型外面那套软件：拼 prompt、执行工具、管上下文、给护栏、加载 skill、接 MCP……

这个脚本问你 8 个问题（针对你正在用的那个软件，比如 OpenCode / Claude Code /
Cursor / WorkBuddy / TraeWork），然后告诉你：它有哪些零件、缺哪些、
以及每一块对应本课程的哪一课。

不调 API，纯离线，也不读你任何文件。

运行：  python exercises/agent/0006-harness-checklist.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

import sys

# (零件名, 问你什么, 对应本课程哪一课)
ITEMS = [
    ("工具执行层",  "它能真的动手吗？（读文件、跑命令、调 API）", "Agent 第 2 课 · 工具调用"),
    ("循环",        "它会「推理→行动→观察」反复转，而不是一问一答吗？", "Agent 第 1、3 课 · 循环"),
    ("上下文管理",  "它自己决定 prompt 怎么拼、历史怎么截、缓存怎么吃吗？", "LLM 底层第 2 课 · KV Cache"),
    ("护栏 / 权限", "有最大步数、工具白名单、危险动作要你确认吗？", "Agent 第 1 课 · 护栏"),
    ("Skill 加载",  "支持按需加载技能包吗？", "Agent 第 5 课 · Skill"),
    ("MCP 接入",    "能接外部标准化的工具吗？", "Agent 第 5 课 · MCP"),
    ("子 agent",    "能派「分身」去跑子任务吗？", "（后面的课会讲）"),
    ("沙箱 / 隔离", "执行环境跟你的电脑隔开吗？", "（工程细节）"),
]


def ask(q):
    while True:
        try:
            a = input(f"  {q}  [y/n] ").strip().lower()
        except EOFError:
            print()
            return False
        if a in ("y", "yes", "是", "1"):
            return True
        if a in ("n", "no", "否", "0"):
            return False
        print("    请输入 y 或 n")


def main():
    print("=" * 58)
    print("给「你正在用的 harness」做个零件盘点")
    print("=" * 58)
    print("先想好一个目标软件（比如 OpenCode / Claude Code / Cursor，")
    print("或者腾讯 WorkBuddy、中国电信 TeleAgent、字节 TraeWork），")
    print("然后照着它回答。答案没有对错，只看它有哪些零件。\n")

    which = input("你要盘点的是哪个软件？（直接回车跳过）> ").strip() or "(未填)"
    print()

    yes, no = [], []
    for name, q, lesson in ITEMS:
        (yes if ask(q) else no).append((name, lesson))

    print("\n" + "=" * 58)
    print(f"盘点结果：{which}")
    print("=" * 58)

    print(f"\n有的零件（{len(yes)} 个）：")
    for name, lesson in yes:
        print(f"  [有] {name:<12} ← {lesson}")

    if no:
        print(f"\n没有的零件（{len(no)} 个）——这正是它跟别的 harness 拉开差距的地方：")
        for name, lesson in no:
            print(f"  [无] {name:<12} ← {lesson}")

    print("\n" + "-" * 58)
    print("怎么读这张表：")
    print("  · 零件不是越多越好——每个零件都在吃 token、加延迟。")
    print("  · 真正的分水岭是前两个：**工具执行** 和 **循环**。")
    print("    少了它们，它只是个聊天框，不是 agent。")
    print("  · 有 / 无不等于好坏，是**取向**：面向办公、面向写代码、面向客服，")
    print("    零件侧重完全不同。")

    print("\n" + "=" * 58)
    print("记住那个公式：Agent = Model + Harness")
    print("你盘点的这套软件就是 Harness；模型是它套在外面的那一堆权重；")
    print("两者合起来，才表现出「agent」这个行为。")
    print("=" * 58)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
