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

- **课程总盘**：35 门 / 26 基础 / 9 进阶 / 24 脚本；19 门已标 completed；audit 全绿（2026-11-05 收工实跑）。
- **✅ 提交史**：`afbec6d` 0007 Harness · `fb12d31` 全库文字返工 · `a6934d7` RAG 0001 · `769dd46` 地图 v5 · `57ce45e` 0004 · `a17f838` 0005 · `13e9934` 0006 · `1e5a7c9` 0004/0005 文字返工 · `653cb01` 0007 查询工程＋0008 上下文组装 · `git log -1` 会话六（0009）。
- **✅ RAG 批 2 第四会话（2026-11-05，本会话）**：
  - **0009「翻车诊断与评估：先分清哪一段坏了」开课**（`lessons/rag/0009-two-failure-modes.html`，291 行）：该来的没来 / 来了但没用上 → 打印提示词诊断 → 分开评 → 检索四尺（Recall/Precision/Hit rate/MRR）→ 忠实度与相关性 → LLM-as-Judge（位置/啰嗦/自我增强偏差＋校准四条）→ 单跳/多跳/否定三类评估集 → 六步最小流程。小测 6 题。
  - 新插图 `assets/rag-diagnosis.svg`（诊断分叉图，XML 校验＋无头 Chrome 实渲＋页内看过）＋沿用两个脚本 `0009-two-failure-modes.py`、`0009-rag-eval.py`（本地跑通，课内 `<pre>` 逐行对账）；术语表补「RAG 评测 / Recall@k / 忠实度 / LLM-as-Judge」。
  - **旧 0009-deep 关停**（内容全部收进 0009 后删除；RAG 轨从此无 deep），目录页 RAG 进阶版区块、README 0009 进阶行同步移除；统计 35/26/9/24。
  - 一手来源抓入 RESOURCES：Anyscale RAG evaluation（分开评/四尺/忠实度/相关性/判官偏差）、RAGAS Faithfulness 与 Context Recall（公式与 1/2 例子）、RAGAS Testset Generation（单跳/多跳）、Zheng et al. 2023（LLM 判官 >80% agreement＋三类偏差）。索引表 `rag/0009` 行同步。
  - **顺手修两个旧问题**：`0009-rag-eval.py` 打印「8 个问题」但标注集实际 10 条（改 10）；旧 deep 里「忠实度 90% 以上 / 低于 70% 不能上线」无出处，已改成「内部红线自己定」。
- **✅ 0004/0005 文字返工完成（2026-11-04）**：两课按 1.5 文章体＋句子层四条整课重写；`<pre>`/表格/图注与改前逐字节一致（git 对照）、摘录对账过、小测 6/6 与答案位置未动；破折号两课归零、垫词与临时比喻清零（存档 5.71）。
- **⚠ 图待目视**：`closed-vs-open-book.svg`（0001）、`chunk-three-cuts.svg`（0004）、`similarity-three-rulers.svg`（0005）、`retrieval-wide-then-narrow.svg`（0006）四张仍未看；`query-engineering.svg`（0007）、`context-assembly.svg`（0008）、`rag-diagnosis.svg`（0009）本会话已实渲＋页内看过，F5 再扫一眼即可。

## 下一步

1. **F5 验收（最优先）**：① 0009 全文通读＋小测点一遍；② 0008 → 0009 连着读，检查「组装侧修法 → 诊断评估」的接口句是否顺；③ 0004/0005 返工后的文字通读（对照 0006～0009 的手感）；④ 七张 SVG 的页内目视（后三张已过，前四张仍未看）。
2. **RAG 批 3 第一会话：0010 评测方法**（攒一套 20 题左右标注集、建 2～3 个切块/检索配置、逐题跑、LLM-as-Judge 只讲方法；把 0009 的尺子落成一次可复现实验）。
3. **RAG 批 3 余下**：0011 Agentic RAG → 0002 地图终稿 → 0003 三选一加厚。
4. **拍板一笔欠账**：LLM 0005/0006/0008 脚本输出摘录三处「同款」要不要连脚本一起改。
5. **Agent 轨 0001/0002 超长**＋体量预算、速查区补卡、「Agent 原理篇」旧轨道名残留：仍待拍板。

## 待确认

- 学习者每周可投入时间（还没收集，影响 RAG 批次排期）。
- `internal/drafts/` 里两份 0001 实验稿＋一份 0008 语言改稿是否长期保留（均未提交）。
- RAG 改版收尾（计划 §9 末项）：MISSION 边界句、`progress.ps1` D/E 段补 RAG 覆盖、并入本文件、建存档、计划文件退役。

> AI生成
