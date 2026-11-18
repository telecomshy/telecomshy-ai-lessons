# 下一会话交接

> 用途：把开发状态从当前会话交接到新会话，避免重读整段对话。只记状态与下一步，不复制课程内容。
> **每轮开发结束重写本文件**（不是追加）。长期欠账也写在这里，不再散在 `NOTES.md` 或标准里。

## 先读这些（按顺序）

1. `AGENTS.md`：会话规则（会话自动加载）。
2. 本文件：当前状态与下一步。
3. [`NOTES.md`](NOTES.md)：学习者画像与教学偏好。
4. [`internal/standards/PROCESS.md`](internal/standards/PROCESS.md)（开发流程与核验纪律）＋ [`internal/standards/COURSE-STANDARD.md`](internal/standards/COURSE-STANDARD.md)（页面结构、讲法、互链、交付检查单）＋ [`internal/standards/ARTICLE-STYLE.md`](internal/standards/ARTICLE-STYLE.md)（文章体，正文文字以此为准）＋ [`internal/standards/REVISION.md`](internal/standards/REVISION.md)（改课／精修流程）＋要动的那一轨 [`internal/standards/tracks/<轨道>.md`](internal/standards/tracks/)。
5. 回写约定：[`lessons-md/README.md`](lessons-md/README.md)。
6. 开工前跑 `pwsh tools/progress.ps1` 拿基线。

## 当前主线：全库精修（2026-11-17 更新）

37 门课、39 篇正文（agent 7＋rag 11＋llm 21，含两篇附录），逐篇按**文章体**重过，再回写 `lessons/` 的 HTML。这是当前唯一主线。

**精修的意思**：学习者手改 `lessons-md/` 的 md，或由 agent 按 `ARTICLE-STYLE.md` 重写 md；定稿后由主代回写 HTML。正文只改 md，不直接改 HTML。流程见 [`REVISION.md`](internal/standards/REVISION.md)。

- **已完成 0 篇**：新标准从 2026-11-17 起算，还没有哪篇按 `ARTICLE-STYLE.md` 定稿。
- **进行中**：`agent/0004`（Skill）。已按学习者指示把 round4 稿 `internal/drafts/0004-skill/round4/variant-deepseek-flash.md` 原样覆盖到 `lessons-md/agent/0004-skill.md`（SHA256 一致，24773 字节）。该稿尚未按 `lessons-md/README.md` 的标记约定整理（无文件头、meta 重复行、Q 标题未加粗），学习者手改时顺手对齐。**暂不回写 HTML**。
- **待精修 38 篇**：agent 7 · rag 11 · llm 21。
  - **`agent/0003`（MCP）明确算未精修**：文字稿已经比 HTML 新（md 219 行／6 题 vs HTML 178 行／5 题），说明有一版改稿尚未回写；按 `ARTICLE-STYLE.md` 整课重过后再回写，不因过去做过一轮而跳过。此时跑 `html2md --check` 会因文字稿领先报 FAIL，属正常待回写，不是数据损坏。
  - **`llm/0003`（KV Cache）同样算未精修**，与其他 llm 课一起排，不因旧的完成标记跳过。
  - `agent/0001` 在 2026-11-07 按旧文章体重写过（5.81），有底稿、改起来快，但仍算未精修。
- **主代不代写正文、不催进度**：学习者交回哪篇做哪篇。要主代先出初稿，他会点名；写作必须给 `ARTICLE-STYLE.md` 全文加一两段范文，不给禁令清单。

## 已拍板的口径

- **排版**：中英文之间统一有空格（0003 已落地）。
- **来源**：当场抓（`PROCESS.md` 第 1 节）。
- **小测**：按精修后的正文重出（5～10 题、选项等长、顺序打乱、✅ 位置均衡）。
- **backup 结构**：`backup/{agent,llm,rag}/<课文件名>.html`（2026-11-08 定，旧的按日期快照作废）。
- **不再有完成标记（2026-11-17 学习者定）**：目录页徽章、README 进度节、主页「门已定稿」计数全部移除；所有课一律按 `REVISION.md` 与交付检查单改，没有「定稿课受保护」这一档。

## 当前状态

- **课程总盘**：37 门、28 基础、9 进阶、26 脚本。
- **文档结构（2026-11-17 重整）**：`NOTES.md` 只留学习者偏好；流程纪律在 `internal/standards/PROCESS.md`；改课标准在 `internal/standards/REVISION.md`；操作手册从 `internal/rules/` 迁到 `internal/playbooks/`；历史索引从 NOTES 第 5 节迁到 `internal/history/INDEX.md`；过时的 Agent 重构蓝图归入 `internal/history/archive/`。
- **lessons-md**：40 个 md。0003 是旧标准回写稿，待按新标准重过；0004 已换成 round4 稿，学习者手改中；其余是镜像原状。
- **待核数字**：TeleAgent 的启用上限（50 还是 100）、导入包限制（1MB／300 文件）。三份草稿都写了 100，但没有独立核实。

## 下一步

1. **0004 手改中**：学习者改完 `lessons-md/agent/0004-skill.md`（round4 稿）后交回，备份 HTML、逐段回写、核验。
2. **agent/0003（MCP）按新标准重过**：2026-11-08 的旧回写稿可当底稿，整课按 `ARTICLE-STYLE.md` 重写，再回写。
3. **逐篇交稿**：学习者改哪篇做哪篇，按 `REVISION.md` 的单篇流程走。0001 有旧稿，也可点名先做。
4. **主线完成后再排**：速查区补卡（`agent-eval-checklist`、`context-budget`、`memory-products` 三页没进目录页底部速查区）、「Agent 原理篇」旧轨道名残留（9 处课件＋4 处文档）、全库出镜句轮（精修时顺手过）、各课 `note` 框按「只装两类」过一遍（没过的课在精修时顺手清）。

## 待确认

- 0004 round4 稿里的 `Q1` 等标题还没加粗成 `**Q1　…**`、文件头与元信息未按 md 约定整理——是让学习者手改时顺手对齐，还是回写前由主代统一补。
- `RESOURCES.md`「腾讯云广场」条目引用的 `backup/agent-track-20261026/` 快照已删，历史注记指向失效，清不清待定。
- 学习者每周可投入时间（影响精修节奏预估，还没收集）。

> AI生成
