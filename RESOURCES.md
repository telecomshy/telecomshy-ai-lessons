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
- [vLLM — Structured Outputs（官方文档）](https://docs.vllm.ai/en/latest/features/structured_outputs/)
  开源引擎这一侧的口径：约束形态**全表**（`choice` 固定选项 / `regex` 正则 / `json` JSON schema / `grammar` 上下文无关文法 / `structural_tag`），后端是 **xgrammar 或 guidance**（旧的 `guided_*` 系列已在 v0.12.0 移除）。**⚠ 实践建议**：官方 Tip 说**在提示词里也写明 schema 与字段怎么填，「can improve the results notably in most cases」**。
- [XGrammar（开源约束解码引擎）](https://github.com/mlc-ai/xgrammar) · [技术报告（arXiv 2411.15100, MLSys'25）](https://arxiv.org/abs/2411.15100)
  README 两句原话：**「leverages constrained decoding to ensure 100% structural correctness」** · **「the default structured generation backend for most LLM inference engines, including vLLM, SGLang, TensorRT-LLM」** —— 说明「划掉非法字」是**引擎的标配能力**、不是某一家独有。技术报告摘要：**最高 100 倍**加速，支持一般上下文无关文法。
- [Leviathan, Kalman, Matias — "Fast Inference from Transformers via Speculative Decoding"（arXiv 2211.17192, ICML 2023 Oral）](https://arxiv.org/abs/2211.17192)
  **投机解码的原始论文**，本课第 3 节末尾那句的依据。摘要原话：**「sample from autoregressive models faster **without any changes to the outputs**」**（←「加速不改答案」的出处）· 「**can accelerate existing off-the-shelf models without retraining or architecture changes**」· **T5-XXL 上 2×–3× 加速、输出完全一致**。
- [vLLM — Speculative Decoding（官方文档）](https://docs.vllm.ai/en/latest/features/speculative_decoding/)
  ① **定位**（正对着第 2 课 decode 带宽受限那条）：「reduce inter-token latency under **medium-to-low QPS**, **memory-bound** workloads」。
  ② **方法族**：EAGLE / MTP / draft model / n-gram / suffix 等，另附按 QPS 给推荐收益的对照表。
  ③ **⚠ 本课演示三那句官方依据**：「**Batch Size and Numerical Stability: Changes in batch size may cause variations in logprobs and output probabilities**」；同节还有「vLLM does not currently guarantee stable token log probabilities (logprobs). This can result in **different outputs for the same request across runs**」。
- [Anthropic — Stop reasons and fallback（官方文档）](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)
  **「为什么停了」那张表的全表**：`end_turn` 答完 · **`max_tokens` 撞上限** · `stop_sequence` 碰停止字 · `tool_use` 要调工具 · `pause_turn` 服务端工具循环到迭代上限 · **`refusal` 拒答** · **`model_context_window_exceeded` 上下文窗口填满（"Treat the response as truncated"）**。
  ⚠ **本课第 4 节第 ② 条的出处**，原文小标题就是 Incomplete tool use blocks：撞上限被截断的回答里**若含未写完的工具块，需要调大 `max_tokens` 重发**。
- [Anthropic — Errors（官方文档）](https://platform.claude.com/docs/en/api/errors)
  **本课第 4 节第 ③ 条的出处**：`429 - rate_limit_error`（hit a rate limit, reached its usage tier's monthly spend cap…；⚠ 原文明说**撞 tier 花费上限的 429 没有 `retry-after` 头、会一直失败到访问恢复**）· **`529 - overloaded_error`（「The API is temporarily overloaded」**，并说明因 high traffic across all users，且**尖峰用量可能触发加速限制而看到 429**）· `500 - api_error`（**Retry the request with exponential backoff**）· 官方 SDK 那条：**「automatically retries transient failures … with exponential backoff, **twice by default**, honoring the retry-after header」**。
- [vLLM — SamplingParams（官方 API 文档）](https://docs.vllm.ai/en/latest/api/vllm/sampling_params.html)
  第 1 课 Q10 已引过。**这一课把它抬成「引擎在执行旋钮」的依据** —— 参数是让 **engine** 去装 logits processor。

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
