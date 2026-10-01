"""RAG · 第 1 课进阶 · 配套脚本：稀疏和稠密各自在哪翻车，混合怎么合。

对应进阶版 Q1。初学版只点了一句「稀疏看字面撞没撞、稠密看意思近不近」，
这里用两道题，让两种方法【各翻一次车】，再用 RRF 把它们合起来。

你会看到：
  1. 查编号（E-2107）：稀疏赢，稠密会把 2108 也排上来
  2. 查症状（发烧）：稠密赢，稀疏根本找不到（文档写的是「发热」）
  3. RRF（倒数排名融合）怎么把两个榜合成一个
  4. k=60 在做什么，以及混合检索的代价

⚠ 「稠密」这里是玩具：先按【同义词表】归一再比字。
  真的用文本嵌入模型——但【两榜各会翻车】这件事一模一样。

运行：  python exercises/rag/0001-sparse-vs-dense.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

# ============ 资料库 ============
DOCS = {
    1: "错误码 E-2107：温度传感器无响应，检查接线后重启。",
    2: "错误码 E-2108：温度传感器读数异常，校准后重试。",
    3: "患者发热时可采用物理降温，温水擦拭额头与腋下。",
    4: "退换货须知：签收后 7 天内可退，商品需保持原包装。",
    5: "发票抬头变更：在「我的-发票」中提交工单，3 个工作日生效。",
}

# 同义词表 ＝ 玩具版「语义理解」。真的模型不用这张表，靠向量。
SYN = {
    "发烧": "发热", "发热": "发热", "退烧": "发热", "降温": "发热",
    "怎么办": "处理", "怎么处理": "处理", "咋办": "处理", "处理": "处理",
    "啥意思": "含义", "是什么意思": "含义", "含义": "含义",
}


def norm(text):
    """玩具版「语义理解」：同义词归一 + 把数字看成一回事。
    真的模型不用这张表，靠向量——但它对【精确字面迟钝】这件事一模一样。"""
    for k in sorted(SYN, key=len, reverse=True):
        text = text.replace(k, SYN[k])
    import re as _re
    return _re.sub(r"\d+", "N", text)


def to_vec(text, vocab):
    pairs = [text[i:i + 2] for i in range(len(text) - 1)]
    return [pairs.count(p) for p in vocab]


def score(query, doc, use_syn):
    q = norm(query) if use_syn else query
    d = norm(doc) if use_syn else doc
    vocab = sorted({p for t in [q, d] for p in [t[i:i + 2] for i in range(len(t) - 1)]})
    return sum(x * y for x, y in zip(to_vec(q, vocab), to_vec(d, vocab)))


def rank(query, use_syn):
    scored = [(score(query, d, use_syn), i) for i, d in DOCS.items()]
    return sorted(scored, key=lambda t: (-t[0], t[1]))


def order_of(ranked, drop_zero=False):
    """drop_zero=True 时只留【真有分】的段 —— 全是 0 分的榜，名次本身就是噪音。"""
    if drop_zero:
        ranked = [t for t in ranked if t[0] > 0]
    return [i for _, i in ranked]


def show(label, ranked):
    cells = "   ".join(f"段{i}＝{s}" for s, i in ranked[:3])
    print(f"      {label}：{cells}   …（全榜：{' > '.join('段'+str(i) for _, i in ranked)}）")


def rrf(rankings, k=60):
    """倒数排名融合：每个榜给每个段 1/(k + 名次)，加起来再排序。"""
    total = {}
    for order in rankings:
        for pos, i in enumerate(order, 1):
            total[i] = total.get(i, 0.0) + 1.0 / (k + pos)
    return [i for i, _ in sorted(total.items(), key=lambda t: (-t[1], t[0]))]


# ============ 问题 A：查编号 ============
QA = "E-2107 是什么意思？"
print("[1] 问题 A：「" + QA + "」  该命中：段 1")
show("稀疏（按字面）", rank(QA, use_syn=False))
show("稠密（按语义）", rank(QA, use_syn=True))
print("      → 稀疏直接撞上「E-2107」，段 1 明显领先（5 段共有的字组合）。")
print("      → 稠密把 2107 / 2108 当成一回事（数字归一），【两段打成同一分】——")
print("        正确那段排第一只是碰巧，它其实【分不出 2107 和 2108】。")
print("        这就是「稠密对精确字面迟钝」的字面意思。")

# ============ 问题 B：查症状 ============
QB = "发烧了要怎么处理？"
print("\n[2] 问题 B：「" + QB + "」  该命中：段 3")
show("稀疏（按字面）", rank(QB, use_syn=False))
show("稠密（按语义）", rank(QB, use_syn=True))
print("      → 文档写的是「发热」和「降温」，问题问的是「发烧」——【字面没撞上】，")
print("        稀疏给段 3 的分是 0，等于漏了。")
print("      → 稠密靠同义词归一找到了它。这就是「换个说法也能找到」的意思。")

# ============ RRF ============
print("\n[3] 合起来：RRF（倒数排名融合）")
print("      两个榜的分数量纲完全不同（字面匹配分 vs 语义相似度），没法直接相加。")
print("      RRF 只看【名次】：每个榜给每段 1/(k + 名次)，加起来再排。")
print()
for name, q in [("问题 A", QA), ("问题 B", QB)]:
    sp = rank(q, use_syn=False)
    de = rank(q, use_syn=True)
    print(f"      {name}")
    print("        稀疏榜　　：" + " > ".join(f"段{i}" for i in order_of(sp)))
    print("        稠密榜　　：" + " > ".join(f"段{i}" for i in order_of(de)))
    print("        RRF 融合　：" + " > ".join(f"段{i}" for i in rrf([order_of(sp), order_of(de)])))

print("\n      ⚠ 看问题 B 的融合结果：【段 1 冒到了第一】，可它跟问题毫无关系。")
print("        因为稀疏榜给所有段都是 0 分——【一个全是并列的榜，名次本身就是噪音】，")
print("        而 RRF 会把每个名次都当真。")
print()
print("      这是 RRF 的真实前提：【它假设每个榜的名次都有意义】。")
print("      解法：分数为 0 的段不进榜（设个阈值），只让「真有分」的段参与融合。")
print()
print("      过滤之后再融：")
for name, q in [("问题 A", QA), ("问题 B", QB)]:
    sp = rank(q, use_syn=False)
    de = rank(q, use_syn=True)
    fused = rrf([order_of(sp, drop_zero=True), order_of(de, drop_zero=True)])
    print(f"        {name}：" + " > ".join(f"段{i}" for i in fused))

# ============ k = 60 ============
print("\n[4] k = 60 在做什么")
for pos in [1, 2, 3, 10]:
    print(f"      第 {pos:>2} 名得 1/(60+{pos}) = {1.0/(60+pos):.5f}")
print(f"      第 1 名只比第 2 名多 {(1/61-1/62)/(1/61)*100:.1f}%；")
print(f"      第 10 名仍有第 1 名的 {(1/70)/(1/61)*100:.0f}% 的权重。")
print("      → 名次被【压得很平】。所以 RRF 奖励的是「两个榜都说它好」，不是「单榜冠军」。")

# ============ 代价 ============
print("\n[5] 混合检索的代价（别当免费午餐）")
print("      · 索引翻倍：一份 BM25 / 倒排，一份向量。存两份、建两份。")
print("      · 融合还要调：两个方法的相对权重怎么给。")
print("      · 所以先量再上：单用一种已经够好的话，就别付这个成本。")

# ============ 带走 ============
print("\n[6] 带走四条")
print("      ① 稀疏看「字面撞没撞」，稠密看「意思近不近」。")
print("         编号 / 型号 / 专有名词 → 稀疏赢；换个说法 → 稠密赢。")
print("      ② 两个都会翻车，翻的还不是同一处 —— 这正是要合的理由。")
print("      ③ RRF 只看名次不看分，所以不用归一化两个量纲 —— 简单、稳、可解释。")
print("      ④ 但 RRF 假设【每个榜的名次都有意义】。")
print("         一个榜全是并列（分都为 0）时，它的名次是噪音，会把融合带偏。")
print("         上线前给「没命中」设个阈值，别让它参与排名。")
