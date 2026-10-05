"""审计：LLM 轨道里"讲的是 LLM 机制"还是"讲的是 agent 该怎么写"。

机械口径：扫 lessons/llm/*.html 的正文块，命中 agent 侧关键词的列出行号与原文片段。
排除体例样板（页脚 / 互链 / 资料出处 / ask-teacher），因为那里的 agent 字样只是互链。

用法：python tools/agent-content-scan.py [最小片段长度=12]
"""
import html
import re
import sys
from pathlib import Path

BOILERPLATE = re.compile(
    r'class="(footer|source|ask-teacher|next|subtitle|badge)"|<footer|<h1>'
)
KEYWORDS = (
    "agent", "harness", "工具定义", "工具调用", "工具结果", "系统提示",
    "你的代码", "你的程序", "框架", "开发者", "你自己的", "并行", "并发",
    "监控", "上线", "生产", "实战",
)


def blocks(path: Path) -> list[tuple[int, str]]:
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if BOILERPLATE.search(line):
            continue
        t = re.sub(r"(?s)<pre.*?</pre>", " 代码块 ", line)
        t = re.sub(r"<[^>]+>", " ", t)
        t = html.unescape(t)
        t = re.sub(r"\s+", " ", t).strip()
        if len(t) >= 8:
            out.append((i, t))
    return out


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    files = sorted(Path("lessons/llm").glob("*.html"))
    total = 0
    for f in files:
        hits = []
        for i, text in blocks(f):
            low = text.lower()
            if any(k.lower() in low for k in KEYWORDS):
                # 只打印命中关键词附近的一小段
                for k in KEYWORDS:
                    idx = low.find(k.lower())
                    if idx >= 0:
                        s = max(0, idx - n)
                        hits.append((i, k, text[s : idx + 3 * n]))
                        break
        if not hits:
            continue
        print(f"\n=== {f.name}（{len(hits)} 处）")
        for i, k, piece in hits:
            print(f"  {i:>4} [{k}] {piece}")
        total += len(hits)
    print(f"\n合计 {total} 处")


if __name__ == "__main__":
    main()
