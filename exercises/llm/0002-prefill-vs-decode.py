"""LLM 底层 · 第 2 课 配套脚本：prefill（预填充）vs decode（解码）。

回答两个问题：
  1. 为什么"读长文"TTFT 高、"写长文"总耗时高？
  2. 前缀缓存能救哪一部分、救不了哪一部分？

不依赖任何 API，用一个极简的时间模型来演示量级关系。
数字是刻意简化的，重点看「相对关系」，别当成真实性能。

运行：  python exercises/llm/0002-prefill-vs-decode.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

# ---- 极简时间模型（单位：秒 / token 相对量）----
PREFILL_PER_TOKEN = 0.00005    # 预填充：处理输入，能并行，每个 token 很便宜
DECODE_BASE = 0.010            # 解码：每写一个 token 的固定开销
DECODE_PER_CTX = 0.0000005     # 解码时每读一个历史 token 的额外开销（要读 KV）

# ---- 价格模型（相对单位，输出约为输入的 5 倍）----
# 输出比输入贵：Anthropic 官方价目里输出一律是输入的 5 倍（Haiku 4.5 $1→$5、Opus 5.5 $4→$20）；
# DeepSeek 官方价目是 3～4 倍（V4.1-Flash $0.15→$0.60、V4-Pro $0.66→$1.98）。
# 原因不是"按 token 收费"（输入输出都是按 token 收费，方式一样），而是 decode 串行、带宽受限，
# 供应商每个输出 token 花掉的 GPU 时间远多于一个输入 token。这里取 5 倍，是偏保守的整数值。
PRICE_IN = 1.0
PRICE_OUT = 5.0
CACHE_HIT_DISCOUNT = 0.1       # 命中前缀按 0.1 倍计。Anthropic 约 0.025～0.1 倍、DeepSeek 低到 0.02～0.03 倍，
                                # 取 0.1 是保守值 —— 真实折扣更深，课里"成本降到约 1/7"是偏保守的说法。


def simulate(name, prompt_tokens, output_tokens, cached_prefix=0):
    fresh = prompt_tokens - cached_prefix            # 未命中、需要真正预填充的部分
    ttft = fresh * PREFILL_PER_TOKEN                 # 首字延迟 ≈ 预填充耗时

    decode_time = 0.0
    for i in range(output_tokens):                   # 一个 token 一个 token 写
        ctx = prompt_tokens + i                      # 这一步要读多长的历史 KV
        decode_time += DECODE_BASE + ctx * DECODE_PER_CTX

    total = ttft + decode_time
    cost = (fresh * PRICE_IN
            + cached_prefix * PRICE_IN * CACHE_HIT_DISCOUNT
            + output_tokens * PRICE_OUT)

    print(f"\n【{name}】输入 {prompt_tokens} / 输出 {output_tokens}"
          + (f" / 命中前缀 {cached_prefix}" if cached_prefix else ""))
    print(f"  首字延迟 TTFT : {ttft:7.3f} s   <- 由 prefill 决定")
    print(f"  生成耗时      : {decode_time:7.3f} s   <- 由 decode 决定")
    print(f"  总耗时        : {total:7.3f} s")
    print(f"  相对成本      : {cost:9.1f}")
    return ttft, decode_time, total, cost


if __name__ == "__main__":
    # 1. 读长文：输入很长、输出很短
    simulate("读长文（比如丢一篇长文档让它总结）", 20000, 50)

    # 2. 写长文：输入很短、输出很长
    simulate("写长文（比如让它写一篇长报告）", 500, 2000)

    # 3. agent 的一轮循环：大前缀 + 短输出，【没有】缓存
    simulate("agent 一轮 · 无缓存", 20000, 80)

    # 4. 同一个 agent 请求，但前 19500 个 token 命中了前缀缓存
    simulate("agent 一轮 · 命中前缀缓存", 20000, 80, cached_prefix=19500)

    print("\n" + "=" * 52)
    print("结论：")
    print("  · 输入长 -> 首字延迟(TTFT)高，但一旦开始写就很快")
    print("  · 输出长 -> 总耗时高，而且是一步一步、没法并行")
    print("  · 前缀缓存能大幅砍掉 TTFT 和成本，但【不会】让解码变快 ——")
    print("    因为输入只要批量算一次，输出一个字就要算一次")
    print("  · 想省钱：输入尽量命中缓存；输出尽量让模型少说几句")
