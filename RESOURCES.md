# AI Agent 资源

本课程的知识只能来自这里的来源，不能来自我的记忆。每条都注明"用来干什么"。

## Knowledge（知识来源）

- [Anthropic — "Building effective agents"](https://www.anthropic.com/engineering/building-effective-agents)
  最重要的入门工程文章。讲清 workflow 与 agent 的区别、五种常见编排模式（提示链、路由、并行、编排者-工作者、评估者-优化者）。**用来**：建立正确的第一心智模型，避免过度设计。
- [Lilian Weng — "LLM Powered Autonomous Agents"](https://lilianweng.github.io/posts/2023-06-23-agent/)
  经典的"三大支柱"框架：Planning / Memory / Tool Use。**用来**：给整个领域画地图、确定课程结构的骨架。
- [OpenAI — "A practical guide to building agents"（PDF）](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
  面向产品/工程团队的实践指南，覆盖单 vs 多 agent、工具设计、护栏与人机协同。**用来**：从原理过渡到工程取舍。
- [Chip Huyen — "Agents"（博客，2025-01）](https://huyenchip.com/2025/01/07/agents.html)
  《AI Engineering》作者对 agent 的清晰拆解，尤其擅长讲**失败模式**与评估。**用来**：讲"会在哪里失败"。
- [Chip Huyen —《AI Engineering》(O'Reilly)](https://www.oreilly.com/library/view/ai-engineering/9781098166298/)
  第 6 章 "RAG and Agents"。**用来**：需要更系统、可作为长期参考的教科书内容时。
- [ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., ICLR 2023)](https://arxiv.org/abs/2210.03629)
  现代 agent 循环范式的原始论文：交替产生"推理轨迹"与"动作"。**用来**：讲清循环的理论来源。
- [Anthropic — "Effective context engineering for AI agents"](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  讲上下文是稀缺资源、如何管理。**用来**：讲记忆与上下文窗口的取舍。
- [DeepLearning.AI — "Agentic AI"（Andrew Ng）](https://www.deeplearning.ai/courses/agentic-ai)
  动手型课程，讲多步 agentic workflow 的构建。**用来**：作为需要视频+练习时的补充。

## Wisdom（社区 · 用于真实世界检验）

- [r/AI_Agents](https://www.reddit.com/r/AI_Agents/)
  最大的 agent 讨论社区，有大量实操踩坑与项目分享。**用来**：把学到的判断拿去对撞、看别人怎么翻车。
- Latent Space（Discord / 播客）
  偏工程与前沿的高信噪比社区。**用来**：跟进正在发生的变化，向从业者提问。

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
- [ClickHouse — "LLM inference latency: TTFT, tokens per second"](https://clickhouse.com/resources/engineering/llm-inference-latency)
  用一条真实时间线（3200 token 输入 → 400ms 首字 → 410 token 输出 → 12.7s）解释 TTFT 与 TPOT 的分工。**用来**：讲两个延迟指标。
- [Anyscale — "Understand LLM latency and throughput metrics"](https://docs.anyscale.com/llm/serving/benchmarking/metrics)
  官方指标定义（TTFT、吞吐）。**用来**：术语对齐。

- [Anyscale — "How continuous batching enables 23x throughput in LLM inference"](https://www.anyscale.com/blog/continuous-batching-llm-inference)
  把"加载一次模型权重、服务多个请求"的机制讲得最清楚，并给出 vLLM 实测 23 倍。**用来**：讲批处理的原理与收益。
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

- [OpenAI — "Function calling"（官方指南）](https://developers.openai.com/api/docs/guides/function-calling)
  官方机制说明：把函数写成 **JSON schema**（名字 + 描述 + 参数）传给模型，模型返回一份"要调哪个函数、参数是什么"的**结构化输出**，由你的应用去执行。**用来**：讲工具调用的完整来回。
- [Anthropic — "Introducing advanced tool use"](https://www.anthropic.com/engineering/advanced-tool-use)
  Anthropic 官方工程文：模型返回 <code>tool_use</code> 块（工具名 + 输入），你的代码执行后把结果以 <code>tool_result</code> 送回，模型接着走。**用来**：讲 tool_use / tool_result 这一对来回。

- [Model Context Protocol — 官方文档](https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro)
  MCP 是"把 AI 应用连到外部系统"的**开放标准**。server 公布 **tools / resources / prompts** 三类能力，client 通过**发现**机制先问"你能干什么"，不用硬编码 endpoint。**用来**：讲工具的标准化与即插即用。
- [Anthropic — "Equipping agents for the real world with Agent Skills"](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
  Skill 的设计理念：把**指令 + 元数据 + 可选资源（脚本、模板）**打包成一个目录；**渐进式加载（progressive disclosure）是核心设计原则**——"像一本组织良好的手册"，只先给目录。**用来**：讲 skill 与按需加载。

- [Martin Fowler — "Harness engineering for coding agent users"](https://martinfowler.com/articles/harness-engineering.html)
  那个关键公式的出处："harness 指 agent 里除模型本身之外的一切 —— **Agent = Model + Harness**"。**用来**：讲 harness 与 agent 的术语区别。
- [LangChain — "The Anatomy of an Agent Harness"](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness)
  同一公式，并拆解 harness 的组成（代码、配置、执行逻辑）。**用来**：讲 harness 里都有什么零件。
- [Databricks — "What is an AI Agent Harness?"](https://www.databricks.com/blog/ai-harness)
  白话定义："围在语言模型外面的**软件脚手架**——工具、记忆、沙箱、反馈回路——**把模型变成 agent**"。**用来**：给初学者的定义。

- [Anthropic — Prompt caching（官方文档）](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
  多轮对话的缓存表（**上一轮模型的回答会在下一轮成为前缀、被命中**）、断点机制、以及"往回最多查 20 个位置"的窗口。**用来**：讲多轮命中与"前缀越长不一定越好"的坑。
- [xAI — Prompt caching（多轮）](https://docs.x.ai/developers/advanced-api-usage/prompt-caching/multi-turn)
  三种打断缓存的真实例子：改早期消息、删消息、调换顺序；并指出推理模型**不带回思考内容**是缓存失效的头号原因。**用来**：讲"只追加、不修改"的后果。

- [Anthropic — "Demystifying evals for AI agents"（官方工程文）](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
  **本缺口的首选答案**：跨框架、不讲具体工具，只讲方法论。四个概念（**task / trial / grader / evaluation harness**）；打分的两个对象（**transcript 轨迹** vs **outcome 结果**）；三类 grader（代码 / 模型 / 人）；**pass@k vs pass^k**（能力 vs 一致性）；**regression evals vs capability evals**；以及几条反直觉的忠告 —— "别拿固定步骤路径判分（会误杀好方案）""LLM 评委必须与人类专家校准，并给它 'Unknown' 这个出口""读 transcript 是 agent 开发的核心技能"。**用来**：讲"怎么量化一个 agent 变好了"。
- [τ-bench（Yao et al., 2024）](https://arxiv.org/abs/2406.12045)
  **`pass^k` 这个指标的出处**。评测"工具-智能体-用户"三方交互：用 LLM 扮演用户、给智能体工具和业务规则，**比对最终数据库状态**判成败（而不是比对固定的工具调用路径）。实测数字很说明问题：最强 agent 单次成功率 >60%，但**连续 8 次全对的比例 <25%**。**用来**：讲"一致性"这个维度。（仓库：`sierra-research/tau2-bench`）
- [Inspect AI（英国 AI 安全研究所）](https://inspect.aisi.org.uk/evals/)
  **跨框架的开源评估框架**：内置 ReAct / deep agent / multi-agent，并提供 **Agent Bridge** 接入第三方框架（OpenAI Agents SDK、LangChain、Pydantic AI）。**用来**：需要"工具"而不只是"方法论"时。
- [AgentBench（Liu et al., 2023）](https://arxiv.org/abs/2308.03688)
  多环境基准：**8 个不同环境**（代码、游戏、网页、操作系统、数据库…），测 LLM-as-Agent 的推理与决策；论文梳理了典型失败原因。**用来**：想看"跨环境广度"的基准时。

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

## Gaps（尚缺的资源）
- ~~缺一份可靠的、跨框架的 agent 评估资料~~ **已补（2026-09）**：见上面四条，首选 Anthropic《Demystifying evals for AI agents》
- 缺中文的高质量一手资料（目前几乎全是英文）
- 缺 **多 agent 协作**的高可信工程资料（编排者-工作者之外的取舍、典型失败模式）——目前只在术语表和 Agent 0006 的追问里出现过
