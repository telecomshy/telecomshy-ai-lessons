"""RAG · 第 11 课配套脚本：固定流水线 vs agentic——查不查、查什么、再查不查。

这不是模型，是一台【决策流程模拟器】：
  - 检索器是玩具（二字组合 + 点积，同第 9/10 课），切块按字数切；
  - 评估器是关键词清单的替身（真实系统里换成一个模型或一个分类器）；
  - 「够不够」按问题的几个方面逐条勾，不碰标准答案。
所以它量的是【流程】——多查一轮换来了什么、预算卡在哪、什么时候该停；
不是模型能力，也不是这批数字的基准。

你会看到：
  1. 固定流水线：每道题都走同一条路，查一次就生成；
  2. 多跳题怎么靠第二轮把缺的那半找回来；
  3. 一道「切块把制度切碎了」的题——查几轮都救不回来；
  4. 轮数上限从 1 放到 5，收益在哪一轮到顶、哪一轮开始白跑；
  5. 一套停止条件的清单（轮数 / 证据 / 预算 / 拒答）。

运行：  python exercises/rag/0011-agentic-rag.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

# ============ 资料库：同第 10 课的员工手册，20 条制度、598 字 ============
FACTS = [
    ("年假天数：入职满一年者每年 5 天，满三年者 10 天，满五年者 15 天。", "满五年"),
    ("年假结转：当年没休完的年假，可以结转至次年 3 月底，逾期清零。", "结转"),
    ("请假三天以内（含三天），向直属主管口头报备即可，事后补一条消息。", "口头报备"),
    ("请假三天以上，需在系统里提交申请单，附上证明材料，主管审批后生效。", "申请单"),
    ("病假：每年 5 天带薪病假，连续两天以上需附医院证明。", "医院证明"),
    ("报销流程：每月 25 日前提交发票，财务在次月 15 日统一打款。", "25 日"),
    ("加班调休：加班满 4 小时可调休半天，调休需当月用完，过期作废。", "当月用完"),
    ("门禁卡办理：入职当天由行政统一办理，遗失补办 20 元。", "补办 20 元"),
    ("会议室预约：提前 1 天在系统预约，超时 15 分钟自动释放。", "自动释放"),
    ("办公用品：每人每月限领签字笔 2 支、笔记本 1 本。", "笔记本"),
    ("打印机：公共打印机在三楼东侧，故障报修走 IT 工单。", "工单"),
    ("工位调整：每季度可申请一次，由部门助理统一报备。", "季度"),
    ("差旅标准：高铁二等座和经济舱可以报销，住宿每晚限额 400 元。", "400 元"),
    ("着装要求：周一至周四商务休闲，周五可以穿便装。", "便装"),
    ("年假申请：年假需提前 3 个工作日在系统申请，节假日不计入。", "3 个工作日"),
    ("调休登记：调休需提前 1 天在系统登记，和加班记录对应。", "登记"),
    ("离职交接：离职需提前 30 天书面通知，交接清单由部门助理存档。", "30 天"),
    ("培训报销：与工作相关的培训费报销需主管预批，每人每年上限 3000 元。", "3000 元"),
    ("快递收发：公司前台统一收发，个人快递请勿寄到公司。", "快递"),
    ("加班餐费：加班超过 20 点可报销晚餐，上限 30 元。", "加班餐"),
]
DOCUMENT = "".join(f[0] for f in FACTS)

CHUNK_SIZE = 90   # 切中档；第 10 课量过，这一档在 20 题上 Recall@3 = 0.87
K = 2             # 固定流水线每轮只取前 2 段；故意取窄，才看得清「再查一轮」补了什么


def pad(s, width):
    """按显示宽度补空格（中日韩全角字符算 2 列）。"""
    w = sum(2 if ord(ch) > 0x2E80 else 1 for ch in s)
    return s + " " * max(0, width - w)


def chunk(text, size):
    return [text[i:i + size] for i in range(0, len(text), size)]


CHUNKS = chunk(DOCUMENT, CHUNK_SIZE)


def to_vec(text, vocab):
    pairs = [text[i:i + 2] for i in range(len(text) - 1)]
    return [pairs.count(p) for p in vocab]


def rank(query, chunks):
    """玩具检索器：按二字组合的重合度打分，分高的排前面。"""
    vocab = sorted({p for t in chunks + [query]
                    for p in [t[i:i + 2] for i in range(len(t) - 1)]})
    qv = to_vec(query, vocab)
    scored = sorted(
        ((sum(x * y for x, y in zip(to_vec(c, vocab), qv)), i)
         for i, c in enumerate(chunks)),
        key=lambda t: (-t[0], t[1]))
    return [i for _, i in scored]


def retrieve(query, k=K):
    """一次检索 = 一次工具调用。返回取到的块号。"""
    return rank(query, CHUNKS)[:k]


def facts_in(i):
    """这一块里躺着哪几条制度（按内容编号）。"""
    return {n for n, (_, marker) in enumerate(FACTS, 1) if marker in CHUNKS[i]}


# ============ 六个场景：不是新基准，是为了看清流程里的分岔 ============
# aspects：一个问题由哪几个「方面」组成。每个方面给一组关键词，
# 关键词都在已取回的文本里，才算这个方面有依据。真实系统用一个评估器做这件事。
QUESTIONS = [
    {
        "id": 1, "kind": "不用查",
        "text": "把刚才的回答整理成三行。",
        "aspects": [], "retrieve": False,
        "why": "这是对上一轮回答的整理，资料库里没有新东西可查。",
    },
    {
        "id": 2, "kind": "单跳",
        "text": "入职满五年有几天年假？",
        "aspects": [("年假天数", ["年假", "满五年"])],
    },
    {
        "id": 3, "kind": "多跳",
        "text": "我准备离职，年假还没休完怎么办？",
        "aspects": [("年假没休完", ["年假", "结转"]),
                    ("离职", ["离职", "交接"])],
        "why": "第一轮只回答了「年假怎么算」，没回答「离职时怎么交接」。",
    },
    {
        "id": 4, "kind": "多跳",
        "text": "加班调休和年假申请分别要提前多久？",
        "aspects": [("加班调休", ["调休", "登记"]),
                    ("年假申请", ["年假", "3 个工作日"])],
        "why": "第一轮答了年假申请，漏了调休登记——两个制度在不同块里。",
    },
    {
        "id": 5, "kind": "否定",
        "text": "公司有班车吗？",
        "aspects": [], "no_answer": ["班车"],
        "why": "资料库里没有「班车」这两个字；评估器判无关，应该拒答。",
    },
    {
        "id": 6, "kind": "切块坏了",
        "text": "请四天假要走什么流程？",
        "aspects": [("三天以内", ["口头报备"]),
                    ("三天以上", ["申请单"])],
        "why": "制度 3 的「口头报备」正好被 90 字的刀口切成两半，哪个块里都不完整。",
    },
]


def coverage(q, text):
    """已取回的文本覆盖了问题的哪几个方面。"""
    return {label for label, kws in q["aspects"]
            if all(kw in text for kw in kws)}


def missing(q, text):
    return [label for label, _ in q["aspects"] if label not in coverage(q, text)]


def next_query(q, text):
    """把还没覆盖的方面的关键词拼成下一轮查询。真实系统让模型改写。"""
    kws = []
    for label, ks in q["aspects"]:
        if label not in coverage(q, text):
            kws.extend(ks)
    return " ".join(dict.fromkeys(kws))


def fixed_pipeline(q):
    """固定流水线：不管问题是什么，都查一次（k 钉死），然后生成。"""
    if not q.get("retrieve", True):
        hits = retrieve(q["text"])          # 不用查也照查
        return {"calls": 1, "rounds": 1, "hits": hits,
                "status": "不用查却查了", "text": "".join(CHUNKS[i] for i in hits)}
    hits = retrieve(q["text"])
    text = "".join(CHUNKS[i] for i in hits)
    if q.get("no_answer"):
        return {"calls": 1, "rounds": 1, "hits": hits,
                "status": "有硬答风险", "text": text}
    miss = missing(q, text)
    return {"calls": 1, "rounds": 1, "hits": hits, "text": text,
            "status": "全中" if not miss else "缺 " + "、".join(miss)}


def agentic(q, max_rounds=2, check_new_evidence=True):
    """Agentic：检索是工具。每轮看结果，决定再查不查；预算到顶就停。"""
    if not q.get("retrieve", True):
        return {"calls": 0, "rounds": 0, "hits": [], "status": "跳过检索",
                "text": "", "trace": []}

    trace = []
    seen = []
    query = q["text"]
    for rd in range(1, max_rounds + 1):
        hits = retrieve(query)
        new = [i for i in hits if i not in seen]
        seen.extend(new)
        text = "".join(CHUNKS[i] for i in seen)
        miss = missing(q, text)
        trace.append((rd, query, hits, new, miss))

        if q.get("no_answer"):
            if not any(kw in text for kw in q["no_answer"]):
                return {"calls": rd, "rounds": rd, "hits": seen,
                        "status": "拒答（没有依据）", "text": text, "trace": trace}
        elif not miss:
            return {"calls": rd, "rounds": rd, "hits": seen,
                    "status": "全中", "text": text, "trace": trace}

        if rd == max_rounds:
            return {"calls": rd, "rounds": rd, "hits": seen,
                    "status": "预算到顶，缺 " + "、".join(miss),
                    "text": text, "trace": trace}
        if check_new_evidence and rd > 1 and not new:
            return {"calls": rd, "rounds": rd, "hits": seen,
                    "status": "没有新证据，停（缺 " + "、".join(miss) + "）",
                    "text": text, "trace": trace}

        query = next_query(q, text)
        if not query:                      # 没有可改写的方向了
            return {"calls": rd, "rounds": rd, "hits": seen,
                    "status": "没有可查的方向，停", "text": text, "trace": trace}

    return {"calls": max_rounds, "rounds": max_rounds, "hits": seen,
            "status": "预算到顶", "text": "", "trace": trace}


print(f"[1] 实验台：{len(DOCUMENT)} 字、{len(FACTS)} 条制度，切成 {len(CHUNKS)} 块"
      f"（每块 {CHUNK_SIZE} 字）；固定流水线每轮 top-k = {K}")
print(f"    6 个场景：不用查 1 · 单跳 1 · 多跳 2 · 否定 1 · 切块坏了 1")
print("    检索器与评估器都是玩具；量的是流程，不是模型能力。")

print("\n[2] 固定流水线：每道题都查一次，然后生成")
print(f"    {pad('题', 4)}{pad('类型', 10)}{pad('取到的块', 12)}{pad('覆盖', 30)}判定")
fixed_results = []
for q in QUESTIONS:
    r = fixed_pipeline(q)
    covered = "、".join(sorted(coverage(q, r["text"]))) or "（没有可勾的方面）"
    fixed_results.append((q, r))
    print(f"    {pad(str(q['id']), 4)}{pad(q['kind'], 10)}"
          f"{pad(str(r['hits']), 12)}{pad(covered, 30)}{r['status']}")
print("    → 多跳题只查一次，缺的那一半不会自己长出来；否定题它照样会生成。")

print("\n[3] 换成 agentic：以「加班调休和年假申请分别要提前多久？」为例")
q3 = next(q for q in QUESTIONS if q["id"] == 4)
r3 = agentic(q3, max_rounds=3)
print(f"    {pad('轮', 4)}{pad('这一轮查什么', 42)}{pad('取到', 8)}{pad('新块', 8)}还缺什么")
for rd, query, hits, new, miss in r3["trace"]:
    print(f"    {pad(str(rd), 4)}{pad(query, 42)}{pad(str(hits), 8)}"
          f"{pad(str(new), 8)}{'、'.join(miss) if miss else '（齐了）'}")
print(f"    结果：{r3['status']}；共 {r3['calls']} 次检索。")
print("    → 第一轮答了年假申请，评估器发现调休登记还没答，")
print("      改写查询再查一轮；第二轮取到调休登记，够了，停。")

print("\n[4] 轮数上限：从 1 放到 5，看收益在哪一轮到顶")
print(f"    {pad('上限', 6)}{pad('检索次数', 10)}{pad('全中', 6)}{pad('拒答', 6)}"
      f"{pad('部分/失败', 12)}白跑的轮次")
for cap in (1, 2, 3, 5):
    total_calls = solved = abstained = partial = wasted = 0
    for q in QUESTIONS:
        r = agentic(q, max_rounds=cap)
        total_calls += r["calls"]
        if r["status"] == "全中":
            solved += 1
        elif r["status"].startswith("拒答"):
            abstained += 1
        elif q.get("retrieve", True):
            partial += 1
        if cap > 1:
            wasted += sum(1 for rd, _, _, new, _ in r["trace"] if rd > 1 and not new)
    print(f"    {pad(str(cap), 6)}{pad(str(total_calls), 10)}{pad(str(solved), 6)}"
          f"{pad(str(abstained), 6)}{pad(str(partial), 12)}{wasted}")

print("\n[5] 固定流水线 vs agentic（上限 2）：多查的几次花在哪")
fixed_calls = sum(r["calls"] for _, r in fixed_results)
agent_results = [(q, agentic(q, max_rounds=2)) for q in QUESTIONS]
agent_calls = sum(r["calls"] for _, r in agent_results)
fixed_solved = sum(1 for _, r in fixed_results if r["status"] == "全中")
agent_solved = sum(1 for _, r in agent_results if r["status"] == "全中")
print(f"    固定：{fixed_calls} 次检索，全中 {fixed_solved} 题，"
      f"否定题硬答，不用查的题也查了一次")
print(f"    代理：{agent_calls} 次检索，全中 {agent_solved} 题，"
      f"否定题拒答，不用查的题 0 次")
print("    → 总次数没降反升：省下的是简单题，多花的是多跳题。")
print("      这笔账要分开记，不能只看一个总数。")

print("\n[6] 那道「切块坏了」的题：查几轮都救不回来")
q6 = next(q for q in QUESTIONS if q["id"] == 6)
for cap in (2, 5):
    r = agentic(q6, max_rounds=cap)
    print(f"    上限 {cap}：{' -> '.join(f'第{rd}轮取到{hits}' for rd, _, hits, _, _ in r['trace'])}"
          f"；结果：{r['status']}")
print("    → 制度 3 的「口头报备」被刀口切成「口头报」+「备」，哪个块里都不完整。")
print("      agentic 只能改查询，改不了已经切碎的文本；先回去修切块（第 4 课）。")

print("\n[7] 停止条件清单（写进代码，不要只写在提示词里）")
print("    ① 证据够了：问题的每个方面都能在已取回的段里找到依据 → 停，去生成。")
print("    ② 没有新证据：这一轮拿回的都是旧块，或分数没升 → 停，别再换问法硬凑。")
print("    ③ 预算到顶：轮数 / 输入 token / 墙钟时间，三个上限先到先停。")
print("    ④ 方向错了：评估器连续判无关 → 拒答或转人工，不要拿相似段落硬答。")
print("    ⑤ 资料冲突：两段说法打架 → 停下来标出来，不要自己选一个。")
print("    这五条是工程做法，不是论文原话；数字（轮数、token、时间）按你的场景定。")

