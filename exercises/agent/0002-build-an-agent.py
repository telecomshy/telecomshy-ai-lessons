"""Agent 篇 · 第 2 课 配套脚本：手写一个 agent（真模型版）。

核心就一个函数 run_agent()：agent 的全部秘密就是这个 for 循环。

跑之前要做三件事（课里第 1～5 节一步一步讲）：
  1. 装包：python -m pip install -U openai python-dotenv
  2. 申请 key：https://platform.deepseek.com/api_keys
  3. 在仓库根目录建 .env，写一行：DEEPSEEK_API_KEY=sk-...

用法：
  python exercises/agent/0002-build-an-agent.py --check     几乎不花钱，验通路
  python exercises/agent/0002-build-an-agent.py             跑四个问题
  python exercises/agent/0002-build-an-agent.py --max-steps 1   制造一次撞护栏的失败

可选环境变量（写在 .env 或 PowerShell 里都行）：
  DEEPSEEK_MODEL     默认 deepseek-flash
  DEEPSEEK_BASE_URL  默认 https://api.deepseek.com

Windows 终端若中文乱码：先执行  chcp 65001
"""

import argparse
import json
import os
import sys
import time

try:
    import openai
    from dotenv import load_dotenv
    from openai import OpenAI
except ModuleNotFoundError as e:
    print(f"缺包：{e.name}")
    print("先确认 .venv 已激活，再装：python -m pip install -U openai python-dotenv")
    raise SystemExit(1)

# 从本文件所在目录逐级往上找 .env —— 放在仓库根目录就行，在哪个目录运行都找得到。
load_dotenv()

MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-flash")
BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com").rstrip("/")

# ============ 外部世界：工具 ============
WEATHER_DB = {
    "北京": {"temp_c": 26, "cond": "晴"},
    "上海": {"temp_c": 28, "cond": "多云"},
    "广州": {"temp_c": 31, "cond": "雷阵雨"},
}


def get_weather(city):
    if city in WEATHER_DB:
        return {"city": city, **WEATHER_DB[city]}
    return {"error": f"查不到「{city}」的天气"}


def list_cities():
    return {"cities": sorted(WEATHER_DB.keys())}


TOOLS = {"get_weather": get_weather, "list_cities": list_cities}

# 工具清单：名字 + 一句话说明 + 参数。模型就是照着这三样挑工具、填参数的。
TOOL_LIST = [
    {"type": "function",
     "function": {
         "name": "get_weather",
         "description": "查某个城市今天的天气。返回气温（摄氏度）和天气状况。",
         "parameters": {"type": "object",
                        "properties": {"city": {"type": "string", "description": "城市名，例如「北京」"}},
                        "required": ["city"]}}},
    {"type": "function",
     "function": {
         "name": "list_cities",
         "description": "列出所有可以查天气的城市。",
         "parameters": {"type": "object", "properties": {}}}},
]

# ============ 真模型：一次接口调用，适配成循环要的形状 ============
CLIENT = None
USAGE = {"prompt_tokens": 0, "completion_tokens": 0}

# deepseek-flash 空闲时段的价（元 / 百万 token，缓存未命中）。
# 价格会变：https://api-docs.deepseek.com/zh-cn/quick_start/pricing
PRICE_IN_PER_M = 1.0
PRICE_OUT_PER_M = 4.0


def get_client():
    global CLIENT
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not key:
        print("=" * 58)
        print("还没找到 DEEPSEEK_API_KEY，先把 key 放好再跑：")
        print("  1. 在仓库根目录建一个 .env（不是 .env.txt）")
        print("  2. 里面写一行：DEEPSEEK_API_KEY=sk-...")
        print("  3. 确认 .env 已在 .gitignore 里（本仓库已加）")
        print("=" * 58)
        sys.exit(1)

    if CLIENT is None:
        CLIENT = OpenAI(api_key=key, base_url=BASE_URL, timeout=90.0, max_retries=2)
    return CLIENT


def call_model(messages, tools):
    """一次真实的 LLM 调用。错误都翻译成看得懂的话。"""
    client = get_client()
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            extra_body={"thinking": {"type": "disabled"}},   # 本课只看循环，关掉思考模式
        )
    except openai.AuthenticationError:
        raise SystemExit("401 认证失败：key 不对或已失效。去 platform.deepseek.com/api_keys 重发一个，"
                         "注意 .env 里不要有引号和空格。")
    except openai.RateLimitError:
        raise SystemExit("429 限流：请求太快，等一会儿再试。")
    except openai.APIStatusError as e:
        if e.status_code == 402:
            raise SystemExit("402 余额不足：去 platform.deepseek.com/top_up 充值。")
        raise SystemExit(f"接口报错 {e.status_code}：{e.message[:300]}")
    except openai.APIConnectionError as e:
        raise SystemExit(f"连不上 {BASE_URL}：{e}\n（检查网络/代理；公司网络可能需要设 HTTPS_PROXY）")

    u = resp.usage
    if u:
        USAGE["prompt_tokens"] += u.prompt_tokens or 0
        USAGE["completion_tokens"] += u.completion_tokens or 0
    return resp.choices[0].message


