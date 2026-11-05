# 下一会话交接

> 用途：把开发状态从当前会话交接到新会话，避免重读整段对话。只记状态与下一步，不复制课程内容。
> **每轮开发结束重写本文件**（不是追加）；与 `NOTES.md` 第 4 节的分工见 `AGENTS.md`「文件职责」。

## 先读这些（按顺序）

1. `AGENTS.md`：会话规则（会话自动加载，不用手动提醒）。
2. 本文件：当前状态与下一步。
3. [`NOTES.md`](NOTES.md) 第 1 节（流程纪律）＋ [`internal/standards/COURSE-STANDARD.md`](internal/standards/COURSE-STANDARD.md)（全局写作标准，**1.5 文章体＋句子层四条是文字质量的硬指标**）＋**本轮要动的那一轨 [`internal/standards/tracks/<轨道>.md`](internal/standards/tracks/)**。
4. **做 RAG 改版任何一课前：读 [`RAG-REVISION-PLAN.md`](RAG-REVISION-PLAN.md)**（总施工图 **v5**：§0 已定决策不得重启讨论、§2 课表 11 门与批次、§5 例子素材、§6 0010 蓝本已消耗、§9 进度）。
5. 开工前跑 `pwsh tools/progress.ps1` 拿基线。

## 当前状态

- **课程总盘**：37 门 / 28 基础 / 9 进阶 / 26 脚本；19 门已标 completed（全在 LLM 轨）；audit 全绿（2026-11-06 收工实跑）。
- **✅ 提交史**：`afbec6d` 0007 Harness · `fb12d31` 全库文字返工 · `a6934d7` RAG 0001 · `769dd46` 地图 v5 · `57ce45e` 0004 · `a17f838` 0005 · `13e9934` 0006 · `1e5a7c9` 0004/0005 文字返工 · `653cb01` 0007 查询工程＋0008 上下文组装 · `3880d8b` 0009 · `72e8bbe` 0010＋F5 验收 · `bdec1a3` 标准查重瘦身（5.76）。**本轮 0011＋0002 未提交**（工作区改动，提交后补哈希）。
- **✅ F5 验收（2026-11-05）**：0009/0008/0004/0005 全文通读＋小测逐题点过；0009 两脚本复跑、课内 `<pre>` 逐行对账；0008→0009 接口句查过；七张 SVG＋`rag-diagnosis.svg`＋`eval-configs.svg` 全部页内目视——图待目视欠账清零。抓出并修两处：0009 §3「六个决定」→「五个决定」；`0009-rag-eval.py` docstring 的「进阶版」残留。
- **✅ RAG 批 3 第一会话（0010）**：`lessons/rag/0010-eval-methods.html` 220 行；20 题标注集模板（单跳 10/多跳 5/否定 5，标内容不标块号）→ 三个切块配置（45/90/180 字）→ 三张成绩单 → 逐题对账 → 切碎 vs 没进前 k → 盲区 → 否定题阈值重叠 → 判官提示词模板＋蓝本三教训 → 结论模板；脚本 `0010-eval-configs.py`、插图 `eval-configs.svg`、小测 6 题；术语补「对照实验/标注集」。
- **✅ RAG 批 3 第二会话（0011）**：`lessons/rag/0011-agentic-rag.html` 320 行；固定流水线假设「一次检索拿全」→ 三类不配合 → 四个决定（查不查/查什么/够不够/再查不查）→ Self-RAG 四类反思 token（含 `continue`）与训练要求 → CRAG 三分支与 0.77B 评估器 → 多轮收益（IRCoT）与代价（串行/token/上下文）→ 五条停止条件与三预算 → 固定/Self-RAG/CRAG/工具型对照 → 六种不该上的情况 → 怎么把多查几次记进 0010 的成绩单；脚本 `0011-agentic-rag.py`、插图 `agentic-rag-loop.svg`、小测 6 题。
- **✅ RAG 批 3 第三会话（0002，本轮）**：
  - **`lessons/rag/0002-rag-pipeline.html` 地图终稿（286 行）**：六步逐个「手上数据→坏法→专课门牌」；RAGFlow 面板锚点（parsing method/recommended chunk size、Embedding model、Search method、Retrieval testing、Top N/Show citations/Empty Response）；第④步标出「固定查一次」与「agentic 循环」的分岔；§4 排查表按「先看块→再看索引→再看嵌入→最后调 k」排序；Anthropic 5.7%→1.9% 四行保留（0006 引用它）。
  - 新插图 `assets/rag-map.svg`（六步＋答题模型分界＋第④步岔口；XML 合法＋页内实渲目视）。
  - `exercises/rag/0002-rag-pipeline.py`：输出改「组装」「答题模型」，补 [2][3] 摘录所需的 123 维与索引数据，删掉资料外的「事后补一条消息」；GBK 直跑会 `UnicodeEncodeError` 的提示已写进课里。
  - **两轮学习审计**：首轮抓出「前五步不生成一个字」与建库模型生成摘要/问题（RAGFlow Extractor、Anthropic 第二行）的矛盾、Indexer「双开」旧口径、排查表缺③、Top N 与 k 关系不明、脚本答案含资料外内容；全部修正。复审确认核心矛盾已消，补了 token 定义、第 7 课四种加工的白话版、成本一句、⑤/⑥边界一句。
  - **一手资料重核（2026-11-06）**：RAGFlow `dataset_configuration` 现行原文明确 Search method 是展示标签「These are not selectable checkboxes in the current panel」；RESOURCES 已补 `retrieval_testing` 页，RAG 计划 §5 的「官方建议双开」已作废旧口径。
  - 接口同步：`0011` 的「最后一步才是生成模型」改「答题模型」；README＋目录卡 0002 摘要同步；主页 stats 不动（无新增课/脚本）。

## 下一步

1. **RAG 批 3 第四会话：0003 三选一加厚**（`lessons/rag/0003-when-not-to-use-rag.html` 现在还是旧「初学版」；标题/meta/互链/课型标识都要整课重写）。主线：RAG vs 微调（知识 vs 行为，链 `llm/0009`）vs 长上下文（成本＋lost-in-the-middle，链 0008）；保留原决策表。动前先读 0001、0002、0004～0011 的接口句。
2. **RAG 改版收尾（0003 后做）**：MISSION 边界句、`progress.ps1` D/E 段补 RAG 覆盖（D 段已被动覆盖 RAG 计数，E 段仍只盯 LLM）、并入本文件、建存档、计划文件退役。
3. **拍板一笔欠账**：LLM 0005/0006/0008 脚本输出摘录三处「同款」要不要连脚本一起改。
4. **Agent 轨 0001/0002 超长**＋体量预算、速查区补卡、「Agent 原理篇」旧轨道名残留：仍待拍板。

## 待确认

- ⚠ **年假语料跨课数字漂移（仍待拍板）**：0008 脚本与正文/小测用「满三年 7 天、满五年 10 天」，0009/0010/0011 的语料用「满三年 10 天、满五年 15 天」（0004 最早的小制度也是 15 天版）。同一「员工手册」贯穿例在两套课里数字不同。两个修法：①把 0008 对齐到 5/10/15（要动脚本＋重跑＋重对账 `<pre>`，摆法机制需复验）；②保持现状（各课脚本自成玩具世界）。**动 0008 前须学习者点头。**
- 学习者每周可投入时间（还没收集，影响 RAG 批次排期）。
- `internal/drafts/` 里四份草稿（两份 0001 实验稿＋0008/0009 语言改稿）是否长期保留（均未提交）。

> AI生成
