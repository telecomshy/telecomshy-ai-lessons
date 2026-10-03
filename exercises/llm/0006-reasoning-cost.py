"""LLM 底层 · 第 6 课 配套脚本：思考 token 进了哪本账。

这一课只讲一件事：会思考的模型多出来的那一步，不是免费的旁白——
它就是【输出 token】，所以它进了和输出一模一样的两本账：贵的账、慢的账。

而且「慢」这件事有两种读法，别混：
  - 多久【有反应】（第一个 token 冒头）：流式展示思考时，几乎不变
  - 多久【看到答案】：暴涨——这才是用户抱怨的那个「怎么想这么久」
账单和上下文跟着后一段走，所以两种读法都得付。

沿用第 2 课那套极简时间模型与价格模型（数字是刻意简化的，
重点看【相对关系】，别当成真实性能）：
  时间：预填充 0.00005 s/token；解码每 token 固定 0.010 s，另加读历史 KV 的开销
  价格：输入 1.0、输出 5.0（5 倍取自各家公开价目表）、命中前缀按 0.1 倍计

运行：  python exercises/llm/0006-reasoning-cost.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

PREFILL_PER_TOKEN = 0.00005
DECODE_BASE = 0.010
DECODE_PER_CTX = 0.0000005

PRICE_IN = 1.0
PRICE_OUT = 5.0
CACHE_HIT_DISCOUNT = 0.1

# 一个「中等难度」的实际请求：agent 跑一轮，前面一大段固定上下文已经缓存
PROMPT_TOKENS = 20000
CACHED_PREFIX = 19500
ANSWER_TOKENS = 80

THINKING_PER_STEP = 2000
TOOL_RESULT_TOKENS = 100


def dwidth(s):
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


def pad(s, w):
    return s + " " * max(0, w - dwidth(s))


def lpad(s, w):
    return " " * max(0, w - dwidth(s)) + s


def simulate(thinking_tokens):
    """把「思考 token」并进输出里，跑一遍第 2 课那套账。返回一列数字。

    两个时间要分开看，这是本课最容易讲错的地方：
      react —— 多久【有反应】：读完问题，再等一个 token 的时间（思考的第一个字）
      wait  —— 多久【看到答案】：思考全程 + 答案全程
    如果客户端【不】展示思考内容，那第一个可见的字就是答案的第一个字，
    于是 react 等于 wait —— 首字延迟一样暴涨。两种客户端两种账。
    """
    output_tokens = thinking_tokens + ANSWER_TOKENS
    fresh = PROMPT_TOKENS - CACHED_PREFIX
    ttft = fresh * PREFILL_PER_TOKEN

    decode_time = 0.0
    for i in range(output_tokens):
        ctx = PROMPT_TOKENS + i
        decode_time += DECODE_BASE + ctx * DECODE_PER_CTX

    react = ttft + DECODE_BASE          # 第一个 token 冒头
    cost = (fresh * PRICE_IN
            + CACHED_PREFIX * PRICE_IN * CACHE_HIT_DISCOUNT
            + output_tokens * PRICE_OUT)

    return {"out": output_tokens, "react": react, "wait": decode_time,
            "total": ttft + decode_time, "cost": cost}


# ============ [1] 思考 token 就是输出 token ============
print("[1] 先钉死一件事：那段「思考」不是免费的旁白，它【就是输出】")
print("      官方文档的原话是：思考花的 token 按【输出 token】计费，")
print("      而且它们和答案一起占用 max_tokens。")
print("      所以本课不需要新的一套账——第 2 课那套原样拿来用。")
print()
print(f"      {pad('场景', 20)}{lpad('思考 token', 13)}{lpad('多久有反应', 13)}"
      f"{lpad('多久看到答案', 15)}{lpad('相对成本', 12)}")

SCENARIOS = [("不开思考", 0), ("短想一会儿", 2000), ("长想一通", 8000)]
rows = []
for label, tk in SCENARIOS:
    r = simulate(tk)
    rows.append((label, tk, r))
    react, wait, cost = r["react"], r["wait"], r["cost"]
    print(f"      {pad(label, 20)}{lpad(str(tk), 13)}{lpad(f'{react:.2f} s', 13)}"
          f"{lpad(f'{wait:.1f} s', 15)}{lpad(f'{cost:.0f}', 12)}")

# ============ [2] 两种「慢」 ============
print("\n[2] 这张表最该盯的是两列时间的差别")
base, short_, long_ = rows[0], rows[1], rows[2]
print(f"      多久有反应：不开 {base[2]['react']:.2f} s -> 长想 {long_[2]['react']:.2f} s"
      f"    （几乎没变）")
print(f"      多久看到答案：不开 {base[2]['wait']:.1f} s -> 长想 {long_[2]['wait']:.1f} s"
      f"（{long_[2]['wait'] / base[2]['wait']:.0f} 倍）")
print(f"      相对成本：{base[2]['cost']:.0f} -> {long_[2]['cost']:.0f}"
      f"（{long_[2]['cost'] / base[2]['cost']:.0f} 倍）")
print("      ——流式展示思考时，思考的第一个字也是立刻冒出来的，所以「多久有反应」不变；")
print("        暴涨的是「多久看到答案」，也就是用户嘴里那句「它怎么想这么久」。")
print()
print("      ⚠ 换一种客户端，账就变了：如果【不】把思考内容显示出来，")
print("        那第一个【可见】的字就是答案的第一个字——首字延迟一样暴涨。")
print("        所以「开思考会不会让首字延迟变差」这个问题，")
print("        没有单一答案，它取决于你的客户端怎么显示（第 2 课第 5 节讲了两个延迟指标）。")

# ============ [3] 你看到的 ≠ 你付的 ============
print("\n[3] 一条容易踩的坑：你看到的思考，和你付的钱不是一回事")
print("      官方文档说：思考可以只回给你一段【摘要】，但计费按【原始全长】算。")
print(f"      假设原始思考 {long_[1]} token，界面只给你看 300 token 的摘要：")
print(f"        账单按 {long_[1]} token 算  ->  相对成本 {long_[2]['cost']:.0f}")
print(f"        你只看见 300 token        ->  屏幕上根本看不出那是 {long_[1]} 的量")
print("      ——所以「它到底想了多久」这件事，光看界面判断不出来。")

# ============ [4] 思考内容会留在对话里 ============
print("\n[4] 还有一个容易忘的后果：思考内容会【留在对话里】")
total_thinking = THINKING_PER_STEP * 10
cached_cost = CACHED_PREFIX * PRICE_IN * CACHE_HIT_DISCOUNT
fresh_cost = (PROMPT_TOKENS - CACHED_PREFIX) * PRICE_IN
total_ctx = PROMPT_TOKENS + 10 * (THINKING_PER_STEP + ANSWER_TOKENS + TOOL_RESULT_TOKENS)
print(f"      一个跑 10 步的 agent 循环，每步思考 {THINKING_PER_STEP} token：")
print(f"        十步攒下来的思考 = {total_thinking} token")
print(f"        到第 10 步，上下文 = {total_ctx} token"
      f"（其中开头那 {CACHED_PREFIX} 是命中缓存的固定段）")
print(f"        十步输出总成本   = {THINKING_PER_STEP * 10 * PRICE_OUT:.0f}"
      f"（{THINKING_PER_STEP * 10} 个思考 token x {PRICE_OUT}）")
print(f"        加上输入侧       = {fresh_cost + cached_cost:.0f}"
      f"（未命中 500 + 命中 {CACHED_PREFIX} 打 {CACHE_HIT_DISCOUNT} 折）")
print(f"        合计             = {THINKING_PER_STEP * 10 * PRICE_OUT + fresh_cost + cached_cost:.0f}")
print("      ——思考不只是【多花的钱】，它还占【上下文】。")
print("         上下文是要被后面每一步反复读的东西（第 2 课：decode 要读历史 KV）。")

# ============ [5] 必须原样带回 ============
print("\n[5] 接第 3 课：思考内容【必须原样带回去】")
print("      官方文档的原话是：把每一个 thinking 块【完整、不改动】地传回去，")
print("      挨着它当初搭配的那个 tool_use 块。")
print()
print("      这条有两种后果，取决于厂商：")
print("        · 有的直接【报错】——请求根本发不出去（400，缺 thinking 块）")
print("        · 有的【让缓存断掉】——xAI 的文档把它列成多轮缓存失效的头号原因")
print("      两种都比「慢一点」严重得多：")
print("        报错 = 跑不起来；缓存断 = 第 3 课那笔账整段重来。")
print("      所以「让模型思考」不只是多给一个参数，")
print("        你的【循环代码】也要跟着改：上一轮的思考块得存下来、原样送回去。")

# ============ [6] 对 agent 的现实检查 ============
print("\n[6] 放到 agent 上算一遍：一个跑 10 步、每步都想 2000 token 的循环")
one = simulate(THINKING_PER_STEP)
print(f"      每步多久看到答案：{one['wait']:.1f} s   x 10 步 = {one['wait'] * 10:.0f} s"
      f"（约 {one['wait'] * 10 / 60:.0f} 分钟）")
print(f"      每步相对成本    ：{one['cost']:.0f}   x 10 步 = {one['cost'] * 10:.0f}")
print("      ——这就是「多花 token 换准确率」的真实价格。")
print("         便宜的任务上开思考，等于按分钟付钱买一点用不上的准确率。")

# ============ [7] 收尾 ============
print("\n[7] 一句话")
print("      会思考的模型【不是换了个更聪明的模型】，是同一个模型被允许")
print("      在回答之前多花一点时间、多花一点 token")
print("      （官方原话：allowing the very same model to give itself more time）。")
print("      而多花的那些 token，和答案一样是输出、按 5 倍价、还占上下文、")
print("      而且必须原样带回否则请求报错或缓存断——四笔账一起算。")
print("      所以它是一个【要不要开、给多大预算】的工程决策，不是一个能力开关。")