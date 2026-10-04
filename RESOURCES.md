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
- [Anthropic — Claude Platform Docs："Context windows"](https://platform.claude.com/docs/en/build-with-claude/context-windows)
  官方行为口径：**输入本身超过上下文窗口时，API 返回 400 `invalid_request_error`（"prompt is too long"）**——是把请求拒掉，不是截断、不是丢掉前面的。**用来**：回答"一次请求超了窗口会怎么处理"（`0001-deep` Q9）。
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
- [Anthropic 官方价目](https://www.anthropic.com/pricing)（2026-10-03 查）
  API 每 MTok 单价。**输出一律是输入的 5 倍**：Fable 5.1 $10/$50、Opus 5.5 $4/$20、Sonnet 5.5 $2/$10、Haiku 4.5 $1/$5。缓存另计：**读** $0.10～$0.25（输入的 0.025～0.1 倍）、**写** 是输入的 1.25 倍；原页注明缓存价对应 **5 分钟 TTL**。**用来**：第 2 课第 6 节"输出比输入贵"的价目表；脚本 `PRICE_OUT` / `CACHE_HIT_DISCOUNT` 的依据。⚠ **价目会变，课件里必须标查证日期并给原页链接。**
- [DeepSeek 官方价目](https://api-docs.deepseek.com/quick_start/pricing)（2026-10-03 查）
  分**非高峰 / 高峰**两档（高峰为 UTC 工作日 01:00–04:00、06:00–10:00，非高峰约为高峰的一半）。非高峰：V4.1-Flash 输入（未命中）$0.15、输出 $0.60 → **4 倍**；V4-Pro 输入（未命中）$0.66、输出 $1.98 → **3 倍**。缓存命中输入低到 $0.003 / $0.022，即**未命中的 1/50 ～ 1/30**。**用来**：与 Anthropic 交叉验证"输出比输入贵"的方向与量级（第二家一手来源）。⚠ 同上，价目会变。
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

### 蒸馏（第 7 课）

- [Hinton, Vinyals, Dean — "Distilling the Knowledge in a Neural Network"（arXiv 1503.02531, NIPS 2014 DL Workshop）](https://arxiv.org/abs/1503.02531)
  **蒸馏这个字的出处**，也是本课机制的原话来源。三句都要记住：
  ① **机制**："Our more general solution, called **distillation**, is to **raise the temperature of the final softmax until the cumbersome model produces a suitably soft set of targets**. We thus use the same high temperature when training the small model to match these soft targets. We show later that matching the **logits** of the cumbersome model is actually **a special case of distillation**."（**温度 + 软标签**，而且"直接对齐 logit"只是它的特例）
  ② **为什么这么做有用**（本课最值钱的一句）："When we are distilling the knowledge from a large model into a small one, however, **we can train the small model to generalize in the same way as the large model**. If the cumbersome model generalizes well because, for example, it is the average of a large ensemble of different models, a small model trained to generalize in the same way will typically do much better on test data than a small model trained on the original data by standard methods."（**学生学的不是答案，是"老师的泛化方式"**）
  ③ **"错字上的分数不是噪声"的原文例子**：论文里说，把某个东西误认成 garbage truck，**"that mistake is still many times more probable than mistaking it for a carrot"**——非答案那几个的概率**编码了"哪个错更像对"**。
  落地证据：摘要给了 MNIST 与**"significantly improve the acoustic model of a heavily used commercial system"**（一个在用的商业语音系统）。
  ⚠ 提取方式：用代理下 PDF 再抽文字（`Invoke-WebRequest -Proxy 'http://127.0.0.1:7890'`），上面三句是**原文**，不是转述。
- [DeepSeek-AI et al. — DeepSeek-R1（Nature 2025 · arXiv 2501.12948）](https://arxiv.org/abs/2501.12948)
  **第 5 课已经引过这篇；但第 7 课要用它的附录 F 和"局限"那一段。**
  ① **R1 的蒸馏是"搬回答"，不是"搬 logit"**：附录 A.2 原话"The reasoning trajectories discovered through this self-exploration are subsequently **distilled** and used to train other models"；附录 F 整节标题就是 **"F DeepSeek-R1 Distillation"**、F.1 是 **"Distillation v.s. Reinforcement Learning"**。**用来**：讲"蒸馏"今天至少有两个机制（软标签 / 搬大模型的输出），别混。
  ② **对 agent 最要紧的一条自述局限**（第 7 课落点）："**Structure Output and Tool Use:** Currently, the structural output capabilities of DeepSeek-R1 remain **suboptimal** compared to existing models. Moreover, **DeepSeek-R1 cannot leverage tools**, such as search engines and calculators, to improve the performance of output."（**推理强 ≠ 工具调用强**——这条出自论文自己的局限章节，不是二手评论）
  ③ 其他两条顺手记下：蒸馏模型"surpassing the performance of their **original instruction-tuned counterparts**"（超越的是它自己的**指令版**，不是超越大模型）；token 效率那条"it uses fewer tokens to solve simple tasks… **instances of excessive reasoning—manifested as overthinking—are still observed**"。
- [DeepSeek-R1 官方仓库（README 评测表）](https://github.com/deepseek-ai/deepseek-r1)
  **蒸馏模型的实测数字出处**（`Distilled Model Evaluation` 表）：`R1-Distill-Qwen-1.5B` — AIME 2024 pass@1 **28.9**、MATH-500 **83.9**、GPQA Diamond **33.8**、LiveCodeBench **16.9**、CodeForces rating **954**；`R1-Distill-Qwen-7B` — **55.5 / 92.8 / 49.1 / 37.6 / 1189**。**用来**：给"1.5B 的模型也能拿 55 分"这种说法一个可查的落点；**⚠ 报的是基准分，不是 agent 能力**，引用时别滑过去。
- [Li et al. — "Textbooks Are All You Need II: phi-1.5 technical report"（arXiv 2309.05463）](https://arxiv.org/abs/2309.05463)
  **用来防止把"小模型变强"全归给蒸馏。** 这条线（TinyStories → phi-1 → phi-1.5）走的是**另一条路**：用已有的大模型**生成"教科书级"数据**来训练 1.3B 的小模型（原文"use existing Large Language Models (LLMs) to generate 'textbook quality' data"），结果是"**performance on natural language tasks comparable to models 5x larger**"。
  **所以"小模型为什么这么强"的诚实答案是三条路一起走**（合成数据 · 蒸馏 · 更好的后训练），**不是"全靠蒸馏"**。⚠ 它**不是** Hinton 那种软标签蒸馏，别当成同一种机制。

### 会思考的模型（第 5 课）

- [Anthropic — Thinking（Claude 平台文档）](https://platform.claude.com/docs/en/build-with-claude/thinking)
  **本课的主来源**。原话（讲清"多出来的那一步"是什么）："A model that answers in a single pass has to get everything right on the first try: **no scratch work, no checking, no changing course halfway through**"；"When thinking is active, Claude works through the problem **in its own words** before answering: it **restates what is being asked, tries approaches, checks intermediate results, and abandons paths that do not hold up**"。
  **三笔账的原话都在这里**：① 计费——"the tokens Claude spends reasoning are **billed as output tokens, even when the thinking text isn't returned to you**, and they count toward `max_tokens` alongside the response text"；② 你看到的 ≠ 你付的——"You're charged for the **full thinking tokens** generated by the original request, **not the summary tokens**"；③ 缓存/工具——"**Pass every `thinking` block back to the API complete and unmodified, alongside the `tool_use` block it accompanied**"，文档里还给了带 cache 断点的完整多轮示例。
  预算规则：`budget_tokens` **下限 1024**，且**是目标不是硬上限**（实际用量随任务浮动）。
  ⚠ **`platform.claude.com` 直连是地区限制页（"App unavailable in region"），要靠搜索索引拿正文**——见 1.1。
- [Anthropic — "Claude's extended thinking"（研究博客，2025-02-24）](https://www.anthropic.com/research/visible-extended-thinking)
  **「不是换了个模型」这句话的出处**，也是本课那句反直觉结论的依据："Extended thinking mode **isn't an option that switches to a different model** with a separate strategy. Instead, it's **allowing the very same model to give itself more time**, and expend more effort, in coming to an answer."
  **收益是递减的**：原话"its accuracy on, for example, math questions improves **logarithmically** with the number of 'thinking tokens' that it's allowed to sample"。给了一个具体数：Claude 3.7 Sonnet 用 64k 思考预算（相当于 256 个独立采样的算力）拿到 GPQA **84.8%**（其中物理子项 96.5%）。
  **「不能靠读思考过程判断它在想什么」的出处**——这是否定"思考过程＝真实推理"的硬证据：原话"models very often make decisions based on factors that they **don't explicitly discuss** in their thinking process. This means **we can't rely on monitoring current models' thinking** to make strong arguments about their safety"。另一句解释了为什么界面上的思考读起来"更冷淡、更像在陈述"：**思考过程没有做他们那套语气训练**，"we wanted to give Claude maximum leeway in thinking whatever thoughts were necessary"——所以"as with human thinking, Claude sometimes finds itself thinking some incorrect, misleading, or half-baked thoughts along the way"。
- [DeepSeek-AI et al. — "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning"（Nature 2025 · arXiv 2501.12948）](https://arxiv.org/abs/2501.12948)
  **「会思考是被训练出来的」这个机制的出处**。原话："the reasoning abilities of LLMs can be incentivized through **pure reinforcement learning (RL), obviating the need for human-labeled reasoning trajectories**"；这个 RL 框架"facilitates the **emergent development** of advanced reasoning patterns, such as **self-reflection, verification, and dynamic strategy adaptation**"（自省、验证、动态换策略——注意这三个词正是界面上常看到的那种动作）。
  **第 7 课（蒸馏）的钩子已经埋在这里**：原话"the emergent reasoning patterns exhibited by these large-scale models can be **systematically harnessed to guide and enhance the reasoning capabilities of smaller models**"。**用来**：讲"为什么现在的小模型也会思考"——不是它自己想通了，是大模型的思考被搬了过去。
- [Lightman et al. — "Let's Verify Step by Step"（arXiv 2305.20050）](https://arxiv.org/abs/2305.20050)
  **「给过程打分」和「只给结果打分」的对照实验**，本课讲"多出来的那一步凭什么更准"的机制依据。原话："we can turn either to **outcome supervision**, which provides feedback for a final result, or **process supervision**, which provides feedback for each intermediate reasoning step"；结论"**process supervision significantly outperforms outcome supervision** for training models to solve problems from the challenging MATH dataset"，具体数：过程监督的模型解出 MATH 测试子集的 **78%**。同时开源了 PRM800K（80 万条步级人工反馈）。
  ⚠ 注意别把它和 R1 的做法混为一谈：**R1 用的是可自动验证的结果奖励**（答案对不对、代码跑不跑过），而这篇是**人去标注每一步**。两条路，别互相冒用出处。
- [AWS — Claude on Bedrock：Extended thinking](https://docs.aws.amazon.com/bedrock/latest/userguide/claude-messages-extended-thinking.html)
  同一套机制在 Bedrock 上的落地说明，**两条运维经验值**：预算**从下限起步逐步加**（"start at the minimum and increase incrementally"）；**预算超过 32K 建议走批量处理**，否则"causes long running requests that might result in system timeouts"。**用来**：讲"预算不是越大越好"以及顶格预算的工程后果。

### 量化（第 6 课）

- [llama.cpp — `tools/quantize/README.md`（官方仓库）](https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/README.md)
  **本课最重要的一条实测来源**。Llama-3.1-8B 在同一台机器上的完整对照表，每档都给了三个数：`bits/weight`（含刻度开销）、`size`、`prompt processing t/s @ 512` 与 `text generation t/s @ 128`。原值：**F16 = 16.0005 bit / 14.96 GiB / prefill 923.49 / decode 29.17**；Q8_0 = 8.5008 / 7.95 / 865.09 / **50.93**；Q6_K = 6.5633 / 6.14 / 812.01 / 58.67；Q5_K_M = 5.7036 / 5.33 / 758.69 / 67.23；**Q4_K_M = 4.8944 / 4.58 / 821.81 / 71.93**；Q3_K_M = 3.9960 / 3.74 / 783.44 / 71.68；Q2_K_S = 2.9697 / 2.78 / 798.91 / 90.01。
  **这张表同时给出两个可直接上课的结论**：① decode 快 2.5 倍（29.17 → 71.93）而 **prefill 几乎没变**（923.49 → 821.81，甚至更慢）——**独立印证第 2 课进阶 Q3 的「prefill 算力受限 / decode 带宽受限」**；② 「4 bit」实测是 4.89 bit，因为缩放因子要占地方。
  另有内存/磁盘表：8B **32.1 GB → 4.9 GB**、70B **280.9 → 43.1**、405B **1,625.1 → 249.1**（Q4_K_M）。README 开头两句也给了定义级说法："reduces the precision of model weights… shrinks the model's size and can speed up inference… may introduce some accuracy loss which is usually measured in Perplexity (ppl) and/or Kullback–Leibler Divergence (kld)"。
  ⚠ **`raw.githubusercontent.com` 直连取不到，要带代理**（见 1.1）。
- [Dettmers et al. — "LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale"（NeurIPS 2022）](https://arxiv.org/abs/2208.07339)
  **int8 量化的原始出处，也是「离群值」这个现象的出处**。原话：int8 矩阵乘 "**cut the memory needed for inference by half while retaining full precision performance**"；做法是 "vector-wise quantization" 处理绝大多数特征，而对 **emergent outliers** 用混合精度分解、单独放进一个 16-bit 矩阵乘里，"**still more than 99.9% of values are multiplied in 8-bit**"。**用来**：讲"为什么朴素压到 8 bit 会掉分、后来者为什么必须特殊处理离群通道"。
- [Frantar et al. — "GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers"（ICLR 2023）](https://arxiv.org/abs/2210.17323)
  **"训练后量化（PTQ）"路线的代表作**。原话：**175B 参数模型约 4 GPU 小时**压到 **3 或 4 bit**，"with negligible accuracy degradation relative to the uncompressed baseline"；比此前的一次性量化方法"more than doubles the compression gains"；极端档位还能压到 **2-bit 甚至三值**。端到端加速原值：**A100 约 3.25×、A6000 约 4.5×**（相对 FP16）。**用来**：讲"压到 4 bit 还能用"这句话的出处与它成立的条件（逐层用二阶信息补偿），以及加速倍数的真实量级。
- [Xiao et al. — "SmoothQuant: Accurate and Efficient Post-Training Quantization for LLMs"（ICML 2023）](https://arxiv.org/abs/2211.10438)
  **给出 W8A8（权重与激活都压到 8 bit）这条路的关键事实判断**，原话："**weights are easy to quantize while activations are not**"，所以用"数学上等价的变换"把激活的离群值**迁移到权重那边**。实测原值：**最高 1.56× 加速、2× 内存下降**，精度损失可忽略。**用来**：讲"只压权重"和"连激活一起压"是两条不同的路，以及离群值为什么专挑激活出来。
- [Lin et al. — "AWQ: Activation-aware Weight Quantization"（MLSys 2024 最佳论文）](https://arxiv.org/abs/2306.00978)
  **"不是所有权重一样重要"的出处**。原话："**not all weights in an LLM are equally important. Protecting only 1% salient weights can greatly reduce quantization error**"；而且判断哪些通道重要**要看激活的分布、不是看权重**（"we should refer to the activation distribution, not weights"），做法是"数学上推导出的等价变换"放大关键通道——所以 **"does not rely on any backpropagation or reconstruction"**。配套 TinyChat 实测：桌面与移动 GPU 上相对 HuggingFace FP16 **超过 3× 加速**，并让 70B 跑进手机 GPU。**用来**：讲"格子粗不是均匀变糊——挑着压才划算"。
- [vLLM — Quantization（官方文档）](https://docs.vllm.ai/en/latest/features/quantization/)
  定义级原话："**Quantization trades off model precision for smaller memory footprint, allowing large models to be run on a wider range of devices.**"支持格式全表（AutoAWQ / GPTQ / BitsAndBytes / FP8 / INT4 / GGUF / TorchAO…）与**逐硬件支持矩阵**（AWQ 不支持 Volta、不支持 AMD GPU；GPTQ 不支持 Ada 之后…）。**用来**：讲"量化不是一个动作，是一堆互不兼容的格式"，以及选型时第一道门槛是硬件。
- [vLLM — INT4 W4A16（官方文档）](https://docs.vllm.ai/en/latest/features/quantization/llm_compressor/int4/)
  **"权重压 4 bit、激活保持 16 bit"这条路线的定位与代价**：这种量化"particularly useful for **reducing model size and maintaining low latency in workloads with low queries per second (QPS)**"；**需要 compute capability > 8.0**（Ampere / Ada / Hopper / Blackwell）。校准数据实践原话："**Start with 512 samples for calibration data, and increase if accuracy drops**"，默认长度 2048；示例里 `group_size=128`。⚠ 一条实用警告："**Quantized models can be sensitive to the presence of the `bos` token**"。**用来**：讲"为什么量化要喂样本、喂什么样本"，以及低 QPS 场景为什么偏爱权重-only。
- [Kurt — "Which Quantization Should I Use? A Unified Evaluation of llama.cpp Quantization on Llama-3.1-8B-Instruct"（arXiv 2601.14277，2026-01）](https://arxiv.org/abs/2601.14277)
  较新的统一评测：同一模型（Llama-3.1-8B-Instruct，FP16/GGUF）上覆盖 3–8 bit 的 K-quant 与 legacy 格式，同时测**下游任务分数、perplexity、CPU 吞吐（prefill 与 decoding 分开）、体积、压缩率、量化耗时**。**用来**：讲"别只问压到什么位，要问在你的任务上掉多少分"——本课若要加进阶版，这是唯一一份同口径横向对比。⚠ 单一模型、单一后端，结论不可外推。

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
