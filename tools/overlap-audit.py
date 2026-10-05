"""审计：两课正文之间"讲的是同一件事"的重复，带行号、排除页眉页脚样板。

机械口径：逐行抽可见文字 -> 去掉样板行（footer/next/source/ask-teacher/标题）
-> 用 difflib 取每对行之间的**最长公共子串** -> 按长度降序输出。
片段自带所在行号，便于逐条核。

用法：python tools/overlap-audit.py <a.html> <b.html> [最小长度=10]
"""
import difflib
import html
import re
import sys
from pathlib import Path

# 这些块里的重复是体例要求（页脚、互链、资料出处），不算内容重复
BOILERPLATE = re.compile(
    r"class=\"(lesson-meta|footer|source|ask-teacher|next|subtitle|badge|quiz)\""
    r"|<h1>|<footer|<h2 id=|更多更难的|检查一下你懂了没|想深挖",
)


def blocks(path: str) -> list[tuple[int, str]]:
    out = []
    for i, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if BOILERPLATE.search(line):
            continue
        text = re.sub(r"(?s)<pre.*?</pre>", " 代码块 ", line)
        text = re.sub(r"<[^>]+>", " ", text)
        text = html.unescape(text)
        text = re.sub(r"[^一-鿿A-Za-z0-9]+", "", text)
        if len(text) >= 6:
            out.append((i, text))
    return out


def main() -> None:
    a_path, b_path = sys.argv[1], sys.argv[2]
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    A, B = blocks(a_path), blocks(b_path)
    print(f"A = {a_path}（{len(A)} 个正文块）")
    print(f"B = {b_path}（{len(B)} 个正文块）\n")

    hits: list[tuple[int, int, int, str]] = []
    for ai, atext in A:
        for bi, btext in B:
            m = difflib.SequenceMatcher(None, atext, btext, autojunk=False)
            block = m.find_longest_match(0, len(atext), 0, len(btext))
            if block.size >= n:
                hits.append((block.size, ai, bi, atext[block.a : block.a + block.size]))
    hits.sort(key=lambda h: (-h[0], h[1]))

    # 片段被更长片段完全覆盖时丢弃（同一处重复只报一次）
    kept: list[tuple[int, int, int, str]] = []
    for h in hits:
        if not any(h[3] in k[3] and k[1] == h[1] and k[2] == h[2] and k[0] > h[0] for k in kept):
            kept.append(h)

    print(f"{'长度':>4}  {'A 行':>5} {'B 行':>5}  片段")
    for size, ai, bi, piece in kept:
        print(f"{size:>4}  {ai:>5} {bi:>5}  {piece}")
    print(f"\n共 {len(kept)} 处")


if __name__ == "__main__":
    main()
