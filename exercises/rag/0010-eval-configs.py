"""RAG · 第 10 课配套脚本：把「切多大，好不好」量出来。

上一课给了尺子（Recall@k / MRR / Precision@k），这一课用尺子做一次
【对照实验】：同一批文档、同一套题、同一把尺子，只动一个变量——
切块大小。三张成绩单的差距，就是「这批文档该切多大」的答案。

你会看到：
  1. 一份 20 题标注集的模板长什么样（单跳 / 多跳 / 否定，答案标「内容」不标「块号」）
  2. 三个切块配置各跑一遍，三张成绩单并排看
  3. 逐题对账：哪些题在哪个配置翻的车，丢分丢在「切碎」还是「没进前 k」
  4. 否定题单独处理（它们没有「该命中的段」）
  5. 一段可以直接抄走的结论模板（检索侧先筛，生成侧判官再比）
  6. 忠实度判官的提示词模板（只有方法，不调任何模型）

⚠ 检索器仍是玩具（二字组合 + 点积），切块按字数切（第 4 课说过，量级和按 token 切一样）。
⚠ 全脚本不装包、不调 API。把标注集换成你自己的题，流程原样能跑。

运行：  python exercises/rag/0010-eval-configs.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

# ============ 资料库：一整份员工手册，20 条制度 ============
# 故意连成一份长文档（不是切好的段），切块大小才有得选。
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

# ============ 标注集模板：20 题 ============
# 这是全脚本唯一需要人工的部分，也是你要替换成自己业务的部分。
# 标注规则（第 9 课立的）：
#   每题标「答案需要哪几条制度」，用内容编号（第几条事实），【不标第几块】——
#   块号随切块大小变，内容不变。换了配置标注照样能用，这是能对照的前提。
#   否定题（资料里根本没有答案）标空列表，它们专测拒答，不进检索平均分。
#   20 条制度不必条条有题：标注集求的是【代表性】（常问的都覆盖），不是穷尽。
QUESTIONS = [
    # —— 单跳：答案在一条制度里 ——
    ("单跳", "入职四年，年假有几天？", [1]),
    ("单跳", "请两天假要走什么流程？", [3]),
    ("单跳", "请五天假要走什么流程？", [4]),
    ("单跳", "发票最晚什么时候交？", [6]),
    ("单跳", "加班能不能调休？", [7]),
    ("单跳", "门禁卡丢了怎么办？", [8]),
    ("单跳", "会议室怎么预约？", [9]),
    ("单跳", "请病假要交证明吗？", [5]),
    ("单跳", "去年没休完的年假还能用吗？", [2]),
    ("单跳", "差旅住宿一晚限额多少？", [13]),
    # —— 多跳：答案要两条制度拼起来 ——
    ("多跳", "我入职四年，没休完的年假能留到什么时候？", [1, 2]),
    ("多跳", "请四天假要走什么流程？", [3, 4]),
    ("多跳", "病假和年假各有多少天？", [1, 5]),
    ("多跳", "请两天病假要交证明吗？流程怎么走？", [3, 5]),
    ("多跳", "调休过期作废，那年假没休完也会作废吗？", [2, 7]),
    # —— 否定：资料里没有答案 ——
    ("否定", "公司有班车吗？", []),
    ("否定", "有租房补贴吗？", []),
    ("否定", "年度体检怎么预约？", []),
    ("否定", "住房公积金按什么比例交？", []),
    ("否定", "产假有多少天？", []),
]

# ============ 对照组：三个切块配置，只动「块多大」这一个变量 ============
CONFIGS = [("切小", 45), ("切中", 90), ("切大", 180)]
K = 3  # top-k 全程钉死。连 k 一起动，就说不清是谁的功劳。
TIE = 0.10  # 粗筛线：Recall 差距在这以内算平手（自己定，写进结论）


def pad(s, width):
    """按显示宽度补空格（中日韩全角字符算 2 列）。"""
    w = sum(2 if ord(ch) > 0x2E80 else 1 for ch in s)
    return s + " " * max(0, width - w)


def chunk(text, size):
    """按字数切，不重叠。演示用；真实工具按 token，第 4 课给过基准。"""
    return [text[i:i + size] for i in range(0, len(text), size)]


def to_vec(text, vocab):
    pairs = [text[i:i + 2] for i in range(len(text) - 1)]
    return [pairs.count(p) for p in vocab]


def rank(query, chunks):
    vocab = sorted({p for t in chunks + [query]
                    for p in [t[i:i + 2] for i in range(len(t) - 1)]})
    qv = to_vec(query, vocab)
    scored = sorted(((sum(x * y for x, y in zip(to_vec(c, vocab), qv)), i)
                     for i, c in enumerate(chunks)), key=lambda t: (-t[0], t[1]))
    return [i for _, i in scored], dict((i, s) for s, i in scored)


def facts_in_chunk(chunk_text):
    """这一块里躺着哪几条制度（按内容编号，配置无关）。"""
    return {n for n, (_, marker) in enumerate(FACTS, 1) if marker in chunk_text}


# ============ 四个尺子（定义同第 9 课，只是「段」换成了「块」） ============
def got_in_top(ranked, chunk_facts, k):
    return set().union(*(chunk_facts[i] for i in ranked[:k])) if ranked[:k] else set()


def recall_at_k(ranked, needed, chunk_facts, k):
    return len(got_in_top(ranked, chunk_facts, k) & needed) / len(needed)


def hit_at_k(ranked, needed, chunk_facts, k):
    return 1.0 if got_in_top(ranked, chunk_facts, k) & needed else 0.0


def precision_at_k(ranked, needed, chunk_facts, k):
    return sum(1 for i in ranked[:k] if chunk_facts[i] & needed) / k


def rr(ranked, needed, chunk_facts):
    for pos, i in enumerate(ranked, 1):
        if chunk_facts[i] & needed:
            return 1.0 / pos
    return 0.0


answered = [q for q in QUESTIONS if q[2]]
negatives = [q for q in QUESTIONS if not q[2]]

print(f"[1] 标注集模板：{len(QUESTIONS)} 题"
      f"（单跳 {sum(1 for q in QUESTIONS if q[0] == '单跳')}"
      f" / 多跳 {sum(1 for q in QUESTIONS if q[0] == '多跳')}"
      f" / 否定 {len(negatives)}），文档 {len(DOCUMENT)} 字、{len(FACTS)} 条制度")
print("    标的是「答案需要哪几条制度」，不是「在第几块」——块号换配置就作废，内容不会。")
for kind in ("单跳", "多跳", "否定"):
    example = next(q for q in QUESTIONS if q[0] == kind)
    tag = " → 该命中制度 " + str(example[2]) if example[2] else " → 标空（专测拒答）"
    print(f"    {kind}：「{example[1]}」{tag}")
print(f"    （{len(FACTS)} 条制度没条条出题：标注集求代表性，不求穷尽）")

print(f"\n[2] 三个切块配置，其他一切不动（k = {K} 钉死，15 道有答案的题进平均分）")
print(f"    {pad('配置', 6)}{pad('块大小', 8)}{pad('块数', 6)}   Recall@{K}  Hit rate@{K}  Precision@{K}   MRR")
results = {}
for name, size in CONFIGS:
    chunks = chunk(DOCUMENT, size)
    chunk_facts = [facts_in_chunk(c) for c in chunks]
    rs, hs, ps = [], [], []
    for _, q, needed in answered:
        ranked, _ = rank(q, chunks)
        rs.append(recall_at_k(ranked, set(needed), chunk_facts, K))
        hs.append(hit_at_k(ranked, set(needed), chunk_facts, K))
        ps.append(precision_at_k(ranked, set(needed), chunk_facts, K))
    mrr = sum(rr(rank(q, chunks)[0], set(needed), chunk_facts)
              for _, q, needed in answered) / len(answered)
    results[name] = dict(size=size, n=len(chunks),
                         recall=sum(rs) / len(rs), hit=sum(hs) / len(hs),
                         precision=sum(ps) / len(ps), mrr=mrr)
    r = results[name]
    print(f"    {pad(name, 6)}{pad(f'{size} 字', 8)}{pad(str(r['n']), 6)}   "
          f"{r['recall']:>8.2f}  {r['hit']:>11.2f}  {r['precision']:>12.2f}  {r['mrr']:>5.2f}")

print("\n[3] 逐题对账：15 道有答案的题，每个配置各是全中还是漏")
print(f"    {pad('问题', 44)}{pad('切小', 8)}{pad('切中', 8)}{'切大'}")
flips = 0
for _, q, needed in answered:
    marks = []
    for _name, size in CONFIGS:
        chunks = chunk(DOCUMENT, size)
        chunk_facts = [facts_in_chunk(c) for c in chunks]
        ranked, _ = rank(q, chunks)
        got = got_in_top(ranked, chunk_facts, K)
        marks.append("全中" if got >= set(needed)
                     else "缺" + ",".join(str(n) for n in sorted(set(needed) - got)))
    if len(set(marks)) > 1:
        flips += 1
    flag = "  ◀ 三个配置不一致" if len(set(marks)) > 1 else ""
    print(f"    {pad(q, 44)}{pad(marks[0], 8)}{pad(marks[1], 8)}{marks[2]}{flag}")
print(f"    （{flips} 道题的结论随配置翻转——这些题就是实验在帮你抓的）")

print("\n[4] 丢分的账，分两种：切碎了（切块的锅）vs 块在但没进前 k（检索的锅）")
for name, size in CONFIGS:
    chunks = chunk(DOCUMENT, size)
    chunk_facts = [facts_in_chunk(c) for c in chunks]
    covered = set().union(*chunk_facts)
    split = [n for n in range(1, len(FACTS) + 1) if n not in covered]
    rank_miss = 0
    for _, q, needed in answered:
        ranked, _ = rank(q, chunks)
        if not got_in_top(ranked, chunk_facts, K) >= set(needed):
            if set(needed) <= covered:
                rank_miss += 1
    print(f"    {name}（{size} 字，{results[name]['n']} 块）：切碎 {len(split)} 条 {split if split else '无'}；"
          f"另有 {rank_miss} 道题块在但没挤进前 {K}")
print("    被切碎的制度，检索器再强也找不回来——先救边界（重叠 / 按句切），再看检索。")

print("\n[5] 否定题（5 道）不进平均分，单独看：拒答这关不随切块变")
for name, size in CONFIGS:
    chunks = chunk(DOCUMENT, size)
    neg_top, ans_top = [], []
    for _, q, _n in QUESTIONS:
        ranked, scores = rank(q, chunks)
        (neg_top if not _n else ans_top).append(scores[ranked[0]])
    sep = "两档之间有闸门的位置" if min(ans_top) > max(neg_top) else "两档有重叠：阈值定不住，这就是否定题抓出来的问题"
    print(f"    {name}：否定题 top-1 最高 {max(neg_top)}；有答案的题 top-1 最低 {min(ans_top)} → {sep}")

max_recall = max(r["recall"] for r in results.values())
candidates = [n for n, r in results.items() if max_recall - r["recall"] <= TIE]
print(f"\n[6] 结论模板（直接抄走：检索侧先筛，生成侧再比）")
print(f"    这批文档（{len(DOCUMENT)} 字、{len(FACTS)} 条制度）和这 {len(answered)} 道题下：")
for name, r in results.items():
    mark = "（候选）" if name in candidates else "（Recall 掉了，先淘汰）"
    print(f"    {name}（{r['size']} 字，{r['n']} 块）：Recall@{K} = {r['recall']:.2f}，"
          f"MRR = {r['mrr']:.2f}，Precision@{K} = {r['precision']:.2f} {mark}")
print(f"    粗筛线：Recall 差距 ≤ {TIE} 算平手（线自己定，写进结论）")
print(f"    → 检索侧候选：{'、'.join(candidates) if candidates else '无'}。")
print("    被淘汰的档先别扔：回 [4] 看它输在切碎还是没进前 k——切碎的挪边界或加重叠再跑，")
print("    那是另一轮实验（还是只动一个变量）。")
print("    → 最后一步：候选的几个档各生成一遍，拿判官比忠实度和相关性（见 [7]），再定档。")
print("    → 结论句：这批文档先按「" + ("、".join(candidates) if candidates else "?") + "」跑；每次改动后，同一套题重跑再比。")

print("\n[7] 忠实度判官的提示词模板（只有方法，本脚本不调任何模型）")
print("    ┌─ 判官提示词 ──────────────────────────────")
print("    │ 你是评审员。下面有【资料】和【回答】。")
print("    │ 只判一件事：回答里的每一句断言，能不能在资料里找到依据。")
print("    │ 逐句输出：支持 / 不支持；最后一行给比例 = 支持数 ÷ 总句数。")
print("    │ 资料里有、但回答没用的内容，不算错；回答里多出来的数字、日期、")
print("    │ 条款，资料里找不到就是「不支持」。不许补充常识。")
print("    │ 【资料】{{ 把检索到的几段原文贴进来 }}")
print("    │ 【回答】{{ 系统的回答贴进来 }}")
print("    └──────────────────────────────────────────")
print("    用法：判官批量初评，低分和边界题人看；换判官模型不换方法。")
