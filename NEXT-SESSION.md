# 下一会话交接

> 用途：把开发状态从当前会话交接到新会话，避免重读整段对话。只记状态与下一步，不复制课程内容。
> **每轮开发结束重写本文件**（不是追加）；与 `NOTES.md` 第 4 节的分工见 `AGENTS.md`「文件职责」。

## 先读这些（按顺序）

1. `AGENTS.md`：会话规则（会话自动加载，不用手动提醒）。
2. 本文件：当前状态与下一步。
3. [`NOTES.md`](NOTES.md) 第 1 节（流程纪律）＋ [`internal/standards/COURSE-STANDARD.md`](internal/standards/COURSE-STANDARD.md)（全局写作标准）＋**本轮要动的那一轨 [`internal/standards/tracks/<轨道>.md`](internal/standards/tracks/)**。
4. **做 RAG 改版任何一课前：读 [`RAG-REVISION-PLAN.md`](RAG-REVISION-PLAN.md)**（总施工图 **v5**：§0 已定决策不得重启讨论、§2 课表 11 门与批次、§5 例子素材、§9 进度）。
5. 开工前跑 `pwsh tools/progress.ps1` 拿基线。

## 当前状态

- **课程总盘**：34 门 / 23 基础 / 11 进阶 / 22 脚本；19 门已标 completed；audit 全绿（2026-11-04 收工实跑）。
- **✅ 提交史**：`afbec6d` 0007 施工 · `fb12d31` 文字返工 · `a6934d7` RAG 批 1 会话一（0001 加厚）· `769dd46` RAG 地图 v5 · `57ce45e` RAG 批 1 会话二（0004＋首个 deep 关停）。
- **✅ RAG 批 1 第三会话（2026-11-04，本会话）**：
  - **0005「嵌入与相似度」开课**（`lessons/rag/0005-embedding-and-similarity.html`，220 行）：嵌入模型生命周期→三把尺子（点积/余弦/欧氏，恒等式机制）→尺子跟模型走（归一化点积≡余弦）→模型侧失手清单（同名不同物/生僻词/细粒度差）→换模型＝整库重算（RAGFlow 兼容性抽查**新口径**）；新插图 `assets/similarity-three-rulers.svg`＋新脚本 `0005-similarity-metrics.py`（玩具向量演示换尺子换名次）＋小测 6 题；术语表补「相似度尺子」。
  - **三尺子一手来源当场抓**（Pinecone "Vector Similarity Explained"）入 RESOURCES。
  - **⚠ 0001-deep 本轮没关**：它的主体（稀疏稠密＋RRF）是 0006 的料，只有失手清单进了 0005——**关停时机判据修正为"内容全部有家的那一轮"**（存档 5.70，计划 §9/§10 已改）。
- **⚠ 三张图渲染未目视**：`closed-vs-open-book.svg`（0001）、`chunk-three-cuts.svg`（0004）、`similarity-three-rulers.svg`（0005），XML 合法都过，按 1.7 还差浏览器渲染看一眼。

## 下一步

1. **F5 验收（五批叠着）**：① `rag/0005` 新课＋三尺子插图渲染目视；② `rag/0004`＋其插图；③ `rag/0001` 加厚稿＋其插图；④ v5 重排抽查（`lessons/rag/0009-two-failure-modes*`）；⑤ 更早的 0007 施工＋文字返工两笔。
2. **RAG 批 2 第一会话**：读 `RAG-REVISION-PLAN.md` 按批 2 施工——**0006 多路召回：混合检索与重排**（0001-deep 主体升格：稀疏/稠密翻车两题＋RRF k=60＋噪音榜陷阱；**同轮关停 0001-deep**、`0001-sparse-vs-dense.py` 随课改名挂 0006）。之后 0007 查询工程 → 0008 组装 → 0009 诊断（收编 0004-deep）。
3. **拍板一笔欠账**：LLM 0005/0006/0008 脚本输出摘录三处「同款」要不要连脚本一起改。
4. **Agent 轨 0001/0002 超长**：待 F5 后定压缩 vs 拆；体量预算要不要入 `tracks/agent.md` 未拍板。
5. **收尾杂项**：`lessons/index.html` 速查区补不补卡；「Agent 原理篇」旧轨道名残留待拍板。

## 待确认

- 学习者每周可投入时间（还没收集，影响 RAG 批次排期）。
- 0003/0004 草稿 `internal/drafts/` 是否归档（上轮遗留）。
- RAG 改版收尾（计划 §9 末项）：MISSION 边界句、`progress.ps1` D/E 段补 RAG 覆盖、旧 deep 关停收尾（还剩 0001-deep→随 0006、0004-deep→随 0009）、计划文件退役。

> AI生成
