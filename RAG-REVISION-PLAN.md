# RAG 系列课件全面修改计划（v4 定稿）

> 状态：**计划定稿；四项选型已确认；机制文件（COURSE-STANDARD / RESOURCES）已修订完成（2026-10-21 晚）。课程文件未动，待新会话按批次施工。**
> 背景：本计划产生于 RAG 课件全面修改的调研会话。同一时期另一会话正在重构 agent 轨课件，为避免共享文件冲突，本计划暂存于此独立文件。2026-10-21 晚经用户确认后已修 COURSE-STANDARD 与 RESOURCES 两份共享文件（agent 会话未触碰它们，无冲突）；课程文件与 NEXT-SESSION/NOTES/lessons 仍不动。
> 生命周期：开工后每轮会话更新本文§进度；全部完工后将本文件要点并入 NEXT-SESSION.md、资料并入 RESOURCES.md，并在 `docs/notes/history/` 建存档，之后本文件删除。

## 0. 已定决策（后续会话不得重启讨论）

1. **轨道定位**：RAG 课程目标是「用好 RAG＋知道背后的原理、取舍、技巧」，不是开发者的从零自建路线（v2 的"手写最小 RAG 系统"方案已撤回）。痛点主轴：**把文档丢进开源 RAG 工具很简单，难在丢进去之后——切片怎么配、效果好不好、坏了怎么调**。
2. **分层模式**：RAG 轨从「基础＋进阶」改为 **理论课＋实操课（工具）** 配对（对齐 agent 轨 0002 的实操课型）。三者职责：
   - 理论课（薄）：机制与取舍，数字只给结论级；受众＝初学者＋业务人员＋本人
   - 实操课（深）：装哪个、点哪里、怎么验通路、怎么不翻车；受众＝本人＋技术同事
   - deep（追问）：等学习记录里出现真问题再写（LLM 轨"只收真问题"纪律），从零重新积累
3. **实验台**：以 **RAGFlow** 为单一天然工具（不做产品横评；讲透所有 RAG 系统通用的参数与原理）。理论课每门带「回实验台」落点。
4. **厚度口径**：理论课 ≥220 行（LLM 基础课均值），实操课 ≥280 行（agent/0002≈317、0004≈289 对标），达标才收工。**三件套**：机制白话 → 工程数字（有出处的实测） → 翻车例子＋怎么救。
5. **贯穿例子**：沿用「年假制度文档」（现有 RAG 课的既有资产，且与 RAGAS 案例的员工手册场景同款，素材可直接复用）。
6. **四项选型（2026-10-21 用户确认）**：①机器满足 Docker Desktop 部署条件；②嵌入用 RAGFlow 内置模型起步，**课件里提一句：其他场景需自行配模型**；③0011 评测判官用 .env 既有的 DeepSeek；④RAGFlow 版本选官方现行文档线（v1.0.0-rc2 Go 后端；Windows 部署文基于 0.17.2 有出入的部分，施工时以官方为准校对）。

## 1. 调研结论（2026-10-21，样本见§7）

优秀课件公共大纲收敛为五层：①动机层（三短板→RAG 是什么→RAG/微调/长上下文三选一）②主干链路四组件（Ingestion→Retrieval→Augmentation→Generation，强调评估先行）③环节深修（切块/嵌入/混合检索/重排/查询工程/上下文组装）④质量环（分开评检索与生成、失败诊断、评估集建设、LLM-as-Judge）⑤演进层（Naive→Advanced→Agentic RAG）。

现状：全轨 7 文件 122~149 行，是全库最薄轨道（LLM 基础课均值约 220 行）。覆盖仅到「动机＋最小主干＋何时不用＋两类翻车」；**重排、查询工程、嵌入机制、上下文组装、Agentic RAG 完全缺失**；评测仅指标定义、无实验设计。

## 2. 新课表（12 门）

