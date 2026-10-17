"""Agent 原理篇 · 第 7 课 配套脚本：两层记忆的小模拟。

看点：
  会话 1：用户说了偏好 → 上下文越来越长 → 撞到预算 → 摘要存进长时记忆
  会话 2：上下文从零开始（模型已经"忘了"）→ 先答一次 → 程序取回长时记忆
          → 条目塞回上下文 → 再答一次就"记得"了
结论：记忆不是模型的功能，是外面的程序替它存、替它取；取回的东西
      也得塞回上下文，模型才看得见。

不依赖任何 API。运行：  python exercises/agent/0007-memory.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

BUDGET = 25  # 上下文预算，单位"字"（玩具口径，真系统按 token 算）

long_term = []  # 长时记忆：存在外面的条目


def remember(text, tags):
    long_term.append({"text": text, "tags": set(tags)})
    print(f"  [长时记忆] 存下一条：{text}")


def recall(keywords):
    got = [m["text"] for m in long_term if m["tags"] & set(keywords)]
    print(f"  [长时记忆] 按关键词「{'/'.join(keywords)}」取回 {len(got)} 条：{got}")
    return got


def fake_model(context, task):
    """假模型：它能看见的只有 context，别的什么都看不见。"""
    joined = "".join(context)
    print(f"  [模型] 我能看见的全部＝上下文 {len(joined)} 字")
    if "靠窗" in joined and "东航" in joined:
        return "给您选了东航 620 元那班，加 20 元要了靠窗"
    return "不知道您的偏好，选了最便宜的那班"


def session1():
    print("===== 会话 1：用户交代偏好 =====")
    context = []
    for turn in ["我的偏好：爱坐东航", "我的偏好：座位要靠窗", "我的偏好：住浦东，出发走虹桥"]:
        context.append(turn)
        used = sum(len(t) for t in context)
        print(f"[上下文] +「{turn}」 已用 {used}/{BUDGET} 字")
        if used > BUDGET:
            # 塞爆了：把旧话压成一条摘要，摘要存进长时记忆，上下文重新开始
            summary = "用户偏好汇总：东航、靠窗、虹桥出发"
            print(f"  [上下文] 塞爆了 → 压缩成「{summary}」，旧内容不白扔")
            remember(summary, tags=["订票", "偏好"])
            context = [summary]
    return context


def session2():
    print("\n===== 会话 2：第二天，上下文从零开始 =====")
    task = "任务：帮用户订明天上海到北京的机票"
    context = [task]
    print(f"[上下文] {task}")

    print("\n-- 先不取回长时记忆 --")
    print("  [回答]", fake_model(context, task))

    print("\n-- 程序替它取回长时记忆，塞进上下文 --")
    for note in recall(["订票", "偏好"]):
        context.append("长时记忆：" + note)
    print(f"  [上下文] 取回后＝{context}")
    print("  [回答]", fake_model(context, task))


if __name__ == "__main__":
    session1()
    session2()
    print("\n结论：模型两轮都只看得见「上下文」。所谓记忆，是程序存的、程序取的。")
