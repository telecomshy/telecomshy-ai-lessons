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

- **课程总盘**：33 门 / 22 基础 / 11 进阶 / 21 脚本（0004 新增＋0002-deep 关停，一加一减总数不变）；19 门已标 completed；audit 全绿（2026-11-03 实跑，收工前会再跑）。
- **✅ 2026-11-02/03 四笔提交**：`afbec6d` 0007 Harness 施工；`fb12d31` 全库文字返工；`a6934d7` RAG 批 1 第一会话（0001 加厚 223 行）；`769dd46` RAG 地图 v5（删工具操作课、评测去工具化、编号前移、旧 0004 重排 0009 占位）。
- **✅ RAG 批 1 第二会话（2026-11-03，本会话）**：
  - **0004「建库：清洗与切块」开课**（`lessons/rag/0004-cleaning-and-chunking.html`，222 行）：清洗三脏→三档切法→尺寸基准→重叠两面→父子块；新插图 `assets/chunk-three-cuts.svg`（答案三切命运）；小测 6 题 6 标记；`0002-chunking.py`→`0004-chunking.py` 随课改名，两块摘录与实跑逐行对账。
  - **首个 deep 关停**：0002-deep（切块到底切多大）内容升格进 0004 后删除，互链 2 处/目录卡/README/统计（22+11，总数 33 不变）同步。
  - **一手资料复抓抓出四处置换**（rc2→rc3、嵌入锁定→兼容性抽查口径、Tag→Picture、Augmented context→Summary），RESOURCES＋计划 §5 已同改——**0005 嵌入课要用新口径写**。存档 **5.69**。
- **⚠ 两张新图渲染未目视**：`closed-vs-open-book.svg`（0001）＋`chunk-three-cuts.svg`（0004），XML 合法已过，按 1.7 还差浏览器渲染看一眼。

## 下一步

1. **F5 验收（四批叠着）**：① `rag/0004` 新课＋`chunk-three-cuts.svg` 渲染目视；② 0001 加厚稿＋其插图渲染目视；③ v5 重排抽查（`lessons/rag/0009-two-failure-modes*`）；④ 更早的 0007 施工＋文字返工两笔仍未细看。
2. **RAG 批 1 第三会话**：读 `RAG-REVISION-PLAN.md` 按批 1 施工——**0005 嵌入与相似度**（0001-deep 失手清单收编，**同轮关停 0001-deep**；嵌入约束按 5.69 的新口径写）。之后批 2：0006→0007→0008→0009。
3. **拍板一笔欠账**：LLM 0005/0006/0008 脚本输出摘录三处「同款」要不要连脚本一起改（改脚本→重跑→同步 `<pre>`）。
4. **Agent 轨 0001/0002 超长**：待 F5 后定压缩 vs 拆；体量预算要不要入 `tracks/agent.md` 未拍板。
5. **收尾杂项**：`lessons/index.html` 速查区补不补卡；「Agent 原理篇」旧轨道名残留待拍板。

## 待确认

- 学习者每周可投入时间（还没收集，影响 RAG 批次排期）。
- 0003/0004 草稿 `internal/drafts/` 是否归档（上轮遗留）。
- RAG 改版收尾（计划 §9 末项）：MISSION 边界句、`progress.ps1` D/E 段补 RAG 覆盖、旧 deep 关停收尾（还剩 0001-deep、0004-deep→随 0009 收编）、计划文件退役。

> AI生成
