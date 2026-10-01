"""Agent 技巧篇 · 0001 配套脚本：给你的 agent 算一笔上下文账。

它不调 API、不读你的文件。你改下面那几个常量，它就告诉你：
  - 每轮上下文都装了什么、各占多少
  - 跑 N 轮一共要付多少输入 token
  - 稳定前缀占多少（能省多少钱）
  - 哪一块最该收拾

为什么值得算？因为 agent 的成本不是「一次调用」，
而是 **轮数 × 每轮上下文长度**——历史会越滚越大。

运行：  python exercises/practice/0001-context-budget.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

# ================== 改这里：你自己的数字 ==================
WINDOW = 200_000          # 上下文窗口（token）

SYSTEM_PROMPT   = 1_200   # 系统提示
TOOL_LIST       = 4_800   # 工具清单（名字 + 说明 + 参数）
SKILL_DESCS     =   600   # 各 skill 的 description
USER_INPUT      =   200   # 用户这一句
TOOL_RESULT_EACH = 3_000  # 每次工具调用返回多少（平均）
CALLS_PER_ROUND =     1   # 平均每轮调几次工具
ROUNDS          =    20   # 这个任务一共跑几轮
GROWTH          =     1   # 历史增长：1 = 每轮都留全量；0.5 = 一半被压缩掉

PRICE_IN        =  1.0    # 输入 token 单价（相对）
PRICE_CACHE     =  0.1    # 命中缓存的读取价（相对）
# ===========================================================


def main():
    stable = SYSTEM_PROMPT + TOOL_LIST + SKILL_DESCS
    per_round_new = USER_INPUT + TOOL_RESULT_EACH * CALLS_PER_ROUND

    print("=" * 58)
    print(f"上下文预算（窗口 {WINDOW} token，任务跑 {ROUNDS} 轮）")
    print("=" * 58)

    total_in_tokens = 0
    worst = (0, 0)

    for r in range(1, ROUNDS + 1):
        history = per_round_new * GROWTH * r
        ctx = stable + history
        total_in_tokens += ctx
        if ctx > worst[1]:
            worst = (r, ctx)

    hist_end = per_round_new * GROWTH * ROUNDS
    ctx_end = stable + hist_end

    print(f"\n{'构成':<14}{'token':>10}{'占比':>9}   稳定？")
    print("-" * 52)
    rows = [
        ("系统提示",   SYSTEM_PROMPT,   "稳定"),
        ("工具清单",   TOOL_LIST,       "稳定"),
        ("skill 说明", SKILL_DESCS,     "稳定"),
        ("历史(末轮)", int(hist_end),   "易变"),
        ("当前输入",   USER_INPUT,      "易变"),
    ]
    for name, v, tag in rows:
        pct = v / ctx_end * 100 if ctx_end else 0
        print(f"{name:<14}{v:>10,}{pct:>8.1f}%   {tag}")

    print("-" * 52)
    print(f"{'每轮合计':<14}{ctx_end:>10,}{100.0:>8.1f}%")
    print(f"\n最挤的一轮：第 {worst[0]} 轮，{worst[1]:,} token"
          f"（占窗口 {worst[1] / WINDOW * 100:.0f}%）")

    cacheable = stable
    cache_pct = cacheable / ctx_end * 100 if ctx_end else 0
    print(f"\n稳定前缀 {cacheable:,} token（占每轮 {cache_pct:.0f}%）"
          f"→ 这部分每轮都一样，可走前缀缓存")

    cost_no_cache = total_in_tokens * PRICE_IN
    cost_cache = cacheable * ROUNDS * PRICE_CACHE + (total_in_tokens - cacheable * ROUNDS) * PRICE_IN
    print(f"\n整个任务输入量：{total_in_tokens:,} token")
    print(f"  不吃缓存 ≈ {cost_no_cache:,.0f} 相对成本")
    print(f"  吃缓存   ≈ {cost_cache:,.0f} 相对成本   （省 {1 - cost_cache / cost_no_cache:.0%}）")

    print("\n" + "-" * 58)
    print("看哪儿：")
    hist_ratio = hist_end / ctx_end if ctx_end else 0
    if hist_ratio > 0.6:
        print(f"  [!] 历史占 {hist_ratio:.0%}——该收拾了。考虑截断 / 压缩 / 摘要。")
    if cache_pct < 40:
        print(f"  [!] 稳定前缀只有 {cache_pct:.0%}——工具清单别全塞，"
              f"考虑按需加载（skill 的做法）。")
    if worst[1] / WINDOW > 0.7:
        print(f"  [!] 峰值已用掉窗口的 {worst[1] / WINDOW:.0%}——"
              f"留白不够，长任务容易触发「上下文腐烂」。")
    if hist_ratio <= 0.6 and cache_pct >= 40 and worst[1] / WINDOW <= 0.7:
        print("  [OK] 这个预算看着健康。")

    print("\n三条通用做法（细节见速查页）：")
    print("  1. 稳定的放前面，易变的放后面（吃缓存）")
    print("  2. 别用满，留白（上下文腐烂不是塞满才出问题）")
    print("  3. 工具结果先裁再塞，返回「模型用得上的信息」而不是原始数据")
    print("-" * 58)


if __name__ == "__main__":
    main()