def model_fn(messages, tools):
    """输入到目前为止的对话，输出下一步动作 —— 和循环的约定只有两种形状：
       {"type": "text", "text": ...}
       {"type": "tool_use", "calls": [{"name", "input", "tool_msg"}, ...], "history": [...]}
       history ＝ 这轮「模型说的那句」怎么塞回对话；tool_msg ＝ 一条结果怎么塞回。
       （两种塞法都由模型侧适配，循环不用管。）"""
    m = call_model(messages, tools)

    if m.tool_calls:
        calls = [{"name": tc.function.name,
                  "input": json.loads(tc.function.arguments or "{}"),
                  "tool_msg": (lambda tid: lambda result: {
                      "role": "tool", "tool_call_id": tid,
                      "content": json.dumps(result, ensure_ascii=False)})(tc.id)}
                 for tc in m.tool_calls]
        return {"type": "tool_use", "calls": calls,
                "history": [m.model_dump(exclude_none=True)]}   # 接口要求：模型说的那句原样放回

    return {"type": "text", "text": (m.content or "").strip()}


# ============ agent 的全部核心代码：就这个循环 ============
def run_agent(question, model_fn, max_steps=6):
    messages = [
        {"role": "system", "content": "你可以使用下列工具来回答问题。"},
        {"role": "user", "content": question},
    ]
    trace = []

    for step in range(1, max_steps + 1):
        reply = model_fn(messages, TOOL_LIST)         # ① 推理

        if reply["type"] == "text":                   # 模型认为说完了 → 停
            trace.append((step, "完成", reply["text"]))
            return {"status": "done", "answer": reply["text"], "steps": step, "trace": trace}

        messages += reply["history"]                  # ③ 观察（上半）：它说的那句

        for call in reply["calls"]:                   # ② 行动：模型一次可能要调好几个工具
            fn = TOOLS.get(call["name"])
            if fn is None:                            # 真模型真会编出不存在的工具
                result = {"error": f"没有这个工具：{call['name']}"}
            else:
                try:
                    result = fn(**call["input"])      # 真模型真会填错参数
                except Exception as e:
                    result = {"error": f"工具执行出错：{e}"}

            trace.append((step, "调工具",
                          f"{call['name']}({call['input']}) -> {json.dumps(result, ensure_ascii=False)}"))
            messages.append(call["tool_msg"](result))   # ③ 观察（下半）：结果逐条塞回

    return {"status": "hit_max_steps", "answer": None, "steps": max_steps, "trace": trace}   # 护栏


def run_stage(title, questions, max_steps):
    print("\n" + "=" * 58)
    print(title)
    print("=" * 58)
    for q in questions:
        print("\n" + "─" * 58)
        print(f"用户问：{q}")
        print("─" * 58)
        t0 = time.perf_counter()
        r = run_agent(q, model_fn, max_steps)
        for step, kind, detail in r["trace"]:
            lines = detail.splitlines() or [""]
            print(f"  [{step}] {kind}：{lines[0]}")
            for line in lines[1:]:
                print(f"      {line}")
        print(f"  >> {r['status']}，共走 {r['steps']} 步，耗时 {time.perf_counter() - t0:.1f} 秒")


def print_bill():
    cost = (USAGE["prompt_tokens"] / 1_000_000 * PRICE_IN_PER_M
            + USAGE["completion_tokens"] / 1_000_000 * PRICE_OUT_PER_M)
    print("\n" + "=" * 58)
    print("这几次调用一共花掉了：")
    print(f"  输入 token：{USAGE['prompt_tokens']}   输出 token：{USAGE['completion_tokens']}")
    print(f"  按空闲时段价估算：约 {cost:.5f} 元（缓存命中会更便宜）")
    print("=" * 58)


def main():
    ap = argparse.ArgumentParser(description="Agent 篇第 2 课的配套脚本")
    ap.add_argument("--check", action="store_true", help="只做一次很小的调用，验 key 和网络")
    ap.add_argument("--max-steps", type=int, default=6, help="最大步数（护栏），默认 6")
    args = ap.parse_args()

    print(f"模型：{MODEL}   接口：{BASE_URL}")

    if args.check:
        client = get_client()
        t0 = time.perf_counter()
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": "只回复两个字：收到"}],
                max_tokens=16,
                extra_body={"thinking": {"type": "disabled"}},
            )
        except openai.AuthenticationError:
            raise SystemExit("401 认证失败：key 不对。检查 .env 里的 DEEPSEEK_API_KEY 有没有多空格或引号。")
        except openai.APIStatusError as e:
            if e.status_code == 402:
                raise SystemExit("402 余额不足：去 platform.deepseek.com/top_up 充值。")
            raise SystemExit(f"接口报错 {e.status_code}：{e.message[:300]}")
        except openai.APIConnectionError as e:
            raise SystemExit(f"连不上 {BASE_URL}：{e}")
        u = resp.usage
        print(f"回复：{resp.choices[0].message.content.strip()}")
        print(f"用掉 token：输入 {u.prompt_tokens} / 输出 {u.completion_tokens}"
              f"，耗时 {time.perf_counter() - t0:.1f} 秒")
        print("通路正常，可以跑正式的了：python exercises/agent/0002-build-an-agent.py")
        return

    get_client()
    run_stage("真模型（deepseek-flash）：同一个 run_agent，看它怎么走", [
        "北京今天多少度？",
        "上海比北京热多少？",
        "有哪些城市能查？",
        "魔都今天多少度？",
    ], args.max_steps)
    print_bill()


if __name__ == "__main__":
    main()
