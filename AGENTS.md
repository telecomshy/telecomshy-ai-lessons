# AGENTS.md

这个仓库是一部中文 AI Agent 教程：课件是 `lessons/` 下自包含的 HTML，配套脚本在 `exercises/`。

## 会话开始时

1. 读 [`NEXT-SESSION.md`](NEXT-SESSION.md)：当前进度与下一步；同时跑一次 `pwsh tools/progress.ps1` 核对实际进度——交接文档可能滞后，以磁盘为准，防重复写课或跳课。
2. 读 [`NOTES.md`](NOTES.md) 第 1 节（流程纪律）＋ [`internal/standards/COURSE-STANDARD.md`](internal/standards/COURSE-STANDARD.md)（全局写作标准，节号同源 1.2～1.6）＋**本轮要动的那一轨 [`internal/standards/tracks/<轨道>.md`](internal/standards/tracks/)（轨道标准：分版/课型标识/受众/脚本分层/编号特例）**。
3. 按 `NEXT-SESSION.md` 的下一步指引按需读：[`MISSION.md`](MISSION.md)、[`RESOURCES.md`](RESOURCES.md)（顶部有「从课找来源」索引表）、[`internal/learning-records/`](internal/learning-records/)。
4. 写某一课前：先读前后相邻课与对应参考卡，对表口径（互链规矩见 `COURSE-STANDARD.md` 1.6）。

## 动手前先读

- **改课、开课、标 `completed`**：先读 [`NOTES.md`](NOTES.md) 第 1 节（流程纪律）、[`internal/standards/COURSE-STANDARD.md`](internal/standards/COURSE-STANDARD.md)（全局写作标准）与该轨 [`internal/standards/tracks/<轨道>.md`](internal/standards/tracks/)；操作细节在 [`internal/rules/`](internal/rules/)，历史决策与教训在 [`internal/history/`](internal/history/)。
- **写任何知识点**：只从 [`RESOURCES.md`](RESOURCES.md) 的一手资料取，不凭模型记忆；新来源当场补进去，并注明用途。
- **学习者已掌握什么**：看 [`internal/learning-records/`](internal/learning-records/)（teach 技能的学习记录）。那是学习证据，别跟 `internal/history/` 的开发史混。

## 文件职责（谁说了算）

| 职责 | 文件 | 怎么维护 |
|---|---|---|
| 入口规则 | `AGENTS.md` | 本文件；会话自动加载 |
| 当前进度与下一步 | `NEXT-SESSION.md` | **唯一权威**；每轮开发结束**重写全文**，不追加 |
| 流程纪律＋画像＋待办 | `NOTES.md` | 第 1 节每次开发前读；写入纪律见其 1.9 |
| 写作标准·全局（零件 · 课型 · deep 体例 · 讲法 · 互链＋自查清单） | `internal/standards/COURSE-STANDARD.md` | 每次写课/改课前读；节号沿用原 1.2～1.6 |
| 写作标准·轨道（分版 · 课型标识 · 受众 · 脚本分层 · 编号特例） | `internal/standards/tracks/<轨道>.md` | **写/改哪轨的课读哪轨**；审计 F 段盯存在与体量 |
| 一手来源 | `RESOURCES.md` | 写任何知识点唯一取材处；顶部索引表按课查 |
| 学习证据 | `internal/learning-records/` | teach 技能的学习记录 |
| 操作细节 | `internal/rules/` | 做那件事的时候读 |
| 历史决策与教训 | `internal/history/` | 旧决策被质疑、续写同款工作时读 |
| 为什么做这门课（使命 · 成功标准 · 范围外） | `MISSION.md` | 开新课定方向时读 |
| 对外门面＋`completed` 落点之一 | `README.md` | 标 `completed` 时按 [`internal/rules/mark-completed.md`](internal/rules/mark-completed.md) 三处落点同步 |
| 术语表 | `reference/glossary.html` | 术语统一以此为准，新术语当场补 |
| 对外文档（读者向） | `docs/` | 对外区：只放面向读者的文档；开发规程（标准/规则/历史/学习记录）集中在 `internal/` |

文件之间内容重复时，以这张表的分工为准。「下一步」只写 `NEXT-SESSION.md`；`NOTES.md` 第 4 节只留长期欠账清单。

## Agent skills

### Issue tracker

Issues 存在 GitHub Issues，仓库 `telecomshy/telecomshy-ai-lessons`，用 `gh` CLI 操作。见 [`internal/agents/issue-tracker.md`](internal/agents/issue-tracker.md)。

### Triage labels

本仓库沿用 GitHub 默认标签（`bug` / `enhancement` / `question` / `documentation` / `wontfix`）。setup 技能要求的五个 triage 角色还没有专用标签，对应关系见 [`internal/agents/triage-labels.md`](internal/agents/triage-labels.md)。

### Domain docs

Single-context：`GLOSSARY.md`（仓库/课程开发领域术语）在仓库根目录，ADR 在 `internal/adr/`，两者都按需懒创建；学习者面向的课程内容术语仍在 [`reference/glossary.html`](reference/glossary.html)。见 [`internal/agents/domain.md`](internal/agents/domain.md)。

> AI生成
