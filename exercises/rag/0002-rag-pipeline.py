"""RAG · 第 2 课 配套脚本：一条 RAG 链，六步各在干什么、出问题会怎样。

把一份原始文档一路走到「模型吐出答案」，每一步打印【手上的数据长什么样】。
最后一段是关键：六步里只有最后一步是模型，前五步全是普通程序。

你会看到：
  1. 切块（chunking）—— 一份文档切成小段；切在哪、切多大都有坑
  2. 变向量（embedding）—— 每段压成一根向量；用的是另一个模型
  3. 存起来（向量库）
  4. 查（retrieval）—— 问题也变向量，比相似度，排序，取 top-k
  5. 塞进提示词
  6. 生成 —— 唯一用到模型的一步

⚠ 「变向量」仍是玩具：按【二字组合】出现几次算。真的用专门的文本嵌入模型。

运行：  python exercises/rag/0002-rag-pipeline.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

DOC = (
    "第一章 年假。入职满一年者每年 5 天，满三年者 10 天，满五年者 15 天。"
    "请假三天以内（含三天），向直属主管口头报备即可。"
    "请假三天以上，需在系统里提交申请单，附上证明材料。"
    "第二章 报销。每月 25 日前提交发票，财务次月 15 日打款。"
    "加班满 4 小时可调休半天，调休需当月用完。"
)

QUESTION = "请三天假要走什么流程？"
TOP_K = 2


# ============ 小工具 ============
def chunk(text, size):
    """按固定字数切成小段（真实系统会按句子/段落切，道理一样）。"""
    return [text[i:i + size] for i in range(0, len(text), size)]


def to_vector_on(text, vocab):
    pairs = [text[i:i + 2] for i in range(len(text) - 1)]
    return [pairs.count(p) for p in vocab]


def dot(a, b):
    """逐位相乘再加起来 —— 就是 LLM 底层第 1 课那个「点积」。"""
    return sum(x * y for x, y in zip(a, b))


def show_prompt(chunks, q):
    print("      ┌──────────────────────────────────────")
    for i, c in enumerate(chunks, 1):
        print(f"      │【资料 {i}】{c}")
    print(f"      │【问题】{q}")
    print("      └──────────────────────────────────────")


# ============ [0] 起点 ============
print("[0] 起点：一份原始文档（手编的《员工手册》）")
print(f"      全文 {len(DOC)} 字：{DOC[:26]}…")

# ============ [1] 切块 ============
SIZE = 32
chunks = chunk(DOC, SIZE)
print(f"\n[1] 第 1 步 · 切块 chunking：按每 {SIZE} 字切成 {len(chunks)} 段")
for i, c in enumerate(chunks, 1):
    print(f"      段 {i}（{len(c):2d} 字）：{c}")
print("      ⚠ 看段 2 开头的「年者 15 天。」——半个词被切在了上一段。")
print("      ⚠ 看段 3 结尾的「第二章 报销。」——两件不相干的事被切进了同一段。")
print("        切块有两个坑：")
print("        切太大 → 相关的一句被一堆无关内容埋住，相似度被稀释")
print("        切得不是地方 → 上下文被切碎，剩下的半句谁也看不懂")

# ============ [2] 变向量 ============
vocab = sorted({p for t in chunks + [QUESTION] for p in [t[i:i + 2] for i in range(len(t) - 1)]})
vectors = [to_vector_on(c, vocab) for c in chunks]
print(f"\n[2] 第 2 步 · 变向量 embedding：每段压成一根 {len(vocab)} 维的向量")
print("      这根向量是【每个「二字组合」出现几次】的一串数，例如：")
for i, c in [(2, chunks[1]), (3, chunks[2])]:
    pairs = [c[j:j + 2] for j in range(len(c) - 1)]
    top = sorted({p: pairs.count(p) for p in set(pairs)}.items(), key=lambda kv: -kv[1])[:3]
    print(f"        段 {i} → " + "、".join(f"「{p}」×{n}" for p, n in top) + " …")
print("      ⚠ 用的是【另一个模型】（文本嵌入模型），不是 LLM 底层第 1 课那个词嵌入。")
print("        词嵌入：一个 token 一根，喂给模型当输入。")
print("        文本嵌入：整段一根，只用来排序，不喂给模型。")

# ============ [3] 存起来 ============
print(f"\n[3] 第 3 步 · 存起来：向量库里现在有 {len(vectors)} 条，等着被查")
print("      （这个「库」就是一堆向量 + 一个能快速比相似度的索引，没有魔法。）")

# ============ [4] 查 ============
qv = to_vector_on(QUESTION, vocab)
scored = sorted(
    ((dot(v, qv), i, c) for i, (v, c) in enumerate(zip(vectors, chunks), 1)),
    key=lambda t: (-t[0], t[1]),
)
print("\n[4] 第 4 步 · 查 retrieval：问题也变向量，逐条比相似度")
for score, i, c in scored:
    print(f"      相似度 = {score}   段 {i}：{c}")
chosen = scored[:TOP_K]
print(f"      按分排序，取前 {TOP_K} 段（top-k，k = {TOP_K}）")
print("      ⚠ 取太少会漏；取太多会把重点淹掉。k 是 RAG 里第一个要调的数。")

# ============ [5] 塞进提示词 ============
print(f"\n[5] 第 5 步 · 塞进提示词：把挑出来的 {len(chosen)} 段排在问题前面")
show_prompt([c for _, _, c in chosen], QUESTION)
print("      ⚠ 这一步也有坑：【检索到 ≠ 用上】。")
print("        塞进去不等于模型会用——排在中间的内容最不容易被用上。")

# ============ [6] 生成 ============
print("\n[6] 第 6 步 · 生成：模型读完提示词，吐出答案")
print("      答：三天含在「三天以内」里，向直属主管口头报备即可，事后补一条消息。")

# ============ [7] 收尾 ============
print("\n[7] 记住一件事")
print("      六步里，只有第 6 步是模型。前五步全是普通程序。")
print("      RAG 的「技术性」全在前五步——切块、变向量、存、查、拼提示词。")
print("      所以 RAG 出问题时，先别怪模型：多半是前五步里哪一步没做好。")
