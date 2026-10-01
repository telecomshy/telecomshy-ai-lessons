"""Agent 原理篇 · 第 5 课 配套脚本：给自己写一个 skill。

这一课不调 API，纯离线。它生成一个 skill 的骨架，然后告诉你每一部分是干嘛的。

skill 是什么？——把「做某类事的做法」打包成一个目录：
    SKILL.md          正文：什么时候用我、怎么做
    （可选）别的文件    脚本、模板、参考资料

关键设计叫**渐进式加载**：平时只把 SKILL.md 里那一句「description」给模型看；
模型觉得用得上，才打开正文；正文里提到的脚本/资料，再按需打开。
这么做是因为**上下文是稀缺资源**（见 LLM 底层第 2 课）。

运行：  python exercises/agent/0005-make-a-skill.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

import os
import re
import sys

SKILL_NAME = "weather-dress"
DESCRIPTION = "查天气并给出穿衣建议。当用户问「今天穿什么」「要不要带伞」这类跟天气有关的出门问题时使用。"

SKILL_MD = """---
name: {name}
description: {description}
---

# 查天气 + 穿衣建议

## 什么时候用我
用户问的是「出门该怎么穿」「要不要带伞」「冷不冷」这类问题。
注意：只在**跟天气有关**时用；单纯问温度数字不用我，直接查就行。

## 怎么做
1. 先调 `get_weather` 拿到城市和气温。
2. 按下面的对照表给建议：
   - 30 度以上：短袖，注意防晒
   - 20~30 度：长袖单衣
   - 10~20 度：外套
   - 10 度以下：厚外套 / 羽绒服
3. 如果天气状况是「雨 / 雷阵雨」，追加一句「记得带伞」。

## 输出格式
先给结论（穿什么），再给一句理由（几度 + 什么天）。
不要复述原始数据。

## 常见翻车怎么救
- 查不到这个城市 → 直接说查不到，别猜。
- 用户没说城市 → 反问，别自己挑一个。

## 还需要更多细节？
看同目录的 `reference.md`。
"""

REFERENCE_MD = """# 补充资料

## 为什么按 10 度一档
粗糙但够用。真要做细，可以加湿度、风力，但会显著增加工具调用次数。

## 什么时候该放弃这个 skill
如果用户连续三次说「不用穿衣服建议」，就只报温度，别再套这个模板。
"""


def check(name, desc):
    """skill 设计自检——最常见的翻车就这几条。"""
    print("\n[自检] 这几条最容易翻车，逐条看：")
    print(f"  {'OK ' if 1 <= len(name) <= 64 and re.fullmatch(r'[a-z0-9-]+', name) else 'BAD'}"
          f" 名字小写字母+连字符、1~64 字符：{name}")
    print(f"  {'OK ' if 20 <= len(desc) <= 1024 else 'BAD'}"
          f" description 长度 20~1024 字符（现在 {len(desc)}）")
    print(f"  {'OK ' if any(k in desc for k in ('当', '使用', '问', '时')) else 'WARN'}"
          f" description 里说了「什么时候用」——光说功能不够，模型靠这句决定用不用")
    print(f"  {'OK ' if len(desc) > 60 else 'WARN'}"
          f" description 里最好写清适用场景，而不只是一句话概括")


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "./my-first-skill"
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    with open(os.path.join(out_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(SKILL_MD.format(name=SKILL_NAME, description=DESCRIPTION))
    with open(os.path.join(out_dir, "reference.md"), "w", encoding="utf-8") as f:
        f.write(REFERENCE_MD)

    print("=" * 58)
    print(f"skill 骨架已生成：{out_dir}")
    print("=" * 58)
    for fn in sorted(os.listdir(out_dir)):
        print(f"  {fn}")

    print("\n[各部分干嘛]")
    print("  SKILL.md 的 frontmatter")
    print("      name         唯一标识")
    print("      description  **最关键的一句**——平时只有这句进上下文")
    print("  SKILL.md 的正文")
    print("      什么时候用 / 怎么做 / 输出格式 / 翻车怎么救")
    print("  reference.md")
    print("      正文里一句「看 reference.md」链过来，用到才加载")

    check(SKILL_NAME, DESCRIPTION)

    print("\n[想让它真生效]")
    print("  把整个目录放到你的 skills 目录下，例如：")
    print(f"      ~/.agents/skills/{SKILL_NAME}/")
    print("  然后重启 agent，问一句「今天穿什么？」试试。")

    print("\n" + "=" * 58)
    print("注意：skill 不是一个函数，是「做某类事的做法」。")
    print("函数（工具）告诉你『能干什么』，skill 告诉你『该怎么做』。")
    print("=" * 58)


if __name__ == "__main__":
    main()
