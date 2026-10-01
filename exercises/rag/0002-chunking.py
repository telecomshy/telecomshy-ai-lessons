"""RAG · 第 2 课进阶 · 配套脚本：切块切多大、重叠多少、按什么切。

对应进阶版 Q1。第 2 课只说「切太大 / 切得不是地方都有坑」，这里把【该切多大】量出来。

你会看到：
  1. 同一份文档，切 16 / 32 / 64 / 整篇，答案那句话分别长什么样
  2. overlap（重叠）到底在救什么
  3. 一条经验值，和一个反直觉的发现

⚠ 脚本按【字数】切；真的系统按 token 切，量级差不多。
  经验值 250–500 token，中文大致就是 250–500 字。

运行：  python exercises/rag/0002-chunking.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

DOC = (
    "第一章 年假。入职满一年者每年 5 天，满三年者 10 天，满五年者 15 天。"
    "请假三天以内（含三天），向直属主管口头报备即可。"
    "请假三天以上，需在系统里提交申请单，附上证明材料。"
    "第二章 报销。每月 25 日前提交发票，财务次月 15 日打款。"
    "加班满 4 小时可调休半天，调休需当月用完。"
)

# 这句是标准答案，看它在各种切法下「活没活得完整」
ANSWER = "请假三天以内（含三天），向直属主管口头报备即可。"


def chunk(text, size, overlap=0):
    """按固定长度切，相邻两段可以重复 overlap 个字。"""
    out = []
    i = 0
    while i < len(text):
        out.append(text[i:i + size])
        i += max(1, size - overlap)
    return out


def report(label, chunks):
    print(f"\n  {label}  →  {len(chunks)} 段")
    intact = broken = buried = 0
    for i, c in enumerate(chunks, 1):
        has = ANSWER in c
        if has:
            intact += 1
            tag = " ◀ 答案完整在这段里"
        elif any(ANSWER[j:j + 6] in c for j in range(0, len(ANSWER) - 6, 6)):
            broken += 1
            tag = " ◀ 答案被切成半句"
        else:
            tag = ""
        if len(c) > 40 and has:
            buried += 1
            tag += "（但这段很长，答案会被稀释）"
        print(f"    段 {i}（{len(c):3d} 字）：{c}{tag}")
    return intact, broken, buried


print("[0] 原文档，全文", len(DOC), "字")
print(f"    标准答案就这一句（{len(ANSWER)} 字）：{ANSWER}")

print("\n" + "=" * 72)
print("[1] 同一份文档，四种切法")
print("=" * 72)
for size in [16, 32, 64, len(DOC)]:
    tag = "整篇，等于没切" if size == len(DOC) else f"每 {size} 字切一段"
    report(f"切法：{tag}", chunk(DOC, size))

print("\n" + "=" * 72)
print("[2] overlap（重叠）在救什么 —— 以及它救不了什么")
print("=" * 72)
print("  ① 先看【救不了】的：切 16 字、重叠 8 字")
report("    切 16 字 + 重叠 8 字", chunk(DOC, 16, overlap=8))
print("      → 答案仍然被切成三段。【因为块本身（16 字）比答案（24 字）还短】，")
print("        再多重叠也塞不下一整句。所以：【第一步是块要够长，第二步才是重叠】。")

print("\n  ② 块够长之后，重叠才开始起作用：切 30 字")
a0, _, _ = report("    切 30 字、不重叠", chunk(DOC, 30))
a1, _, _ = report("    切 30 字、重叠 20 字", chunk(DOC, 30, overlap=20))
print(f"\n      不重叠：答案完整的段数 = {a0} 段")
print(f"      重叠 20 字：答案完整的段数 = {a1} 段")
print("      重叠干的事：【把上一段的尾巴复制到下一段开头】，")
print("      于是横跨切口的那句话，至少在某一段里是完整的。")

print("\n" + "=" * 72)
print("[3] 一条经验值，和一个反直觉的发现")
print("=" * 72)
print("  经验值（多家基准一致）：")
print("    · 块大小 250～500 token（中文大致就是 250～500 字）")
print("    · 重叠 10%～20%")
print("    · 按「段落 → 换行 → 句号」逐级退让着切，别按死字数")
print()
print("  实测支撑：")
print("    · 九种切块配置跑同一批语料与查询，【最好与最差相差 8 个召回点】")
print("    · 但朴素的递归切块（400 token）已经拿到 89.5%，")
print("      最好的语义切块只比它【多不到 2 个点】；最差的语义切块反而更低")
print("    · NVIDIA 五个数据集基准：512～1024 token 最好，【128 token 最差】")
print()
print("  反直觉（2026 年一项系统分析）：")
print("    · 用 SPLADE + Mistral-8B 在 Natural Questions 上测，")
print("      【重叠没有可测的收益，只是增加了索引成本】")
print("    · 所以重叠要【拿自己的查询去量】，别当默认真理")
print()
print("  带走：")
print("    ① 从 400 token、15% 重叠起步——这个起点已经离最好不到 2 个点。")
print("    ② 切块是整条链里【最便宜的调优点】：改一次设置只花一次重建索引。")
print("    ③ 别一上来就上语义切块——先确认朴素方法真的不够，再上复杂的。")
