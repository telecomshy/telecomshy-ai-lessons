# 下一会话交接

> 用途：把开发状态从当前会话交接到新会话，避免重读整段对话。只记状态与下一步，不复制课程内容。
> **每轮开发结束重写本文件**（不是追加）；与 `NOTES.md` 第 4 节的分工见 `AGENTS.md`「文件职责」。

## 先读这些（按顺序）

1. `AGENTS.md`：会话规则（会话自动加载，不用手动提醒）。
2. 本文件：当前状态与下一步。
3. [`NOTES.md`](NOTES.md) 第 1 节（流程纪律）＋ [`internal/standards/COURSE-STANDARD.md`](internal/standards/COURSE-STANDARD.md)（全局写作标准）＋**本轮要动的那一轨 [`internal/standards/tracks/<轨道>.md`](internal/standards/tracks/)**。
4. 按下一步的事按需读：[`5.66`](internal/history/5.66-concept-ladder-and-familiar-start.md)（MCP/Skill 开场法与文字返工全程）／[`5.65`](internal/history/5.65-agent-track-split-and-renumber.md)（拆课与全链重排，7 课制）／[`5.54`](internal/history/5.54-agent-model-and-0001-rework.md)（0007 Harness 施工图在其 §三「0005」行，内容照旧、课号已顺延）／[`5.57`](internal/history/5.57-llm-track-language-rework.md)（编辑工具教训全集）。
5. 开工前跑 `pwsh tools/progress.ps1` 拿基线。

## 当前状态

- **课程总盘**：33 门 / 21 基础 / 12 进阶 / 21 脚本；存档 66 篇；audit 全绿（2026-10-27 实跑）。
- **✅ 0003/0004 已用草稿替换正文（2026-10-27）**：
  - `lessons/agent/0003-mcp.html` ← `internal/drafts/mcp-v3-problem-first.html`：问题先行、文章体；§5 补了「启用只是登记，第一次请求才把工具定义带给模型，之后每轮重带」；6 题。
  - `lessons/agent/0004-skill.html` ← `internal/drafts/skill-from-familiar.html`：文章体重写；§4 讲「目录常驻、正文按需」，并注明 Anthropic 放系统提示／OpenCode 放 `skill` 工具说明／TeleAgent 手册未写内部位置；6 题。
  - 配套速查 `reference/mcp-config-cheatsheet.html` 已从草稿落正式页，0003 正文与 next 都已链过去。
  - 旧正文备份：`backup/agent-0003-0004-pre-draft-replace-20261027/0003-mcp.before.html`、`0004-skill.before.html`；文字返工前草稿备份在 `backup/agent-0003-0004-mechanism-20261027/`。
  - `assets/skill-anatomy.svg` 图内「进系统提示」已改「进模型能看到的目录」；发布版 0003/0004 的同一句、图注、表头已同步。
- **✅ 0003-0006 已按 5.65 拆分出版**；0007 顺延完成。两张图（编排时序→0005／注入数据流→0006）渲染**待学习者目视**。
- **✅ 0001/0002 文字过（2026-10-28）**：删 goal/note 标签；去「撞墙」「三根柱子」比喻；0001 §7 重写为「计划是写出的文字，不是独立规划模块；错误先回上下文；harness 用提示词+工具/权限+存储把 Plan 模式固定成流程」；0002 的「翻车/撞了/一半」改直陈。
- **⚠ 0001/0002 仍超长**（各约 40 分钟+）：待 F5 后定压缩 vs 拆。
- **⚠ 0007 尚缺 1 图**（压缩 vs 交接时间线）＋Verification 展开成节＋四产品对照表降薄——5.54 §三遗留项。
- **⚠ 未提交**：Agent 轨 7 课＋两张新 SVG＋`internal/drafts/` 草稿＋备份＋glossary＋标准拆分＋目录重组＋RESOURCES＋存档 5.60～5.66——均在工作区。
- **写作标准 1.5 已补缺口**（2026-10-27）：场景可构造但要像真的、表格不用大表替代推理、列表前后有引导/收束、标题让读者预期下一步；**5.51 的 `English（中文）` 与「软件工作场景优先、不要生活比喻」仍未引入**，别把「只补缺口」误读成翻案。

## 下一步

1. **F5 验收 0001-0004 本轮文字改动（最优先）**：0003/0004 新稿读体感（20-30 分钟）、文章感、互链、速查页、图渲染；0001 §7「规划」与 0002 §9「真模型出错」重点读是否顺、还有没有别扭比喻。验收后 git 提交（建议 0001/0002 与 0003/0004 分笔）。
2. **0007 Harness 施工**：一轮一课，先读 [`internal/standards/tracks/agent.md`](internal/standards/tracks/agent.md)，改前备份；补 1 图（压缩 vs 交接时间线）＋Verification 展开成节＋四产品对照表降薄；体量压回 30 分钟内。⚠ 盲测须学习者同意才跑。
3. **0001/0002 超长**：F5 后定压缩 vs 拆；**体量预算（5000-7000 字＋6-8 题）要不要入 `tracks/agent.md`**；RAG 轨要不要纳入语言返工＋盲测。
4. **收尾**：`lessons/index.html` 速查区补不补三页（MCP 配置速查已落 `reference/`，目录页还没卡片）；「Agent 原理篇」旧轨道名 7 处课件＋5 处文档待拍板；GLOSSARY.md 是否约定到 `internal/`。

## 待确认

- 学习者每周可投入时间（还没收集）。
- 学员版留档的课程级观察：小测暂无「把判断用到自己业务场景」的题——全课程可能的演化方向，未动。
- 0003/0004 的草稿是否在 F5 后删除或归档（目前 `internal/drafts/` 留源稿；`reference/` 是正式速查页）。

> AI生成
