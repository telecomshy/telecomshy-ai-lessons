# 课程目录

> 这是 `lessons/index.html` 的文字稿：**直接在上面改，改完交回，我逐段映射回 HTML 并跑核验**。
> 改法与标记约定见 [README](README.md)：✅ 标正确选项、「答对时/答错时」是小测反馈、【图】【选读框】等标记说明、小节可增删合并（节号乱了没关系，回写时重排）。

---

【meta】目录 / Index

目录 / Index

一个 mission，四条轨道。各轨独立编号，可以分开翻。

【选读框｜怎么读这个目录】

这个仓库只有**一个目标**：搞懂 AI Agent 的原理与工程。但课程分成四条轨道——

**LLM 底层**只讲"影响 agent 成本 / 延迟 / 设计"的机制，以及能力和失效的来源；**Agent 篇**直接服务这个目标（**理论**讲是什么、为什么，**实操**动手做出来、拆真实的壳）；**RAG**讲"怎么让模型用上手边没有的信息"，只讲机制与取舍。

四条轨道**各自从 0001 编号**，所以提课号时要说清轨道，例如「LLM 底层第 3 课」。轨道之间用超链接互相打通。

课程是**AI 先生成、我再逐课修改**的，进度分三档：标题后带 （completed） 的是**已经改过一遍**的；普通卡片是**还在改**；虚线卡片标着「下一步开」的**还没写**。带标记的课可以直接照着读。

## LLM 底层

只讲影响 agent 成本 / 延迟 / 设计的机制，**以及能力与失效的来源**。教材放在 `lessons/llm/`。**基础课给初学者和业务人员，进阶版给技术读者。**

**基础课** —— 给初学者和业务人员。给结论和直觉，**不给推导和算式**。

【三柱框】

**[0000 · 模型是怎么学出来的](../lessons/llm/0000-how-models-learn.html)（completed）**

**先导课，先读这个**：大模型作为程序为什么多一个训练阶段，那些数字是哪来的、怎么被调的，以及为什么它天生只会「接下一个字」。

动手：`exercises/llm/0000-how-models-learn.py`

**[0001 · 从「token」到「下一个 token」](../lessons/llm/0001-from-token-to-next-token.html)（completed）**

**基石课**：文字 → token → 向量 → 注意力 → FFN → 采样，看懂全貌。

动手：`exercises/llm/0001-tiny-attention.py` · `exercises/llm/0001-sampling-params.py`

**[0002 · 一次请求的两段：prefill 与 decode](../lessons/llm/0002-prefill-vs-decode.html)（completed）**

为什么「读长文」快、「写长文」慢，还把**一次请求 / 一轮 / 层**三个词分清。

动手：`exercises/llm/0002-prefill-vs-decode.py`

**[0003 · KV Cache 与「缓存命中」是两回事](../lessons/llm/0003-kv-cache-and-prompt-caching.html)（completed）**

请求内算过的别重算，跨请求接着用。本课实测：**只改开头一处，成本差 3.7 倍**。

动手：`exercises/llm/0003-cache-hit-simulator.py`

**[0004 · 一趟装满的卡车](../lessons/llm/0004-batching.html)（completed）**

排队 ＋ 拼车：一张卡怎么同时服务几百个人。用一点点延迟，换几十倍吞吐。

动手：`exercises/llm/0004-batching.py`

**[0005 · 它真的在思考吗？](../lessons/llm/0005-reasoning-models.html)（completed）**

屏幕上那段「思考」，是真在想还是演给你看？**它确实在打草稿**——但草稿不是它的想法，还按字收钱。

动手：`exercises/llm/0005-reasoning-cost.py`

**[0006 · 量化：把模型压小，把字吐快](../lessons/llm/0006-quantization.html)（completed）**

压小 = 吐字快，**但读长文一点不快**。附实测：同一台机器，只改存法。

动手：`exercises/llm/0006-quantization.py`

