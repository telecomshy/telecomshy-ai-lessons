"""Agent 原理篇 · 第 3 课 配套脚本：从零手写一个最小 agent（多步 + 工具调用 + 护栏）。

前面两课是零件：
    第 1 课  给了循环骨架（推理 → 行动 → 观察 → 再推理）
    第 2 课  给了工具调用的来回（tool_use / tool_result）
这一课把它们装在一起 —— 装完就是个真的 agent。

注意：agent 的全部核心代码就是 run_agent() 那十几行。别的都是零件。

用的是「假模型」（fake_model），好让你盯住循环结构。
真模型只要换掉 fake_model() 一个函数即可，那一处有注释标明。

运行：  python exercises/agent/0003-mini-agent.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

import json

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

TOOL_LIST = [
    {"name": "get_weather",
     "description": "查某个城市今天的天气。返回气温（摄氏度）和天气状况。",
     "input_schema": {"type": "object",
                      "properties": {"city": {"type": "string", "description": "城市名，例如「北京」"}},
                      "required": ["city"]}},
    {"name": "list_cities",
     "description": "列出所有可以查天气的城市。",
     "input_schema": {"type": "object", "properties": {}}},
]


# ============ 假模型 ============
# 真模型：把整个函数体换成一次 API 调用即可，其它代码一行不用改。
def fake_model(messages, tools):
    asked = next(m["content"] for m in reversed(messages) if m["role"] == "user")

    # 看看这一轮已经拿到了什么（这一步叫「看观察」）
    got = {}
    listed = False
    for m in messages:
        if m["role"] != "tool":
            continue
        if m["name"] == "get_weather" and "city" in m["content"]:
            got[m["content"]["city"]] = m["content"]
        if m["name"] == "list_cities":
            listed = True

    # 问题类型 A：比较两个城市 → 需要连调两次工具
    if "比" in asked and ("热" in asked or "冷" in asked):
        cities = [c for c in WEATHER_DB if c in asked]
        if len(cities) >= 2:
            missing = [c for c in cities if c not in got]
            if missing:
                return {"type": "tool_use", "name": "get_weather", "input": {"city": missing[0]}}
            a, b = cities[0], cities[1]
            d = got[b]["temp_c"] - got[a]["temp_c"]
            word = "热" if d > 0 else ("冷" if d < 0 else "一样热，都是")
            tail = f"{abs(d)} 度" if d != 0 else ""
            return {"type": "text",
                    "text": f"{b}比{a}{word} {tail}（{a} {got[a]['temp_c']} 度 / {b} {got[b]['temp_c']} 度）。"}

    # 问题类型 B：问某个城市的天气
    if "多少度" in asked or "天气" in asked:
        city = next((c for c in WEATHER_DB if c in asked), None)
        if city and city not in got:
            return {"type": "tool_use", "name": "get_weather", "input": {"city": city}}
        if city:
            return {"type": "text", "text": f"{city}今天 {got[city]['temp_c']} 度，{got[city]['cond']}。"}

    # 问题类型 C：问有哪些城市
    if "哪些城市" in asked or "能查" in asked:
        if not listed:
            return {"type": "tool_use", "name": "list_cities", "input": {}}
        return {"type": "text", "text": "我能查这些城市：" + "、".join(WEATHER_DB) + "。"}

    return {"type": "text", "text": "这个问题我答不了。"}


# ============ agent 的全部核心代码：就这个循环 ============
def run_agent(question, tools=TOOL_LIST, max_steps=5):
    messages = [
        {"role": "system", "content": "你可以使用下列工具来回答问题。"},
        {"role": "user", "content": question},
    ]
    trace = []

    for step in range(1, max_steps + 1):
        reply = fake_model(messages, tools)          # ① 推理

        if reply["type"] == "text":                  # 模型认为说完了 → 停
            trace.append((step, "完成", reply["text"]))
            return {"status": "done", "answer": reply["text"], "steps": step, "trace": trace}

        fn = TOOLS[reply["name"]]                    # ② 行动
        result = fn(**reply["input"])
        trace.append((step, "调工具", f"{reply['name']}({reply['input']}) → {json.dumps(result, ensure_ascii=False)}"))

        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "tool", "name": reply["name"], "content": result})   # ③ 观察

    return {"status": "hit_max_steps", "answer": None, "steps": max_steps, "trace": trace}   # 护栏


# ============ 跑三个问题看 trace ============
if __name__ == "__main__":
    QUESTIONS = [
        "北京今天多少度？",          # 1 步
        "上海比北京热多少？",        # 2 次调工具 —— 看它怎么连环调
        "有哪些城市能查？",          # 1 步
    ]

    for q in QUESTIONS:
        print("\n" + "─" * 58)
        print(f"用户问：{q}")
        print("─" * 58)
        r = run_agent(q)
        for step, kind, detail in r["trace"]:
            print(f"  [{step}] {kind}：{detail}")
        print(f"  >> {r['status']}，共走 {r['steps']} 步")

    print("\n" + "=" * 58)
    print("看 trace：每一步都是「推理 → 行动 → 观察」转一圈。")
    print("agent 能连环调工具，靠的就是把观察塞回去再走一轮。")
    print("=" * 58)
