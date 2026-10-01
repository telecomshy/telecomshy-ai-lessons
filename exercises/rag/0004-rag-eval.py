"""RAG · 第 4 课进阶 · 配套脚本：RAG 到底怎么评。

对应进阶版 Q1。第 4 课教了「两类翻车」，这里给【能分开量它们】的尺子。

你会看到：
  1. 一份最小标注集长什么样（不用几百条，50～100 条就够起步）
  2. 检索侧四个数：Recall@k / Hit rate@k / Precision@k / MRR
  3. 【为什么必须分开评】——同一个系统，检索分高、忠实度可以很低
  4. 起步做法：把线上答错的问题，变成回归测试

⚠ 检索器仍是玩具（二字组合 + 点积）。评的是【尺子】，不是检索器。

运行：  python exercises/rag/0004-rag-eval.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

# ============ 资料库（同前几课） ============
DOCS = {
    1: "年假天数：入职满一年者每年 5 天，满三年者 10 天，满五年者 15 天。",
    2: "请假三天以内（含三天），向直属主管口头报备即可，事后补一条消息。",
    3: "请假三天以上，需在系统里提交申请单，附上证明材料，主管审批后生效。",
    4: "报销流程：每月 25 日前提交发票，财务在次月 15 日统一打款。",
    5: "加班调休：加班满 4 小时可调休半天，调休需当月用完，过期作废。",
}

# ============ 最小标注集：问题 → 「该命中哪几段」 ============
# 这就是全部的准备工作。真人标，50～100 条就够起步。
LABELS = [
    ("入职四年，年假有几天？", {1}),
    ("满三年能休多少天年假？", {1}),
    ("请两天假要走什么流程？", {2}),
    ("请三天假要走什么流程？", {2, 3}),
    ("请假都要走什么流程？", {2, 3}),
    ("请五天假要走什么流程？", {3}),
    ("请长假要交什么材料？", {3}),
    ("发票什么时候交？", {4}),
    ("加班半天能不能调休？", {5}),
    ("调休过期了怎么办？", {5}),
]


# ============ 玩具检索器（同第 1 课） ============
def to_vec(text, vocab):
    pairs = [text[i:i + 2] for i in range(len(text) - 1)]
    return [pairs.count(p) for p in vocab]


def rank(query):
    vocab = sorted({p for t in list(DOCS.values()) + [query]
                    for p in [t[i:i + 2] for i in range(len(t) - 1)]})
    qv = to_vec(query, vocab)
    scored = [(sum(x * y for x, y in zip(to_vec(d, vocab), qv)), i) for i, d in DOCS.items()]
    return [i for _, i in sorted(scored, key=lambda t: (-t[0], t[1]))]


# ============ 四个尺子 ============
def recall_at_k(ranked, rel, k):
    """该命中的段里，被我拿到的比例。问的是【漏没漏】。"""
    return len(set(ranked[:k]) & rel) / len(rel)


def hit_at_k(ranked, rel, k):
    """top-k 里至少有一段正确 —— 0 或 1。问的是【这一次成没成】。"""
    return 1.0 if set(ranked[:k]) & rel else 0.0


def precision_at_k(ranked, rel, k):
    """拿到的 k 段里，有用的比例。问的是【噪音多不多】。"""
    return len(set(ranked[:k]) & rel) / k


def rr(ranked, rel):
    """第一段正确出现在第几位的倒数。问的是【正确的排得靠不靠前】。"""
    for pos, i in enumerate(ranked, 1):
        if i in rel:
            return 1.0 / pos
    return 0.0


print("[1] 最小标注集：8 个问题（真实项目建议 50～100 个）")
for q, rel in LABELS:
    print(f"    「{q}」→ 该命中段 {sorted(rel)}")

print("\n[2] 跑一遍检索，看四个数（k 越大越容易蒙对）")
print(f"    {'k':>3}  {'Recall@k':>9}  {'Hit rate@k':>11}  {'Precision@k':>12}")
for k in [1, 2, 3, 5]:
    rs = [recall_at_k(rank(q), rel, k) for q, rel in LABELS]
    hs = [hit_at_k(rank(q), rel, k) for q, rel in LABELS]
    ps = [precision_at_k(rank(q), rel, k) for q, rel in LABELS]
    print(f"    {k:>3}  {sum(rs)/len(rs):>8.2f}   {sum(hs)/len(hs):>10.2f}   {sum(ps)/len(ps):>11.2f}")
mrr = sum(rr(rank(q), rel) for q, rel in LABELS) / len(LABELS)
print(f"\n    MRR = {mrr:.2f}   （1.0 = 每次正确那段都排第一）")

print("\n[3] 三个数各在回答什么问题，别混")
print("    Recall@k      ：该拿的都拿到了吗？   ← 漏没漏（缺了就答不出）")
print("    Hit rate@k    ：这一次成没成？       ← 最粗的及格线")
print("    Precision@k   ：拿到的里面噪音多吗？ ← 会不会把答案淹了")
print("    MRR           ：正确的排得靠前吗？   ← 排序好不好")
print()
print("    典型失衡：")
print("      k 调到 5 → Recall 和 Hit rate 都好看，Precision 掉下来")
print("                 （多塞了 3 段没用的，正好制造「来了但没用上」）")
print("      k 只给 1 → Precision 最高，但漏掉第二条规则")
print()
print("    所以【不能只看一个数】。这就是为什么建议同时报 Recall@k + MRR。")

print("\n[4] 最要紧的一条：分开评，别只看最终答案")
print("    RAG 只有两段：检索 → 生成。评也必须分开。")
print()
print("    检索侧（本脚本在算的）：Recall@k / MRR / Precision@k")
print("      ——需要「问题 → 该命中哪几段」的标注")
print()
print("    生成侧：Faithfulness（忠实度）")
print("      ——答案里每一句，能不能在检索到的资料里找到依据")
print("      ——生产目标 90% 以上；低于 70% 不能上线")
print()
print("    为什么要分开：")
print("      检索分高 + 忠实度低 = 【来了但没用上】→ 修提示词 / 顺序")
print("      检索分低 + 忠实度高 = 【该来的没来】→ 修切块 / 变向量 / k")
print("    这正好是第 4 课那两类翻车。【尺子和病灶是一一对应的】。")

print("\n[5] 起步做法（照抄）")
print("    ① 收集 50～100 个真实问题（别自己编，用用户真问的）")
print("    ② 每个问题手标「该命中哪几段」——二元判断就够，不用打分")
print("    ③ 每次改动后重跑一遍，看四个数怎么变")
print("    ④ 【线上答错的问题，加进标注集当回归测试】——这才是标注集的正确长大方式")
print()
print("    为什么 50～100 条：这个量已经能测出「一个点」的差别；")
print("    超过 200 条，标注成本线性涨，统计功效却已经饱和。")