| 号 | 课 | 类型 | 来路 | 主线内容 | 回实验台落点 |
|---|---|---|---|---|---|
| 0001 | 为什么先查资料再回答 | 理论 | 原课加厚 | 三短板（知识截止/幻觉/私有数据）各配一个展开案例；RAG 一句话定义（开卷考试）；参数没动的事实 | —（无下游依赖，可先做） |
| 0002 | 一条 RAG 链长什么样 | 理论（地图课） | 原课终稿 | 六步每步：机制一句话＋手上数据长什么样＋在 RAGFlow 里对应哪块面板＋翻车预告＋挂专门课 | 全程「六步→面板」对照表 |
| 0003 | 该不该上 RAG：三选一 | 理论 | 原 0003 扩充 | RAG vs 微调（知识 vs 行为，链 llm/0009）vs 长上下文（成本＋lost-in-the-middle，链 0009）；保留原决策表 | — |
| 0004 | 上手 RAGFlow：从部署到第一问 | **实操·工具** | 新课 | Docker Desktop＋WSL2 部署（Windows 坑）→ 配 DeepSeek＋嵌入模型 → 建库传年假文档 → **检索测试**问第一句 | 本课即实验台落成 |
| 0005 | 建库：清洗与切块 | 理论 | 0002-deep 升格＋新内容 | 加载清洗三脏（页眉/表格换行/代码块）；三档切法＋重叠救什么；切块基准数字；RAGFlow 12 种解析模板怎么选 | 换模板/chunk 大小，看同一文档切块差异 |
| 0006 | 嵌入与相似度 | 理论 | 新课（0001-deep 失手清单收编） | 嵌入模型是另一个模型（区别于 llm/0001 词嵌入）；三算法（点积/余弦/欧氏）；失手清单（同名不同物/生僻词）；换模型＝全量重算 | 切换嵌入模型，亲眼看整库重建 |
| 0007 | 多路召回：混合检索与重排 | 理论 | 0001-deep 升格＋新内容 | 稀疏/稠密各自翻车；RRF（k=60）；cross-encoder 为什么准（独立编码 vs 拼接算）；召回宽精排窄（召回50→精排5）；阈值丢弃；Anthropic 数字链 5.7%→1.9% | 混合权重/开 rerank，检索测试对比 |
| 0008 | 查询工程 | 理论 | 新课 | 原话不是查询（"那价格呢"）；改写（补指代/保关键词/过度改写反例）；HyDE（适合/不适合/温度）；Step-back；子问题分解；路由与拒绝能力 | 同一意图换三种问法打检索测试（零成本实验） |
| 0009 | 上下文组装与生成 | 理论 | 新课（主讲权从 0002 移入） | Lost in the Middle；顺序策略；少而精与噪音；引用溯源；约束提示词（"未找到相关资料"）；温度；拒答 | top-k/阈值/引用面板；Empty response 设置 |
| 0010 | 翻车诊断与评估原理 | 理论 | 0004＋0004-deep 合并 | 两种翻车；先查检索再怪模型的排查顺序；分开评（检索四尺/忠实度）；LLM-as-Judge；三类评估集（单跳/多跳/否定题） | 打印提示词归因（0.17 API 会话/引用可见） |
| 0011 | 评测实战：切多大，好不好 | **实操·评测** | 新课 | 同一批文档建 2~3 个切块配置库；攒 20 题标注集（含否定题）；逐题跑标命中；进阶接 RAGAS（DeepSeek 当判官）；得出"这批文档该切多大"的结论模板 | 本课即评测落成 |
| 0012 | Agentic RAG：检索变成工具 | 理论 | 新课 | 固定流水线 vs agent 决策（查不查/查什么/再查不查）；Self-RAG 反思 token；CRAG 评估器三分支；迭代上限与延迟代价；链 agent/0002 | RAGFlow Agents 编排页 |

**不入正课**（维持 MISSION 边界）：GraphRAG、多模态 RAG、生产化部署三件（增量更新/权限/延迟预算）。RAGFlow 的 Knowledge Compilation（Wiki/Graph）可在 0012 顺带一句，不展开。

### 施工批次（每门一次会话）

- **批 1（地基＋工具）**：0001 加厚 → 0004 上手 → 0005 建库切块 → 0006 嵌入
- **批 2（用好）**：0007 混合重排 → 0008 查询工程 → 0009 上下文组装 → 0010 诊断评估原理
- **批 3（判好＋压轴）**：0011 评测实战 → 0012 Agentic → 0002 地图终稿 → 0003 三选一加厚

