"""Agent 原理篇 · 第 1 课 配套脚本：一个最小 agent 循环。

特点：不依赖任何框架，也不需要真实 LLM API。
模型被替换成一个「假模型」(fake_model)，好让你把注意力全放在循环机制上。
真实世界里，fake_model 那个位置就是一次 LLM 调用。

运行：  python exercises/agent/0001-minimal-agent.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

# ---- 工具：agent 能对外做的事 ----
def reverse_string(s: str) -> str:
    return s[::-1]


def string_length(s: str) -> int:
    return len(s)


TOOLS = {
    "reverse_string": reverse_string,
    "string_length": string_length,
}


# ---- 假模型：真实世界里，这里是一次 LLM 调用 ----
# 输入：到目前为止的轨迹(trace)。输出：一个动作(action)。
def fake_model(trace):
    used = {s["tool"] for s in trace if s["type"] == "action"}

    if "reverse_string" not in used:
        return {"tool": "reverse_string", "args": {"s": "hello"}}

    rev = next(s["result"] for s in trace
               if s["type"] == "observation" and s["tool"] == "reverse_string")

    if "string_length" not in used:
        return {"tool": "string_length", "args": {"s": rev}}

    n = next(s["result"] for s in trace
             if s["type"] == "observation" and s["tool"] == "string_length")

    return {"final": rev + str(n)}


# ---- 循环：agent 的心脏 ----
def run_agent(task, max_steps=8):
    print(f"任务：{task}")
    trace = []

    for step in range(1, max_steps + 1):
        print(f"\n--- 第 {step} 步：推理 ---")
        action = fake_model(trace)
        print("模型决定：", action)

        if "final" in action:
            print("\n[完成] 最终答案：", action["final"])
            print(f"（共用了 {step} 步）")
            return action["final"]

        tool = action["tool"]
        result = TOOLS[tool](**action["args"])

        trace.append({"type": "action", "tool": tool, "args": action["args"]})
        trace.append({"type": "observation", "tool": tool, "result": result})
        print(f"--- 观察：{tool}({action['args']}) -> {result}")

    raise RuntimeError(
        "达到最大步数仍未完成 —— 这就是经典的 agent 失败模式：死循环。"
    )


if __name__ == "__main__":
    run_agent("把 'hello' 反转，再拼上它的长度")