**[0007 · 蒸馏：小模型的本事从哪来](../lessons/llm/0007-distillation.html)（completed）**

教小模型时**你给它什么**，它就只能学到什么。附实测：只搬答案是最差的一档。

动手：`exercises/llm/0007-distillation.py`

**[0008 · 这件事到底是谁干的](../lessons/llm/0008-who-does-what.html)（completed）**

四层归属表：**哪些本事是引擎给的，不是模型的**。附四条 agent 侧的坑。

动手：`exercises/llm/0008-who-does-what.py`

**[0009 · 后训练的几种练法](../lessons/llm/0009-post-training-recipes.html)（completed）**

SFT、RLHF、DPO、GRPO 是**同一条循环换扣分单**。附「微调为什么常常不灵」的正解。

动手：`exercises/llm/0009-post-training-recipes.py`

**进阶版** —— 给想动手验算的技术读者。装的是**基础课没讲的那部分理由**，不是加强版；按需跳读，读基础课遇到括号链接就能直达。

【三柱框】

**[0001 进阶 · 十一个追问](../lessons/llm/0001-from-token-to-next-token-deep.html)（completed）**

初学版讲「是什么」，这篇答「为什么 / 还有什么坑」。

**[0002 进阶 · 里面到底在转什么](../lessons/llm/0002-prefill-vs-decode-deep.html)（completed）**

初学版讲「是什么」，这篇答「里面具体在转什么」。

**[0003 进阶 · 三个绕人的细节](../lessons/llm/0003-kv-cache-and-prompt-caching-deep.html)（completed）**

初学版讲「两回事」，这篇答「具体到多轮、到工具、到断点，又是怎样」。

**[0004 进阶 · 批从哪来、拐点、工业界的招](../lessons/llm/0004-batching-deep.html)（completed）**

初学版讲「怎么排队、怎么拼车」，这篇答「批从哪儿来、什么时候到头、工业界怎么绕过去」。

**[0005 进阶 · 谁写的、怎么切的、谁收着、怎么练出来的](../lessons/llm/0005-reasoning-models-deep.html)（completed）**

初学版讲「那段思考是什么、值不值」，这篇答「那段字谁写的、边界谁切的、签名收着什么、它怎么练出来的」。

**[0006 进阶 · 压法是什么、误差怎么救回来、KV 是什么精度](../lessons/llm/0006-quantization-deep.html)（completed）**

初学版讲「量化是什么、会掉什么」，这篇答「压法是什么、4 bit 为什么还能用、int4 的模型 KV 存多少位」。

**[0007 进阶 · 抄什么、扣什么、怎么练](../lessons/llm/0007-distillation-deep.html)（completed）**

初学版讲「小模型的本事从哪来」，这篇答「三种抄法差在哪、扣分扣的是什么、学生自己写老师逐字批在做什么、这笔账划不划算、工具调用能不能蒸」。

**[0008 进阶 · 在哪配、怎么验、代价是什么](../lessons/llm/0008-who-does-what-deep.html)（completed）**

初学版讲「结构化输出保证格式」，这篇答「为什么偶尔还是失败、在哪配怎么验真开着、代价有哪些、两招能同时开吗、为什么分四层不分成两块」。

**[0009 进阶 · 七问：差在哪、谁在打分、算法在拧什么、窄领域会不会练坏、练完改得动什么](../lessons/llm/0009-post-training-recipes-deep.html)（completed）**

初学版讲「同一条循环换扣分单」，这篇答「预训练和后训练差在哪、后训练又动了多少权重、奖励模型打错了会怎样、PPO/GRPO 在拧什么、不先做 SFT 直接上 RL 行不行、什么时候用 DPO 什么时候还得 RLHF、窄领域猛练会不会把别处的本事练坏、一轮练完改得动什么」。

**附录** —— 不占课号，是某门课的延伸。**不属于正式课程内容**，但卡住时最值得回来对一遍。

【三柱框】

