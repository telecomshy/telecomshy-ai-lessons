# AI Agent 资源

本课程的知识只能来自这里的来源，不能来自我的记忆。每条都注明"用来干什么"。

## 从课找来源（写课前先查这张表）

> 正文按来源逐条罗列；这张表只放**指针**——写哪门课，先来这里定位优先来源，再读正文对应条目。新来源进正文对应分组，不复制进本表。

| 要写／改的课 | 优先来源（按正文条目名定位） |
|---|---|
| `agent/0001`（是什么·循环·workflow 谱系·三柱·记忆） | Knowledge 通用段（Anthropic Building effective agents · Dify Workflow · Lilian Weng 三支柱 · Anthropic context engineering · ReAct）＋「记忆」小节 |
| `agent/0002`（实操·真模型接入） | 「Agent 篇 0002 实操」小节（全部当场抓）＋ OpenAI Function calling · Anthropic advanced tool use |
| `agent/0003`（MCP 与 Skill） | MCP 系条目（MCP 官方文档 · 腾讯云 · 阿里云百炼 · ModelScope · npx · Anthropic Agent Skills）＋「TeleAgent 案例」小节的操作手册 |
| `agent/0004`（多 agent 与安全） | Anthropic Building effective agents · multi-agent research system · Orchestrator-workers · OpenAI 实践指南 · TeleAgent 操作手册（任务委派） |
| `agent/0005`（Harness） | 「TeleAgent 案例」小节（TeleAgent／OpenCode／Hermes／WorkBuddy 四款）＋ harness 系（Fowler · LangChain · Databricks · Learn Harness Engineering · Anthropic long-running） |
| `llm/0000`（模型怎么学） | 注意力原始论文系（Vaswani · Formal Algorithms · CS224n）＋ Karpathy 系＋图解系（Jay Alammar · Transformer Explainer · Brandon Rohrer） |
| `llm/0001`（token→下一 token） | Tokenizer 系（HF Tokenizers · Redis · Raschka BPE · fast.ai · Mikolov）＋采样系（HF how-to-generate · Holtzman · Transformer Explainer） |
| `llm/0002`（prefill vs decode） | prefill／decode 系（Redis · Weka）＋延迟指标系（ClickHouse · Anyscale） |
| `llm/0003`（KV cache 与 prompt caching） | KV cache 系（Raschka · HF KV Caching · Sankalp）＋缓存官方系（Anthropic Extended thinking · Prompt caching · OpenAI · Google · DeepSeek · xAI）＋价目（Anthropic · DeepSeek） |
| `llm/0004`（batching） | batching 系（Anyscale · Databricks · Orca · DistServe · Sarathi · Runpod）＋ Pope et al. |
| `llm/0005`（会思考的模型） | 「会思考的模型」小节 |
| `llm/0006`（量化） | 「量化」小节 |
| `llm/0007`（蒸馏） | 「蒸馏」小节 |
| `llm/0008`（引擎在做什么） | 「推理引擎」小节（结构化输出 · 投机解码 · stop reasons · errors · Supported Models · SamplingParams） |
| `llm/0009`＋附录（后训练） | 「蒸馏」小节的后训练条目（InstructGPT · DPO · GRPO · TRL · LoRA · PPO · Gudibande） |
| `rag/0001`（为什么先查·三短板） | Lewis 原论文＋Pinecone RAG 指南（五局限·四组件） |
| `rag/0002`（链路地图·六步） | Pinecone RAG 指南（四组件）＋RAGFlow quickstart/Dataset Configuration（六步→面板对照）＋管线实践 |
| `rag/0003`（该不该上·三选一） | Lewis＋Pinecone RAG 指南（四条好处）＋llm/0009 微调课互链 |
| `rag/0004`（实操·上手 RAGFlow） | 「RAG 系列」实验台组（RAGFlow quickstart · Windows 部署避坑） |
| `rag/0005`（建库·清洗与切块） | Pinecone Chunking＋RAGFlow Dataset Configuration＋Windows 部署（调参顺序） |
| `rag/0006`（嵌入与相似度） | RAGFlow quickstart（嵌入锁定）＋旧 0001-deep 收编内容 |
| `rag/0007`（混合检索与重排） | Anthropic Contextual Retrieval（数字链）＋12 种增强（RRF k=60）＋管线实践（召回 50 精排 5） |
| `rag/0008`（查询工程） | HyDE＋Step-back＋12 种增强（适用边界与温度） |
| `rag/0009`（上下文组装与生成） | Lost in the Middle＋管线实践（约束 prompt）＋RAGFlow quickstart（Empty response） |
| `rag/0010`（翻车诊断与评估原理） | Anyscale（分开评四尺）＋RAGAS metrics＋survey＋5 组配置评测（翻车数字） |
| `rag/0011`（实操·评测实战） | 5 组配置评测（实验蓝本）＋RAGAS metrics（DeepSeek 当判官） |
| `rag/0012`（Agentic RAG） | Self-RAG＋CRAG＋Pinecone RAG 指南（agentic 一节）＋agent/0002 互链 |
| `reference/` 速查页 | 评估系（Anthropic evals · τ-bench · Inspect AI · AgentBench）→ agent-eval-checklist；「记忆」小节 → memory-products；缓存官方系 → prompt-caching；采样系 → sampling-params |

## Knowledge（知识来源）

