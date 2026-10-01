"""Agent 原理篇 · 第 2 课 配套脚本：一次工具调用的完整来回。

核心只有一句话：**模型不执行工具，它只是「说要调」**。真正去调的是你的程序。

这个脚本把整个来回打印出来：
    工具清单 → 用户问 → 模型说「我要调 X」→ 程序执行 → 结果塞回 → 模型说人话

用的是「假模型」（一个写死的小函数），好让你把注意力全放在**来回结构**上。
真模型只要换掉 fake_model() 一个函数即可，那一处有注释标明。

运行：  python exercises/agent/0002-tool-call-roundtrip.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

import json

# ============ ① 「外部世界」这一侧：你的程序能干的事 ============
WEATHER_DB = {
    "北京": {"temp_c": 26, "cond": "晴"},
    "上海": {"temp_c": 28, "cond": "多云"},
    "广州": {"temp_c": 31, "cond": "雷阵雨"},
}


def get_weather(city):
    """真的去查天气（这里假装是个数据库 / 外部 API）。"""
    if city in WEATHER_DB:
        return {"city": city, **WEATHER_DB[city]}
    return {"error": f"查不到「{city}」的天气"}


def list_cities():
    """真的去列出能查的城市。"""
    return {"cities": sorted(WEATHER_DB.keys())}


TOOLS = {
    "get_weather": get_weather,
    "list_cities": list_cities,
}

# ============ ② 我们发给模型的「工具清单」============
# 模型就靠这几行字来决定调哪个工具、参数填什么。
TOOL_LIST = [
    {
        "name": "get_weather",
        "description": "查某个城市今天的天气。返回气温（摄氏度）和天气状况。",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名，例如「北京」"}
            },
            "required": ["city"],
        },
    },
    {
        "name": "list_cities",
        "description": "列出所有可以查天气的城市。",
        "input_schema": {"type": "object", "properties": {}},
    },
]


# ============ ③ 假模型：按对话内容挑工具 ============
# 真模型就是把这个函数换成一次 API 调用，其它代码一行都不用改。
def fake_model(messages, tools):
    last = messages[-1]

    # 如果上一条是「工具结果」，就编一句人话
    if last["role"] == "tool":
        data = last["content"]
        if "cities" in data:
            return {"type": "text", "text": "我能查这些城市：" + "、".join(data["cities"]) + "。"}
        if "error" in data:
            return {"type": "text", "text": "抱歉，" + data["error"] + "。"}
        return {"type": "text",
                "text": f"{data['city']}今天 {data['temp_c']} 度，{data['cond']}。"}

    # 否则：看用户问什么，决定调哪个工具
    q = last["content"]
    if "哪些城市" in q or "能查" in q:
        return {"type": "tool_use", "name": "list_cities", "input": {}}
    if "天气" in q or "多少度" in q:
        city = next((c for c in WEATHER_DB if c in q), "北京")
        return {"type": "tool_use", "name": "get_weather", "input": {"city": city}}
    return {"type": "text", "text": "我不知道，这个问题我答不了。"}


# ============ ④ 一轮完整的来回 ============
def one_round(question, messages):
    print("\n" + "─" * 58)
    print(f"用户问：{question}")
    print("─" * 58)

    messages.append({"role": "user", "content": question})

    for step in range(1, 6):                     # 最多 5 轮，这就是一种「护栏」
        reply = fake_model(messages, TOOL_LIST)

        if reply["type"] == "text":
            print(f"\n[{step}] 模型说人话了")
            print(f"      「{reply['text']}」")
            messages.append({"role": "assistant", "content": reply["text"]})
            return

        # 模型没给答案，而是「说要调一个工具」
        print(f"\n[{step}] 模型返回的不是答案，是「一段调用意图」")
        print("      " + json.dumps(reply, ensure_ascii=False))
        messages.append({"role": "assistant", "content": reply})

        # —— 程序接手：解析 → 真的去调 ——
        fn = TOOLS[reply["name"]]
        result = fn(**reply["input"])
        print(f"\n[{step}] 程序接手：真的去调 {reply['name']}({reply['input']})")
        print("      → 返回 " + json.dumps(result, ensure_ascii=False))

        # —— 把结果塞回对话 ——
        messages.append({"role": "tool", "name": reply["name"], "content": result})
        print(f"\n[{step}] 结果塞回对话（tool_result），再问模型一次")

    print("\n⚠ 走满 5 轮还没结束——护栏把它拦下来了。")


if __name__ == "__main__":
    print("=" * 58)
    print("我们发给模型的「工具清单」——模型就靠这几行字挑工具：")
    print("=" * 58)
    for t in TOOL_LIST:
        print(f"  · {t['name']}：{t['description']}")

    history = [{"role": "system", "content": "你可以使用下列工具。"}]
    one_round("北京今天多少度？", history)
    one_round("那还有哪些城市能查？", history)

    print("\n" + "=" * 58)
    print("看清楚了：模型从头到尾只吐字。")
    print("它说「我要调 get_weather」——那是一段**文字**；")
    print("真正去调天气库的，是你的程序。")
    print("=" * 58)