**[附录 · 训练背后的那点数学](../lessons/llm/appendix-training-math.html)**

第 0 课「算扣分、拧一点点」那一格的**数学展开**：损失、斜率、反向传播，**扣几分不直接决定拧多少**。

动手：`exercises/llm/appendix-training-math.py`

**[附录 · 微调项目怎么不翻车](../lessons/llm/appendix-tuning-projects.html)**

需求到手先切**「怎么答」和「答什么」**：决策单＋内测五步排查＋「什么时候不要微调」。

## Agent 篇

**理论**讲是什么、为什么，**实操**动手做出来、拆真实的壳（每课标着课型）。教材放在 `lessons/agent/`。

【三柱框】

**[0001 · Agent 是什么：循环、工具、记忆](../lessons/agent/0001-what-is-an-agent.html)**

分清**「用 AI」和「用 agent」**，以及中间那一档 workflow；循环怎么转、什么时候停；工具从哪来；记忆为什么没有标准做法。**本课只讲原理，动手在下一课。**

**[0002 · 手写一个 agent](../lessons/agent/0002-build-an-agent.html)**

从**装 Python 包、配 API key** 开始，用**真模型**跑通循环；亲手撞一次护栏。核心代码就是一个循环。

`exercises/agent/0002-build-an-agent.py`

**[0003 · MCP：给工具定一个统一插口](../lessons/agent/0003-mcp.html)**

工具写不完的那堵墙怎么破：**MCP** 统一「怎么接」（像 USB-C）。三个角色、一次「发现 → 调用」、本地/远程配置与排错、**什么时候不该用 MCP**。

**[0004 · Skill：把做法打包成文件](../lessons/agent/0004-skill.html)**

「做法教不会」怎么破：**Skill** 统一「怎么做」（像菜谱）。目录结构、渐进式加载、TeleAgent 创建技能跟做、**MCP 还是 Skill 怎么选**。

**[0005 · 多 agent 协作：什么时候叫帮手、怎么分工](../lessons/agent/0005-multi-agent.html)**

什么时候该上多 agent、几种连法（拓扑谱系）；**编排者-工作者、派单四件、只回结论**；**审计为什么适合派子代理**，TeleAgent 自动委派 vs OpenCode `@` 点名；这笔 token 账。

**[0006 · 提示词注入与护栏：怎么不出事](../lessons/agent/0006-injection-and-guardrails.html)**

**纸条攻击**（直接/间接注入）怎么发生、为什么没有根治；**三个「少」：少信、少能、有人管**；对着 **OWASP 风险榜**检查自己漏了哪层。

**[0007 · Harness：Agent = Model + Harness](../lessons/agent/0007-harness.html)**

**公式＋五个子系统＋长任务交接**；TeleAgent / OpenCode / Hermes / WorkBuddy 四款对照，按场景选而不是按功能数量选。

## RAG

只讲**机制与取舍**：为什么要检索、一条链六步各在干什么、该不该上、三条路怎么选。**不讲向量库选型 / 产品对比**（会烂，也超出这份教程的使命）。教材放在 `lessons/rag/`。

**基础课** —— 给初学者和业务人员。给结论和直觉，**不给推导和算式**。

【三柱框】

**[0001 · 为什么得「先查资料再回答」](../lessons/rag/0001-why-retrieval.html)**

模型不知道你的数据，是因为**信息不在它手边**，不是因为它笨。RAG ＝ 先替它翻书。

动手：`exercises/rag/0001-why-retrieval.py`

**[0002 · 一条 RAG 链长什么样](../lessons/rag/0002-rag-pipeline.html)**

切块 → 变向量 → 存 → 查 → 组装 → 生成。**前五步由代码调度，只有最后一步是答题模型**；第④步还分固定查一次和 agent 循环。

动手：`exercises/rag/0002-rag-pipeline.py`

**[0003 · 该不该上 RAG：三条路怎么选](../lessons/rag/0003-when-not-to-use-rag.html)**

