# 标 `completed` 与核验操作（NOTES 1.7 的操作细节）

> 本文件只在**标/取消 `completed`、或课数脚本数变动后核验**时读。规矩本身见 [NOTES.md](../../NOTES.md) 第 1.7 节；来历见存档 [5.10](../history/5.10-data-alias-single-source.md)、[5.11](../history/5.11-question-count-to-script.md)。

## 先审计，再动手（优先用脚本，别手改）

```
pwsh tools/progress.ps1                                                  # 审计，不改文件
pwsh tools/progress.ps1 -Action mark   -Lesson llm/0003-kv-cache-and-prompt-caching.html
pwsh tools/progress.ps1 -Action unmark -Lesson llm/0003-xxxx.html
```

- 退出码 0 ＝ 全通过，可直接当 CI 用。**`audit` 那一半比 `mark` 值钱** —— 不标任何东西也能查出三处漂移、主页 stats 与实测不符、以及进阶版别名三处是否一致（E 段）。**动手前先审计**，状态已经不一致时脚本会拒绝叠加改动。
- **进阶版的 README 条目能自动写**（2026-10-05 起）：别名以页面上的 `data-alias` 为唯一落点，卡片 / `<title>` / README 三处都从它派生；进阶版条目自动挂在**基础课那一行末尾**（README 的约定是两课并排一行）。基础课那一行不在清单里就报错让你先标基础课，不瞎猜。
- **E 段共三条检查**：① 三处相等 ② **Q 编号连续 1…N**（抓删题留断号）③ **别名开头的数字 == 带编号的 Q 数**（抓"问数变了忘改名"）。②③ 只数**带编号**的 Q ——「附 · 两个别误会」那种没编号的补丁块不算一问，这正是"问数"唯一说得清的算法。
- 改别名**只改 `data-alias` 一处** —— 以前三处各抄一遍，抄漏过。

## 标记要改三处，缺一即漏

1. **`lessons/index.html` —— 权威落点。** 卡片加 `class="pillar completed"`，标题里紧跟 `<a>` 之后加 `<span class="badge">completed</span>`（样式已在 `assets/base.css`，不用改 CSS）。
2. **`README.md` 里「课程进度怎么标记」那一节** —— 锚点是 `目前标为 completed 的是：` 那句，在它下面的清单里加一行带链接的条目。**按那句定位，不要按行号**（行号会随 README 改动漂）。
3. **根目录 `index.html` 的「N 门已定稿」那个 stat** —— 硬编码计数，忘了改就跟目录页对不上，而主页面恰恰是学习者第一眼看到的地方。
   - ⚠️ **两份文件同名**：`lessons/index.html` 和根目录 `index.html` 都叫 `index.html`。用 `Select-String` 时**必须打 `$_.Path` 而不是 `$_.Filename`** —— 后者会把两处都显示成 `index.html`，看错文件改错地方（曾差点踩）。
   - 这个数字**数的是卡片数、不是课数**：`0001` 基础课和 `0001-deep` 是两张卡、算 2（与目录页一致）；而 README 那份清单数的是课、算 1。**两处口径不同是刻意的，别顺手"对齐"成同一个数。**

## 主页 stats 与课数核对

- **主页那一排 stats 全是硬编码**，加课或拆课时要一起重数（`0005/0006/0007` 拆课时主页四个数全过期没人发现）。**这 6 个数已由 audit 的 D 段覆盖**（lede 的基础/进阶/脚本 ＋ stat 的门课/脚本）—— ⚠️ **但只有 LLM 轨道**的门数被核，agent / rag / practice 三条轨道的门数仍不在任何脚本覆盖范围里。
- 判据：**动 `lessons/` 里的课数或 `exercises/` 里的脚本数之后，跑一次 `pwsh tools/progress.ps1` 的 audit**（实测口径：基础课 ＝ 不带 `-deep` 的课文件数，进阶版 ＝ 带 `-deep` 的，脚本 ＝ `exercises/**/*.py`）。
