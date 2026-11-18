# AGENTS.md

这个仓库是一部中文 AI Agent 教程：课件是 `lessons/` 下自包含的 HTML，配套脚本在 `exercises/`。

## 会话开始时

1. 读 [`NEXT-SESSION.md`](NEXT-SESSION.md)：当前进度与下一步；同时跑一次 `pwsh tools/progress.ps1` 核对实际状态——交接文档可能滞后，以磁盘为准，防重复写课或跳课。
2. 读 [`NOTES.md`](NOTES.md)：学习者画像与教学偏好（teach 技能用的便签本）。
3. 读 [`internal/standards/PROCESS.md`](internal/standards/PROCESS.md)（开发流程与核验纪律）＋ [`internal/standards/COURSE-STANDARD.md`](internal/standards/COURSE-STANDARD.md)（页面结构、课型、讲法、互链）＋ [`internal/standards/ARTICLE-STYLE.md`](internal/standards/ARTICLE-STYLE.md)（正文文章体）＋**本轮要动的那一轨 [`internal/standards/tracks/<轨道>.md`](internal/standards/tracks/)**。**改已有课**再读 [`internal/standards/REVISION.md`](internal/standards/REVISION.md)。
4. 按 `NEXT-SESSION.md` 的下一步指引按需读：[`MISSION.md`](MISSION.md)、[`RESOURCES.md`](RESOURCES.md)（顶部有「从课找来源」索引表）、[`internal/learning-records/`](internal/learning-records/)。
5. 写某一课前：先读前后相邻课与对应参考卡，对表口径（互链规矩见 `COURSE-STANDARD.md` 1.6）。**前后课只用来对口径，不用来学文字**：语感按 `ARTICLE-STYLE.md`；派写作子代理时不喂前后课，避免被旧文风带偏。

## 动手前先读

- **开课、改课、精修**：先读 [`internal/standards/PROCESS.md`](internal/standards/PROCESS.md)、[`COURSE-STANDARD.md`](internal/standards/COURSE-STANDARD.md)、[`ARTICLE-STYLE.md`](internal/standards/ARTICLE-STYLE.md) 与该轨 [`internal/standards/tracks/<轨道>.md`](internal/standards/tracks/)；改已有课另读 [`REVISION.md`](internal/standards/REVISION.md)。具体操作手册在 [`internal/playbooks/`](internal/playbooks/)，历史决策与教训在 [`internal/history/INDEX.md`](internal/history/INDEX.md)。
- **写任何知识点**：只从 [`RESOURCES.md`](RESOURCES.md) 的一手资料取，不凭模型记忆；新来源当场补进去，并注明用途。
- **学习者已掌握什么**：看 [`internal/learning-records/`](internal/learning-records/)（teach 技能的学习记录）。那是学习证据，别跟 `internal/history/` 的开发史混。

## 文件职责（谁说了算）

| 职责 | 文件 | 怎么维护 |
|---|---|---|
| 入口规则 | `AGENTS.md` | 本文件；会话自动加载 |
| 当前进度与下一步 | `NEXT-SESSION.md` | **唯一权威**；每轮开发结束**重写全文**，不追加 |
| 学习者画像与教学偏好 | `NOTES.md` | teach 的便签本；只记学习者是谁、怎么教他，不记流程与待办 |
| 开发流程与核验纪律 | `internal/standards/PROCESS.md` | 取材、交付门槛、开发一课、文档写入纪律 |
| 课程标准·全局（结构 · 课型 · 讲法 · 互链＋交付检查单） | `internal/standards/COURSE-STANDARD.md` | 每次写课/改课前读 |
| 写作标准·文章体（结构 · 段落 · 句子 · 正反例 · 验收） | `internal/standards/ARTICLE-STYLE.md` | 写/改任何正文前读；正文文字以此为准 |
| 改课与精修标准 | `internal/standards/REVISION.md` | 改已有课、精修 md 稿时读 |
| 轨道标准（分版 · 课型标识 · 受众 · 脚本分层 · 编号特例） | `internal/standards/tracks/<轨道>.md` | **写/改哪轨的课读哪轨**；审计 E 段盯存在与体量 |
| 一手来源 | `RESOURCES.md` | 写任何知识点唯一取材处；顶部索引表按课查 |
| 课件文字稿（精修底稿＋文字版） | `lessons-md/` | **精修以它为文字底稿**：学习者改 md，或 agent 按 `ARTICLE-STYLE.md` 重写，主代回写 HTML；镜像由 `html2md` 生成，别跑全量转换覆盖未交回的稿 |
| 学习证据 | `internal/learning-records/` | teach 技能的学习记录 |
| 操作手册（联网 · 改课件 · 学习审计） | `internal/playbooks/` | 做那件事的时候读 |
| 历史决策与教训 | `internal/history/` | 索引在 [`INDEX.md`](internal/history/INDEX.md)；旧决策被质疑、续写同款工作时读 |
| 为什么做这门课（使命 · 成功标准 · 范围外） | `MISSION.md` | 开新课定方向时读 |
| 对外门面 | `README.md` | 课程总览、用法、仓库结构；不再维护完成标记 |
| 术语表 | `reference/glossary.html` | 术语统一以此为准，新术语当场补 |
| 对外文档（读者向） | `docs/` | 只放面向读者的文档；开发规程集中在 `internal/` |

文件之间内容重复时，以这张表的分工为准。「下一步」只写 `NEXT-SESSION.md`；长期欠账也写在那里，不散在 NOTES 或标准里。

## Agent skills

### Issue tracker

Issues 存在 GitHub Issues，仓库 `telecomshy/telecomshy-ai-lessons`，用 `gh` CLI 操作。见 [`internal/agents/issue-tracker.md`](internal/agents/issue-tracker.md)。

### Triage labels

本仓库沿用 GitHub 默认标签（`bug` / `enhancement` / `question` / `documentation` / `wontfix`）。setup 技能要求的五个 triage 角色还没有专用标签，对应关系见 [`internal/agents/triage-labels.md`](internal/agents/triage-labels.md)。

### Domain docs

Single-context：`GLOSSARY.md`（仓库/课程开发领域术语）在仓库根目录，ADR 在 `internal/adr/`，两者都按需懒创建；学习者面向的课程内容术语仍在 [`reference/glossary.html`](reference/glossary.html)。见 [`internal/agents/domain.md`](internal/agents/domain.md)。
