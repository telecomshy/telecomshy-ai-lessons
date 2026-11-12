# -*- coding: utf-8 -*-
"""RAG 第 8 课：上下文组装与生成（玩具演示，不调任何模型）

这一课不换检索器、不换模型，只看一件事：
检索回来的那几段，摆成什么样的一屏，交给模型。

脚本做三件事：
  1. 同一批资料，两种摆法，答案落在第几段；
  2. 答案里的引用，机器能核到哪一步、核不到哪一步；
  3. 检索不到时，一屏应该长什么样。

运行：python exercises/rag/0008-context-assembly.py
Windows 终端若中文乱码，先执行 chcp 65001。
"""

# 八段员工手册。score 是“重排之后的相关性分”，不是检索器的原始相似度。
CHUNKS = [
    {"id": 1, "title": "年假天数", "score": 0.44,
     "text": "入职满一年每年 5 天，满三年 10 天，满五年 15 天。"},
    {"id": 2, "title": "年假折算", "score": 0.39,
     "text": "年中入职的，按当年剩余日历天数折算，不足 1 天不计。"},
    {"id": 3, "title": "病假", "score": 0.71,
     "text": "每年 5 天带薪病假，连续两天以上需附医院证明。"},
    {"id": 4, "title": "请假三天以内", "score": 0.86,
     "text": "请假三天以内（含三天），向直属主管口头报备即可，事后补一条消息。"},
    {"id": 5, "title": "请假三天以上", "score": 0.73,
     "text": "请假三天以上，需在系统里提交申请单，附上证明材料，主管审批后生效。"},
    {"id": 6, "title": "年假结转", "score": 0.35,
     "text": "当年未休完的年假可结转至次年第一季度，逾期清零。"},
    {"id": 7, "title": "报销", "score": 0.68,
     "text": "差旅报销在系统里提交，附发票和行程单，财务审核后打款。"},
    {"id": 8, "title": "门禁卡", "score": 0.52,
     "text": "门禁卡入职当天由行政统一办理，遗失补办 20 元。"},
]

BY_ID = {c["id"]: c for c in CHUNKS}
QUESTION = "请五天假要走什么流程？"
ANSWER_ID = 5


def screen(order, question=QUESTION):
    """把一屏提示词打印成人能看的样子。"""
    lines = ["┌── 模型看到的那一屏 " + "─" * 26]
    for i, cid in enumerate(order, 1):
        c = BY_ID[cid]
        lines.append(f"│【资料 {i}】{c['title']}：{c['text']}")
    lines.append(f"│【问题】{question}")
    lines.append("└" + "─" * 40)
    return "\n".join(lines)


def where(order):
    """答案段落在这一屏的第几段，靠开头、中间还是结尾。"""
    pos = order.index(ANSWER_ID) + 1
    n = len(order)
    ratio = pos / n
    if ratio <= 1 / 3:
        zone = "开头"
    elif ratio > 2 / 3:
        zone = "靠后"
    else:
        zone = "中间"
    return pos, n, zone


def run_order():
    print("[1] 同一批资料，两种摆法")
    print("    检索回来八段，按重排分从高到低取六段。")
    ranked = [4, 3, 7, 5, 8, 1]  # 按 score 降序
    print()
    print("    摆法 A：按分数从高到低，直接铺")
    print(screen(ranked))
    pos, n, zone = where(ranked)
    print(f"    答案（段 5，五天假那条）落在第 {pos}/{n} 段，{zone}。")
    print("    中间是模型最容易漏掉的位置：前后都压着别的段。")

    print()
    print("    摆法 B：两头夹。第 1 名放最前，其余按名次从后往前铺到结尾，问题仍在最后")
    edge = [ranked[0], ranked[2], ranked[4], ranked[5], ranked[3], ranked[1]]
    print(screen(edge))
    pos, n, zone = where(edge)
    print(f"    答案现在在第 {pos}/{n} 段，{zone}。")
    print("    资料一段没多、一段没少，只是换了个摆法。")


def parse_citations(answer):
    """从回答里抠出 [资料 N]，返回 N 的列表。"""
    out = []
    i = 0
    while True:
        start = answer.find("[资料 ", i)
        if start == -1:
            break
        end = answer.find("]", start)
        if end == -1:
            break
        num = answer[start + 4:end]
        out.append(int(num) if num.isdigit() else -1)
        i = end + 1
    return out


def check_citation(answer, order, quote):
    """核两件事：编号在不在这一屏里；引的那句话是不是逐字出现在那一段。"""
    problems = []
    nums = parse_citations(answer)
    if not nums:
        problems.append("没有标出处")
    for num in nums:
        if num < 1 or num > len(order):
            problems.append(f"[资料 {num}] 不在这一屏里（一共只有 {len(order)} 段）")
            continue
        cid = order[num - 1]
        if quote not in BY_ID[cid]["text"]:
            problems.append(f"引文不在【资料 {num}】（{BY_ID[cid]['title']}）里")
    return problems


def run_citation():
    print()
    print("[2] 引用核对：能抓编出处，抓不了推错")
    edge = [4, 7, 8, 1, 5, 3]  # 与 [1] 的摆法 B 同一屏；答案段 5 是【资料 5】

    good = "请五天假要在系统里提交申请单，附上证明材料，主管审批后生效。[资料 5]"
    quote = "请假三天以上，需在系统里提交申请单，附上证明材料，主管审批后生效。"
    print("    回答 A：", good)
    print("    核对结果：", check_citation(good, edge, quote) or "编号和引文都对得上")

    fake = "请五天假口头报备即可。[资料 9]"
    print()
    print("    回答 B：", fake)
    print("    核对结果：", "；".join(check_citation(fake, edge, "口头报备")))

    wrong = "请五天假口头报备即可。[资料 1]"
    print()
    print("    回答 C：", wrong)
    result = check_citation(wrong, edge, "口头报备")
    print("    核对结果：", result or "机器这两关都过了")
    print("    注意：这段只覆盖「三天以内」。机器只能证明「口头报备」四个字在这段里，")
    print("      证明不了这段能推出「五天」。引用核对是核对出处，不是核对结论。")


def run_refusal():
    print()
    print("[3] 检索不到时，一屏应该怎么长")
    threshold = 0.30
    print(f"    拒答阈值：{threshold:.2f}（这道线来自重排分，见第 6 课）")

    print()
    print("    问题：「公司有班车吗？」")
    print("    检索回来的最高分：0.18")
    print("    → 低于阈值，不进提示词。")
    print("    → 兜底句：资料里没有找到和「班车」相关的内容。")

    print()
    print("    问题：", QUESTION)
    print("    检索回来的最高分：0.86")
    print("    → 高于阈值，正常组装。")
    print("    → 如果这一屏里没有能回答的段，仍然要回兜底句，不能拿相似的段硬凑。")


def run_recipe():
    print()
    print("[4] 一屏的五个决定")
    print("    顺序：最相关的放开头，其次的放结尾，问题放最后")
    print("    段数：够回答就行；单点事实一两段，多跳按需要的证据段数")
    print("    标签：每段带编号和来源，让模型和你都能指回原文")
    print("    约束：只依据资料；先引原文再回答；资料里没有就说没有")
    print("    拒答：最高分低于阈值，或这一屏里没有答案，统一走兜底句")


if __name__ == "__main__":
    run_order()
    run_citation()
    run_refusal()
    run_recipe()
