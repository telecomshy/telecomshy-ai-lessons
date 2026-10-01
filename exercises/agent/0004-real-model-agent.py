"""Agent 原理篇 · 第 4 课 配套脚本：把假模型换成真模型。

关键看点：**骨架一行没改**。
0003 里的 run_agent() 原样搬过来，只把 fake_model() 换成 real_model()。

真模型走 OpenAI 兼容接口（OpenAI / DeepSeek / 智谱 / Moonshot / OpenRouter 都算）。
只用标准库，不用 pip install 任何东西。

配置（环境变量）：
    OPENAI_API_KEY   必填   你的 key
    OPENAI_BASE_URL  选填   接口地址，默认 https://api.openai.com/v1
    OPENAI_MODEL     选填   模型名，默认 gpt-4o-mini

PowerShell 里这么设（只对当前窗口有效）：
    $env:OPENAI_API_KEY = "sk-..."
    $env:OPENAI_MODEL   = "gpt-4o-mini"

运行：  python exercises/agent/0004-real-model-agent.py
Windows 终端若中文乱码：先执行  chcp 65001

⚠ 这会真的花钱（虽然很少）。跑一次大概几厘到几分钱。
"""

import json
import os
import sys
import urllib.error
import urllib.request

# ============ 配置 ============
API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()
BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

USAGE = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}   # 记账：真模型要花钱

# ============ 外部世界：工具（和 0003 一模一样） ============
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

TOOL_LIST = [
    {"name": "get_weather",
     "description": "查某个城市今天的天气。返回气温（摄氏度）和天气状况。",
     "parameters": {"type": "object",
                    "properties": {"city": {"type": "string", "description": "城市名，例如「北京」"}},
                    "required": ["city"]}},
    {"name": "list_cities",
     "description": "列出所有可以查天气的城市。",
     "parameters": {"type": "object", "properties": {}}},
]


# ============ 真模型：一次 HTTP 调用 ============
def call_chat(messages, tools):
    body = {
        "model": MODEL,
        "messages": messages,
        "tools": [{"type": "function", "function": t} for t in tools],
    }
    req = urllib.request.Request(
        BASE_URL + "/chat/completions",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + API_KEY},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"\n接口报错 {e.code}：{e.read().decode('utf-8', 'ignore')[:300]}\n"
                         f"（401 = key 不对；429 = 限流或欠费；404 = 模型名 / 接口地址不对）")
    except urllib.error.URLError as e:
        raise SystemExit(f"\n连不上接口：{e.reason}\n（检查网络，或 OPENAI_BASE_URL 是否写对）")

    u = data.get("usage") or {}
    for k in USAGE:
        USAGE[k] += u.get(k, 0) or 0
    return data["choices"][0]["message"]


def real_model(messages, tools):
    """把真模型的返回，统一成和 fake_model 一样的形状：{"type": "tool_use"|"text", ...}"""
    m = call_chat(messages, tools)

    if m.get("tool_calls"):                       # 模型想调工具
        tc = m["tool_calls"][0]
        return {"type": "tool_use",
                "name": tc["function"]["name"],
                "input": json.loads(tc["function"].get("arguments") or "{}"),
                "raw": m}                          # 接口要求把这句话原样放回历史

    return {"type": "text", "text": (m.get("content") or "").strip(),
            "raw": {"role": "assistant", "content": m.get("content")}}


# ============ agent 的骨架：和 0003 一模一样 ============
def run_agent(question, tools=TOOL_LIST, max_steps=6):
    messages = [
        {"role": "system", "content": "你可以使用下列工具来回答问题。"},
        {"role": "user", "content": question},
    ]
    trace = []

    for step in range(1, max_steps + 1):
        reply = real_model(messages, tools)                # ① 推理

        if reply["type"] == "text":                        # 模型认为说完了 → 停
            trace.append((step, "完成", reply["text"]))
            return {"status": "done", "answer": reply["text"],
                    "steps": step, "trace": trace}

        fn = TOOLS.get(reply["name"])
        if fn is None:                                     # 真模型真会编出不存在的工具
            result = {"error": f"没有这个工具：{reply['name']}"}
        else:
            try:
                result = fn(**reply["input"])              # ② 行动
            except Exception as e:
                result = {"error": f"工具执行出错：{e}"}   # 真模型真会填错参数

        trace.append((step, "调工具",
                      f"{reply['name']}({reply['input']}) -> {json.dumps(result, ensure_ascii=False)}"))

        messages.append(reply["raw"])                      # ③ 观察
        messages.append({"role": "tool",
                         "tool_call_id": reply["raw"].get("tool_calls", [{}])[0].get("id"),
                         "content": json.dumps(result, ensure_ascii=False)})

    return {"status": "hit_max_steps", "answer": None,
            "steps": max_steps, "trace": trace}            # 护栏


# ============ 跑三个问题看差异 ============
if __name__ == "__main__":
    if not API_KEY:
        print("还没配 API key。PowerShell 里执行：")
        print('    $env:OPENAI_API_KEY = "sk-..."')
        print("（可选）$env:OPENAI_BASE_URL = \"https://api.deepseek.com/v1\"")
        print("（可选）$env:OPENAI_MODEL   = \"deepseek-chat\"")
        sys.exit(1)

    print(f"模型：{MODEL}   接口：{BASE_URL}")

    QUESTIONS = [
        "北京今天多少度？",
        "上海比北京热多少？",      # 看它能不能连着调两次
        "魔都今天多少度？",        # 真模型该认出「魔都」= 上海；假模型会翻车
    ]

    for q in QUESTIONS:
        print("\n" + "-" * 58)
        print(f"用户问：{q}")
        print("-" * 58)
        r = run_agent(q)
        for step, kind, detail in r["trace"]:
            print(f"  [{step}] {kind}：{detail}")
        print(f"  >> {r['status']}，共走 {r['steps']} 步")

    print("\n" + "=" * 58)
    print("这几次调用一共花了：")
    print(f"  输入 token：{USAGE['prompt_tokens']}   输出 token：{USAGE['completion_tokens']}")
    print(f"  合计：{USAGE['total_tokens']} 个 token（真金白银）")
    print("=" * 58)