**前三课的处置**（用户确认过都要改，不弃任何一门）：0001 无下游依赖，提前到批 1 第一门，兼当新厚度口径的"试笔"；0002 是地图课，每步要挂新课链＋标面板，只能等全部下游课定稿后压轴重画（0002 过早加厚＝重做）；0003 的三选一要引用 0009 的 lost-in-the-middle 落点，批 3 收尾。

## 3. 连带改动清单（按施工顺序）

1. ~~**先修标准**~~ ✅ **2026-10-21 已完成**：COURSE-STANDARD 1.2 meta 行（RAG 并入理论｜实操）与动手零件（RAG 玩具脚本/实操分层）、1.4 RAG 改制条（三层分工）与 Agent 先例括号改写、1.5 数量关系去处（进阶版→深读层）、自查清单（进阶版→进阶版／RAG deep）五处修订完毕。
2. ~~**RESOURCES.md 并入§7 资料清单**~~ ✅ **2026-10-21 已完成**：索引表 rag 行拆为 12 门课各行；正文「RAG 系列」小节建组扩充（概念地图/实验台/评测实战/前沿论文/工程经验五组共 11 条）。§7 的"待抓"清单仍在本文件，各课施工时再抓。
3. **NOTES.md 4.1**：旧"RAG 骨架候选"段按新 12 门重写；销掉旧 deep 骨架候选条目。
4. **MISSION.md 边界句**：细化为"不做产品横评；以 RAGFlow 为单一天然实验台，讲通用参数"。
5. **三篇旧 deep 关停映射**（对应课上线同轮关停，双版本不共存）：0001-deep→0006/0007（失手清单进 0006，稀疏稠密进 0007）；0002-deep→0005；0004-deep→0010。
6. **统计口径**：progress.ps1 D/E 段补 RAG 覆盖（顺手清掉"RAG 门数不在任何脚本覆盖"的已知欠账）；理论课计入现行口径、实操课另定标记；`lessons/index.html` RAG 区、README 三处落点同步。
7. **0012 施工时重核 agent 互链**（agent 轨正被另一会话重构，file 名可能变化）；llm/0003→rag/0002、agent/0003→rag/0001 两处既有链无需动（文件号不变）。
8. **exercises 分置**：现有 7 个无模型玩具脚本继续挂理论课；实操课新增操作手册式材料（0004：部署验收清单；0011：标注集模板＋评测跑分脚本），形态施工时定，脚本不调 API 的原则维持（0011 若接 RAGAS 用 .env 的 DeepSeek，见§8-3）。

## 4. 旧文件处置一览

| 文件 | 处置 |
|---|---|
| 0001/0002/0003 基础页 | 保留按批加厚改写 |
| 0004 两翻车页 | 并入 0010（合并后旧文件号让位） |
| 0001-deep / 0002-deep / 0004-deep | 内容升格进 0006/0007、0005、0010 后各轮关停 |

## 5. RAGFlow 实验台关键事实（已核，写 0004/0005 直接用）

**部署**（官方 quickstart + Windows 实战文）：
- 硬件门槛：官方原文 "4 CPU cores (x86-64), 16 GB RAM, and 50 GB free disk space"；Docker ≥24.0.0、Compose ≥v2.26.1；`vm.max_map_count`≥262144（Docker Desktop 设在其 Linux VM 内）。
- 版本：官方 quickstart 当前教 **v1.0.0-rc2（Go 后端）**，docs 分 DEV/1.0.0-rc2；社区通行 **0.17.2 zip（Python 后端）**，2026-10 仍大量部署文。**选型见§8-4**。
- 架构：主服务＋四件底座（MySQL 元数据 / Redis 队列缓存 / MinIO 文件 / ES 全文＋向量）。单镜像编排，Docker Desktop 的 WSL2 可直接拉起。
- Windows 坑清单（0004"怎么不翻车"节素材）：①镜像拉取断→Docker registry mirror；②ES 反复重启→WSL2 内存不够（.wslconfig memory=12GB/processors=6/swap=4GB + `wsl --shutdown`，改完 ES 堆内存 2G）；③解析永久 pending→解析/嵌入模型没下载成功（HF_ENDPOINT 镜像端点，或先手动下模型再建库）；④挂载卷空/读不到→路径避开中文、空格、同步盘，正斜杠写法；⑤登录页打不开→宿主端口映射/防火墙（默认 80 冲突，改 9380 之类）。默认账号在 docker/.env（首登改密）。
- 模型配置：Chat＝DeepSeek（.env 既有）；嵌入见§8-2。生成模型配置三字段：API 地址（写到版本级）/Key/模型名必须与实际加载一致。

