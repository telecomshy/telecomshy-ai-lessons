"""RAG · 第 1 课 配套脚本：不检索 vs 检索之后，模型手上有什么。

这一课只讲一件事：为什么需要「先查资料再回答」。
脚本不调任何模型，只演一件事——【检索这一步到底在干什么】：
把你资料里相关的那几段挑出来，递到模型手上。仅此而已。

你会看到：
  1. 不检索时，模型手上只有那一句问题 → 它只能「接得像」（见 LLM 底层第 0 课）
  2. 检索这一步：把每段压成一根向量，跟问题比相似度（就是点积）
  3. 检索之后，模型手上多了几段资料 → 它这才有可能答对

⚠ 这里的「变向量」是玩具：按【二字组合】出现几次来算（很像关键词匹配）。
  真的 RAG 用一个专门的模型（文本嵌入模型）算语义相似度。
  但【排序、取最像的几段】这一步一模一样。

运行：  python exercises/rag/0001-why-retrieval.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

# ============ 你的资料库（手编的 5 段公司制度） ============
DOCS = [
    "年假天数：入职满一年者每年 5 天，满三年者 10 天，满五年者 15 天。",
    "请假三天以内（含三天），向直属主管口头报备即可，事后补一条消息。",
    "请假三天以上，需在系统里提交申请单，附上证明材料，主管审批后生效。",
    "报销流程：每月 25 日前提交发票，财务在次月 15 日统一打款。",
    "加班调休：加班满 4 小时可调休半天，调休需当月用完，过期作废。",
]

QUESTION = "请三天假要走什么流程？"


# ============ 小工具 ============
def to_vector(text):
    """把一段文字压成一根向量：每个数 = 某个「二字组合」出现几次。"""
    pairs = [text[i:i + 2] for i in range(len(text) - 1)]
    vocab = sorted(set(pairs))
    return vocab, [pairs.count(p) for p in vocab]


def to_vector_on(text, vocab):
    pairs = [text[i:i + 2] for i in range(len(text) - 1)]
    return [pairs.count(p) for p in vocab]


def dot(a, b):
    """逐位相乘再加起来 —— 就是 LLM 底层第 1 课那个「点积」。"""
    return sum(x * y for x, y in zip(a, b))


# ============ [1] 资料库 ============
print("[1] 你的资料库：5 段公司制度（模型完全没见过）")
for i, d in enumerate(DOCS, 1):
    print(f"      段 {i}．{d}")

# ============ [2] 提问 ============
print(f"\n[2] 提问：{QUESTION}")

# ============ [3] 不检索 ============
print("\n[3] 不检索时，模型手上有什么")
print("      ——只有那一句问题。资料一个字都没有。")
print("      ——它学的是「接得像」（见 LLM 底层第 0 课），于是会编一套听起来合理的流程。")
print("      ——注意：它不会说「我不知道」。它不知道自己不知道。")

# ============ [4] 检索 ============
all_vocab = sorted({p for t in DOCS + [QUESTION] for p in [t[i:i + 2] for i in range(len(t) - 1)]})
qv = to_vector_on(QUESTION, all_vocab)
scored = sorted(
    ((dot(to_vector_on(d, all_vocab), qv), i, d) for i, d in enumerate(DOCS, 1)),
    key=lambda t: (-t[0], t[1]),
)
print("\n[4] 检索：把每段压成一根向量，跟问题比相似度（点积）")
for score, i, d in scored:
    print(f"      相似度 = {score}   段 {i}．{d}")
print("      （分数打平时按原顺序排——玩具的补丁。真的检索器另有办法，见进阶版。）")
top2 = scored[:2]
print(f"      按分排序，取最像的 {len(top2)} 段（这叫 top-k，k = 2）")

# ============ [5] 检索之后 ============
print("\n[5] 检索之后，模型手上有什么")
for rank, (score, i, d) in enumerate(top2, 1):
    print(f"      【资料 {rank}】（原第 {i} 段）{d}")
print(f"      【问题】{QUESTION}")

# ============ [6] 一句话 ============
print("\n[6] 一句话")
print("      RAG ＝ 先替它翻书，再让它回答。模型一个字都没变，变的只是你发过去的那段话。")
print("      ——注意「三天以内」和「三天以上」两段都拿到了：问题正好卡在分界线上。")
print("        只取 1 段，模型看到的就只有半套规则——【k 取多少，是 RAG 里第一个要调的数】。")
print("      ——顺带：这里比相似度用的就是 LLM 底层第 1 课那个【点积】。")
print("        同一个动作，用在两处：注意力里比「像不像」，这里比「相不相关」。")
