"""LLM 底层 · 第 3 课 配套脚本：模拟「前缀缓存」，看你的请求结构能命中多少缓存。

不依赖任何 API。为了演示，粗暴地把「一个空格分隔的词」当成 1 个 token。
真实世界里分词方式不同，但"前缀匹配"这个机制是一模一样的。

运行：  python exercises/llm/0003-cache-hit-simulator.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

# ---- 模拟的 KV 缓存：只记住"上一次请求的完整 token 序列" ----
class PrefixCache:
    def __init__(self):
        self.cached = []

    def request(self, prompt_tokens, price_per_token=1.0, hit_discount=0.1):
        """返回 (命中 token 数, 总 token 数, 等效成本)。

        命中读取按 hit_discount 折价（现实中约 0.1 倍）；
        未命中的部分按原价重算。
        """
        hit = 0
        for a, b in zip(self.cached, prompt_tokens):
            if a == b:
                hit += 1
            else:
                break  # 一旦对不上，从这里往后全部作废

        total = len(prompt_tokens)
        cost = (total - hit) * price_per_token + hit * price_per_token * hit_discount
        self.cached = prompt_tokens  # 本次请求的完整前缀成为新的缓存
        return hit, total, cost


# ---- 一个 agent 请求的四个部分（注意顺序：稳定的在前，易变的在后）----
SYSTEM = (
    "你是客服系统「小助手」的对话代理 "
    "工作规则 1 只依据知识库回答 2 每句话给出文档编号 3 不确定就说不确定 "
    "4 涉及退款必须提醒核对订单号 5 语气友好 不要用感叹号"
)
TOOLS = (
    "可用工具 查知识库search_kb(query) 取文档get_doc(doc_id) 查订单get_order(order_id) "
    "发起退款refund(order_id,amount) 发邮件send_email(to,body)"
)
HISTORY = (
    "对话历史 用户:你好 助手:你好请问有什么可以帮你 用户:我上周买的鞋想退 "
    "助手:好的请提供订单号 用户:订单号是A12345 助手:收到我先帮你查一下状态"
)


def build_prompt(user_msg, system=SYSTEM, tools=TOOLS, history=HISTORY):
    return f"{system} {tools} {history} {user_msg}".split()


def run(label, prompts, price_per_token=1.0, hit_discount=0.1):
    cache = PrefixCache()
    print(f"\n=== {label} ===")
    total_cost = 0.0
    for q, p in prompts:
        hit, total, cost = cache.request(p, price_per_token, hit_discount)
        total_cost += cost
        print(f"  {q!r:<10} 总长 {total:>3}  命中 {hit:>3}  "
              f"命中率 {hit / total:>5.0%}  等效成本 {cost:>6.1f}")
    print(f"  --> 合计等效成本：{total_cost:.1f}")
    return total_cost


if __name__ == "__main__":
    questions = ["能不能退", "几天到账", "要寄回去吗", "运费谁出", "那就退吧", "谢谢"]

    # A. 推荐结构：稳定内容（系统提示/工具/历史）在前，只有最后一句在变
    good = [(q, build_prompt(q)) for q in questions]

    # B. 踩坑结构：把"每次都变"的用户名塞进了系统提示的最前面
    users = ["alice", "bob", "carol", "dave", "erin", "frank"]
    bad = [
        (q, build_prompt(q, system=f"你是客服系统小助手(当前用户:{users[i]}) " + SYSTEM))
        for i, q in enumerate(questions)
    ]

    cost_good = run("A. 前缀稳定（推荐）", good)
    cost_bad = run("B. 系统提示最前面塞了每次都变的用户名（踩坑）", bad)

    print(f"\n结论：B 比 A 贵了约 {cost_bad / cost_good:.1f} 倍。")
    print("只改动开头一个细节，后面所有缓存就全废了——这就是前缀的威力。")