**切块**（官方 dataset configuration 页，写 0005 直接用）：
- 12 种内置解析模板：General / Q&A（每对一 chunk）/ Manual（按层级章节）/ Table（每行一 chunk）/ Paper / Book / Laws / Presentation（每页一 chunk）/ One（整篇一 chunk）/ Tag / Audio（ASR 转写）/ Email。选法官方原文："choose the parsing method based on the form of the material"，常规文档先 General、表格先 Table。
- 全局切块器参数：recommended chunk size 默认 **512 token**（目标值非硬限）；overlap ratio（%，0＝无重叠）；delimiter 后可加自定义；表格/图片可带上下文窗口（前后 N token）；**Use sub-chunks（父子检索：小块检索、父块供上下文）**。
- 标题切块器两模式：**Hierarchy**（保留完整标题路径"Part 1>Chapter 3>Section 2"，适合法规/合同/技术规范） vs **Group**（同层相邻小节合并，适合书/手册/报告，重连续性）。
- PDF 解析器：DeepDOC（默认，OCR＋表格结构＋版面）/ Naive（纯文本快）/ Docling / TCADP / MonkeyOCRv2 / 外接视觉模型（复杂版面更强但多花 token）。
- Extractor（切块后增强）：自动关键词、**自动问题**（预生成该 chunk 能答什么问题，索引 Questions 字段可让用户问题直接命中）、标签、**Augmented context（给每 chunk 生成上下文摘要——与 Anthropic Contextual Retrieval 同思想，理论课直接对照讲）**、自动元数据。
- Indexer：Embedding / Full-text / 双开（官方建议双开）；filename embedding weight；索引字段可选 Processed text/Questions/Augmented context。
- **嵌入锁定**：官方原文"Once you have selected an embedding model and used it to parse a file, you are no longer allowed to change it"（同一库必须在同一嵌入空间）——0006"换模型全重算"在工具里的刚性体现；换模型＝新建库＋全量重嵌。
- 其他：数据集级 PageRank 权重、Tag sets、Table 列角色（索引/元数据/both）、自定义 Ingestion Pipeline、Knowledge Compilation（Wiki/Navigation/Graph）。

**检索与生成**（写 0007/0009 用）：
- 检索测试面板（Retrieval testing）：不开对话、直接看某 query 召回哪些 chunk 及相似度——评检索的第一只眼；Chunk 页可人工加关键词/问题提权。
- Chat 的 Empty response：官方原文——填了则"confine answers to your datasets"（检索不到统一回这句话＝拒答）；留空则"improvise，may give rise to hallucinations"。0009 拒答的实验台落点。
- Windows 实战文的调参经验（行业经验值，标注出处）：中文文档 chunk token 300~500、overlap 50~100、top_k 8~12、相似度阈值 0.2~0.3；先开混合检索，机器差就把 rerank 缓一缓。
- 调参顺序法则（该文）：**先看解析结果对不对→再调切块→最后才动检索参数**；"检索参数影响找到什么，切块参数影响怎么被找到"。
- 干预能力：chunk 可视化＋人工增删关键词/问题/启用禁用。

## 6. 0011 评测实验蓝本（源自 RAGAS+RAGFlow 5 配置对比案例，快照全文在 .temp）

