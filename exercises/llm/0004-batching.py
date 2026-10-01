"""LLM 底层 · 第 4 课 配套脚本：批处理（batching）怎么救 decode。

核心想法：
  decode 每一步都要把「模型权重」（大头）+「各请求的 KV」从显存搬到计算单元。
  如果一次只服务 1 个请求，那趟「搬权重」的车大部分是空的。
  批处理 = 一趟车装满 N 个请求，权重的搬运费被 N 个请求分摊。

不依赖任何 API。数字是刻意简化的量级模型，重点看「相对关系」。

运行：  python exercises/llm/0004-batching.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

# ---- 极简量级模型 ----
WEIGHT_GB = 140.0     # 模型权重（每一步都必须读一遍的"大头"）
KV_GB = 0.5           # 每个请求自己的 KV cache
BW = 1000.0           # 显存带宽（GB/秒，相对单位）
VRAM_GB = 200.0       # 可用于"权重 + KV"的显存


def per_step_time(batch):
    """一步（batch 个请求同时前进一个 token）的耗时 = 要搬的数据 / 带宽。

    ⚠ 这是一个**只画了"搬运"那一半**的模型：没有算力上限，所以它永远不会
       自己出现"吞吐不涨"的拐点——批大小是被显存卡住的（见上面的 max_batch）。
       真实系统里还有一个"算力上限"跟它赛跑：批大到某个点，搬运不再是瓶颈、
       算力成了瓶颈，那时再加大批量吞吐就基本不涨了（延迟照涨）。
       那半边没画进来，是为了让这张表的因果关系一眼看得清。
    """
    moved = WEIGHT_GB + batch * KV_GB
    return moved / BW


if __name__ == "__main__":
    max_batch = int((VRAM_GB - WEIGHT_GB) / KV_GB)
    print(f"模型权重 {WEIGHT_GB} GB | 单请求 KV {KV_GB} GB | 可用显存 {VRAM_GB} GB")
    print(f"=> 显存决定的批大小上限 = ({VRAM_GB} - {WEIGHT_GB}) / {KV_GB} = {max_batch}\n")

    print(f"{'批大小':>5} | {'每步耗时':>9} | {'吞吐(tok/s)':>11} | {'单请求每 token':>14}")
    print("-" * 54)
    for b in [1, 2, 4, 8, 16, 32, 64, max_batch]:
        if b > max_batch:
            continue
        step = per_step_time(b)
        print(f"{b:>5} | {step:>8.3f}s | {b / step:>11.1f} | {step:>13.3f}s")

    base = per_step_time(1)
    best = per_step_time(max_batch)
    print("\n" + "=" * 54)
    print(f"批大小 1 -> {max_batch}：")
    print(f"  吞吐      : {1 / base:>7.1f} -> {max_batch / best:>7.1f} tok/s"
          f"   (提升 {max_batch / best / (1 / base):.0f} 倍)")
    print(f"  单请求延迟: {base:>7.3f} -> {best:>7.3f} s/token"
          f"   (变差 {(best / base - 1) * 100:.0f}%)")
    print(f"\n理论吞吐上限 = 带宽 / 单请求 KV = {BW} / {KV_GB} = {BW / KV_GB:.0f} tok/s")
    print("  —— 批越大，权重那笔固定开销被摊得越薄，越接近这个上限。")
    print("\n结论：批处理用【一点点延迟】换【巨大吞吐】。")
    print("      这也是为什么所有推理服务都在拼命凑批、以及为什么要『连续批处理』。")
