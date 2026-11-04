# 下一会话交接

> 用途：把开发状态从当前会话交接到新会话，避免重读整段对话。只记状态与下一步，不复制课程内容。
> **每轮开发结束重写本文件**（不是追加）；与 `NOTES.md` 第 4 节的分工见 `AGENTS.md`「文件职责」。

## 先读这些（按顺序）

1. `AGENTS.md`：会话规则（会话自动加载，不用手动提醒）。
2. 本文件：当前状态与下一步。
3. [`NOTES.md`](NOTES.md) 第 1 节（流程纪律）＋ [`internal/standards/COURSE-STANDARD.md`](internal/standards/COURSE-STANDARD.md)（全局写作标准，**1.5 文章体＋句子层四条是文字质量的硬指标**）＋**本轮要动的那一轨 [`internal/standards/tracks/<轨道>.md`](internal/standards/tracks/)**。
4. **做 RAG 改版任何一课前：读 [`RAG-REVISION-PLAN.md`](RAG-REVISION-PLAN.md)**（总施工图 **v5**：§0 已定决策不得重启讨论、§2 课表 11 门与批次、§5 例子素材、§9 进度）。
5. 开工前跑 `pwsh tools/progress.ps1` 拿基线。

## 当前状态

- **课程总盘**：36 门 / 26 基础 / 10 进阶 / 24 脚本；19 门已标 completed；audit 全绿（2026-11-05 收工实跑）。
- **✅ 提交史**：`afbec6d` 0007 施工 · `fb12d31` 文字返工 · `a6934d7` RAG 会话一（0001）· `769dd46` 地图 v5 · `57ce45e` 会话二（0004）· `a17f838` 会话三（0005）· `13e9934` 会话四（0006）· `1e5a7c9` 0004/0005 文字返工 · `git log -1` 会话五（0008）。
- **✅ RAG 批 2 第三会话（2026-11-05，本会话）**：
  - **0008「上下文组装与生成：塞进去，不等于用上」开课**（`lessons/rag/0008-context-assembly.html`，263 行）：位置（Lost in the Middle）→ 段数（20→50 只 +1.5%/+1%）→ 标签（编号/来源/版本）→ 约束（任务/证据/格式/兜底，RAGFlow Empty Response/System prompt）→ 引用（提示词层核对 vs Anthropic Citations）→ 拒答（两道闸门、过度拒答）。小测 6 题。
  - 新插图 `assets/context-assembly.svg`（两栏摆法对比＋U 形结论；XML 校验＋无头 Chrome 实渲＋页内看过）＋新脚本 `exercises/rag/0008-context-assembly.py`（本地跑通，课内 `<pre>` 逐行对账）＋术语表补「上下文组装 / Lost in the Middle / 引用溯源 / 拒答」。
  - 一手来源当场抓入 RESOURCES：Lost in the Middle 原文数字、Anthropic 长上下文提示（问题放最后、最多 30%）、Anthropic Citations、RAGFlow Chat Configuration。**RAGFlow Empty Response 旧 quote（"may give rise to hallucinations"）已退役**，RESOURCES 与计划 §5 同步现行口径；索引表 `rag/0008` 行同步。
  - 课程目录卡、README RAG 表、主页 stats（36/26/10/24）同步；**0007 的「第 8 课（在写）」已改成真链接**。
- **✅ 0004/0005 文字返工完成（2026-11-04）**：两课按 1.5 文章体＋句子层四条整课重写；`<pre>`/表格/图注与改前逐字节一致（git 对照）、摘录对账过、小测 6/6 与答案位置未动；破折号两课归零（原 10/12 处）、垫词与临时比喻清零。返工配方在存档 5.71 末节。
- **⚠ 图待目视**：`closed-vs-open-book.svg`（0001）、`chunk-three-cuts.svg`（0004）、`similarity-three-rulers.svg`（0005）、`retrieval-wide-then-narrow.svg`（0006）、`query-engineering.svg`（0007，已渲染看过）、`context-assembly.svg`（0008，本会话已渲染＋页内看过，F5 再看一眼即可）。

## 下一步

1. **F5 验收（最优先）**：① 0008 全文通读＋小测点一遍；② 0007 与 0008 连着读，检查「查询侧→生成侧」的接口句是否顺；③ 0004/0005 返工后的文字通读（对照 0006/0007/0008 的手感）；④ 六张 SVG 的页内目视（0007/0008 已过，另四张仍未看）。
2. **RAG 批 2 第四会话：0009 翻车诊断与评估**（收编 0004-deep：两种翻车、先查检索再怪模型的排查顺序、分开评检索与生成、LLM-as-Judge、三类评估集；最后一个 deep 关停）。
3. **RAG 批 3**：0010 评测方法 → 0011 Agentic RAG → 0002 地图终稿 → 0003 三选一加厚。
4. **拍板一笔欠账**：LLM 0005/0006/0008 脚本输出摘录三处「同款」要不要连脚本一起改。
5. **Agent 轨 0001/0002 超长**＋体量预算、速查区补卡、「Agent 原理篇」旧轨道名残留：仍待拍板。

## 待确认

- 学习者每周可投入时间（还没收集，影响 RAG 批次排期）。
- `internal/drafts/` 里两份 0001 实验稿是否长期保留（本轮只移动未删）。
- RAG 改版收尾（计划 §9 末项）：MISSION 边界句、`progress.ps1` D/E 段补 RAG 覆盖、0004-deep 关停、计划文件退役。

> AI生成
