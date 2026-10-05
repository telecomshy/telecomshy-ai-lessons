"""交付核验：链接可解析 / 锚点能落地 / 旧措辞零残留。

用法：python tools/check-links.py <file.html> [more.html ...]
"""
import re
import sys
from pathlib import Path

LINK = re.compile(r'(?:href|src)="([^"]+)"')


def main() -> None:
    bad = 0
    for arg in sys.argv[1:]:
        f = Path(arg)
        text = f.read_text(encoding="utf-8")
        for m in LINK.finditer(text):
            u = m.group(1)
            if u.startswith(("http", "mailto:")):
                continue
            parts = u.split("#")
            # 同页锚点（u 以 # 开头）：目标就是本文件本身。
            # 早先写成 (f.parent / parts[0] or f) 会拼成 reference/reference/*.html，
            # 报出一堆假 FAIL —— 报错先确认是文件错了还是脚本错了。
            full = f.resolve() if not parts[0] else (f.parent / parts[0]).resolve()
            if not full.exists():
                print(f"  FAIL file   {u}   (in {f})")
                bad += 1
                continue
            if len(parts) > 1 and parts[1]:
                target = full.read_text(encoding="utf-8", errors="ignore")
                if f'id="{parts[1]}"' not in target:
                    print(f"  FAIL anchor {u}   (in {f})")
                    bad += 1
        print(f"  checked {f}")
    print("OK" if bad == 0 else f"{bad} failures")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