RAG 和长上下文都在补「资料不在手边」，**一个建库查、一个整份塞**；微调改的是「怎么答」。按四问选路线。

动手：`exercises/rag/0003-when-not-to-use-rag.py`

**[0004 · 建库：清洗与切块](../lessons/rag/0004-cleaning-and-chunking.html)**

文档进库前做两件事：**洗成干净的文字，切成「答案装得下」的块**。尺寸有基准，重叠未必有用。

动手：`exercises/rag/0004-chunking.py`

**[0005 · 嵌入与相似度](../lessons/rag/0005-embedding-and-similarity.html)**

文字变向量之后靠什么排名次？**三把尺子量的不是同一件事，尺子跟模型走**。嵌入只懂「像」，不懂「对」。

动手：`exercises/rag/0005-similarity-metrics.py`

**[0006 · 多路召回：混合检索与重排](../lessons/rag/0006-hybrid-and-rerank.html)**

两种检索翻车的位置不同，**各排一个榜用名次合成，再逐段精挑**。全程没换模型。

动手：`exercises/rag/0006-sparse-vs-dense.py`

**[0007 · 查询工程：原话不是查询](../lessons/rag/0007-query-engineering.html)**

用户说「那还能休几天」，检索器不知道「那」指什么。**补全、拆开、升高、换形态**，把原话变成能查的查询。

动手：`exercises/rag/0007-query-engineering.py`

**[0008 · 上下文组装与生成](../lessons/rag/0008-context-assembly.html)**

资料检索到了，模型未必用得上。**放几段、怎么排、怎么约束、没有答案怎么说**，决定这一屏能不能答对。

动手：`exercises/rag/0008-context-assembly.py`

**[0009 · 翻车诊断与评估](../lessons/rag/0009-two-failure-modes.html)**

**该来的没来** vs **来了但没用上**——先看提示词分清哪类；再看四个检索数和忠实度，量出改动有没有变好。

动手：`exercises/rag/0009-two-failure-modes.py` · `0009-rag-eval.py`

**[0010 · 评测方法：切多大，好不好](../lessons/rag/0010-eval-methods.html)**

「切多大」没有通用答案。**同一套题、三个切块配置、只动一个变量**，三张成绩单的差距就是答案。

动手：`exercises/rag/0010-eval-configs.py`

**[0011 · Agentic RAG：检索变成工具](../lessons/rag/0011-agentic-rag.html)**

固定流水线假设一次检索就够。**查不查、查什么、够不够、再查不查**——把检索放进循环，再用预算和停止条件管住它。

动手：`exercises/rag/0011-agentic-rag.py`

## 速查 / Reference

课会很少回看，速查会。放在 `reference/`。

【三柱框】

**[术语表](../reference/glossary.html)**

全课程统一用词。课里出现的词，回来这里对一遍。

**[KV Cache 与「缓存命中」速查](../reference/prompt-caching.html)**

LLM 底层第 3 课的压缩版，方便随时回看。

**[图 · 一次请求，从头到尾](../reference/one-request-end-to-end.html)**

prefill ＋ decode 全过程的**可点逐步版**——看货架（KV cache）怎么一点点变满。

**[采样参数速查](../reference/sampling-params.html)**

temperature / top_p / top_k / seed：**怎么设、什么时候别设**。配模型的时候照着抄。

**[权威架构图 · 对照](../reference/canonical-diagrams.html)**

英文资料里那几张图认得出是哪一块。**当对照，不当教材**；附中英认词表。

## 提问框

**不知道从哪开始？**从 [LLM 底层 · 第 0 课](../lessons/llm/0000-how-models-learn.html)（先导）读起，再顺着 [第 1 课](../lessons/llm/0001-from-token-to-next-token.html)（基石）往下；看完想动手做自己的 agent，就转 [Agent 原理篇 · 第 1 课](../lessons/agent/0001-what-is-an-agent.html)。随时问我"下一课学什么"。
