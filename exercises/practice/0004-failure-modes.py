"""技巧篇 · 0004 配套脚本：故意翻四种车，走一遍"症状 → 定位 → 救法"。

四种翻车都是玩具实现，但每种对应一种真实症状：
  ① 工具报错（接口超时）      → 读错误信息、退避重试
  ② 输出格式坏（JSON 断了）   → 靠接口钉格式（结构化输出），别靠嘴求
  ③ 撞上限截断               → 查 stop reason、调大上限重发
  ④ 不收尾（死循环）          → 最大步数护栏拦下来

不依赖任何 API。运行：  python exercises/practice/0004-failure-modes.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

import json


def symptom_1_tool_error():
    print("===== 症状 ① 工具报错 =====")
    trace = ["推理：查一下明天的航班"]

    def call_tool(try_no):
        # 玩具：前两次假装接口超时，第三次成功
        if try_no < 3:
            raise TimeoutError("get_flights 超时（网关 504）")
        return "23 个航班"

    for try_no in (1, 2, 3):
        try:
            result = call_tool(try_no)
            trace.append(f"行动：查航班 → {result}")
            print(f"  第 {try_no} 次调用成功：{result}")
            break
        except TimeoutError as e:
            trace.append(f"观察：工具报错「{e}」")
            wait = 2 ** try_no  # 退避：1 秒、2 秒……真系统里是 2/4/8 秒
            print(f"  第 {try_no} 次调用报错：{e}")
            print(f"  [当场救] 读懂错误是「超时」→ 退避 {wait}s 再试（玩具里不真等，真系统等的是秒级）")
    print(f"  [下一跑防] 超时阈值写进工具配置；重试交给 SDK（Anthropic 的 SDK 默认自动退避重试两次）")
    print(f"  [trace] {trace}")


def symptom_2_bad_format():
    print("\n===== 症状 ② 输出格式坏（JSON 断了）=====")
    bad = '{"city": "北京'  # 模型吐了个断掉的 JSON
    print(f"  模型吐出：{bad}")
    try:
        json.loads(bad)
    except json.JSONDecodeError as e:
        print(f"  [当场救] 解析报错：{e}")
        print("  [当场救] 不改提示词碰运气——开结构化输出，接口替你把格式钉住")
    good = '{"city": "北京"}'  # 开了结构化输出之后，格式是保证的
    print(f"  开结构化输出后：{good} → 解析成功：{json.loads(good)}")
    print("  [下一跑防] schema 写清字段必填；拒答时按 stop reason 另行处理，别当格式错")


def symptom_3_truncated():
    print("\n===== 症状 ③ 撞上限截断 =====")
    response = {"stop_reason": "max_tokens", "text": "第一步：先查航班，第二步：比"}
    print(f"  返回里 stop_reason＝{response['stop_reason']}，正文停在「{response['text']}」")
    print("  [当场救] 查 stop reason 就知道为什么停——max_tokens 是撞上限，不是答完")
    response = {"stop_reason": "end_turn", "text": "第一步：查航班，第二步：比价，第三步：下单"}
    print(f"  调大上限重发后：stop_reason＝{response['stop_reason']}，正文完整")
    print("  [下一跑防] 预算留白（技巧篇 0001）；回答里若有没写完的工具调用，必须调大重发")


def symptom_4_no_stop():
    print("\n===== 症状 ④ 不收尾（死循环）=====")
    max_steps = 4
    steps = 0
    try:
        for step in range(1, max_steps + 1):
            steps = step
            print(f"  第 {step} 步：模型说「再查一家」……（就是不说完成）")
        raise RuntimeError(f"达到最大步数 {max_steps} 仍未完成 → 护栏拦下")
    except RuntimeError as e:
        print(f"  [当场救] {e}")
    print("  [下一跑防] 最大步数是兜底；更根本的是给它「什么时候算完成」的约定")


if __name__ == "__main__":
    symptom_1_tool_error()
    symptom_2_bad_format()
    symptom_3_truncated()
    symptom_4_no_stop()
    print("\n带走一句：第一动作永远是看 trace——先定位是循环哪一步翻的车，救法基本就定了。")