- **场景同款**：员工手册知识库（考勤休假/报销/福利/员工信息表）——与我们年假贯穿例几乎一致。
- **5 组配置**：baseline（top_n=8, threshold=0.2, temp=0.1）/ high_recall（top_n=15, thr=0.15）/ high_precision（top_n=5, thr=0.3）/ anti_hallucination（检索不变，prompt 强约束）/ contextual（top_n=12+CoT prompt）。
- **结果**：High Recall 三项最佳（Context Recall 1.0 / Answer Relevancy 0.597 / Faithfulness 0.477）；**High Precision 与 Anti-hallucination 的 Answer Relevancy 归零（全拒答）**；anti-hallucination 的 Faithfulness 仅 0.025（评估框架误判拒答）。
- **三个反直觉教训**：①参数非线性（threshold 0.2→0.35 直接失效）；②指标与业务目标要一致（"宁可不答不错答"场景下 Faithfulness 严重低估价值）；③过度约束 prompt 反噬。
- **测试集三挑战**：代表性>数量；LLM 生成初稿＋专家改写（"员工的年假政策是什么" vs "我2021年3月入职现在能休几天年假"）；GT 标注"够用即可"（含限定词，多答案显式写条件分支）；核心题全标＋边缘题轻量评。
- **Ragas 要点**：30+ 指标分检索/生成/端到端三类；完整模式（要 GT）vs 轻量模式（只要 q+a）；实践中 context_precision 与 answer_correctness 常返 NaN→重点看三个稳定指标 Context Recall / Answer Relevancy / Faithfulness。低分→优化方向对照表（recall 低→增 top_n/降阈值/改分块；precision 低→减 top_n/升阈值/开重排；faithfulness 低→prompt 约束/降温度）。
- Manual 模式分块（Document.add_chunk API、结构化文档按章节、跳过解析快 60%）——0011 若需精确控制 chunk 边界的备选路径。

## 7. 资料清单（RESOURCES.md 待并入；agent 会话结束后第一批施工会话操作）

**已有于 RESOURCES.md（直接引用）**：Lewis RAG 原论文（RAG 名字出处、换索引不重训）；Anthropic Contextual Retrieval（5.7%→3.7%→2.9%→1.9% 实测链）；Lost in the Middle；Pinecone Chunking Strategies；Anyscale RAG evaluation（分开评＋四尺定义）；RAGAS available metrics；RAG 评测 survey（各框架指标对照）。

**本轮新核（并入时用下列摘录）**：
- [RAGFlow 官方 quickstart]（https://ragflow.io/docs/）——硬件门槛原文、部署步骤、嵌入锁定原文、检索测试、Empty response 原文。用途：0004/0006/0009。
- [RAGFlow Dataset Configuration]（https://ragflow.io/docs/dataset_configuration）——12 模板清单、切块器参数、Extractor/Indexer 全量配置。用途：0002（面板对照）/0005。
- [Windows Docker Desktop 部署与避坑（0.17.2）] CSDN 168435333——五坑、.wslconfig、中文参数经验、调参顺序法则。用途：0004。⚠️版本口径待定（§8-4）。
- [RAGAS+RAGFlow 5 组配置评测实战] CSDN 153839845（2025-10）——§6 全部。用途：0011/0010。
- [Gao et al. — HyDE "Precise Zero-Shot Dense Retrieval without Relevance Labels"]（arXiv 2212.10496）——摘要关键句："HyDE first zero-shot instructs an instruction-following language model to generate a hypothetical document... an unsupervised contrastively learned encoder encodes the document into an embedding vector... the encoder's dense bottleneck filtering out the incorrect details"（假文档过编码器瓶颈滤掉错误细节）。用途：0008。
- [Asai et al. — Self-RAG]（arXiv 2310.11511）——关键句："indiscriminately retrieving and incorporating a fixed number of retrieved passages, regardless of whether retrieval is necessary, or passages are relevant, diminishes LM versatility"；"adaptively retrieves passages on-demand... using special tokens, called reflection tokens"。用途：0012。
- [Yan et al. — CRAG "Corrective Retrieval Augmented Generation"]（arXiv 2401.15884）——关键句："a lightweight retrieval evaluator... returning a confidence degree based on which different knowledge retrieval actions can be triggered"；web search 兜底；"decompose-then-recompose"。用途：0012。
- [Zheng et al. — Step-Back Prompting]（arXiv 2310.06117，ICLR 2024）——"enables LLMs to do abstractions to derive high-level concepts and first principles from instances containing specific details"。用途：0008。
- [RAG 前沿 12 种增强技术综述] CSDN 168187407——查询/索引/检索/重排/生成五环节方法归类；"基础 RAG＋混合检索＋重排＋干净切块解决 80% 问题"；HyDE 适用边界与温度；RRF 公式 k=60。用途：0007/0008（结构参考）。
- [RAG 系统化拆解：索引/检索/生成工程实践] CSDN 168161496——约束 prompt 模板（"未找到相关资料"）、召回50精排5、temperature 0.1~0.2、幻觉先归因检索、Recall@5/@10 排查法。用途：0007/0009/0010（经验素材，需与一手数字分开标注）。

