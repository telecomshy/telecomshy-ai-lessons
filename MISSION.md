# Mission: AI Agent 的原理与工程

## Why
想把 AI Agent 这件事**真正搞懂**——不只是会调 LLM API，而是理解它为什么能工作、会在哪里失败、不同设计之间如何取舍。动力主要来自好奇心和"掌握感"，而不是某个外部交付。但"搞懂"要用能动手、可检验的方式来证明，而不是停留在术语层面。

## Success looks like
- 能用一张图或一段话讲清 agent 的核心执行循环，并指出**每一步典型的失效方式**
- 能不依赖框架，从零手写一个带工具调用与多步循环的最小 agent
- 能读懂一篇 agent 领域的代表性论文或工程文章，说清它的**核心思想、证据与局限**
- 面对"单 agent 还是多 agent""要不要上 RAG / 长期记忆"这类问题，能给出**有依据、能自圆其说**的判断

## Constraints
- **受众分层（2026-09-30 定，2026-10-24 细则下放轨道标准）**：LLM 轨基础课＝初学者＋业务人员（学完能听懂技术对话）、deep＝本人＋技术同事内训（能验算、能读一手资料），受众细则以 [`internal/standards/tracks/llm.md`](internal/standards/tracks/llm.md) 为准；deep 页体例（所有 deep 页通用，含"给结论和直觉，不给推导和算式"等门槛细则）以 [`internal/standards/COURSE-STANDARD.md`](internal/standards/COURSE-STANDARD.md) 1.4 为唯一出处。**Agent 篇不分两版**——按**理论｜实操**分课型，深度走三条吸收渠道，见 [`internal/standards/tracks/agent.md`](internal/standards/tracks/agent.md)；**RAG 轨同改理论｜实操**，见 [`internal/standards/tracks/rag.md`](internal/standards/tracks/rag.md)。
- **配套脚本保留但可跳过**：主线不依赖跑代码，脚本当加分项。
- **本人画像**：已有编程基础，用过 LLM API（调接口、写 prompt），但没系统构建过 agent；**会追问机制的精确性，会自己验算**。
- 偏好**项目驱动、边做边学**：每节课都要有一件能亲手做、且有即时反馈的事
- 讲解用中文；一手资料多为英文，接受
- 课程组织为**三条轨道**：**Agent 篇**（`lessons/agent/`，理论＋实操，直接服务本 mission）· **LLM 底层**（`lessons/llm/`，只在"影响 agent 成本 / 延迟 / 设计"**以及"能力与失效的来源"**的范围内讲，见 Out of scope）· **RAG**（`lessons/rag/`，只讲机制与取舍，**不讲向量库选型 / 产品对比**）。「怎么不翻车」的技巧类内容按主题归轨（进实操课的节／LLM 附录／`reference/` 速查）。
- 节奏：以"一次会话完成一课"为主，可长期累积

## Out of scope（暂缓，以保护学习焦点）
- 从零预训练 / 深度微调大模型
- Transformer 内部数学：**不追求公式推导**；但凡**直接影响 agent 成本 / 延迟 / 设计取舍**的机制（如 KV cache、缓存命中、prefill/decode），照讲
- 强化学习理论的完整体系（除非它直接解释某个 agent 机制）

> AI生成
