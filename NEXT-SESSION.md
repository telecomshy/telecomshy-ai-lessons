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

- **课程总盘**：33 门 / 21 基础 / 12 进阶 / 21 脚本；19 门已标 completed；audit 全绿（2026-11-03 实跑）。
- **✅ 2026-11-02 三笔提交**：`afbec6d` 0007 Harness 施工；`fb12d31` 全库文字返工；`a6934d7` RAG 批 1 第一会话（NOTES 4.1 骨架段作废＋`rag/0001` 加厚试笔 223 行，存档 5.67）。
- **✅ RAG 课程地图 v5（2026-11-03，本会话）**：学习者拍板**工具操作不进课**（"RAGFlow 安装看官网即可，课件聚焦通用知识"）——删「上手 RAGFlow」课、原 0011 改「评测方法」去工具化、RAGFlow 降为例子锚点、编号整体前移一号（**11 门全理论，0001–0011**）。已执行：旧 0004＋0004-deep＋两脚本**重排 0009 占位**（互链 6 文件＋脚本打印串改后重跑对账，约 20 处）；`tracks/rag.md` 改写、COURSE-STANDARD 两处、RESOURCES 课号全同步。决策与教训存档 **5.68**，计划进度见 §9。
- **⚠ 0001 新图渲染未目视**（`assets/closed-vs-open-book.svg`，XML 合法已过，按 1.7 还差浏览器渲染看一眼）。

## 下一步

1. **F5 验收（三批叠着）**：① `rag/0001` 加厚稿＋新图渲染目视（上轮遗留）；② v5 重排抽查（`lessons/rag/0009-two-failure-modes*` 两页课号/脚本路径、目录卡、README 三处）；③ 更早的 0007 施工＋文字返工两笔（`afbec6d`/`fb12d31`）你说了"回头仔细修订"，仍未细看。
2. **RAG 批 1 第二会话**：读 `RAG-REVISION-PLAN.md` 按批 1 施工——**0004 建库：清洗与切块**（0002-deep 升格＋新内容，同轮关停 0002-deep）→ 0005 嵌入（同轮关停 0001-deep）。
3. **拍板一笔欠账**：LLM 0005/0006/0008 脚本输出摘录三处「同款」要不要连脚本一起改（改脚本→重跑→同步 `<pre>`）。
4. **Agent 轨 0001/0002 超长**：待 F5 后定压缩 vs 拆；体量预算要不要入 `tracks/agent.md` 未拍板。
5. **收尾杂项**：`lessons/index.html` 速查区补不补卡；「Agent 原理篇」旧轨道名残留待拍板。

## 待确认

- 学习者每周可投入时间（还没收集，影响 RAG 批次排期）。
- 0003/0004 草稿 `internal/drafts/` 是否归档（上轮遗留）。
- RAG 改版收尾（计划 §9 末项）：MISSION 边界句、`progress.ps1` D/E 段补 RAG 覆盖、index/README/统计口径同步、旧 deep 关停收尾、计划文件退役。

> AI生成