**待抓**（写对应课时再抓，项目惯例）：RAGFlow retrieval_testing / chunk 管理官方页；Pinecone sparse-retrieval、refine-with-rerank（0007）；Lilian Weng RAG 长文新址（旧 lilianweng.github.io/posts/2024-07-07-rag/ 已 404）；Pinecone learn RAG 指南已在线读过（四组件＋agentic RAG 收尾），并入时按需再抓。

**快照**：`.temp/rag-research/`（01 评测案例 87KB / 02 Windows 部署 55KB / 03 管线实践 62KB / 04 增强技术 68KB）——中间产物，可随时清理不损失结论（精华均在上文§5~§7）。

## 8. 选型确认记录（2026-10-21 用户拍板，已升入§0 第 6 条）

机器条件可以；嵌入＝内置模型（课件提一句其他场景需自配）；评测判官＝DeepSeek；版本＝官方现行（1.0.0-rc2）。原四个待确认问题全部关闭，无遗留。

## 9. 进度记录

- [x] 2026-10-21 调研＋v1~v3 计划定稿（调研会话）
- [x] 2026-10-21 v4：实操课改 RAGFlow 工具型；0001 提前批 1；计划落盘；资料快照就位
- [x] 2026-10-21 晚：四项选型确认（§0-6）；COURSE-STANDARD 五处修建完成；RESOURCES 索引表＋「RAG 系列」小节并入完成
- [ ] 批 1 第一会话：NOTES 4.1 骨架段按新 12 门重写（⚠ 现与新政暂矛盾，第一件事必做）→ 0001 加厚（三件套试笔）
- [ ] 批 1：0004 上手 RAGFlow → 0005 → 0006
- [ ] 批 2：0007 → 0008 → 0009 → 0010
- [ ] 批 3：0011 → 0012 → 0002 地图终稿 → 0003 三选一
- [ ] 收尾：MISSION/index/README/progress.ps1 同步、旧 deep 关停、并入 NEXT-SESSION.md、建存档、本文件退役

## 10. 新会话开工指引（回答"下次怎么接上"）

新会话开工课程施工时，第一句直接说：**"读 RAG-REVISION-PLAN.md，按批 1 施工"**。本文件自包含施工所需全部上下文（已定决策§0、课表与批次§2、连带改动§3、资料去处§7、进度§9），新会话读完即可动手。注意事项：

1. **时机**：等 agent 轨会话收工后再开新会话。批 1 的 0001/0004 本身不依赖 agent 轨，但 NOTES/lessons/index 等共享文件不能两个会话同时写。
2. **开场**：新会话按 AGENTS.md 标准流程会先读 NEXT-SESSION.md——当前那份文件由 agent 轨会话维护，里面没有 RAG 计划指引，所以必须手动点名本文件。若 agent 会话收工后你顺手让它在 NEXT-SESSION.md 里写一句"下一步：读 RAG-REVISION-PLAN.md 按批 1 施工"，则今后新会话走标准流程即可自动接上；不写也不影响，手动点名即可。
3. **批 1 第一会话的具体活**：①重写 NOTES 4.1 骨架段（现在与新政矛盾）；②0001 加厚（三件套试笔，验收行数 ≥220）。机制文件已就位，无需再动 COURSE-STANDARD/RESOURCES。

## 变更履历

- v1（初表 11 门全理论）→ v2（＋2 门自建实操）→ **v3**（实操改 RAGFlow 工具型，回应"不自建、要会用"）→ **v4**（0001 提前至批 1，回应"前三课也要改"；批 3 定稿含 0002/0003 压轴的依赖理由）。厚度口径、三层职责、三件套自 v3 起固定。
- 2026-10-21 晚（机制会话）：四项选型落定进 §0-6；COURSE-STANDARD 五处、RESOURCES 索引表＋RAG 小节五组修订完成（§3-1/§3-2 勾销）；新增 §10 新会话开工指引。课程文件未动。

> AI生成