- [Anthropic — "Building effective agents"](https://www.anthropic.com/engineering/building-effective-agents)
  最重要的入门工程文章。讲清 workflow 与 agent 的区别、五种常见编排模式（提示链、路由、并行、编排者-工作者、评估者-优化者）。**用来**：建立正确的第一心智模型，避免过度设计。**2026-10-21 复抓（`agent/0001` §5 workflow 谱系节用）**：定义原话——Workflows＝"systems where LLMs and tools are orchestrated through **predefined code paths**"，Agents＝"systems where LLMs **dynamically direct their own processes** and tool usage"；五骨架名与例子核实无改；"先找最简单可行解"、"拿延迟和成本换任务表现"、"compounding errors（错误滚动放大）"三句为劝告口径。文首官方勘误注：工具生态部分已变旧，概念框架仍是正源。
- [Lilian Weng — "LLM Powered Autonomous Agents"](https://lilianweng.github.io/posts/2023-06-23-agent/)
  经典的"三大支柱"框架：Planning / Memory / Tool Use。**用来**：给整个领域画地图、确定课程结构的骨架。**2026-10-13 复抓（`agent/0001` §6 三柱深讲用，直连 200）**："Agent System Overview" 一节的分类原话——Planning＝**Subgoal and decomposition**（"breaks down large tasks into smaller, manageable subgoals"）＋ **Reflection and refinement**（"self-criticism and self-reflection over past actions, learn from mistakes and refine them for future steps"）；Memory＝**short-term**（"all the in-context learning"）／**long-term**（"retain and recall (infinite) information over extended periods, often by leveraging an external vector store and fast retrieval"）；Tool use＝"call external APIs for extra information that is **missing from the model weights**"，给的三类缺口＝**current information / code execution capability / access to proprietary information sources**。**用来**：`agent/0001` §6 每柱 2～3 句（分类名与"三样东西"照这节抄，白话译文不引申）。
- [OpenAI — "A practical guide to building agents"（PDF）](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
  面向产品/工程团队的实践指南，覆盖单 vs 多 agent、工具设计、护栏与人机协同。**用来**：从原理过渡到工程取舍。
- [Dify 官方文档 — Workflow 与 Chatflow](https://docs.dify.ai/zh/cloud/use-dify/build/workflow-chatflow) ／ [编排逻辑](https://docs.dify.ai/zh/cloud/use-dify/build/orchestrate-node)
  workflow 档的产品正源。**2026-10-21 抓（`agent/0001` §5「三处能摸到」用）**：Workflow 自我定位「可靠、可重复的流程」；节点族含<b>问题分类器、If-Else、迭代/循环、Agent 节点</b>（Agent 节点定义「将 Agent 作为工作流中的一步运行」——流程里嵌自主循环的公开实例）；编排页含「串行与并行」。<b>同类平台（二手口径，仅提及不展开）</b>：扣子 Coze＝字节旗下一站式智能体开发与工作流编排平台（百科口径）；n8n 偏自动化集成。
- [Chip Huyen — "Agents"（博客，2025-01）](https://huyenchip.com/2025/01/07/agents.html)
  《AI Engineering》作者对 agent 的清晰拆解，尤其擅长讲**失败模式**与评估。**用来**：讲"会在哪里失败"。
- [Chip Huyen —《AI Engineering》(O'Reilly)](https://www.oreilly.com/library/view/ai-engineering/9781098166298/)
  第 6 章 "RAG and Agents"。**用来**：需要更系统、可作为长期参考的教科书内容时。
- [ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., ICLR 2023)](https://arxiv.org/abs/2210.03629)
  现代 agent 循环范式的原始论文：交替产生"推理轨迹"与"动作"。**用来**：讲清循环的理论来源。
- [Anthropic — "Effective context engineering for AI agents"](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  讲上下文是稀缺资源、如何管理。**用来**：讲记忆与上下文窗口的取舍。**2026-10-13 复抓（`agent/0007` 记忆课用，直连 200，五处原话）**：① **context rot**——"as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases"，且 "this characteristic emerges across all models"；② **attention budget**——"LLMs have an 'attention budget' … Every new token introduced depletes this budget by some amount"（上下文是有限资源、边际递减）；③ **结构化笔记＝agentic memory**——"Structured note-taking, or agentic memory, is a technique where the agent regularly writes notes **persisted to memory outside of the context window**. These notes get **pulled back into the context window at later times**"（存外面、用时取回——`agent/0007` §3 的出处）；④ **compaction**——"taking a conversation nearing the context window limit, summarizing its contents, and reinitiating a new context window with the summary"；⑤ 长上下文是"梯度、不是断崖"（"performance gradient rather than a hard cliff … reduced precision for information retrieval and long-range reasoning"）。
- [Anthropic — Claude Platform Docs："Context windows"](https://platform.claude.com/docs/en/build-with-claude/context-windows)
  官方行为口径：**输入本身超过上下文窗口时，API 返回 400 `invalid_request_error`（"prompt is too long"）**——是把请求拒掉，不是截断、不是丢掉前面的。**用来**：回答"一次请求超了窗口会怎么处理"（`0001-deep` Q9）。
- [DeepLearning.AI — "Agentic AI"（Andrew Ng）](https://www.deeplearning.ai/courses/agentic-ai)
  动手型课程，讲多步 agentic workflow 的构建。**用来**：作为需要视频+练习时的补充。

### 推理引擎（第 8 课 · 2026-10-07 新增）

这一课的一手来源**全是这一轮从零查的**（此前全库只有 `reference/sampling-params.html` 里一句「让接口帮你约束格式」，没有出处）。
⚠ `platform.claude.com` 直连是地区限制页，**取正文要走本地代理**（见 1.1）。

- [Anthropic — Structured outputs（官方文档）](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
  **本课第 3 节的主来源**，定义级原话六处：
  ① **机制**：「Structured outputs **guarantee schema-compliant responses through constrained decoding**」；「Always valid: **No more `JSON.parse()` errors**」。
  ② **怎么做到的**：「Structured outputs **work by compiling your JSON schemas into a grammar that constrains Claude's output**」—— 编译成文法，这是「划掉非法字」那句白话的出处。
  ③ **四条实情**（Grammar compilation and caching 一节）：**首次用某 schema 会多花时间等编译** · 「Compiled grammars are **cached for 24 hours from last use**」· **「The cache is invalidated if you change」**（且明说**只改 `name`/`description` 不作废**）· **「Changing the `output_config.format` parameter will invalidate any prompt cache for that conversation thread」**（← 与第 3 课「改配置让缓存前缀作废」同源）。
  ④ **代价与上限**：可选参数上限 **24**、strict 工具上限 **20**、带 `anyOf`/类型数组的参数「**create exponential compilation cost**」；超限返回 **400 "Schema is too complex for compilation"**；另有 **180 秒**兜底超时。
  ⑤ **⚠ 这个「保证」的例外**（本课第 3 节那句「仍然要检查」的依据）：文档自列 Invalid outputs —— **拒答（`stop_reason: "refusal"`）时拒答内容优先于 schema 约束**；另**字符串 `enum`/`const` 的大小写不保证**。
  ⑥ **Strict tool use（`strict: true`）**：「**Guarantee schema validation on tool names and inputs**」；组合原话「guaranteed-valid parameters **AND** return structured JSON responses … useful for **agentic workflows**」—— **本课第 4 节第 ① 条的依据**。
  ⚠ 文档明说**在提示词里也写清 schema 通常明显提升效果**（vLLM 也这么说），**别把结构化输出当「不用管提示词了」**。
  ⑦ **2026-10-13 复核（进阶 Q2 最小例子用，代理抓全文）**：原文请求形状是 `output_config={"format": {"type": "json_schema", "schema": …}}`（"Using a raw JSON schema" 一节的 Python 例子）；SDK 更推荐 `client.messages.parse(output_format=PydanticModel)`——SDK 把模型的 schema 转成 `output_config.format` 再发出去。**例子照这页抄，不凭记忆。**
- [vLLM — Structured Outputs（官方文档）](https://docs.vllm.ai/en/latest/features/structured_outputs/)
  开源引擎这一侧的口径：约束形态**全表**（`choice` 固定选项 / `regex` 正则 / `json` JSON schema / `grammar` 上下文无关文法 / `structural_tag`），后端是 **xgrammar 或 guidance**（旧的 `guided_*` 系列已在 v0.12.0 移除）。**2026-10-13 复核**：新拼写是 `response_format={"type": "json_schema", "json_schema": {"name": …, "schema": …}}` 或 `extra_body={"structured_outputs": {"json": …}}`，文档顶部还给了 `guided_*` → `structured_outputs` 的**完整改名映射**（进阶 Q2 的 vLLM 拼写照这页抄）。**另一句关键原文**：「Structured outputs are **supported by default** in the OpenAI-Compatible Server」——**能力常备**；服务端只有「怎么干活」的配置（`--structured-outputs-config.backend` 默认 `auto`、`--structured-outputs-config.enable_in_reasoning=True`），**没有「替你约束」的总开关**（进阶 Q2「引擎侧配置 vs 请求侧开关」的依据）。**⚠ 实践建议**：官方 Tip 说**在提示词里也写明 schema 与字段怎么填，「can improve the results notably in most cases」**。
- [XGrammar（开源约束解码引擎）](https://github.com/mlc-ai/xgrammar) · [技术报告（arXiv 2411.15100, MLSys'25）](https://arxiv.org/abs/2411.15100)
  README 两句原话：**「leverages constrained decoding to ensure 100% structural correctness」** · **「the default structured generation backend for most LLM inference engines, including vLLM, SGLang, TensorRT-LLM」** —— 说明「划掉非法字」是**引擎的标配能力**、不是某一家独有。技术报告摘要：**最高 100 倍**加速，支持一般上下文无关文法。
- [Leviathan, Kalman, Matias — "Fast Inference from Transformers via Speculative Decoding"（arXiv 2211.17192, ICML 2023 Oral）](https://arxiv.org/abs/2211.17192)
  **投机解码的原始论文**，本课第 3 节末尾那句的依据。摘要原话：**「sample from autoregressive models faster **without any changes to the outputs**」**（←「加速不改答案」的出处）· 「**can accelerate existing off-the-shelf models without retraining or architecture changes**」· **T5-XXL 上 2×–3× 加速、输出完全一致**。
- [vLLM — Speculative Decoding（官方文档）](https://docs.vllm.ai/en/latest/features/speculative_decoding/)
  ① **定位**（正对着第 2 课 decode 带宽受限那条）：「reduce inter-token latency under **medium-to-low QPS**, **memory-bound** workloads」。
  ② **方法族**：EAGLE / MTP / draft model / n-gram / suffix 等，另附按 QPS 给推荐收益的对照表。
  ③ **⚠ 本课演示三那句官方依据**：「**Batch Size and Numerical Stability: Changes in batch size may cause variations in logprobs and output probabilities**」；同节还有「vLLM does not currently guarantee stable token log probabilities (logprobs). This can result in **different outputs for the same request across runs**」。
  ④ **2026-10-12 复抓补（`0008` 进阶 Q5「两招能同时开吗」的依据）**：「**Lossless guarantees of Speculative Decoding**」一节三层——理论无损**在硬件数值精度范围内**（浮点误差仍致细微差异）· 算法无损（**拒绝采样器与目标分布一致**的收敛测试、**贪心采样开不开草稿结果相等**）· logprob 不稳仍可能输出不同；**「Known Feature Incompatibility」清单只列流水线并行（vllm<=0.15.0）与旧版 draft model（vllm<=0.10.0），未列结构化输出**——即约束解码与投机解码可同时开，且"不变"的基线是**开了约束的目标分布**。
- [Anthropic — Stop reasons and fallback（官方文档）](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)
  **「为什么停了」那张表的全表**：`end_turn` 答完 · **`max_tokens` 撞上限** · `stop_sequence` 碰停止字 · `tool_use` 要调工具 · `pause_turn` 服务端工具循环到迭代上限 · **`refusal` 拒答** · **`model_context_window_exceeded` 上下文窗口填满（"Treat the response as truncated"）**。
  ⚠ **本课第 4 节第 ② 条的出处**，原文小标题就是 Incomplete tool use blocks：撞上限被截断的回答里**若含未写完的工具块，需要调大 `max_tokens` 重发**。**2026-10-13 复核（`practice/0004` 技巧四用，走代理抓全文）**：Quick reference 表逐格核过——`max_tokens` 行 "What to do" 格原文 **"Raise max_tokens or continue the response"**；另有 **`model_context_window_exceeded`**（"Treat the response as truncated"）与 `tool_use`（"Run the tool and return the result"）。
- [Anthropic — Errors（官方文档）](https://platform.claude.com/docs/en/api/errors)
  **本课第 4 节第 ③ 条的出处**：`429 - rate_limit_error`（hit a rate limit, reached its usage tier's monthly spend cap…；⚠ 原文明说**撞 tier 花费上限的 429 没有 `retry-after` 头、会一直失败到访问恢复**）· **`529 - overloaded_error`（「The API is temporarily overloaded」**，并说明因 high traffic across all users，且**尖峰用量可能触发加速限制而看到 429**）· `500 - api_error`（**Retry the request with exponential backoff**）· 官方 SDK 那条：**「automatically retries transient failures … with exponential backoff, **twice by default**, honoring the retry-after header」**。**2026-10-13 复核（`practice/0004` 技巧二用，走代理抓全文）**：三行数字与措辞一个没变——`500` 行 "Retry the request with **exponential backoff**"；SDK 行补全主语（"The official SDK automatically retries transient failures (such as connection errors, rate limits, and 5xx server errors) … **twice by default**"）。
- [vLLM — SamplingParams（官方 API 文档）](https://docs.vllm.ai/en/latest/api/vllm/sampling_params.html)
  第 1 课 Q10 已引过。**这一课把它抬成「引擎在执行旋钮」的依据** —— 参数是让 **engine** 去装 logits processor。
- [vLLM — Supported Models（官方文档）](https://docs.vllm.ai/en/latest/models/supported_models/)（2026-10-11 新增）
  **「算法在引擎这一侧」的定义级证据**：①「If vLLM natively supports a model, **its implementation can be found in `vllm/model_executor/models`**」——模型的实现代码是 vLLM 安装包里的代码；②「To determine whether a given model is natively supported, you can check the **`config.json`** … If the **`"architectures"`** field contains a model architecture listed below, then it should be natively supported」——config.json 的 `architectures` 字段对号入座挑实现；③ 没实现过的架构要按 **Adding a New Model** 自己**写代码**（反过来证明光有权重跑不起来）；④ DeepSeek-V3／R1／V3.1 在支持列表里（`DeepseekV3ForCausalLM`）。**用来**：`0008` §1「装好 vLLM＝算法代码就装好了，不用另外下载/导入」。
- [HuggingFace — `deepseek-ai/DeepSeek-V3` 仓库文件清单（HF API，2026-10-11 抓）](https://huggingface.co/api/models/deepseek-ai/DeepSeek-V3)
  **「部署一个开源模型到底下载什么」的实测清单**：163 个 `model-000xx-of-000163.safetensors` 权重分片（里面全是数字）＋ `config.json`（`architectures: ["DeepseekV3ForCausalLM"]`，另有层数等骨架尺寸）＋ `model.safetensors.index.json`（分片清单）＋ `tokenizer.json`／`tokenizer_config.json`（分词器）。⚠ **另带** `configuration_deepseek.py`／`modeling_deepseek.py`（custom code 的算法文件）与官方 `inference/` 脚本——**「仓库自带算法代码」的活例**（给 transformers 的 `trust_remote_code` 或 DeepSeek 自家脚本用）。**用来**：`0008` §1「要下载的是权重＋两个小文件；算法为什么不用下载」。

- [OpenAI — Prompt caching（API 指南）](https://developers.openai.com/api/docs/guides/prompt-caching)
  官方说明：缓存的是 **KV 张量而非 token**；缓存单元是"前缀"（cache breakpoint）；需整个渲染后的前缀完全匹配。**用来**：讲"缓存命中"到底指什么、为什么前缀要稳定。
- [Anthropic — Prompt caching（Claude 平台文档）](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
  讲 <code>cache_control</code> 断点、缓存顺序（tools→system→messages）、cache write/read 计费。**用来**：讲缓存的实际接法与成本。
- [Sebastian Raschka — "Understanding and Coding the KV Cache in LLMs from Scratch"](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms)
  从零实现 KV cache，讲清 K/V 为何复用、省下的到底是什么计算。**用来**：讲 KV cache 的原理。
- [HuggingFace — "KV Caching Explained"](https://huggingface.co/blog/not-lain/kv-caching)
  通俗版 KV cache 讲解。**用来**：入门类比与直觉。
- [Sankalp — "How prompt caching works"](https://sankalp.bearblog.dev/how-prompt-caching-works/)
  工程视角：PagedAttention / 自动前缀缓存、命中率优化清单、Manus 的 context engineering 实践。**用来**：讲 agent 场景下的命中率优化。

- [Redis — "Prefill vs Decode: LLM Inference Phases Explained"](https://redis.io/blog/prefill-vs-decode/)
  讲清两段的瓶颈差异（prefill 算力受限 / decode 显存带宽受限），并给出"输入越长、TTFT 越高"的实测数字。**用来**：讲 prefill/decode 的直觉与量级。
- [Weka — "Prefill and Decode: A Technical Guide"](https://www.weka.io/learn/ai-ml/prefill-and-decode/)
  给出 decode 的算术强度（60–80 ops/byte）与 GPU 利用率（20–40%）等具体数字。**用来**：给"decode 为什么慢"提供量级证据。⚠ **这两个数字是综述转引、不是原始实测**，课件里引用时要说明出处级别。
- [Mistral 7B 发布公告](https://mistral.ai/news/announcing-mistral-7b/)
  官方原话：Mistral 7B uses a sliding window attention (SWA) mechanism, in which **each layer attends to the previous 4,096 tokens**（层数堆叠后有效上下文可达 32k）。**用来**：讲滑动窗口不只是教科书里的选项、**生产模型确实在用** —— 第 2 课进阶 Q7 与基础课那句"生产上不会每次都读全部 KV"的依据。
- [HuggingFace — "How to generate text: using different decoding methods"](https://huggingface.co/blog/how-to-generate)
  把"挑字"的几种挑法讲全：**贪婪搜索**（每步取概率最高的那个）、beam search、**采样**（原文："randomly picking the next word according to its conditional probability distribution"）、**Top-K**、**Top-p（nucleus）**，以及 **temperature**（"调 softmax 的锐度"）。**用来**：讲"字是怎么从分表里被挑出来的、有哪些挑法"。
- [vLLM — SamplingParams（官方 API 文档）](https://docs.vllm.ai/en/latest/api/vllm/sampling_params.html)
  推理引擎的**采样参数全表**（`temperature` / `top_p` / `top_k` / `seed` / `logit_bias` / `logprobs` …），并明说"我们沿用 OpenAI 的采样参数"；参数是让 **engine** 去装 logits processor，`logprobs` 则决定"回给你几个分数"。**用来**：讲"字是怎么被挑出来的、挑法谁定、谁来挑"。
- [Holtzman et al. — "The Curious Case of Neural Text Degeneration"（ICLR 2020）](https://arxiv.org/abs/1904.09751)
  **top_p（核采样 nucleus sampling）的原始出处**："砍掉不可靠的尾巴，只从模型真正有把握的那批里抽"；同时给出"**拿最大值当生成目标，对开放式写作不合适**"的实验依据（贪心 / beam search 生成的文本重复、平淡）。**用来**：讲 top_p 的来历，以及"温度不是越低越好"。
- [HuggingFace — LogitsProcessor / LogitsWarper（官方 API 文档）](https://huggingface.co/docs/transformers/en/internal/generation_utils)
  温度、top_k、top_p 各是一个 <code>LogitsWarper</code>，在 `generate` 里**排成一串依次作用**（temperature → top_k → top_p），最后才从剩下的里抽。**用来**：给"叠着用有先后、起作用的是更紧的那把"提供出处。
- [Pope et al. — "Efficiently Scaling Transformer Inference"（2022）](https://arxiv.org/abs/2211.05102)
  Google 的推理优化论文，给"两段"的**硬件画像**：**处理输入 token 时 MFU 达 76%**（算力几乎打满），而**生成时低批延迟 29ms/token**（在等数据）。并说明 MQA 让上下文能扩到 32 倍。**用来**：给"prefill 算力受限 / decode 带宽受限"提供论文级依据。
- [Anthropic 官方价目](https://www.anthropic.com/pricing)（2026-10-03 查）
  API 每 MTok 单价。**输出一律是输入的 5 倍**：Fable 5.1 $10/$50、Opus 5.5 $4/$20、Sonnet 5.5 $2/$10、Haiku 4.5 $1/$5。缓存另计：**读** $0.10～$0.25（输入的 0.025～0.1 倍）、**写** 是输入的 1.25 倍；原页注明缓存价对应 **5 分钟 TTL**。**用来**：第 2 课第 6 节"输出比输入贵"的价目表；脚本 `PRICE_OUT` / `CACHE_HIT_DISCOUNT` 的依据。⚠ **价目会变，课件里必须标查证日期并给原页链接。**
- [DeepSeek 官方价目](https://api-docs.deepseek.com/quick_start/pricing)（2026-10-03 查）
  分**非高峰 / 高峰**两档（高峰为 UTC 工作日 01:00–04:00、06:00–10:00，非高峰约为高峰的一半）。非高峰：V4.1-Flash 输入（未命中）$0.15、输出 $0.60 → **4 倍**；V4-Pro 输入（未命中）$0.66、输出 $1.98 → **3 倍**。缓存命中输入低到 $0.003 / $0.022，即**未命中的 1/50 ～ 1/30**。**用来**：与 Anthropic 交叉验证"输出比输入贵"的方向与量级（第二家一手来源）。⚠ 同上，价目会变。
- [ClickHouse — "LLM inference latency: TTFT, tokens per second"](https://clickhouse.com/resources/engineering/llm-inference-latency)
  用一条真实时间线（3200 token 输入 → 400ms 首字 → 410 token 输出 → 12.7s）解释 TTFT 与 TPOT 的分工。**用来**：讲两个延迟指标。
- [Anyscale — "Understand LLM latency and throughput metrics"](https://docs.anyscale.com/llm/serving/benchmarking/metrics)
  官方指标定义（TTFT、吞吐）。**用来**：术语对齐；**第 4 课**的三处硬话——"排队等待会加到 TTFT 上"、"系统吞吐随负载上升直到基础设施上限，而并发上去单个用户的出字速度反而降"、"只看平均延迟会骗人、要改看百分位"（最后一条是**技巧篇 0002 技巧四**的反例依据）。

- [Anyscale — "How continuous batching enables 23x throughput in LLM inference"](https://www.anyscale.com/blog/continuous-batching-llm-inference)
  把"加载一次模型权重、服务多个请求"的机制讲得最清楚，并给出 vLLM 实测 23 倍。**用来**：讲批处理的原理与收益；**第 4 课进阶 Q1**——Orca 的迭代级调度、延迟实验按**泊松到达**送请求（所以批大小是浮动的）、"系统越饱和，新请求越难立刻插进批里"、vLLM 在他们那台上约 **QPS≈8 / 吞吐≈1900 token/s** 饱和。
- [Databricks — "LLM Inference Performance Engineering: Best Practices"](https://www.databricks.com/blog/llm-inference-performance-engineering-best-practices)
  给出吞吐/延迟权衡的实测（A100、7B：batch 64 → 吞吐 14×、单请求延迟 4×），并提出 MBU 指标。**用来**：量化权衡曲线。
- [Orca 论文 (OSDI'22)](https://www.usenix.org/system/files/osdi22-yu.pdf)
  连续批处理（iteration-level scheduling）的原始论文，报告同延迟下 36.9× 吞吐。**用来**：追溯 continuous batching 的来源。
- [DistServe 论文 (OSDI 2024)](https://www.usenix.org/conference/osdi24/presentation/zhong-yinmin)
  [arXiv 全文](https://arxiv.org/html/2401.09670v3)。**§2.1 给了本课那句根因的原话**：prefill "tends to be compute-bound"，而 decode "despite processing only one new token per step, the decoding phase incurs a **similar level of I/O to the prefill phase**, making it constrained by the GPU's memory bandwidth" —— 即两段搬运的量级相近，差的是算的量。
  **附录 A.2 / A.3 给了矩阵乘法的原始推导**（第 2 课进阶 Q2 的出处）：prefill 那四个 GEMM 形状是 M=(t,h)、N=(h,·)，**算术强度 O(t)**，A100 上 AI>156 即算力受限，t 通常几百所以必然受限；decode 把 t 换成 batch size B，**算术强度掉到 O(B)**，B 受显存与延迟限制，因此这四个 GEMM 全部 memory-bound。延迟公式也在那里：`T_prefill = C₁(4th²+2thm) + C₂·3ht²/b`，`T_decode = C₄(4h²+2hm) + C₅·3ht`。**权重项 4h²+2hm 两边一样**——这正是"搬运量相同、算量不同"的公式依据。
  **prefill/decode 分离**的正式论文。课程里用的数字（多服务 7.4× 请求 / SLO 达标收紧 12.6×；Perplexity、Meta、LinkedIn、Mistral 在生产里跑）**取自 Weka 综述的转述，未直接读原文——引用前先核**。**用来**：讲"把两段放到不同机器上"。
- [Sarathi 论文](https://arxiv.org/abs/2308.16369)
  **分块预填充（chunked prefill）**的出处。课程里"最多 6.9× 吞吐提升"这个数字同样出自 Weka 综述转述，未直接读原文。**用来**：讲"把长 prefill 切块、和 decode 交替跑"。
- [Runpod — "vLLM Explained: PagedAttention and Continuous Batching"](https://www.runpod.io/articles/guides/vllm-pagedattention-continuous-batching)
  工业落地的科普版：静态批处理 vs 连续批处理、PagedAttention。**用来**：讲工程实现。

### 蒸馏（第 7 课）

- [Hinton, Vinyals, Dean — "Distilling the Knowledge in a Neural Network"（arXiv 1503.02531, NIPS 2014 DL Workshop）](https://arxiv.org/abs/1503.02531)
  **蒸馏这个字的出处**，也是本课机制的原话来源。三句都要记住：
  ① **机制**："Our more general solution, called **distillation**, is to **raise the temperature of the final softmax until the cumbersome model produces a suitably soft set of targets**. We thus use the same high temperature when training the small model to match these soft targets. We show later that matching the **logits** of the cumbersome model is actually **a special case of distillation**."（**温度 + 软标签**，而且"直接对齐 logit"只是它的特例）
  ② **为什么这么做有用**（本课最值钱的一句）："When we are distilling the knowledge from a large model into a small one, however, **we can train the small model to generalize in the same way as the large model**. If the cumbersome model generalizes well because, for example, it is the average of a large ensemble of different models, a small model trained to generalize in the same way will typically do much better on test data than a small model trained on the original data by standard methods."（**学生学的不是答案，是"老师的泛化方式"**）
  ③ **"错字上的分数不是噪声"的原文例子**：论文里说，把某个东西误认成 garbage truck，**"that mistake is still many times more probable than mistaking it for a carrot"**——非答案那几个的概率**编码了"哪个错更像对"**。
  ④ **进阶版 Q2 用的五处（2026-10-12 抓 arXiv HTML 全文，原话）**：**两笔账**——"a better way is to simply use **a weighted average of two different objective functions**"（软目标那笔高温算、正确答案那笔温度 1 算），且 "the best results were generally obtained by using a **considerably lower weight on the second** objective function"；**为什么留正确答案那笔**——"the small model cannot exactly match the soft targets and **erring in the direction of the correct answer turns out to be helpful**"；**T²**——"Since the magnitudes of the gradients produced by the soft targets scale as **1/T²** it is important to **multiply them by T²** … the relative contributions of the hard and soft targets remain roughly unchanged"；**温度的另一半**——"The same high temperature is used when training the distilled model, but **after it has been trained it uses a temperature of 1**"；**特例**——2.1 节标题就是 "Matching logits is a special case of distillation"，推导给出高温极限下 ≈ 最小化 ½(z−v)²，且 "when the distilled model is much too small to capture all of the knowledge … **intermediate temperatures work best**"（学生装不下时中间档温度最好）。另有 3% 数据那组（soft 57.0% vs hard 44.5%，硬标签必须提前停）。**用来**：进阶版 Q2 全部。
  落地证据：摘要给了 MNIST 与**"significantly improve the acoustic model of a heavily used commercial system"**（一个在用的商业语音系统）。
  ⚠ 提取方式：用代理下 PDF 再抽文字（`Invoke-WebRequest -Proxy 'http://127.0.0.1:7890'`），上面三句是**原文**，不是转述。（④ 另走 arXiv 官方 HTML 全文，同为原文。）
- [DeepSeek-AI et al. — DeepSeek-R1（Nature 2025 · arXiv 2501.12948）](https://arxiv.org/abs/2501.12948)
  **第 5 课已经引过这篇；但第 7 课要用它的附录 F 和"局限"那一段。**
  ① **R1 的蒸馏是"搬回答"，不是"搬 logit"**：附录 A.2 原话"The reasoning trajectories discovered through this self-exploration are subsequently **distilled** and used to train other models"；附录 F 整节标题就是 **"F DeepSeek-R1 Distillation"**、F.1 是 **"Distillation v.s. Reinforcement Learning"**。**用来**：讲"蒸馏"今天至少有两个机制（软标签 / 搬大模型的输出），别混。
  ② **对 agent 最要紧的一条自述局限**（第 7 课落点）："**Structure Output and Tool Use:** Currently, the structural output capabilities of DeepSeek-R1 remain **suboptimal** compared to existing models. Moreover, **DeepSeek-R1 cannot leverage tools**, such as search engines and calculators, to improve the performance of output."（**推理强 ≠ 工具调用强**——这条出自论文自己的局限章节，不是二手评论）
  ③ 其他两条顺手记下：蒸馏模型"surpassing the performance of their **original instruction-tuned counterparts**"（超越的是它自己的**指令版**，不是超越大模型）；token 效率那条"it uses fewer tokens to solve simple tasks… **instances of excessive reasoning—manifested as overthinking—are still observed**"。
- [DeepSeek-R1 官方仓库（README 评测表）](https://github.com/deepseek-ai/deepseek-r1)
  **蒸馏模型的实测数字出处**（`Distilled Model Evaluation` 表）：`R1-Distill-Qwen-1.5B` — AIME 2024 pass@1 **28.9**、MATH-500 **83.9**、GPQA Diamond **33.8**、LiveCodeBench **16.9**、CodeForces rating **954**；`R1-Distill-Qwen-7B` — **55.5 / 92.8 / 49.1 / 37.6 / 1189**。**用来**：给"70 亿个数的小模型竞赛题考出 55.5 分"这种说法一个可查的落点；**⚠ 报的是基准分，不是 agent 能力**，引用时别滑过去。**2026-10-10 复核（第 7 课重写时当场再抓一次 README）：数字一个没变。**
  **四门考题各是什么（第 7 课第 5 节的白话身份，出自 R1 论文）**：AIME 2024 ＝ "American Invitational Mathematics Examination 2024"，论文 E.2 明写 "the AIME is a mathematics competition designed for **high school students**"；MATH-500 ＝ 数学题；GPQA Diamond ＝ "GPQA assesses the ability to solve **Ph.D.-level tasks in physics, chemistry, and biology**"；LiveCodeBench ＝ 编程竞赛题，"data collected between **August 2024 and January 2025**"。**两个人类对照**（论文 E.2）："For AIME and Codeforces, the human scores represent the **average performance of all human competitors**. In the case of GPQA, the human score corresponds to **Ph.D.-level individuals who had access to the web**"，且 "human performance remains **superior** to that of DeepSeek-R1"（GPQA 上博士仍赢）。**⚠ 对照的主体是 DeepSeek-R1 本人（671B，老师），不是蒸馏学生**——引用到蒸馏模型头上就错了（5.20.7 踩过）。
  **老师 R1 本人那行分数（第 7 课第 5 节表格第三行，2026-10-10 登）**：`DeepSeek-R1-Evaluation` 表 —— AIME 2024 pass@1 **79.8**、MATH-500 **97.3**、GPQA-Diamond **71.5**、LiveCodeBench **65.9**（这格是 Pass@1-COT）。**用来**：给"学生追平老师了吗"一个可对的数——没追平。⚠ 与蒸馏表分数口径：前三格同为 pass@1，LiveCodeBench 两表标注不同（Pass@1 vs Pass@1-COT），对读时留意。**学生底座**（仓库 `Base Model` 列）：`Qwen2.5-Math-1.5B`／`Qwen2.5-Math-7B`；"超越的是它自己的指令版"＝论文 "surpassing the performance of their **original instruction-tuned counterparts**"，指同底座系列里未蒸馏的指令版。
  **「80 万条样本」的出处**：仓库 License 节写蒸馏的 Qwen 系列是 "finetuned with **800k samples** curated with DeepSeek-R1"，模型卡另说 "fine-tuned based on open-source models, using samples generated by DeepSeek-R1"（第 7 课第 4 节用）。
- [Li et al. — "Textbooks Are All You Need II: phi-1.5 technical report"（arXiv 2309.05463）](https://arxiv.org/abs/2309.05463)
  **用来防止把"小模型变强"全归给蒸馏。** 这条线（TinyStories → phi-1 → phi-1.5）走的是**另一条路**：用已有的大模型**生成"教科书级"数据**来训练 1.3B 的小模型（原文"use existing Large Language Models (LLMs) to generate 'textbook quality' data"），结果是"**performance on natural language tasks comparable to models 5x larger**"。
  **所以"小模型为什么这么强"的诚实答案是三条路一起走**（合成数据 · 蒸馏 · 更好的后训练），**不是"全靠蒸馏"**。⚠ 它**不是** Hinton 那种软标签蒸馏，别当成同一种机制。
- [Yang et al. — "Qwen2.5-Math Technical Report"（arXiv 2409.12122）](https://arxiv.org/abs/2409.12122)
  **用来**：给"没被 R1 教过的原版有多强"一个可查的数（第 7 课第 5 节，2026-10-10 查）。Table 5（AIME24 竞赛表，CoT 只答一次那档）：`Qwen2.5-Math-1.5B-Instruct` **3/30**、`Qwen2.5-Math-7B-Instruct` **5/30**（RM@256 时各 10/30）；上一代 `Qwen2-Math-7B-Instruct` 4/30。顺带两条：Table 2（base，few-shot CoT）`Qwen2.5-Math-1.5B` MATH **49.8**、`Qwen2.5-Math-7B` **55.4**；Table 3（instruct，CoT）MATH **75.8 / 83.6**。
  ⚠ **口径**：千问是 greedy（只答一次），R1 蒸馏表是抽 64 次估 pass@1——**不能并进同一张表**，课里换算成"30 道答对几道"当量级参考。

**进阶版（0007-deep）新用来源，2026-10-12 当场抓、当场登：**

- [Kevin Lu 与 Thinking Machines Lab — "On-Policy Distillation"（博客，2025-10-27）](https://thinkingmachines.ai/blog/on-policy-distillation)
  **在策略蒸馏的现代配方与全部实测数字**（一手，全文抓过）。**用来**：`0007` 进阶版 Q3 的做法与数字、Q4 的分界（SFT／蒸馏）与「范文现成」、Q6「工具调用在行为清单里」；`0009` 初学版 §3 与进阶 Q6 的「照指令办事 85→45」、进阶 Q1「蒸馏用的范文是 40 万条」（⚠ 这组是该博客自报的实验，未见独立论文）。
  ① **做法**：学生自己采样轨迹，老师对每个字打分（per-token reverse KL）；老师只要 `compute_logprobs`（一个前缀过一遍），不用写答案。
  ② **三种练法对照表**（原文表格）：SFT＝off-policy＋dense、RL＝on-policy＋sparse、on-policy distillation＝on-policy＋dense。
  ③ **数字**（学生 Qwen3-8B，考 AIME'24）：离策略 SFT 40 万条＝60%；外推 200 万条≈70%；on-policy distillation **约 150 步（≈7.7 万题 × 4 样本）到 70%**，成本 **9×（SFT 数据现成）～30×（连老师采样费都算）**，GPU 时约 **18×**；自蒸馏实验：追平 RL 老师快 **7–10×**（梯度步数）、累计算力 **50–100×**。
  ④ **离策略的两个毛病**（Q3）：训练序列分布和学生推理时自己生成的分布对不上（误差累积）；"学生学到老师的风格和自信，**未必学到事实正确率**"（引 Gudibande et al. 2023, arXiv 2305.15717 —— ⚠ **该文未直接读，属转引**）。
  ⑤ **reverse KL 的说法**："mode seeking"——学一个具体行为而不是摊到几个次优选项；还降 exposure bias。另：logit 蒸馏 vs 采样序列是同一目标的两种估法。
  ⑥ **蒸馏／SFT 的分界**（Q4，2026-10-14 当场抓）：离策略蒸馏的原文定义 ＝ "SFT on a dataset of **teacher-generated** examples"——练法就是 SFT，叫法看范文是谁写的；那 40 万条 **OpenThoughts-3 是 QwQ-32B 生成的**（"generated by QwQ-32B"），**范文现成＝生成费发生在数据集制作时、不进训练这次的账**（9× 与 30× 两种记法的根）。
- [Qwen3 技术报告（arXiv 2505.09388）](https://arxiv.org/abs/2505.09388)
  Table 21 那组（⚠ **转引自上条博客的引用，未读原表**）：off-policy distillation AIME'24 **55.0%**；+RL **67.6% / 17,920 GPU 时**；+on-policy distillation **74.4% / 1,800 GPU 时**。**用来**：进阶版 Q3「约十分之一开销、分数更高」。
- [Ouyang et al. — "Training language models to follow instructions with human feedback"（InstructGPT，arXiv 2203.02155，2022）](https://arxiv.org/abs/2203.02155)
  **RLHF 三步走的出处**（摘要原话）：先用标注员写的示范**监督微调**，再收集**对模型输出的排序**、用 RL 继续练。实测：**1.3B 的 InstructGPT 输出比 175B GPT-3 更受偏爱**（参数少 100 倍）；truthfulness 提升、毒性下降、公开 NLP 数据集上退步很小。**用来**：`0009`「奖励模型出扣分单」那条与「后训练练的是行为不是聪明」。
- [Rafailov et al. — "Direct Preference Optimization: Your Language Model is Secretly a Reward Model"（DPO，arXiv 2305.18290，2023）](https://arxiv.org/abs/2305.18290)
  **DPO 的出处**（摘要原话）：RLHF "a complex and often unstable procedure"（先拟合奖励模型、再 RL 求最大化且不能漂太远）；DPO 换参数化后**最优策略有闭式解**，整个问题变成"a simple classification loss"，**不用在微调时从模型采样**、超参也省。实测不输 PPO 版 RLHF。**2026-10-15 补边界**：摘要同一句里那句 **"eliminating the need for sampling from the LM during fine-tuning"** 是它的卖点之一——**所以别把 DPO 写进"先让模型当场采样、再逐条打分"那条线**：DPO 用的是**数据集里备好的答案对**（`prompt + chosen + rejected`），属于**离策略**；RLHF／RLVR 才需要当场采。⚠ 写"一句式的通用四步"时，DPO 要单独交代。**用来**：`0009`「偏好对比直接出扣分单，奖励模型不单练了」＋ §4 四步的适用范围括注。
- [Shao et al. — "DeepSeekMath"（GRPO 出处，arXiv 2402.03300，2024）](https://arxiv.org/abs/2402.03300)
  **GRPO 的出处**（摘要原话）：Group Relative Policy Optimization 是 **PPO 的变体**，提升数学推理的同时**优化 PPO 的显存开销**。**2026-10-14 另抓正文（arXiv HTML v3）**：PPO 的"这一步功劳"用 **GAE＋一个学出来的价值函数** 算、价值函数要跟政策一起练；为减轻**对奖励模型的过度优化**，标准做法是加逐字 KL 惩罚、不许离参考模型太远；**GRPO "foregoes the critic model, instead estimating the baseline from group scores"**——同一题采一组回答、用组内均分当对照线，显著省资源（实测 GSM8K 82.9→88.2、MATH 46.8→51.7）。**用来**：`0009` 进阶 Q2「拴绳」、Q3「算法在拧什么」。
- [Hugging Face — TRL「SFT Trainer」（官方文档）](https://huggingface.co/docs/trl/main/en/sft_trainer)（2026-10-15 新增）
  **「一条 SFT 数据长什么样、损失算在哪一段」的第一手出处**（2026-10-15 抓，走 mintlify 镜像正文——`huggingface.co` 直连取不到，见 1.1）。原文两句：① 数据集格式一节给出四种形态——`{"text": …}`（整段文本）、`{"messages": [{"role": "user", …}, {"role": "assistant", …}]}`（对话）、`{"prompt": …, "completion": …}`（问答对）、以及对话版问答对；② **损失范围**："For prompt-completion datasets, **loss is computed only on the completion tokens by default**. For language modeling datasets, **loss is computed on the full sequence**."——**问答对＝只算回答，整段文本＝整段都算**。③ 官方目标是 "minimize the negative log-likelihood (NLL) of the target sequence, conditioning on the input"。**用来**：`0009` §3「SFT 数据＝一问一答、只对回答算扣分」＋§6 六种练法对照表的「扣分算在哪一段」一列。⚠ 一条边界：**只算回答那段是这套工具的默认行为**，不是所有框架都这样（`completion_only_loss` 可关）——课里写「只算回答」，**别写成「任何工具都这样」**。
- [Hugging Face — TRL「GRPO Trainer」（官方文档）](https://huggingface.co/docs/trl/main/en/grpo_trainer) ＋ [`trl/trainer/grpo_trainer.py`（源码）](https://github.com/huggingface/trl/blob/main/trl/trainer/grpo_trainer.py)（2026-10-15 新增）
  **「一句话式的分怎么摊到每个字上」的第一手出处**（2026-10-15 抓：文档走 mintlify 镜像正文，**源码走本地代理** `Invoke-WebRequest -Proxy http://127.0.0.1:7890` 抓 `raw.githubusercontent.com`，见 1.1）。文档原话四步：「At each step, GRPO **generates a group of completions per prompt, computes rewards for each completion, normalizes the rewards within the group to obtain advantages, and updates the policy to increase the probability of high-advantage completions**」；"How GRPO works" 一节逐步写：① generate `num_generations`（**G**）completions per prompt；② **Group normalization (default): subtract the group mean and divide by the group standard deviation**；④ maximize advantages while penalizing deviation from the reference policy（KL）。**源码核实了「一个分怎么落到每个 token」**（`grpo_trainer.py`，2026-10-15 版）：`advantages` 形状 `(B, 1)`（**一条回答一个值**；注释写明 base GRPO 的 advantages 是 `(B,)`，为支持子类才条件性 unsqueeze）→ `per_token_loss1 = coef_1 * advantages`、`per_token_loss2 = coef_2 * advantages` → `loss = ((per_token_loss * mask).sum(-1) / mask.sum(-1).clamp(min=1.0)).mean()`（按 completion mask 逐条平均）。**用来**：`0009` 初学版 §4「采→打→摊」四步 ＋ 进阶 Q3「整段一个分怎么摊到每个字上」（`(B,1)` 广播＝「教得粗」在代码里的样子）＋ 术语表 `#rlhf` 那句「一个分怎么用」。⚠ 三条边界：**（a）打分的是奖励函数／奖励模型，不是训练现场的人**——人的活是更早更小的一步（标排序练奖励模型，见 InstructGPT 条）；**（b）「一组采几条」有默认值可引**：`GRPOConfig` 里 `num_generations (int, optional, defaults to 8)`——「Number of generations per prompt to sample」，课里按这个写「训练工具里默认 8 条」，**别写凭经验的区间**；**（c）KL 那一项默认是关的**：TRL 文档写明 `beta=0.0`（default）时不加载参考模型——写「标准做法都加 KL 惩罚」会跟这条冲突（DeepSeekMath 正文讲的「拴绳」是那边论文的做法）。
- [Phan et al. — "Beyond Reasoning Gains: Mitigating General-Capability Forgetting in Large Reasoning Models"（arXiv 2510.21978；Findings of ACL 2026）](https://arxiv.org/abs/2510.21978)（2026-10-16 新增）
  **「窄领域猛练会不会把别处练坏」的第一手出处**（2026-10-16 抓 arXiv 摘要 ＋ ACL Anthology 页，逐句核对）。摘要原话四句：① **RLVR 有回退风险**——"the RLVR recipe introduces a significant risk of **capability regression**, in which models forget foundational skills **after prolonged training without employing regularization strategies**"；② **实测到的掉分位置**——"open-source reasoning models suffer performance degradation on core capabilities such as **perception and faithfulness**"；③ **⭐ 那条反直觉的边界**——"While imposing regularization terms like **KL divergence** can help prevent deviation from the base model, these terms are **calculated on the current task, thus they do not guarantee broader knowledge**"（**KL 只护住当前任务那片**）；④ **解法方向**——跨领域 experience replay ＋ **动态重新配权**（把重心从"已饱和的目标"移到"还不行／还不稳的目标"），实测在 Qwen2.5-VL-3B／7B 上既保住通用能力又提升推理。**用来**：`0009-deep` Q6（窄领域会不会练坏）＋ Q7 负面第三条（练得又久又窄连累别处）＋ 初学版 §6 收口那句「教不到的这次训练就改不动它」的机制（2026-10-16 同日两轮改口径：「扣分单里没有的」→「后训练数据里没教到的」→ 整段挪进 `0009-deep` Q7，见存档 5.34）。⚠ 他们的实验是**视觉语言模型**（Qwen2.5-VL），引用"感知/忠实性"那两项时别抹掉这个前提。
- [Yang, Li & Holtzman — "LLM Probability Concentration: How Alignment Shrinks the Generative Horizon"（arXiv 2506.17871；TMLR 2026）](https://arxiv.org/abs/2506.17871)（2026-10-16 新增）
  **「后训练会让输出变窄」的量化出处**（2026-10-16 抓摘要）。摘要原话：① 现象——"aligned large language models (LLMs) often generate outputs that **lack diversity**"；② 量法——**Branching Factor（BF）**＝输出分布"长度平均熵的指数"，读作"**生成时下一步有多少种合理走法**"；③ **数字**——"**Alignment tuning sharpens the output distribution from the outset, reducing BF by a factor of 2--5 overall and up to an order of magnitude (e.g., from 12 to 1.2) at early positions**"；④ 连带解释——所以"aligned models are **less sensitive to decoding strategies**"（对齐后的模型对采样参数没那么敏感）；⑤ 作者的理解（**是假设**）——对齐"does not fundamentally change model behavior, but instead **steers** the model toward stylistic tokens (e.g., ``Sure'') that unlock low-entropy trajectories **already present in the base model**"。**用来**：`0009-deep` Q6「顺带一个必然后果：输出会变窄」＋「同一个问题问十次答案越来越像」＋ Q7 负面第三条。⚠ 第 ⑤ 条标着 "We hypothesize"，**不是实测结论**。
- [Sun et al. — "Curiosity-Driven Reinforcement Learning from Human Feedback"（arXiv 2501.11463；ACL 2025）](https://arxiv.org/abs/2501.11463)（2026-10-16 新增）
  **「多样性被牺牲」这句话的第三方旁证**。摘要原话："Reinforcement learning from human feedback (RLHF) has proven effective in aligning large language models (LLMs) with human preferences, **but often at the cost of reduced output diversity**"＋"This trade-off between diversity and alignment quality remains a significant challenge"。**用来**：说明"输出变窄"不是某一篇的孤例（它自己的解法是加"新奇状态"的内在奖励）。
- [Hu et al. — "LoRA: Low-Rank Adaptation of Large Language Models"（arXiv 2106.09685，2021）](https://arxiv.org/abs/2106.09685)（2026-10-15 新增）
  **「后训练动多少权重」这一轴的第一手出处。**摘要原话三句：① **全参数训练是什么**——"**full fine-tuning, which retrains all model parameters**, becomes less feasible"，且举 GPT-3 175B「每个微调版都是一份 175B 参数的独立实例，贵到不可行」；② **LoRA 做什么**——"**freezes the pre-trained model weights and injects trainable rank decomposition matrices into each layer of the Transformer architecture**, greatly reducing the number of trainable parameters"；③ **省多少、亏不亏**——比 Adam 全参数微调的 GPT-3 175B，**可训练参数少 10,000 倍、显存少 3 倍**，质量"on-par or better"，且"**unlike adapters, no additional inference latency**"。**用来**：`0009` 进阶 Q1 新增的那条轴（全参数 vs 只拧一个补丁）与「这条轴跟练法正交」。⚠ 取法记录：arXiv **HTML 全文两次 30 秒超时**，改用 **arXiv API（`export.arxiv.org/api/query?id_list=2106.09685`）** 拿到官方摘要原文；`huggingface.co` 直连失败（预期内，见 1.1），PEFT 那类落地文档**本轮没取到正文**，所以课里只写论文摘要能支撑的部分，不写"怎么合并、怎么部署"。

- [Schulman et al. — "Proximal Policy Optimization Algorithms"（PPO，arXiv 1707.06347，2017）](https://arxiv.org/abs/1707.06347)
  **PPO 的出处**（摘要原话）：策略梯度家族；旧方法每样本只更新一次，PPO 换目标函数后**一次采样可反复小批更新多轮**；兼有 TRPO 的好处但实现简单、样本效率更好。**用来**：`0009` 进阶 Q3「PPO 在拧什么、为什么常见」。
- [Gudibande et al. — "The False Promise of Imitating Proprietary LLMs"（arXiv 2305.15717，2023）](https://arxiv.org/abs/2305.15717)
  **「学得会腔调、学不会事实」的原文出处（2026-10-14 从转引升级为直读）**（摘要原话）：模仿模型在**模仿数据里没怎么覆盖的任务上**"close little to none of the gap"；人评分高是因为"adept at mimicking ChatGPT's style but not its factuality"。结论：差距只能靠**大到离谱的模仿数据或更强的底座**填。**2026-10-15 复核（`0009` §3 补白话背景时当场再抓一遍摘要，原话逐句核过）**：① **实验设置**——"finetune a series of LMs that imitate ChatGPT using varying base model sizes (**1.5B--13B**), data sources, and imitation data amounts (**0.3M--150M tokens**)"；② **两把尺子**——"evaluate the models using **crowd raters and canonical NLP benchmarks**"，人这边是"crowd workers **rate** their outputs as **competitive with ChatGPT**"；③ **作者的意外**——"Initially, **we were surprised** by the output quality of our imitation models -- they **appear far better at following instructions**"；④ **判据句**（课里 §3 新补的「人看追上了、机器看差得远」全出自这里）——"when conducting more **targeted automatic evaluations**, we find that imitation models close little to none of the gap **from the base LM** to ChatGPT"，且"these performance discrepancies may **slip past human raters**"；⑤ **两条出路**——"**using an unwieldy amount of imitation data or by using more capable base LMs**"。⚠ 课里写「跟**它自己没微调之前**比几乎没长」时，原文口径是"from the base LM"（底座＝微调前的基座模型），**别写成"比大模型差多少"**。**用来**：`0009` §3「SFT 教得动什么、教不动什么」那两段白话背景＋`0007-deep` Q3 那句的直证＋`0009-deep` Q7 负面第一条（事实搬不进几个）。
- [DeepSeek-R1（arXiv 2501.12948，Nature 2025）](https://arxiv.org/abs/2501.12948)
  **「对错一比特」那条的出处**（摘要原话，2026-10-14 经 arXiv API 抓）：推理能力可以**纯 RL** 激发出来、"obviating the need for human-labeled reasoning trajectories"；涌现**自我反思、验证、动态换策略**等推理模式；在 **verifiable tasks**（数学、编程竞赛、理工）上**超过照人工示范做监督学习**的同类。**用来**：`0009`「可验证对错出扣分单」与「RL 能教出 SFT 教不出的推理习惯」。
- [Agarwal et al. — "On-Policy Distillation of Language Models: Learning from Self-Generated Mistakes"（GKD，ICLR 2024, arXiv 2306.13649）](https://arxiv.org/abs/2306.13649)
  摘要原话："current KD methods … suffer from **distribution mismatch between output sequences seen during training and those generated by the student during inference**"；GKD＝**在学生自己生成的序列上练**，老师给反馈；并允许换损失函数（"when the student lacks the expressivity to mimic the teacher's distribution"）。**用来**：进阶版 Q3「范文里的世界和学生自己走出来的世界不是一回事」。
- [Gu et al. — "MiniLLM: Knowledge Distillation of Large Language Models"（ICLR 2024, arXiv 2306.08543）](https://arxiv.org/abs/2306.08543)
  摘要原话：把标准 KD 的 forward KLD 换成 **reverse KLD**，"to **prevent the student model from overestimating the low-probability regions** of the teacher distribution"（反着量＝认准老师有把握的那几条路）。**用来**：进阶版 Q3 正反两种量法。（条目按摘要写，正文未通读。）
- [Mirzadeh et al. — "Improved Knowledge Distillation via Teacher Assistant"（AAAI 2020, arXiv 1902.03393）](https://arxiv.org/abs/1902.03393)
  摘要原话："the student network performance **degrades when the gap between student and teacher is large**"；"Given a fixed student network, **one cannot employ an arbitrarily large teacher**"；解法＝中间垫 **teacher assistant** 分步搬。**用来**：进阶版 Q4「老师不是越大越好」。⚠ **图像上的实验（CIFAR/ImageNet）**，大模型口径见下条。
- [Busbridge et al. — "Distillation Scaling Laws"（ICML 2025 · Apple, arXiv 2502.08606）](https://arxiv.org/abs/2502.08606)
  摘要三句（一手）："In settings involving **many students or an existing teacher**, distillation outperforms supervised learning **up to a compute level that scales predictably with student size**. Conversely, if **only one student** is to be distilled **and a teacher also requires training**, supervised learning is generally preferable." **用来**：进阶版 Q4 三条结论。⚠ 学生 1.4 亿–126 亿个数、教材至多 5120 亿词那组范围**转引自二手报道（Import AI 400），原文 69 页未通读**。
- [Kang et al. — "Distilling LLM Agent into Small Models with Retrieval and Code Tools"（NeurIPS 2025 Spotlight, arXiv 2505.17612）](https://arxiv.org/abs/2505.17612)
  摘要原话：只蒸 CoT 的做法"struggles in scenarios requiring rare factual knowledge or precise computation, where sLMs often **hallucinate**"；Agent Distillation 蒸的是**整套解题行为**（轨迹含检索、代码工具）；"sLMs as small as **0.5B, 1.5B, 3B** … competitive with **next-tier larger 1.5B, 3B, 7B** models fine-tuned using CoT distillation"。**用来**：进阶版 Q5 全部（「教材里没的它不会」的正面解法）。

### 会思考的模型（第 5 课）

- [Anthropic — Thinking（Claude 平台文档）](https://platform.claude.com/docs/en/build-with-claude/thinking)
  **本课的主来源**。原话（讲清那段「思考」是什么）："A model that answers in a single pass has to get everything right on the first try: **no scratch work, no checking, no changing course halfway through**"；"When thinking is active, Claude works through the problem **in its own words** before answering: it **restates what is being asked, tries approaches, checks intermediate results, and abandons paths that do not hold up**"。
  **三笔账的原话都在这里**：① 计费——"the tokens Claude spends reasoning are **billed as output tokens, even when the thinking text isn't returned to you**, and they count toward `max_tokens` alongside the response text"；② 你看到的 ≠ 你付的——"You're charged for the **full thinking tokens** generated by the original request, **not the summary tokens**"；③ 缓存/工具——"**Pass every `thinking` block back to the API complete and unmodified, alongside the `tool_use` block it accompanied**"，文档里还给了带 cache 断点的完整多轮示例。
  预算规则：`budget_tokens` **下限 1024**，且**是目标不是硬上限**（实际用量随任务浮动）。
  **2026-10-05 补核（第 5 课新增的第 3 节全部出处）**：① **思考是一类独立的内容块**——响应 `content` 数组按顺序放 `{"type":"thinking","thinking":...,"signature":...}` 和 `{"type":"text",...}`，"That up-front thinking arrives in thinking content blocks ahead of the response"；② **客户端靠块的类型认边界**，请求里的思考参数**只给许可和预算、不含位置信息**；③ **流式事件序列**（`content_block_start` → `thinking_delta` ×N → `signature_delta` → `content_block_stop` → `content_block_start`(text) → `text_delta`），"Thinking blocks stream as `thinking_delta` events inside `content_block_delta` events, followed by a **single `signature_delta` event just before the block's `content_block_stop`**"；④ **模型可以整个跳过思考**——"when the model skips thinking for a simple request, **no thinking block is produced** regardless of `display`"，所以客户端判断"这次想没想"只能靠有没有这个块；⑤ **`display` 三档**（`summarized` / `omitted` / `updates`(beta)），`omitted` 时 `thinking` 字段为空但只回签名，**计费不变、只是流式更快**；⑥ **`signature` 是加密的完整思考**，"The API uses the signature to **verify that thinking blocks were generated by Claude** when you pass them back"，且厂商明说 **"The signature field is opaque: don't interpret or parse it"** —— 这就是"改一个字就 400"的物理原因。
  ⚠ **`platform.claude.com` 直连是地区限制页（"App unavailable in region"），要靠搜索索引拿正文**——见 1.1。⚠ **2026-10-05 实测：走本地代理（`-Proxy http://127.0.0.1:7890`）能拿到完整正文**，含完整事件 trace 和代码示例（与 5.13.4 记的一致，那次是补核）。
  **2026-10-08 补核（学习者问「看到的那段是不是思考完再总结的」，查到四句硬话）**：① **思考块里那段字是摘要、不是原始思考**——"the text in a thinking block is **a summary of Claude's reasoning**"、"**what you see is never the raw chain of thought**"、"**No display setting returns the raw chain of thought**"；② **摘要是另一个模型做的**——"**Summarization is processed by a different model from the one you target in your requests. The thinking model does not see the summarized output**"（所以"思考模型自己收尾写总结"是错的），且 "summaries can **stream as they arrive**"（不必等全部想完才出）；③ **流程原话**："Claude thinks up front, then **distills a summary into the "thinking" block**"；④ **`signature` 是"an encrypted copy of the full reasoning"**——完整思考存在、只是不给你看，服务端"The server decrypts the signature to reconstruct the original thinking for prompt construction"。另注：**思考块与文本块同为生成内容**——"The thinking block is **still generated content**, like the text block that follows it, but it is **separated from the canonical response**"。
- [Anthropic — "Claude's extended thinking"（研究博客，2025-02-24）](https://www.anthropic.com/research/visible-extended-thinking)
  **「不是换了个模型」这句话的出处**，也是本课那句反直觉结论的依据："Extended thinking mode **isn't an option that switches to a different model** with a separate strategy. Instead, it's **allowing the very same model to give itself more time**, and expend more effort, in coming to an answer."
  **收益是递减的**：原话"its accuracy on, for example, math questions improves **logarithmically** with the number of 'thinking tokens' that it's allowed to sample"。给了一个具体数：Claude 3.7 Sonnet 用 64k 思考预算（相当于 256 个独立采样的算力）拿到 GPQA **84.8%**（其中物理子项 96.5%）。
  **「不能靠读思考过程判断它在想什么」的出处**——这是否定"思考过程＝真实推理"的硬证据：原话"models very often make decisions based on factors that they **don't explicitly discuss** in their thinking process. This means **we can't rely on monitoring current models' thinking** to make strong arguments about their safety"。另一句解释了为什么界面上的思考读起来"更冷淡、更像在陈述"：**思考过程没有做他们那套语气训练**，"we wanted to give Claude maximum leeway in thinking whatever thoughts were necessary"——所以"as with human thinking, Claude sometimes finds itself thinking some incorrect, misleading, or half-baked thoughts along the way"。
- [DeepSeek-AI et al. — "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning"（Nature 2025 · arXiv 2501.12948）](https://arxiv.org/abs/2501.12948)
  **「会思考是被训练出来的」这个机制的出处**。原话："the reasoning abilities of LLMs can be incentivized through **pure reinforcement learning (RL), obviating the need for human-labeled reasoning trajectories**"；这个 RL 框架"facilitates the **emergent development** of advanced reasoning patterns, such as **self-reflection, verification, and dynamic strategy adaptation**"（自省、验证、动态换策略——注意这三个词正是界面上常看到的那种动作）。
  **第 7 课（蒸馏）的钩子已经埋在这里**：原话"the emergent reasoning patterns exhibited by these large-scale models can be **systematically harnessed to guide and enhance the reasoning capabilities of smaller models**"。**用来**：讲"为什么现在的小模型也会思考"——不是它自己想通了，是大模型的思考被搬了过去。
  **2026-10-08 三查（学习者问「涌现的到底是什么、标签是不是也是练出来的」）**：① **格式是设计的**——"During training, we **design a straightforward template**, to require DeepSeek-R1-Zero to first produce a reasoning process, followed by the final answer"，Table 1 模板把标签写死：思考装 `<think>…</think>`、答案装 `<answer>…</answer>`；② **标签是格式奖励逼出来的**——"the model is **incentivized to encapsulate its reasoning process within designated tags**"（奖励＝准确率奖励＋格式奖励）；③ **涌现的是招式**——"facilitates the **emergent development** of advanced reasoning patterns, such as self-reflection, verification, and dynamic strategy adaptation"，另有 "aha moment"（"Wait, wait. Wait. That's an aha moment I can flag here"）；④ **论文自己刹车**——"the observed vivid reasoning patterns primarily reflect **DeepSeek-engineered heuristics**, rather than indicating that the model has inherently acquired human-like intelligence"；⑤ **正式版 R1 有冷启动人写数据**——"construct and collect a small amount of long CoT data to fine-tune the model as the initial RL actor"，动机 "primarily product-driven"。**用来**：进阶 Q5「怎么想是涌现的、写成什么格式是设计的」。
- [Lightman et al. — "Let's Verify Step by Step"（arXiv 2305.20050）](https://arxiv.org/abs/2305.20050)
  **「给过程打分」和「只给结果打分」的对照实验**，本课讲"思考凭什么更准"的机制依据。原话："we can turn either to **outcome supervision**, which provides feedback for a final result, or **process supervision**, which provides feedback for each intermediate reasoning step"；结论"**process supervision significantly outperforms outcome supervision** for training models to solve problems from the challenging MATH dataset"，具体数：过程监督的模型解出 MATH 测试子集的 **78%**。同时开源了 PRM800K（80 万条步级人工反馈）。
  ⚠ 注意别把它和 R1 的做法混为一谈：**R1 用的是可自动验证的结果奖励**（答案对不对、代码跑不跑过），而这篇是**人去标注每一步**。两条路，别互相冒用出处。
- [AWS — Claude on Bedrock：Extended thinking](https://docs.aws.amazon.com/bedrock/latest/userguide/claude-messages-extended-thinking.html)
  同一套机制在 Bedrock 上的落地说明，**两条运维经验值**：预算**从下限起步逐步加**（"start at the minimum and increase incrementally"）；**预算超过 32K 建议走批量处理**，否则"causes long running requests that might result in system timeouts"。**用来**：讲"预算不是越大越好"以及顶格预算的工程后果。
- [vLLM — Reasoning Outputs（官方文档）](https://docs.vllm.ai/en/latest/features/reasoning_outputs/)（2026-10-08 新增）
  **「开始/结束的标记就是模型输出的字」的实证**（学习者问到、查证前课里只敢标推论）。三句硬话：① 推理引擎是从模型输出里**切**出思考的——`--reasoning-parser` 的定义是 "extracting reasoning content **from the model output**"（模型吐的是一条流，引擎切成 `reasoning` / `content` 两个字段）；② 记号有名字——`--reasoning-config` 定义 "reasoning **boundary tokens**"（`reasoning_start_str` / `reasoning_end_str`），Qwen3 的实例是 `<think>` 与 `</think>`（结束记号前还可以带一句过渡话）；③ **结束记号就是个普通 token，甚至能被强制吐出来**——"Once the reasoning token count reaches the configured `thinking_token_budget`, vLLM **forces the model to produce `reasoning_end_str`**, effectively terminating the reasoning block"。**用来**：第 5 课第 1 节"草稿怎么收笔"那句（把"我从规则反推的"升级成有出处），以及"切分不是理解"（同 `agent/0002` 的工具调用）。
  **2026-10-08 二查（学习者追问"标签谁加、引擎加不行吗"）补两句**：④ **开源思考模型的输出里字面同时装着思考和答案**——"reasoning models like DeepSeek R1, which are **designed to generate outputs containing both reasoning steps and final conclusions**"，`reasoning` 字段装的就是"the reasoning steps that led to the final conclusion"（**原文，不是摘要**——开源这条链路没有摘要器）；⑤ **记号是模型词表里的 token**：文档贴的 DeepSeek-R 系 parser 源码里 start_token / end_token 就是 `<think>` 与 `</think>`，且 `start_token_id = tokenizer.encode(...)[0]`——**模型写记号、引擎按记号切**；引擎造不出边界，要提前收块只能"forces the model to produce `reasoning_end_str`"。附：`reasoning` 字段旧名叫 `reasoning_content`。


- [OpenAI — Reasoning（官方指南）](https://platform.openai.com/docs/guides/reasoning)（2026-10-08 新增）
  **跨厂商对照用**："While **we don't expose the raw reasoning tokens emitted by the model**, you can view a summary of the model's reasoning using the `summary` parameter"——**同族"给摘要、扣原文"**，摘要还分档（concise / detailed / auto）。带回机制同 Anthropic 的 signature：reasoning item "remains **opaque**"、"the API does not return their reasoning text"，无状态模式下用 `encrypted_content` 带回。**用来**：回答"是不是所有厂商都用另一个模型做总结"——**只有 Anthropic 白纸黑字写了"另一个模型"**，OpenAI 只说"给你摘要"（没说谁做），开源系（vLLM）直接给原文，**三家三种口径**。


- [Qwen — Qwen3（官方仓库 README）](https://github.com/QwenLM/Qwen3)（2026-10-08 新增）
  **「标签谁写」的最后一块拼图**：Qwen3-Thinking-2507 的官方 Note——"to enforce model thinking, the **default chat template automatically includes `<think>`**. Therefore, it is normal for the model's output to contain only `</think>` without an explicit opening `<think>` tag"（**开始标签是模板塞进提示的，模型只写到结束标签收尾**）；官方示例还直接拿 **结束标签的 token 编号 151668** 切分思考/答案（`# rindex finding 151668`）。另有开关两条：`enable_thinking=False`（模板参数）与 `/think` `/no_think` 指令。**多轮回传没有「签名」那套**——官方建议 "passing the content as it is, without extracting thinking content, and the chat template will correctly handle the processing"（原样传回，模板自己处理）；**开源链路里 signature / 加密存根出现次数为 0**（vLLM 的 `reasoning` 是明文字段，解析器返回的也是明文串）。**用来**：进阶 Q3／Q5。
### 量化（第 6 课）

- [llama.cpp — `tools/quantize/README.md`（官方仓库）](https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/README.md)
  **本课最重要的一条实测来源**。Llama-3.1-8B 在同一台机器上的完整对照表，每档都给了三个数：`bits/weight`（含换算说明的开销）、`size`、`prompt processing t/s @ 512` 与 `text generation t/s @ 128`。原值：**F16 = 16.0005 bit / 14.96 GiB / prefill 923.49 / decode 29.17**；Q8_0 = 8.5008 / 7.95 / 865.09 / **50.93**；Q6_K = 6.5633 / 6.14 / 812.01 / 58.67；Q5_K_M = 5.7036 / 5.33 / 758.69 / 67.23；**Q4_K_M = 4.8944 / 4.58 / 821.81 / 71.93**；Q3_K_M = 3.9960 / 3.74 / 783.44 / 71.68；Q2_K_S = 2.9697 / 2.78 / 798.91 / 90.01。
  **这张表同时给出两个可直接上课的结论**：① decode 快 2.5 倍（29.17 → 71.93）而 **prefill 几乎没变**（923.49 → 821.81，甚至更慢）——**独立印证第 2 课进阶 Q3 的「prefill 算力受限 / decode 带宽受限」**；② 「4 bit」实测是 4.89 bit，因为缩放因子要占地方。
  另有内存/磁盘表：8B **32.1 GB → 4.9 GB**、70B **280.9 → 43.1**、405B **1,625.1 → 249.1**（Q4_K_M）。README 开头两句也给了定义级说法："reduces the precision of model weights… shrinks the model's size and can speed up inference… may introduce some accuracy loss which is usually measured in Perplexity (ppl) and/or Kullback–Leibler Divergence (kld)"。
  **「压的是哪些数」的直接证据（2026-10-08 核）**：定义句是 "reduces the precision of **model weights**"，而工具按 **tensor** 动手——`--token-embedding-type`（"use a specific quant type for the **token embeddings tensor**"）、`--output-tensor-type`（`output.weight`）、`--leave-output-tensor`（"leave output.weight un(re)quantized. **Increases model size** but may also increase quality"）、`--tensor-type`（按名字指定个别张量的档）。**所以嵌入表、输出表默认都在压的范围内**，只是可以给它们单独换档或干脆不压。⚠ **`raw.githubusercontent.com` 直连取不到，要带代理**（见 1.1）。
- [Dettmers et al. — "LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale"（NeurIPS 2022）](https://arxiv.org/abs/2208.07339)
  **int8 量化的原始出处，也是「离群值」这个现象的出处**。原话：int8 矩阵乘 "**cut the memory needed for inference by half while retaining full precision performance**"；做法是 "vector-wise quantization" 处理绝大多数特征，而对 **emergent outliers** 用混合精度分解、单独放进一个 16-bit 矩阵乘里，"**still more than 99.9% of values are multiplied in 8-bit**"。**用来**：讲"为什么朴素压到 8 bit 会掉分、后来者为什么必须特殊处理离群通道"。
- [Frantar et al. — "GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers"（ICLR 2023）](https://arxiv.org/abs/2210.17323)
  **"训练后量化（PTQ）"路线的代表作**。原话：**175B 参数模型约 4 GPU 小时**压到 **3 或 4 bit**，"with negligible accuracy degradation relative to the uncompressed baseline"；比此前的一次性量化方法"more than doubles the compression gains"；极端档位还能压到 **2-bit 甚至三值**。端到端加速原值：**A100 约 3.25×、A6000 约 4.5×**（相对 FP16）。**用来**：讲"压到 4 bit 还能用"这句话的出处与它成立的条件（逐层用二阶信息补偿），以及加速倍数的真实量级。
- [Xiao et al. — "SmoothQuant: Accurate and Efficient Post-Training Quantization for LLMs"（ICML 2023）](https://arxiv.org/abs/2211.10438)
  **给出 W8A8（权重与激活都压到 8 bit）这条路的关键事实判断**，原话："**weights are easy to quantize while activations are not**"，所以用"数学上等价的变换"把激活的离群值**迁移到权重那边**。实测原值：**最高 1.56× 加速、2× 内存下降**，精度损失可忽略。**用来**：讲"只压权重"和"连激活一起压"是两条不同的路，以及离群值为什么专挑激活出来。
- [Lin et al. — "AWQ: Activation-aware Weight Quantization"（MLSys 2024 最佳论文）](https://arxiv.org/abs/2306.00978)
  **"不是所有权重一样重要"的出处**。原话："**not all weights in an LLM are equally important. Protecting only 1% salient weights can greatly reduce quantization error**"；而且判断哪些通道重要**要看激活的分布、不是看权重**（"we should refer to the activation distribution, not weights"），做法是"数学上推导出的等价变换"放大关键通道——所以 **"does not rely on any backpropagation or reconstruction"**。配套 TinyChat 实测：桌面与移动 GPU 上相对 HuggingFace FP16 **超过 3× 加速**，并让 70B 跑进手机 GPU。**用来**：讲"误差不是均匀的——挑着压才划算"。
- [vLLM — Quantization（官方文档）](https://docs.vllm.ai/en/latest/features/quantization/)
  定义级原话："**Quantization trades off model precision for smaller memory footprint, allowing large models to be run on a wider range of devices.**"支持格式全表（AutoAWQ / GPTQ / BitsAndBytes / FP8 / INT4 / GGUF / TorchAO…）与**逐硬件支持矩阵**。⚠ **这张表会变，引用前重新抓**（2026-10-10 复核）：**AWQ** Volta ❌／Turing-Ampere-Ada-Hopper ✅／**AMD ❌**；**GPTQ** Volta→Hopper **全 ✅**／**AMD ❌**；GGUF 同 GPTQ（NVIDIA 五代全 ✅、AMD ❌）。**（旧记录写过"GPTQ 不支持 Ada 之后"，那是过期值。）用来**：讲"量化不是一个动作、是一堆互不通用的压法，能不能跑先看你的显卡支不支持"（第 6 课 §1）。
- [vLLM — INT4 W4A16（官方文档）](https://docs.vllm.ai/en/latest/features/quantization/llm_compressor/int4/)
  **"权重压 4 bit、激活保持 16 bit"这条路线的定位与代价**：这种量化"particularly useful for **reducing model size and maintaining low latency in workloads with low queries per second (QPS)**"；**需要 compute capability > 8.0**（Ampere / Ada / Hopper / Blackwell）。校准数据实践原话："**Start with 512 samples for calibration data, and increase if accuracy drops**"，默认长度 2048；示例里 `group_size=128`。⚠ 一条实用警告："**Quantized models can be sensitive to the presence of the `bos` token**"。**用来**：讲"为什么量化要喂样本、喂什么样本"，以及低 QPS 场景为什么偏爱权重-only。
- [Kurt — "Which Quantization Should I Use? A Unified Evaluation of llama.cpp Quantization on Llama-3.1-8B-Instruct"（arXiv 2601.14277，2026-01）](https://arxiv.org/abs/2601.14277)
  较新的统一评测：同一模型（Llama-3.1-8B-Instruct，FP16/GGUF）上覆盖 3–8 bit 的 K-quant 与 legacy 格式，同时测**下游任务分数、perplexity、CPU 吞吐（prefill 与 decoding 分开）、体积、压缩率、量化耗时**。**用来**：讲"别只问压到什么位，要问在你的任务上掉多少分"——本课若要加进阶版，这是唯一一份同口径横向对比。⚠ 单一模型、单一后端，结论不可外推。
- [vLLM — Quantized KV Cache（官方文档）](https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/)（2026-10-08 新增）
  **"KV 也能压，但那是另一笔账"的出处**。页面标题就写着 **FP8 KV Cache**，给出 "Quantize Llama Attention KV Cache to FP8" 的完整做法（llm-compressor 一次性校准，`tensor` / `attn_head` 两种策略）；配置字段是 `kv_cache_dtype`，另有 `kv_cache_dtype_skip_layers`（"Layer patterns to skip KV cache quantization"，可按层跳过）。⚠ **它压的是 KV 缓存，不是权重**——与第 6 课讲的存法那笔账是两回事。**用来**：回答学习者"权重压了，那 KV 会不会也被压"（已进第 6 课 ask-teacher）。**2026-10-10 补（默认档位）**：`CacheConfig.cache_dtype` 默认 `"auto"`，文档原话 "Data type for kv cache storage. If 'auto', **will use model data type**"；开量化时还会自己警告 "**it may cause accuracy drop without a proper scaling factor**"。
- [llama.cpp — `tools/server/README.md`（官方仓库，服务程序参数表）](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)（2026-10-10 新增）
  **"int4 的模型，KV 是什么精度"的直接答案**：`-ctk, --cache-type-k` ／ `-ctv, --cache-type-v` ＝ "KV cache data type for K/V"，allowed values `f32, f16, bf16, q8_0, q4_0, q4_1, iq4_nl, q5_0, q5_1`，**default: f16**。**结论：KV 的档位跟权重压到几 bit 无关，默认是 16 bit（f16）；要压 KV 是另一个开关。**⚠ `raw.githubusercontent.com` 直连取不到，带代理。
- [Li et al. — "Quantization Meets Reasoning: Exploring LLM Low-Bit Quantization Degradation for Mathematical Reasoning"（arXiv 2501.03035）](https://arxiv.org/abs/2501.03035)（2026-10-10 新增）
  **"语义也会掉"的直接实测**。原话：AWQ／GPTQ 这类激进量化 "introduce **up to 32.39% accuracy degradation (average 11.31%) on Llama-3 models**, particularly in **numerical computation and reasoning planning**"。**用来**：回答学习者"只影响文本准确性，还是语义也影响"——**语义会掉，有数字**。
- [Li et al. — "Quantization Meets Reasoning: Exploring and Mitigating Degradation of Low-Bit LLMs in Mathematical Reasoning"（arXiv 2505.11574）](https://arxiv.org/abs/2505.11574)（2026-10-10 新增）
  **掉的位置有偏向**。原话：数学推理 "drops up to **69.81%** in our harder settings"；错误归类两条规律——"(i) PTQ disproportionately elevates **method and execution errors** relative to high-level conceptual mistakes; (ii) failures emerge early, with the first vulnerable step flipping and cascading to the final answer"。**用来**：讲"它多半不是看不懂，是**算不对、写不准**"（执行 > 概念）。⚠ 同文还给了回补办法（332～545 条样本微调能恢复大半），本课不展开。
- [Lee et al. — "Exploring the Trade-Offs: Quantization Methods, Task Difficulty, and Model Size in Large Language Models From Edge to Giant"（arXiv 2409.11055）](https://arxiv.org/abs/2409.11055)（2026-10-10 新增）
  1B～405B、四种量化方法、**13 个数据集**的全面评测。五条结论里与本课相关的四条：① 量化模型 "often struggle with **instruction-following and hallucination detection**"；② "**FP8 consistently emerges as the most robust option across tasks**"，权重-only 里 AWQ 优于 GPTQ；③ 小模型 4-bit 掉得狠，**70B 级别稳**；④ "**hard tasks do not always experience the largest accuracy losses**"——**量化是放大模型本来的弱点，不是简单跟任务难度挂钩**。**用来**：① 支撑"8 bit（FP8）是更稳的一档"；② **修正"格式敏感的活掉最多"这种一刀切的说法**（那条没有直接对照实测）。

- [Vaswani et al. — "Attention Is All You Need" (2017)](https://arxiv.org/abs/1706.03762)
  Transformer 与注意力机制的原始论文。定义 Query/Key/Value、scaled dot-product attention（"输出是 Value 的加权和，权重由 Query 与 Key 的相似度决定"）、以及因果掩码（"每个位置只能注意到自己及之前的位置"）。**用来**：所有注意力相关说法的最终依据。
- [Phuong & Hutter — "Formal Algorithms for Transformers" (2022)](https://arxiv.org/abs/2207.09238)
  用伪代码给 Transformer 各步骤下精确定义：masked self-attention（"把之前所有 token —— **包括自己** —— 当作上下文"）、unembedding、softmax 采样。**用来**：需要"精确到算法"的措辞时。
- [Stanford CS224n — "Self-Attention & Transformers"](https://web.stanford.edu/class/cs224n/readings/cs224n-self-attention-transformers-2023_draft.pdf)
  把注意力讲成"对 Key-Value 做软查找"，并推导权重 α_ij 与加权和。**用来**：教学类比与推导细节。

- [Karpathy — "Deep Dive into LLMs like ChatGPT"](https://www.youtube.com/watch?v=7xTGNNLPyMI)
  **大众轨**（他自己就是这么分的）：不写代码，讲清"模型到底在做什么、为什么会一本正经地胡说、能力与失效各从哪来"。**用来**：给「第 0 课」这种面向初学者/业务人员的内容**定深浅的标尺**。
- [Karpathy — "Neural Networks: Zero to Hero"（播放列表）](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ)
  **技术轨**：micrograd（从零写反向传播）→ makemore（字符级语言模型）→ 从零搭 GPT。**用来**：进阶版读者想把"训练"亲手做一遍时。
- [Karpathy — micrograd](https://github.com/karpathy/micrograd)
  100 行左右的自动求导小引擎，把"从出口往回追责"写成代码。**用来**：给"反向传播＝一次算出几十亿个权重各该往哪拧"提供一份能读完的实现。

- [Jay Alammar — "The Illustrated Transformer"](https://jalammar.github.io/illustrated-transformer/)
  **业界公认最常被引的图解**：把注意力拆成 Q/K/V 矩阵 → 多头切分 → 掩码 → softmax → 加权求和一张图走完。**用来**：给"英文权威图 ↔ 我们课里的白话图"做对照（图是 **CC BY-NC-SA 4.0**，引用要署名、非商业、相同方式共享）。
- [Transformer Explainer（Georgia Tech poloclub）](https://poloclub.github.io/transformer-explainer/)
  浏览器里跑**真 GPT-2（1.24 亿参数）**的交互图：文字→向量→block→logits→softmax→采样，**能拖 temperature / top-k / top-p 三个滑块看分布变**。**用来**：讲采样参数时让人亲手拧一次；也佐证词表 50,257、MLP 768→3072。
- [Brandon Rohrer — "Transformers from Scratch"](https://brandonrohrer.com/transformers.html)
  专讲"论文图 1 里的这一块，到底对应代码里的哪一步"。**用来**：帮学员把 Fig.1 的方框对上自己已懂的概念。

- [HuggingFace — "Tokenizers"](https://github.com/huggingface/blog/blob/main/tokenizers.md)
  最清晰的定义来源："语言模型不读原始文本，它消费的是 **token ID 序列**"；token 是模型看到的最小字符串单位，**词表**把每个 token 映射到 token ID。**用来**：讲"文字 → token → 编号"。
- [Redis — "Tokenization in LLMs"](https://redis.io/blog/tokenization-in-llms/)
  把整条管线拆成四步：预分词 → 子词切分 → 词表查编号 → 嵌入表查向量；并明确指出"分词产生整数 ID，嵌入把 ID 变成稠密向量，**这两步常被混淆**"。**用来**：讲清 token 与向量是两回事。

- [learn-mech-interp — Transformer architecture 学习笔记](https://github.com/FlyingPumba/learn-mech-interp/blob/main/src/topics/transformer-foundations/transformer-architecture/index.md)
  明确写出"给定 n 个 token，模型**同时做出 n 个预测**，每个位置预测它自己的下一个 token（因果掩码保证只看得到之前的位置）"。**用来**：讲清"整句一起送、只听最后一个位置"。（配套硬底：Vaswani §3.2.3 关于"输出偏移一位、位置 i 只依赖 i 之前的输出"的说明。）

- [Geva et al. — "Transformer Feed-Forward Layers Are Key-Value Memories"（EMNLP 2021）](https://aclanthology.org/2021.emnlp-main.446/)
  实证：FFN 层运作得像<b>键值记忆</b>——"键"对应输入里的<b>文本模式</b>，"值"把某个/某些词的分往上推。原例：`Eiffel Tower is located in` 触发某条记忆，推动「Paris」。**用来**：回答"FFN 到底在改什么"。
- [Geva et al. — "Transformer Feed-Forward Layers Build Predictions by Promoting Concepts in the Vocabulary Space"（EMNLP 2022）](https://aclanthology.org/2022.emnlp-main.3/)
  上一篇的后续：FFN 的输出可以看成一次次<b>推动概念</b>的更新，最终预测是逐层"推"出来的。**用来**：讲"预测是一层一层打磨的"。
- [Belrose et al. — "Eliciting Latent Predictions from Transformers with the Tuned Lens"（ACL 2023）](https://aclanthology.org/2023.acl-long.325/)
  **logit lens 的正式出处**：拿中间层的 hidden 直接过最终那层"打分表"，就能读出模型当时预测的词。**用来**：支撑"只走一半的层、拿当时的数字去词表对分，也能猜出个大概"这个说法（别只引 Geva 2022，那篇讲的是 FFN 推动概念，不是这个实验）。

- [Sebastian Raschka — "Implementing A Byte Pair Encoding (BPE) Tokenizer From Scratch"](https://sebastianraschka.com/blog/2025/bpe-from-scratch.html)
  给出各家词表规模的实测数字（GPT-2 = 50,257；GPT-4 = 100,256；GPT-4o = 199,997），并讲清词表是怎么**训练出来的**（反复合并高频相邻对）。**用来**：讲词表规模与"词表怎么来的"。

- [fast.ai — "Let's Build the GPT Tokenizer"（Karpathy 系列整理）](https://www.fast.ai/posts/2025-10-16-karpathy-tokenizers)
  明确切分边界："tokenizer 是把字符串翻译成 token ID 的独立程序"；而<b>嵌入表的每一行是可训练参数，靠反向传播优化</b>，喂给 transformer 的是这些向量。**用来**：讲清"什么算模型、什么不算"。
- [Mikolov et al. — "Efficient Estimation of Word Representations in Vector Space"（arXiv 1301.3781）](https://arxiv.org/abs/1301.3781) · [Mikolov, Yih & Zweig — "Linguistic Regularities in Continuous Space Word Representations"（NAACL 2013）](https://aclanthology.org/N13-1090/)（2026-10-10 核）
  **「向量＝空间里的一个点、向量近＝意思近」的出处**。摘要原话：「computing **continuous vector representations of words** from very large data sets」；表示的质量就是在「a **word similarity task**」上量的，「**syntactic and semantic word similarities**」都靠它——**两个词的向量近，就是意思近**。后一篇标题即「**Continuous Space** Word Representations」（词的表示就在连续空间里）。**用来**：`llm/0000` 外星人比喻（"每个字是高维空间里的一个点"）落地前的出处核查（5.7：框架性比喻查不到出处不进课件）。⚠ 凭记忆写的编号当场翻车过一次（1308.0750 是物理论文）——**引用编号必须打开核对**。

- [OpenAI — "Function calling"（官方指南）](https://developers.openai.com/api/docs/guides/function-calling)
  官方机制说明：把函数写成 **JSON schema**（名字 + 描述 + 参数）传给模型，模型返回一份"要调哪个函数、参数是什么"的**结构化输出**，由你的应用去执行。**用来**：讲工具调用的完整来回。
- [Anthropic — "Introducing advanced tool use"](https://www.anthropic.com/engineering/advanced-tool-use)
  Anthropic 官方工程文：模型返回 <code>tool_use</code> 块（工具名 + 输入），你的代码执行后把结果以 <code>tool_result</code> 送回，模型接着走。**用来**：讲 tool_use / tool_result 这一对来回。

- [Model Context Protocol — 官方文档（Architecture + Connect to local servers）](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture)（2026-10-18 抓；配置页 [connect-local-servers](https://modelcontextprotocol.io/docs/2026-07-28/develop/connect-local-servers)）
  **角色**：MCP host（AI 应用）给每个 server 建一个 MCP client；本地 stdio server 通常单客户端，远程 Streamable HTTP server 可服务多个客户端。**传输**：stdio（本机进程标准输入/输出）／Streamable HTTP（远程，支持 Bearer/API key/OAuth）。**数据层**：JSON-RPC 2.0、**无状态**（每个请求自带版本与能力）；发现 `server/discover`、`tools/list`，执行 `tools/call`；server 公布 **tools / resources / prompts**；工具清单变化可通知。**配置**：本地 server 的 JSON 形状是 `mcpServers` → 服务名 → `command` / `args` / `env`（env 放 key）；官方示例是 filesystem server。**安全**：本地 server 以你的用户权限运行，只给需要的目录。**用来**：0003 MCP 三个角色、传输、发现/调用、配置字段与安全；0003「MCP 还是 Skill」里"标准接口/多客户端/发现"那一列；0003 的"发现"。
- [腾讯云开发者 — MCP 广场介绍（官方文档）](https://cloud.tencent.cn/document/product/1212/123193)（2026-10-18 抓）
  **本地 vs 托管的一手口径**：MCP 广场提供 **Local 模式**（部署在本地设备，适合依赖本地文件/服务的 server，如文件系统；配置是 `mcpServers` 里的 `command`/`args`/`env`，示例用 `uvx` 启动）和 **Hosted 模式**（部署在广场的免费云资源上，远程连接、跨端友好，是主推模式）。广场还提供安全扫描、免费托管、远程连接。**用来**：0003「本地 server / 远程 server」对照、`npx`/`uvx` 只属于本地、资源广场一例。
- [腾讯云 — MCP 广场（入口）](https://cloud.tencent.com/developer/mcp)（2026-10-18 抓）
  官方 + 第三方 MCP 目录；分类（腾讯产品/搜索/数据库/支付/位置/文档…）与卡片，可直接看每个 server 的接法。**用来**：0003 §4 资源入口；截图 `mcp-square-tencent.png` 的来源。
- [腾讯云 CloudBase — Connection Modes: Local vs Hosted（官方文档）](https://docs.cloudbase.net/en/ai/cloudbase-ai-toolkit/connection-modes)（2026-10-18 抓）
  **远程配置的实际形状**：Local Mode 用 `npx` 跑本地 server；Hosted Mode 跑在腾讯云，IDE 通过 HTTP 连，**不用本地 Node**。Hosted 配置示例：`type: "http"` + `url` + `headers`（`X-TencentCloud-SecretId` / `X-TencentCloud-SecretKey`），没有 `command`/`args`。**用来**：0003 远程示例（与本地 `mcpServers` 对照）；也解释"npx 是本地，远程只要 URL/鉴权"。
- [阿里云百炼 — 官方 MCP 服务（官方文档）](https://help.aliyun.com/zh/model-studio/official-and-third-party-mcp)（2026-10-18 抓）
  **One Key MCP**：首次调用自动生效；在 MCP 广场选服务 → 服务详情页复制接入配置或一键配置到客户端，用 `DASHSCOPE_API_KEY` 鉴权。**云部署**：MCP 服务跑在云端；敏感数据用 KMS 加密。**用来**：0003 远程/托管 MCP 的第二个例子、资源入口。
- [阿里云百炼 — Skill（官方文档）](https://help.aliyun.com/zh/model-studio/introduction-to-skill)（2026-10-18 抓）
  **Skill 的通用格式**：ZIP 根目录必须有 `SKILL.md`，YAML frontmatter 写 `name`/`description`，≤10MB；官方 Skill 添加即用，自定义 Skill 上传后自动审查；描述建议包含输入类型、操作、触发关键词、不适用场景。**用来**：0003 §4 技能资源、导入/创建要求；`npx` 不是 Skill 的事。
- [ModelScope — MCP 广场](https://modelscope.cn/mcp) · [Skills 技能中心](https://modelscope.cn/skills)（2026-10-18 抓）
  国内的浏览入口：MCP 服务和技能分别有目录页（只核到页面标题与入口，具体条目按页面为准）。**用来**：0003 §4 资源入口。
- [npm — npx（官方文档）](https://docs.npmjs.com/cli/v10/commands/npx)（2026-10-18 抓）
  `npx` 是 npm 的包运行器：运行包里的命令；包不在本地时先取下来。**用来**：0003「npx 到底干了什么」；`-y` 跳过安装确认。
- [Anthropic — "Equipping agents for the real world with Agent Skills"](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
  Skill 的设计理念：**目录 + SKILL.md（YAML frontmatter 的 name/description + 正文）+ 可选脚本/资料**；**渐进式加载三层**（metadata 常驻 → 触发后读正文 → 按需读引用文件），"像一本组织良好的手册"。**创建建议**：从评估开始（先看 agent 在哪卡住再补 skill）、结构可扩展（正文太长就拆文件）、站在模型视角盯 name/description、用真实任务迭代；**安全**：只装可信来源，装前读指令和脚本。**用来**：0003 Skill 结构、渐进加载、创建技巧与安全；0003「MCP 还是 Skill」里"技能可带脚本、但不是带 schema 的 callable"那一句；0003 的 skill 骨架。

- [Martin Fowler — "Harness engineering for coding agent users"](https://martinfowler.com/articles/harness-engineering.html)
  那个关键公式的出处："harness 指 agent 里除模型本身之外的一切 —— **Agent = Model + Harness**"。**用来**：讲 harness 与 agent 的术语区别。
- [LangChain — "The Anatomy of an Agent Harness"](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness)
  同一公式，并拆解 harness 的组成（代码、配置、执行逻辑）。**用来**：讲 harness 里都有什么零件。
- [Databricks — "What is an AI Agent Harness?"](https://www.databricks.com/blog/ai-harness)
  白话定义："围在语言模型外面的**软件脚手架**——工具、记忆、沙箱、反馈回路——**把模型变成 agent**"。**用来**：给初学者的定义。
- [LangChain — "How to Build a Custom Agent Harness"](https://www.langchain.com/blog/how-to-build-a-custom-agent-harness)（2026-10-18 抓）
  **task-harness fit**：壳要和任务需要的上下文、失败模式、策略、环境匹配；harness 能力表（上下文防溢出、记忆、执行环境、子任务、重试/降级、策略、人审、成本）；middleware 在 loop 的模型调用/工具调用前后挂钩。**用来**：0005「没有最好的 harness，只有任务-壳匹配」和五个子系统的补充。
- [Learn Harness Engineering（开源课程）](https://github.com/walkinglabs/learn-harness-engineering) · [文档站](https://walkinglabs.github.io/learn-harness-engineering/)（2026-10-18 抓）
  **五个子系统**：Instructions（按需加载的指令结构）· State（进度/feature list/磁盘状态）· Verification（测试通过才算完成）· Scope（一次一个 feature）· Session Lifecycle（开始初始化、结束留干净状态）。**用来**：0005 §3 五个子系统、长任务交接。
- [Anthropic — "Effective harnesses for long-running agents"](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)（2026-10-18 抓）
  **长任务 harness 的实证**：initializer agent 先写 feature list/init.sh/progress/git commit；coding agent 每次读状态、只推一个 feature、端到端测试、提交并更新进度；四类翻车（一口吃成、过早宣布完成、留烂摊子、没测就说完成）。**用来**：0005 §4 长任务跨会话、状态/验证/范围/收尾。

- [Anthropic — Extended thinking（官方文档）](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)
  **2026-10-06 补核**：其「Prompt caching in manual mode」一节给了一个**三步实测**（思考块 + 系统提示共 1370 token）——第 1 次 `cache_creation_input_tokens=1370, cache_read_input_tokens=0`；第 2 次（**thinking 参数不动**）`cache_creation=0, cache_read=1370`（命中）；第 3 次（**改了 budget**）`cache_creation=1370, cache_read=0`（不命中，**前缀作废重算并重写**）。同一节还给出两个参数名：**`budget_tokens`**（旧模式，给一个 token 目标，**是目标不是硬上限**）与 **`output_config: {effort: ...}`**（新模式，low/medium/high 分档，原话"用它代替 token 预算来控制推理深度"），并明说**在新模式里 effort 扮演 budget_tokens 在这里的角色**。**用来**：讲"改 thinking 配置会让缓存连系统提示和工具定义一起作废"，也是第 3 课进阶 Q1 那张表的出处。⚠ 注意**这一页不是 prompt-caching 那页**，讲缓存计费/命中规则要去 Prompt caching。
- [Anthropic — Prompt caching（官方文档）](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
  多轮对话的缓存表（**上一轮模型的回答会在下一轮成为前缀、被命中**）、断点机制、以及"往回最多查 20 个位置"的窗口。**2026-10-05 补核**：同一页还给出了 ① **哪些模型保留 thinking blocks**（Opus 4.5+ / Sonnet 4.6+ 默认保留、缓存仍有效；更早的 Opus/Sonnet 与所有 Haiku 剥除，并把跟在后面的消息也从缓存移除）② **改 thinking 配置会让缓存前缀作废、连系统提示与工具定义一起作废**（配置被渲染进 prompt）③ **写入计价 1.25×（5 分钟）/ 2×（1 小时）、读取约 0.1×** ④ **核对是否命中的官方方法：看 `cache_read_input_tokens` 与 `cache_creation_input_tokens`，两者都是 0 就是没缓存且不报错** ⑤ 最小可缓存长度按模型 512/1024/2048/4096 ⑥ **"缓存条目要等第一个响应开始之后才可用"——并发请求想命中就得等第一个响应回来**。**用来**：讲多轮命中与"前缀越长不一定越好"的坑；也是第 3 课进阶版 Q2/Q3/Q5 的出处。
  **2026-10-06 补核（Q2 重写的全部依据）**：这一页现在把缓存分成**两种模式**，讲 Q2 时**必须先分清** ——
  - **三种核心规则的原话**：① "Cache writes happen only at your breakpoint… **a hash of the prefix ending at that block**. The system does not write entries for any earlier position" ② "Cache reads look backward for entries that **prior requests** wrote… **It is looking for prior writes, not for stable content**" ③ "The lookback window is **20 blocks**… counting the breakpoint itself as the first"；**同一段还规定 "a run of consecutive `tool_use` blocks counts as one position, and so does a run of consecutive `tool_result` blocks"**。
  - **自动缓存（新增功能，旧稿完全没提）**：请求**顶层**写一个 `cache_control` → "the system automatically applies the cache breakpoint to **the last cacheable block**"，随对话增长自动前移；**它与显式断点共用那 4 个槽位**，20 块窗口等规则完全相同。⚠ **官方明确说自动模式踩同一个坑**："Automatic caching hits the same trap: it places the breakpoint on the last cacheable block, which in this structure is the one that changes every request"——所以"标在每次都变的那块后面"这条坑对新旧两种模式都成立。
  - **官方那个 10 → 15 → 35 块的例子**（Q2 那张三行表）：第 3 轮 "checks 20 positions (blocks 35 through 16)… The turn-2 entry at block 15 is **one position outside the window**"。
  - **"Common mistake: Breakpoint on content that changes every request"**：请求 1 写在第 6 块（含时间戳）、请求 2 时间戳变了 → 回退经过 5/4/3/2/1 但**那些位置从没写过** → 一次都不命中，还每次付写入费。
  - **参数放法（Q2 那段 JSON 照它抄）**：工具定义上标**最后一个** tool；`system` 数组里那块标；最后一条用户消息的 `input_text`/`text` 块里标。
  - **"Cache breakpoints themselves don't add any cost"** —— 断点本身免费，**别写成"多打断点要多花钱"**。
  - **四个断点的完整例子**：第 1 次请求 `cache_creation` = 四个段全部；后续只加一句用户消息时 `cache_creation` = **只有新增那一段**（新用户消息 + 上一轮助手回复）、`cache_read` = 之前所有已缓存的。→ **存的是完整副本，收的是增量**。
  - **最短的缓存写法**：`max_tokens: 0` 预热请求（"reads your prompt into the model and writes the cache… returns immediately without generating any output"），且预热必须用**与正式请求相同的 thinking 配置与 effort**。
  - **存储与留存**："Prompt caching is ZDR eligible… Anthropic does not store the raw text… **KV representations and cryptographic hashes** of cached content are held in memory only and are not stored at rest"；缓存条目**按组织与 workspace 隔离**。→ **"指纹"＝ 那些 cryptographic hash 之一**。
- [Google — Gemini Context caching（官方文档）](https://ai.google.dev/gemini-api/docs/caching)
  **默认开启的隐式缓存**（Gemini 2.5 及以后全部模型，用户**什么都不用做**）：最小 token 数按模型 4096（Flash 系 / 3.1 Pro）或 2048（2.5 Pro/Flash）；命中数在 `usage.total_cached_tokens`。另一条关键信息：**显式缓存＝"manually creating and managing cache objects"，且 Interactions API 不支持、要用 `generateContent` API** → 所以 Gemini 的"显式"**不是请求里的一个标记，形状完全不同**。**用来**：讲"断点有两种流派"时的那一行。（⚠ 这一页 2026-09-02 更新，隐式部分完整；显式那节在页面上是懒加载的，我**没取到正文**，所以只引它明说的两句。）
- [DeepSeek — Context Caching（官方文档）](https://api-docs.deepseek.com/guides/kv_cache)
  **默认开启、代码一行不改**：系统自己在四种位置切出"缓存单元"——**用户输入末尾、模型输出末尾、检测到的公共前缀、固定 token 间隔**；"Each cached prefix is an **independent, complete unit**"，后续请求必须**完整对上**一个单元才算命中。usage 字段是 `prompt_cache_hit_tokens` / `prompt_cache_miss_tokens`（**字段名与其他家都不一样**）；"best-effort，不保证 100% 命中"；缓存通常几小时到几天后自动清。**用来**：讲"断点不是只有 Claude 有"、以及"每个缓存单元都是完整的一份"。

- [Anthropic — Thinking in tool and multi-turn workflows（官方文档）](https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows)
  多轮与工具场景下 thinking block 的处置规则：**"完整、不改动地把 thinking blocks 带回来"**、**"原样回传那条助手消息"——重建它或过滤掉里面的块会触发 400 报错**。**用来**：讲"思考内容带不带回去是客户端的义务"，以及为什么"能正常用就说明客户端已经做了"。
- [Anthropic — Tool use with prompt caching（官方文档）](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching)
  工具调用与缓存的配合（工具结果落在前缀的哪个位置、断点该打在哪）。**用来**：讲"工具结果算输入前缀的一部分"的官方依据。
- [OpenAI — Prompt caching（API 指南）· 断点那一节](https://developers.openai.com/api/docs/guides/prompt-caching)
  **2026-10-06 补核（讲"OpenAI 也支持断点"时必须带的前提）**：`prompt_cache_options: {mode: "implicit"|"explicit"}` ＋ 块上的 `prompt_cache_breakpoint: {mode: "explicit"}`，**只出现在 Responses API 的例子里、只对 GPT-5.6 及以后有效**；"**Earlier models: Only implicit caching is supported**"（隐式断点按模型定的间隔打）。**显式-only 模式下不打标记就完全不缓存**（"the request does not use prompt caching or create cache writes"），隐式断点打在**最新一条合格消息**末尾（合格＝user 消息、连续一串 tool 响应里的最后一个、开头那串 developer 消息里的最后一个）。**查找边界（不是"块数"）**：显式 = "the first 2 and latest 50 explicit breakpoints"；隐式 = 上述 ＋ 隐式断点 ＋ "up to 20 earlier eligible message endings" ＋ 开头那串 developer 消息末端。每次请求最多 **4 次写入**，隐式断点占掉一个槽位。**GPT-5.6+ 的迁移陷阱**（文档单列一节 "A shared prefix is not always a cached prefix"）：以前"第一个请求隐式缓存了整条"就会让较短的前缀可复用，新行为下**不再如此**——要在稳定内容之后**另加一个显式断点**。最小可缓存长度 **GPT-5.6+ 为 1024**，隐藏 system token 不计入；`cached_tokens` = 减去隐藏 system token 后**向下取整到 128 的倍数**。**用来**：Q2 那张两派对照表；以及"厂商行为断言要写清对谁成立"（5.13.4）的又一个例子 —— **"OpenAI 支持手动断点"这句话离开版本与 API 就是假的**。
- [OpenAI — Prompt caching（API 指南）· 路由那一节](https://developers.openai.com/api/docs/guides/prompt-caching)
  **2026-10-05 补核**：**"缓存状态存在单台机器上，一个请求只有被路由到那台持有匹配且未过期条目的机器才撞得上"**；流量超过 **15 请求/分钟**可能触发 overflow routing；`prompt_cache_key` **separates cache reuse between groups of requests and helps optimize cache routing**（GPT-5.6 及以后路由自动、不需要它），且官方明说 **"keys influence routing; they do not pin requests to a machine or guarantee a cache hit"**。**用来**：讲"为什么有时前缀一样却不命中"——答案常常不是 prompt 写错了，而是没落到同一台机器上。
- [xAI — Prompt caching（多轮）](https://docs.x.ai/developers/advanced-api-usage/prompt-caching/multi-turn)
  三种打断缓存的真实例子：改早期消息、删消息、调换顺序；并指出推理模型**不带回思考内容**是缓存失效的头号原因。⚠ **2026-10-05 更正**：这条只对**较老**的模型成立 —— 按 Anthropic 现行文档，Opus 4.5+ / Sonnet 4.6+ **默认保留**思考块、缓存不受影响。讲这一段时**以 Anthropic 那份为准**，xAI 这条只用来支撑"三种打断方式"。**用来**：讲"只追加、不修改"的后果。

- [Anthropic — "Demystifying evals for AI agents"（官方工程文）](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
  **本缺口的首选答案**：跨框架、不讲具体工具，只讲方法论。四个概念（**task / trial / grader / evaluation harness**）；打分的两个对象（**transcript 轨迹** vs **outcome 结果**）；三类 grader（代码 / 模型 / 人）；**pass@k vs pass^k**（能力 vs 一致性）；**regression evals vs capability evals**；以及几条反直觉的忠告 —— "别拿固定步骤路径判分（会误杀好方案）""LLM 评委必须与人类专家校准，并给它 'Unknown' 这个出口""读 transcript 是 agent 开发的核心技能"。**用来**：讲"怎么量化一个 agent 变好了"。
- [τ-bench（Yao et al., 2024）](https://arxiv.org/abs/2406.12045)
  **`pass^k` 这个指标的出处**。评测"工具-智能体-用户"三方交互：用 LLM 扮演用户、给智能体工具和业务规则，**比对最终数据库状态**判成败（而不是比对固定的工具调用路径）。实测数字很说明问题：最强 agent 单次成功率 >60%，但**连续 8 次全对的比例 <25%**。**用来**：讲"一致性"这个维度。（仓库：`sierra-research/tau2-bench`）
- [Inspect AI（英国 AI 安全研究所）](https://inspect.aisi.org.uk/evals/)
  **跨框架的开源评估框架**：内置 ReAct / deep agent / multi-agent，并提供 **Agent Bridge** 接入第三方框架（OpenAI Agents SDK、LangChain、Pydantic AI）。**用来**：需要"工具"而不只是"方法论"时。
- [AgentBench（Liu et al., 2023）](https://arxiv.org/abs/2308.03688)
  多环境基准：**8 个不同环境**（代码、游戏、网页、操作系统、数据库…），测 LLM-as-Agent 的推理与决策；论文梳理了典型失败原因。**用来**：想看"跨环境广度"的基准时。

### RAG 系列（2026-10-21 重构扩充）

> RAG 轨 2026-10-21 起改制为「理论课＋实操课（RAGFlow 实验台）」，新课表与施工批次见根目录 `RAG-REVISION-PLAN.md`。本节前两段（原论文、切块与评估）为旧制时代存量，其后四段为改制当日扩充。

- [Lewis et al. — "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"（NeurIPS 2020）](https://arxiv.org/abs/2005.11401)
  **RAG 这个名字的原始出处**。核心说法："模型对知识的访问与精确操控能力仍然有限""给出来源、更新世界知识仍是未解问题"。最值钱的一句结论：<b>换掉那份资料索引就能更新知识，不用重新训练</b>。**用来**：讲"RAG 到底在补什么、它不改模型"。
- [Anthropic — "Introducing Contextual Retrieval"（2024-09）](https://www.anthropic.com/engineering/contextual-retrieval)
  工业界怎么做检索那一步，带**实测数字**：取前 20 段时没取到正确那段的比例，普通 RAG **5.7%** → 给每段补一句"这段在讲什么" **3.7%** → 叠上关键词检索 **2.9%** → 再加重排序 **1.9%**。**用来**：证明"RAG 的技术性全在前五步、没有一步是换更强模型"。
- [Liu et al. — "Lost in the Middle: How Language Models Use Long Contexts"（2023）](https://arxiv.org/abs/2307.03172)
  **"检索到 ≠ 用上"的出处**：相关信息放在长上下文**中间**时成绩显著下降，**GPT-3.5 在多文档问答上甚至低于完全不给文档的水平**；给 20 篇以上收益几乎归零（GPT-3.5 约 +1.5%、Claude-1.3 约 +1%）。**用来**：讲"检索完还要管顺序"以及"别一味堆资料"。

- [Pinecone — "Chunking Strategies for LLM Applications"](https://www.pinecone.io/learn/chunking-strategies/)
  固定长度 / 递归 / 语义三档切法的**定义与取舍**，并明确说"**先从固定长度起步，确定不够再迭代**"。**用来**：给"切块有哪几档"提供标准分类。
- [Anyscale — "RAG evaluation"](https://docs.anyscale.com/rag/evaluation)
  **"分开评"的出处**："先分别评检索与生成，再评端到端——这样才能定位瓶颈、正确归因"。给全 Precision@k / Recall@k / Hit rate@k / MRR / MAP 的定义与取舍。**用来**：讲 RAG 该怎么评、为什么不能只看最终答案。
- [RAGAS — "List of available metrics"](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/)
  Context Precision / Context Recall / **Faithfulness**（"答案里的断言能否追溯到检索到的上下文"）那一套。**用来**：讲生成侧的忠实度。
- [Evaluation of Retrieval-Augmented Generation: A Survey（2024）](https://arxiv.org/html/2405.07437v2)
  各框架（RAGAS / ARES / TruLens / DeepEval…）指标的**对照表**。**用来**：知道"同一个概念各家叫法不同"。

**概念地图（0001/0002/0003/0012 用 · 2026-10-21 抓）**

- [Pinecone — "Retrieval-Augmented Generation (RAG)"](https://www.pinecone.io/learn/retrieval-augmented-generation/)
  基础模型的五类局限（**知识截止／领域知识浅／拿不到私有数据／不可溯源／概率性生成**）与 RAG 四组件（**Ingestion → Retrieval → Augmentation → Generation**）；四条好处（实时与私有数据、信任与引用、可控、比训练/微调/硬塞上下文省钱）。**agentic 演进**（官方收尾口径，引号内为原话）：agent 当 RAG 组件的编排者——"construct more effective queries"（构造更有效的查询）、"access additional retrieval tools"、"evaluate the accuracy and relevance of the retrieved context"、"apply reasoning to validate retrieved information"（推理验证後再决定信不信）。**用来**：0001 三短板、0002 四组件地图、0003 三选一、0012 Agentic 收尾。

**RAGFlow 实验台（0004/0005 用 · 2026-10-21 抓）**

- [RAGFlow — quickstart（官方文档）](https://ragflow.io/docs/)
  部署门槛原文："**4 CPU cores (x86-64), 16 GB RAM, and 50 GB free disk space**"；Docker ≥24.0.0＋Compose ≥v2.26.1；`vm.max_map_count`≥262144；流程＝起服务→配模型→建 dataset 传文件解析→检索测试→建 chat。两条**定义级原话**：① **嵌入锁定**——"Once you have selected an embedding model and used it to parse a file, **you are no longer allowed to change it**"（同一库必须在同一嵌入空间；换模型＝新建库全量重嵌）；② **Empty response**——填了则把回答限定在知识库内（检索不到就统一回这句话），留空则模型自由发挥（"may give rise to hallucinations"）。另有：Chunk 页可人工给块加关键词/问题提权。**用来**：0004 部署与验通路、0006"换模型全重算"、0009 拒答设置。
- [RAGFlow — Dataset Configuration（官方文档）](https://ragflow.io/docs/dataset_configuration)
  **12 种内置解析模板**：General／Q&A（每对一块）／Manual（按手册层级）／Table（每行一块）／Paper／Book／Laws／Presentation（每页一块）／One（整篇一块）／Tag／Audio（ASR）／Email；官方选法原话"choose the parsing method based on the form of the material"（常规先 General、表格先 Table）。**切块器参数**：chunk size 默认 **512 token**（"a target rather than a strict limit"）／overlap ratio（%）／自定义分隔符／表格与图片前后文窗口／**sub-chunks 父子块**（小块检索、父块供上下文）。**标题切块器两模式**：Hierarchy（块带完整标题路径，适合法规契约）vs Group（同层相邻小节合并，适合书/手册/报告）。**Extractor**：自动关键词／自动问题／标签／**Augmented context（给每块生成上下文摘要——与 Anthropic Contextual Retrieval 同思想）**／元数据。**Indexer**：Embedding／Full-text／双开（官方建议双开）；索引字段三选（Processed text／Questions／Augmented context）。⚠ 改解析配置后需重新解析才生效。**用来**：0002 面板对照表、0005 切块、0007 检索配置、0012 顺带一句 Knowledge Compilation。
- [Windows Docker Desktop 部署 RAGFlow 0.17.2 避坑实录（CSDN）](https://blog.csdn.net/weixin_31220401/article/details/168435333)（⚠ 个人博客，经验值需实操校核）
  Windows 五坑全清单：① 镜像拉取断→registry mirror；② ES 反复重启→WSL2 内存不足（`.wslconfig` memory=12GB/processors=6/swap=4GB ＋ `wsl --shutdown`，ES 堆限 2G）；③ 解析永久 pending→解析/嵌入模型没下载成（HF_ENDPOINT 指镜像端点或先手动下好模型再建库）；④ 挂载卷读不到→路径避开中文/空格/同步盘、用正斜杠；⑤ 登录页打不开→宿主端口映射与防火墙（默认 80 常冲突，改 9380 类）。**调参顺序法则**：先解析→再切块→最后才动检索参数（"检索参数影响找到什么，切块参数影响怎么被找到"）。中文经验值：chunk 300~500 token、overlap 50~100、top_k 8~12、相似度阈值 0.2~0.3。**用来**：0004"怎么不翻车"节、0005/0007 经验参考。⚠ 该文基于 0.17.2（Python 后端 zip 部署），与已选官方现行版（1.0.0-rc2 Go 后端）流程有出入，施工时以官方文档为准校对。

**评测实战（0010/0011 用 · 2026-10-21 抓）**

- [RAGAS＋RAGFlow 5 组配置评测实战（CSDN，2025-10）](https://blog.csdn.net/m0_59235945/article/details/153839845)（⚠ 第三方实测——作实验设计蓝本，数字不可当基准）
  场景＝员工手册知识库（考勤休假/报销/福利/员工信息表），与本项目年假贯穿例同款。**5 组对照**：baseline（top_n=8, 阈值 0.2, temp 0.1）／high_recall（15, 0.15）／high_precision（5, 0.3）／anti_hallucination（检索不变＋prompt 强约束）／contextual（12＋CoT prompt）。**结果与三个反直觉**：high_recall 三指标全最佳（Context Recall 1.0／Answer Relevancy 0.597／Faithfulness 0.477）；high_precision 与 anti_hallucination 的 Answer Relevancy **归零（全拒答）**；anti 的 Faithfulness 仅 **0.025**——不是不忠实，是 Ragas 把"拒答"判为不忠实（评估假设与业务目标错位）；过度约束 prompt 反噬。**测试集三挑战**：代表性＞数量（10-15 道精题＞100 道泛化题）；LLM 初稿＋专家改写（"员工的年假政策是什么" vs "我 2021 年 3 月入职现在能休几天"）；GT 标注"够用即可"、条件分支写明限定词、核心题全标＋边缘题轻量评。**稳定指标**：context_precision 与 answer_correctness 常返 NaN，重点看 Context Recall／Answer Relevancy／Faithfulness；附"低分→优化方向"对照表。另：RAGFlow Manual 模式分块（Document.add_chunk API、按章节精确控块、跳过解析）。**用来**：0011 实验设计蓝本（主体）、0010 翻车与归因数字。

**查询与 Agentic 前沿论文（0008/0012 用 · 2026-10-21 核摘要）**

- [Gao et al. — "Precise Zero-Shot Dense Retrieval without Relevance Labels"（HyDE · arXiv 2212.10496）](https://arxiv.org/abs/2212.10496)
  **HyDE 一手出处**：先让 LLM 生成假想文档（"captures relevance patterns but is unreal and may contain false details"），用无监督编码器把它编码成向量去检索真文档——"the encoder's dense bottleneck **filtering out the incorrect details**"（编码瓶颈天然滤掉假细节）。**用来**：0008——"答案的语义空间比问题更接近文档"。
- [Zheng et al. — "Take a Step Back"（Step-Back Prompting · ICLR 2024 · arXiv 2310.06117）](https://arxiv.org/abs/2310.06117)
  **Step-back 一手出处**：先从具体问题抽象出上位概念/原理再推理；PaLM-2L 在 MMLU 物理 +7%、化学 +11%、TimeQA +27%、MuSiQue +7%。**用来**：0008——"拿上位问题去检索背景知识"一支。
- [Asai et al. — "Self-RAG"（ICLR 2024 · arXiv 2310.11511）](https://arxiv.org/abs/2310.11511)
  **Self-RAG 一手出处**，两句关键：传统 RAG "indiscriminately retrieving and incorporating a fixed number of retrieved passages, regardless of whether retrieval is necessary, or passages are relevant, **diminishes LM versatility**"；Self-RAG "adaptively retrieves passages **on-demand**…using special tokens, called **reflection tokens**"（反思 token 控制检索时机与自我批判）。**用来**：0012。
- [Yan et al. — "Corrective Retrieval Augmented Generation"（CRAG · arXiv 2401.15884）](https://arxiv.org/abs/2401.15884)
  **CRAG 一手出处**：轻量**检索评估器**给检回文档打置信度、据此触发不同检索动作；静态语料不够时**网搜兜底**；"decompose-then-recompose"选择性聚焦关键信息。**用来**：0012。

**工程经验综述（0007/0009 用 · 2026-10-21 抓 · ⚠ 二手，引用时标"经验"）**

- [12 种 RAG 前沿增强技术与落地选型（CSDN，2026-10）](https://blog.csdn.net/weixin_29039773/article/details/168187407)
  增强方法按五环节归类（查询/索引/检索/重排/生成）；好用口径："**基础 RAG＋混合检索＋重排＋干净切块**解决 80% 的问题"；HyDE 适用边界（短查询适合/完整句不适合）与温度 0~0.3；RRF 公式 k=60 起步；重排后设分数阈值丢噪声；Agent 调用设上限。**用来**：0007/0008 结构参考与经验口径。
- [RAG 系统化拆解：索引/检索/生成的工程实践与调优（CSDN，2026-10）](https://blog.csdn.net/weixin_32377497/article/details/168161496)（⚠ 个人博客）
  工程细节：约束式 prompt 模板四块（指令/资料/问题/约束，核心是"资料中没有就明确回答'未找到相关资料'，严禁编造"）；"召回 50 → 精排取 5"两阶段量级；temperature 0.1~0.2；**幻觉先归因检索**（"先把检索到的 chunk 打印出来，人工判断模型是不是真的有料可依"）；多轮对话必做查询改写；Recall@5 与 Recall@10 看差定位；chunk_size 改完必须重嵌重建索引。**用来**：0007/0009/0010 经验素材（与一手数字分开标注）。

### 记忆（Agent 篇第 1 课记忆节 · 2026-10-17 新增，2026-10-18 补产品口径）

- [OpenCode — Rules（官方文档）](https://opencode.ai/docs/rules/)（2026-10-18 抓）
  **跨会话靠规则文件，不是记忆子系统**：项目根 `AGENTS.md`（也兼容 `CLAUDE.md`）、全局 `~/.config/opencode/AGENTS.md`，这些指令"will be included in the LLM's context"；另有 `opencode.json` 的 `instructions` 字段可挂外部文件。文档里没有"长期记忆"这一层。**用来**：0001 记忆节"OpenCode 不内置长期记忆"那一例（按这一版文档）。
- [Supermemory — How it works（官方文档）](https://supermemory.ai/docs/concepts/how-it-works)（2026-10-18 抓）
  **记忆服务的存/取**：`add` 文档 → 切块、抽记忆（不是原文）→ 时序向量图；输出三样：chunks（RAG 用）、memories（事实图）、profile（常驻摘要）；`search` 取回；`dreaming` 是后台把相关记忆连起来/合并的阶段。**用来**：0001 的 Supermemory 一例。
- [Supermemory — Graph memory（官方文档）](https://supermemory.ai/docs/concepts/graph-memory)（2026-10-18 抓）
  **记忆怎么变、怎么忘**：关系三种 `updates`（新事实替换旧的，历史可留）、`extends`（补细节）、`derives`（推断出没明说的）；记忆类型 `facts` / `preferences` / `episodes`（**episodes 会衰减**）；自动遗忘三种：时间过期、矛盾更新、噪音过滤；也可显式 forget/update。**用来**：0001 的"按内容分"（facts/preferences/episodes）与"自动遗忘"。
- [Mem0 — How Mem0 Works（官方文档）](https://docs.mem0.ai/core-concepts/how-it-works)（2026-10-18 抓）
  **事实抽取 + 多路检索**：`add` 抽 durable facts，存 SQL（事实）、向量库（embedding）、实体库（实体）；`search` 融合语义/关键词/实体/时间四个信号；按 user/agent/run 隔离。**用来**：0001 的 Mem0 一例。
- [Mem0 — Add Memory（官方文档）](https://docs.mem0.ai/core-concepts/memory-operations/add)（2026-10-18 抓）
  **现在是 ADD-only**："New memories are added without overwriting or deleting existing memories"；要改旧/删旧得显式 update/delete；`infer=False` 才原样存。**用来**：0001 的"默认只追加"以及"论文四动作 vs 现产品口径"的对照。
- [Sumers et al. — "Cognitive Architectures for Language Agents"（arXiv 2309.02427）](https://arxiv.org/abs/2309.02427)
  **记忆三分法的出处**：经历（episodic）／事实（semantic）／做法（procedural）与"工作记忆"并列的认知架构分层。**用来**：讲"研究文献按内容分三种"；⚠ 它是研究分法，不是产品标准（0001 已改成按产品讲）。
- [Chhikara et al. — "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory"（arXiv 2504.19413）](https://arxiv.org/abs/2504.19413)
  **记忆四个动作的出处**：提取阶段抽出候选事实，更新阶段由模型用**工具调用**在 **ADD / UPDATE / DELETE / NOOP** 里挑一个（覆盖式做法的代表）。⚠ **2026-10-18 复核**：现产品文档写的是 **ADD-only**（新记忆只追加，改旧要显式 update/delete），四动作是**论文当时**的口径；引用时写清"论文"还是"产品"，别把论文当现状。**用来**：0001 的 Mem0 段与"口径会变"那一条。
- ["Zep: A Temporal Knowledge Graph Architecture for Agent Memory"（arXiv 2501.13956）](https://arxiv.org/abs/2501.13956)
  **留痕式做法的代表**：双时间知识图——旧事实**标失效、不删除**，按时间仲裁"当时是什么"。**用来**：讲"推翻的旧条目删不删"的两种做法与取舍。
- [Wu et al. — "LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory"（ICLR 2025 · arXiv 2410.10813）](https://arxiv.org/abs/2410.10813)
  **"记忆怎么评"的尺子**：五个能力（信息提取／跨会话串联／时间推理／知识更新／**该说不知道**）；S 档约 115k token、M 档约 150 万。**用来**：讲验收五能力与"分数先问口径"。
- [Maharana et al. — "Evaluating Very Long-Term Conversational Memory of LLM Agents"（LoCoMo，ACL 2024 · arXiv 2402.17753）](https://arxiv.org/abs/2402.17753)
  老牌记忆基准（10 段长对话、约 2000 题，单跳／多跳／时间／开放域）。**用来**：与 LongMemEval 对照，讲"尺子也会饱和（多数系统 80 分上下）"。
- [Packer et al. — "MemGPT: Towards LLMs as Operating Systems"（arXiv 2310.08560）](https://arxiv.org/abs/2310.08560)
  **"记忆即工具"的源头**：分层记忆（主上下文／外部存储）＋模型自己发起存取。产品 Letta 出自它。**用来**：讲"agent 自己管自己的记忆"这一路。
- [NirDiamant — Agent_Memory_Techniques（GitHub 教程仓库）](https://github.com/NirDiamant/Agent_Memory_Techniques)
  30 个可跑 notebook 的记忆技术教程（工作／情节／语义／程序记忆、检索模式、LoCoMo／LongMemEval 跑法）。**用来**：给"想自己动手搭记忆"的延伸阅读。
- [DeepLearning.AI — "Building Adaptive AI Agents"（2026）](https://www.deeplearning.ai/courses/building-adaptive-ai-agents)
  四分类（working／episodic／semantic／procedural）的白话教学口径，与"从 trace 长出技能"的持续学习线。**用来**：核对四分类的讲法别讲歪。
- 厂商自报对比页：[Mem0 — Compare](https://mem0.ai/compare) · [Zep — State of the art agent memory](https://www.getzep.com/blog/state-of-the-art-agent-memory)（均 2026-10-17 抓）
  ⚠ **厂商自报数字，只作"自报"引用**：同尺不同数（LongMemEval 上 Zep 被 Mem0 页记 71.2、自家报 90.2），还有"没跑这块尺子"的。**用来**：速查页对照表的"自报分数"列，以及讲"分数先问谁说的、什么口径、哪天的"。

### Agent 篇重构素材：TeleAgent 案例（2026-10-18 新增）

- [天翼 AI — 星辰超级智能体 TeleAgent《快速上手指南》](https://www.teleai.com.cn/doc/bKrLmQNepNQpUHjWEfqX/pUxSKj00HB5artzpBdgZ)（2026-10-18 抓）
  **0005 对照表的官方引源之一**：安装/工作空间（任务跑在指定文件夹）、`@文件`/`@技能` 引用、任务与历史。**用来**：讲"一个真实 harness 的用户面"。
- [天翼 AI — 《星辰超级智能体·桌面版操作手册》](https://www.teleai.com.cn/doc/7czHMDStGDQr1JsAMKcZ/Gik5VRTWAer7xDrqNBS7)（2026-10-18 抓）
  **0005 对照表的 TeleAgent 素材主源**：技能系统——技能广场/导入（`.zip`／`.skill`；根目录必须有 `SKILL.md`；头部 YAML 写 name/description；≤10MB；导入过安全审查）／**自然语言创建**（技能广场右上角【创建技能】：描述需求、流程、场景，自动生成进"我的技能"）／**「技能孵化器」**（手把手引导从零创建/迭代，见 1.2.2 常用技能）／我的技能（启用/停用、`@` 引用、启用上限 50、上架广场）／**同一技能用 ≥20 次触发自进化** · **授权三选项（允许一次/一直允许/拒绝）＋YOLO 模式** · **MCP 工具管理**（设置→工具设置→从 JSON 导入/添加；`mcpServers` 根对象；服务名、`command`、`args`、`env` 字段；绿色"已连接"；连接/断开/编辑；改工具名后历史任务可能引用不到；示例 `math-server` 用 `npx @modelcontextprotocol/server-everything`）· 代码执行三模式与安全沙箱 · **任务监控区（深度思考/操作执行/任务委派（子智能体））** · 上下文用量查看与清理 · 自定义模型（OpenAI 兼容 Base URL＋Key）· 任务排查五类（文件/技能/工具/模型/网络）。**用来**：0003 MCP 配置与创建技能跟做、0004 安全篇的授权实证、0005 对照表的授权/技能/MCP/消息列。
- **TeleAgent 记忆子系统自述**（2026-10-18 学习者转述，手册无此节，引源标"自述"）：按**来源＋时间尺度**归档（`USER.md`＝用户明说记住的 / `MEMORY.md`＝系统推断的稳定事实 / `daily-log/YYYY-MM-DD.md`＝每日流水）；底层**纯 Markdown 文件**；检索＝**关键词/正则**（`memory_search`）＋按名读取（`memory_get`）；三种载入：USER.md+MEMORY.md **每次自动注入系统提示**、日志**按需检索**、`LATEST_DAILY_MEMORY.md` **滚动摘录**。**用来**：推翻"内容三分法是标准分法"“取回=相似度"两处旧口径（见 `docs/notes/rules/agent-track-redesign.md` §3）。
- [OpenCode — Docs](https://opencode.ai/docs/) · [Agents](https://opencode.ai/docs/agents/) · [Permissions](https://opencode.ai/docs/permissions/) · [MCP servers](https://opencode.ai/docs/mcp-servers/) · [Agent Skills](https://opencode.ai/docs/skills/)（2026-10-18 抓）
  **0005 对照表的 OpenCode 来源**：开源 AI coding agent，终端 TUI/桌面/IDE；任意 provider/API key（含 OpenCode Zen）；Plan/Build primary agents + General/Explore/Scout subagents；按 agent 配 ask/allow/deny；Agent Skills/MCP/插件/自定义工具；AGENTS.md 项目规则；CLI/Server/SDK、GitHub/GitLab。**用来**：四款对照、按场景选。
- [Hermes Agent — Docs](https://hermes-agent.nousresearch.com/docs) · [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security) · [MCP](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)（2026-10-18 抓）
  **0005 对照表的 Hermes 来源**：Nous Research 的自主 agent，MIT；CLI/Desktop/服务器；Nous Portal/OpenRouter/OpenAI/任意 endpoint；60+ 工具、7 种终端后端（本机/Docker/SSH/Daytona/Singularity/Modal/Vercel Sandbox）；Skills/MCP/插件/Bot Mode；approval smart/manual/off + 容器隔离 + 硬黑名单；跨会话记忆/技能自改进；cron + 20+ 消息平台 + 语音。**用来**：四款对照、按场景选。
- [Tencent WorkBuddy — Overview](https://www.workbuddy.ai/docs/workbuddy/Overview) · [Permission Modes](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Permission-Modes) · [Skills](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market) · [Connectors](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Connector) · [MCP](https://www.workbuddy.ai/docs/zh/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/MCP-Guide) · [Model](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Model) · [Automation](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Automation-Guide) · [Memory](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Memory)（2026-10-18 抓）
  **0005 对照表的 WorkBuddy 来源**：腾讯办公桌面工作站（Windows/macOS）；内置+自定义模型（provider 预设/自定义 API/Ollama 本地）；本地文件/文档/表格/PPT/数据；Skill Marketplace/Connectors/MCP；Default Permissions/Full Access + 工作空间/沙箱；对话记忆+夜间摘要；定时/周期任务 + Slack/Telegram/Discord/企微/飞书/钉钉/QQ/微信。**用来**：四款对照、按场景选。
- [Microsoft — AI Agents for Beginners（GitHub）](https://github.com/microsoft/ai-agents-for-beginners)
  18 讲课表（tool use／planning／multi-agent／context engineering／agent memory／protocols／production／securing…）。**用来**：重构课表的对表清单，判"还缺什么"。

- [Anthropic — "How we built our multi-agent research system"](https://www.anthropic.com/engineering/multi-agent-research-system)
  **多 agent 篇（0004 上篇）的主源**：编排者-工作者形状、派单要写清（目标/输出格式/边界，"调研一下 X"这种含糊指令会重复劳动）、只回结论不回流水、失败模式（spawn 50 workers、无限搜寻、互相干扰）；量级全部是**他们自报口径**（简单查证 1 agent 3～10 次调用／对比 2～4 workers·10～15 次／复杂 10+ workers；token 单 agent ×4、多 agent ×15；复杂调研"强编排＋worker"比单强模型 +90.2%）。**用来**：讲"什么时候该上多 agent、怎么分工、账怎么算"。
- [Anthropic — Orchestrator-workers 模式（Cookbook）](https://platform.claude.com/cookbook/patterns-agents-orchestrator-workers)
  编排者动态拆活、worker 各拿一段任务的标准形状与最小实现。**用来**：0004 多 agent 篇的形状依据。

### Agent 篇 0002 实操：真模型接入（2026-10-18 新增，全部当场抓取）

- [DeepSeek — 首次调用 API](https://api-docs.deepseek.com/zh-cn/)（2026-10-18 抓）
  `base_url`（OpenAI 格式）＝`https://api.deepseek.com`；模型名 `deepseek-flash`（旧名 `deepseek-v4-flash` 仍接受，实际由 V4.1-Flash 服务）与 `deepseek-v4-pro`；key 申请页 `https://platform.deepseek.com/api_keys`；官方示例就是 `from openai import OpenAI` ＋ `client.chat.completions.create`。**用来**：0002 第 1～2 节的装包/配 key/模型名，一个字都不凭记忆。
- [DeepSeek — Tool Calls](https://api-docs.deepseek.com/zh-cn/guides/tool_calls)（2026-10-18 抓）
  **非思考模式的完整 Python 例子**：`tools=[{"type":"function","function":{...}}]`，请求带 `extra_body={"thinking": {"type": "disabled"}}`；模型回 `message.tool_calls[0]`，执行后把 `{"role":"tool","tool_call_id": tool.id,"content": ...}` 塞回去。**用来**：0002 的适配层写法和"关掉思考模式"这一步。
- [DeepSeek — Thinking Mode](https://api-docs.deepseek.com/zh-cn/guides/thinking_mode)（2026-10-18 抓）
  **思考模式默认开启**（effort 默认 high）；带 `tools` 的请求**必须把历次 `reasoning_content` 原样传回**，否则 400；不带 `tools` 时传了也被忽略。**用来**：解释为什么 0002 要显式 `thinking: disabled`（否则循环得处理思考内容，主线被带偏）。
- [DeepSeek — 模型 & 价格](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)（2026-10-18 抓）
  `deepseek-flash`：输入（缓存未命中）空闲 ¥1／百万 token、高峰 ¥2；输出空闲 ¥4、高峰 ¥8；缓存命中输入 ¥0.02／¥0.04。**高峰＝北京时间周一至周五 9:00–12:00、14:00–18:00**（不含法定节假日），其余时段空闲。**用来**：0002 第 8 节账单与"一次实操不到一分钱"的量级依据；脚本里的单价常量。
- [DeepSeek — 错误码](https://api-docs.deepseek.com/zh-cn/quick_start/error_codes)（2026-10-18 抓）
  400 格式／401 key 错／402 余额不足／422 参数错／429 限流／500 服务端／503 过载。**用来**：0002 的排错表；脚本把 401／429／其它状态码分开报。
- [OpenAI Python SDK（PyPI）](https://pypi.org/project/openai/)（2026-10-18 抓）
  `pip install openai`；当前 3.35.1，**要求 Python 3.10+**；`OpenAI(api_key=..., base_url=...)` 可用于任何 OpenAI 兼容接口；错误类型 `AuthenticationError`／`RateLimitError`／`APIStatusError`／`APIConnectionError`，默认对连接错误与 5xx 重试 2 次。**用来**：0002 第 1 节装包与第 5 节错误处理。
- [Python — Downloads](https://www.python.org/downloads/)（2026-10-18 只作链接）
  装 Python 的官方入口。**用来**：0002 第 1 节"先确认 python 命令能跑"。

## Wisdom（社区 · 用于真实世界检验）

- [r/AI_Agents](https://www.reddit.com/r/AI_Agents/)
  最大的 agent 讨论社区，有大量实操踩坑与项目分享。**用来**：把学到的判断拿去对撞、看别人怎么翻车。
- Latent Space（Discord / 播客）
  偏工程与前沿的高信噪比社区。**用来**：跟进正在发生的变化，向从业者提问。

## Gaps（尚缺的资源）
- ~~缺一份可靠的、跨框架的 agent 评估资料~~ **已补（2026-09）**：见上面 **Knowledge** 里的四条，首选 Anthropic《Demystifying evals for AI agents》
- 缺中文的高质量一手资料（目前几乎全是英文）
- ~~缺 **多 agent 协作**的高可信工程资料~~ **已补（2026-10-18）**：Anthropic《How we built our multi-agent research system》（带实测量级、派单与失败教训）＋Orchestrator-workers Cookbook——`agent/0004` 已开课。

> AI生成
