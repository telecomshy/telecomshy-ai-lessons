"""Agent 技巧篇 · 0002 配套脚本：给你手上的 agent 打个分（使用者视角）。

不调 API、不读任何文件。你把「试出来的数字」填进去，它算给你看：
  - 每个任务的单次成功率
  - **连着做 N 次全对**的概率（这才是你真正要赌的那个数）
  - 平均每次成本

为什么要算这个？因为 agent 是不确定的：
单次 90% 听着很稳，但连着做 8 次全对只剩约 43% —— 一半以上会翻车。

运行：  python exercises/practice/0002-agent-scorecard.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

import sys
from math import pow

CONSISTENCY_K = 5          # 关心"连着做几次全对"，默认 5 次（可改）


def ask_num(prompt, cast=float):
    while True:
        try:
            return cast(input(prompt).strip())
        except (ValueError, EOFError):
            print("    请输入数字。")


def main():
    print("=" * 62)
    print("Agent 记分卡：给你手上的 agent 打个分")
    print("=" * 62)
    print("先想好你真实要它干的几件活，各跑几遍，把结果填进来。")
    print("（不用很多：3~5 个任务、每个跑 3~5 遍，就能看出苗头。）\n")

    n = int(ask_num("你试了几个任务？ > ", int))
    rows = []
    for i in range(1, n + 1):
        print(f"\n任务 {i}")
        name = input("  名字 > ").strip() or f"任务{i}"
        trials = int(ask_num("  跑了几次 > ", int))
        wins = int(ask_num("  成功几次 > ", int))
        cost = ask_num("  平均每次花的相对成本（随便填，比如 10）> ")
        p = wins / trials if trials else 0.0
        rows.append((name, trials, wins, p, cost))

    print("\n" + "=" * 62)
    print("记分卡")
    print("=" * 62)
    print(f"{'任务':<20}{'跑次':>5}{'成功':>5}{'单次成功率':>11}"
          f"{'连做'+str(CONSISTENCY_K)+'次全对':>14}{'每次成本':>10}")
    print("-" * 62)
    for name, trials, wins, p, cost in rows:
        pk = pow(p, CONSISTENCY_K)
        label = name if len(name) <= 18 else name[:17] + "…"
        print(f"{label:<20}{trials:>5}{wins:>5}{p * 100:>10.0f}%{pk * 100:>13.0f}%{cost:>10.1f}")

    print("\n" + "-" * 62)
    print("怎么读：")
    bad = []
    for name, trials, wins, p, cost in rows:
        pk = pow(p, CONSISTENCY_K)
        if pk < 0.5:
            bad.append((name, p, pk))

    if bad:
        print(f"  [!] 这几个任务的「连做 {CONSISTENCY_K} 次全对」不到一半——"
              f"别让它们无人值守：")
        for name, p, pk in bad:
            print(f"        {name}：单次 {p*100:.0f}% -> 连做 {CONSISTENCY_K} 次 {pk*100:.0f}%")
    else:
        print(f"  [OK] 所有任务「连做 {CONSISTENCY_K} 次全对」都在一半以上，比较稳。")

    # 成本差异
    costs = [c for _, _, _, _, c in rows]
    if costs and min(costs) > 0:
        ratio = max(costs) / min(costs)
        if ratio >= 3:
            print(f"  [!] 各任务成本差 {ratio:.1f} 倍——注意别只看「对不对」，"
                  f"也看它绕了多少圈。")
        else:
            print(f"  [OK] 各任务成本差别不大（{ratio:.1f} 倍）。")

    print("\n" + "-" * 62)
    print("记住三句话：")
    print("  1. 跑一次不算数 —— agent 是不确定的，多跑几遍。")
    print("  2. 它说成了，不等于成了 —— 去查真实状态（文件/订单/邮件）。")
    print("  3. 别只问「对不对」，也问「绕了多大圈」—— 同样的结果，代价能差几十倍。")
    print("-" * 62)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
