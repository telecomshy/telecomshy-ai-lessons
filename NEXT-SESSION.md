# 下一会话交接

> 用途：把开发状态从当前会话交接到新会话，避免重读整段对话。只记状态与下一步，不复制课程内容。
> **每轮开发结束重写本文件**（不是追加）；与 `NOTES.md` 第 4 节的分工见 `AGENTS.md`「文件职责」。

## 先读这些（按顺序）

1. `AGENTS.md`：会话规则（会话自动加载，不用手动提醒）。
2. 本文件：当前状态与下一步。
3. [`NOTES.md`](NOTES.md) 第 1 节（流程纪律）＋ [`internal/standards/COURSE-STANDARD.md`](internal/standards/COURSE-STANDARD.md)（全局写作标准）＋**本轮要动的那一轨 [`internal/standards/tracks/<轨道>.md`](internal/standards/tracks/)**。
4. 按下一步的事按需读：[`5.54`](internal/history/5.54-agent-model-and-0001-rework.md)（**Agent 篇 0002→0005 施工图在其 §三**）／[`5.59`](internal/history/5.59-agent-0001-dualblind-rework.md)（盲测法原始提案）／[`5.60`](internal/history/5.60-track-standard-split.md)（**标准两层化拆分＋盲测约束＋0002 文章体过**）／[`5.61`](internal/history/5.61-directory-reorg.md)（**目录重组：对内 internal/、对外 docs/——勿把内部资料放回 docs/**）／[`5.57`](internal/history/5.57-llm-track-language-rework.md)（编辑工具教训全集）。
5. 开工前跑 `pwsh tools/progress.ps1` 拿基线。

## 当前状态

- **课程总盘**：31 门 / 19 基础 / 12 进阶 / 21 脚本；存档 61 篇；audit 全绿。
- **✅ 目录重组完成（存档 5.61，2026-10-25）**：对内/对外语义分层。结构：三轨标准改名移入 `internal/standards/tracks/{agent,llm,rag}.md`＋`internal/standards/COURSE-STANDARD.md`；docs/ 四子树（history 60＋rules 4＋learning-records 5＋agents 3）整体平移 `internal/`；`docs/` 腾空为对外读者区（README.md 占位）；ADR 懒创建约定改 `internal/adr/`；lessons/ 从此只含课件 HTML（正文零改动，未碰任何 completed 课）。工作量：76 文件移动＋13 文件 40+ 处引用同步＋2 新建；改前备份 `backup/structure-reorg-20261025/`（11 件，已 gitignore）。验收（以实跑为准）：progress.ps1 两轮全绿；audit 子代理独立核验通过（结构 9/9；与 git HEAD 逐字对账 68/70 哈希一致，5 篇改动均为路径同步，5.59/5.60/5.61 属新文件无基线）；audit 查出 6 处「链接深度未重算」死链（NOTES:37、COURSE-STANDARD:3、internal/rules 三件）＋NEXT-SESSION 旧链接 5 处，均已当轮补修并复扫归零。⚠ audit 同时指出 progress C 段只核 lessons 课卡链接，**根目录 md 与 internal 子树的 markdown 链接是盲区**。
- **✅ 写作标准两层化（存档 5.60，2026-10-24）**：全局 `internal/standards/COURSE-STANDARD.md` 只留共用规矩＋deep 体例（措辞统一「薄层课/deep」）；**分版/课型标识/受众/脚本分层/编号特例下放三轨 `internal/standards/tracks/<轨道>.md`**（行数以 audit 实跑为准，F 段第 (5) 项盯存在与体量）。同轮：语言洗练四条并入文章体「句子层」；盲测质检入 1.5（只委派一个学生子代理、定位自学教材非讲稿、**须学习者同意或主动才跑**）；拆分后审计子代理独立复核（通过 4/5，11 条问题已修 9 条、2 条审计自评可不改项未动，见 5.60 §五）。
- **✅ `agent/0002` 文章体过完成（4 处手术）**：goal 删垫词、§3/§4 补因果承接；核验全绿（b 74/74、code 104/104、quiz 5×1、链接锚点 miss=0、双 audit 绿）。施工图内「拟补长任务体感」无学习者拍板记录，**已移除**。*改前备份 `backup/agent-track-20261024/`。*
- **✅ `agent/0001` 自学向返工完成（存档 5.59）**：18 处手术＋术语表 API 词条；**待学习者 F5 验收**。
- **⚠ 未提交**：`agent/0001`＋`reference/glossary.html`＋`agent/0002`＋标准拆分六文件＋三轨标准＋存档 5.60**＋本轮目录重组（76 移动＋13 同步＋docs/README＋存档 5.61＋本文件重写）**——均在工作区；git 提交时移动会被识别为 rename，历史不断。三备份目录已 gitignore。
- **Agent 篇**：0001 三轮全过（内容/语言/自学向）；0002 文章体过完成；0003→0005 施工图在 5.54 §三待开工。

## 下一步

1. **学习者 F5 验收**：`agent/0002`（§3/§4 承接句）与 0001（已验收两轮）**＋目录重组目视核对**（lessons/ 只剩 HTML、docs/ 只剩一个 README、internal/ 五子树齐全）——验收后 git 提交（0001 语言+盲测、0002 文章体、标准拆分、目录重组，建议按机制分笔，粒度待学习者定）。
2. **开工 Agent 篇 0003→0005**（一轮一课，先读 [`internal/standards/tracks/agent.md`](internal/standards/tracks/agent.md)，改前备份 `backup/agent-track-YYYYMMDD/`）：施工图 5.54 §三——0003 广场截图降薄／0004 补 2 图＋拓扑谱系＋OWASP＋回链 0001 workflow 节／0005 补 1 图＋Verification 展开＋对照表降薄。⚠ 盲测质检须**学习者同意或主动提出**才跑（1.5 盲测规矩）。
3. RAG 轨四门要不要纳入语言返工＋盲测（学习者拍板）。
   ✔ 原第 4 条（补审计盲区）已于 2026-10-25 完成（progress G 段），见当前状态「审计盲区已补」。

## 待确认

- `lessons/index.html` 速查区补不补三页（原定 0005 轮一并定，尚未定）。
- 「Agent 原理篇」旧轨道名 9 处课件＋4 处文档——内容层改名，待拍板。⚠ 0008 系 footer「AI Agent 原理与工程」同批。
- RAG 轨是否纳入语言返工。
- 学习者每周可投入时间（还没收集）。
- 学员版留档的课程级观察：小测暂无「把判断用到自己业务场景」的题——全课程可能的演化方向，未动。
- **GLOSSARY.md（仓库开发术语表，懒创建约定在根目录）**：语义上属对内，是否也约定到 `internal/`？本次未动（AGENTS.md:50 仍写根目录），待拍板。

> AI生成