# AI Agent 原理与工程

> ### 📖 在线阅读
> 
> **https://telecomshy.github.io/telecomshy-ai-lessons/**
> 
> 从这里进，能直接看到排版好的课件、插图，能答题。
> 本页下面的课程链接也都指向那里 —— 在 GitHub 仓库里点 `.html` 文件只会
> 显示源码，不是课件。

## 为什么会有这个仓库

这个仓库是**给我女儿的一份礼物**。

她是个聪明、善良、坚韧的女孩，虽然是个艺术生，但兴趣爱好广泛——除了画画，她还喜欢自然科学，喜欢物理和天文，喜欢编程和人工智能。她有时候会感到孤独，因此她的梦想是：**亲手做一个能陪伴自己的机器人**。

所以我想为她做些什么——干脆写一份教程吧。这是我最初的想法。网上肯定已经有很多优秀的教程，比我写得好，但我还是想写一份，因为我希望她读这份教程的时候，能感受到我的陪伴。

我不是人工智能专业的研究者，只是一名普通工程师，写这份教程之前我自己也是 AI 领域的初学者。所以对我来说，写这份教程的过程，也是一次系统学习。因此教程一定有错漏，一定有讲得不够好的地方，**如果你发现了错误，或者有更好的讲法，欢迎开一个 Issue 告诉我**。

教程基于 [mattpocock 的 `teach` 技能](https://github.com/mattpocock/skills/blob/main/docs/productivity/teach.md) 开发，因此一开始就有一个现成的骨架：AI 先生成课件，我再一课一课地修改和调整。

### 课程进度怎么标记

整个教程的课件是 **AI 辅助生成**的，我一课一课地改。所以进度分三档，目录页上一眼能分清：

| 标记                          | 含义                              |
| --------------------------- | ------------------------------- |
| 标题后带 <code>completed</code> | **已经逐课改过一遍**，内容定稿，可以直接照着读       |
| 普通卡片                        | 已经写出来了，但**还在改** —— 措辞、举例、配图都可能变 |
| 虚线卡片，标着「下一步开」               | **还没写**                         |

目前标为 `completed` 的是：

- **LLM 底层 · 第 0 课**（[模型是怎么学出来的](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0000-how-models-learn.html)）
- **LLM 底层 · 第 1 课**（[从「token」到「下一个 token」](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0001-from-token-to-next-token.html)）＋ [进阶版「十一个追问」](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0001-from-token-to-next-token-deep.html)
- **LLM 底层 · 第 2 课**（[一次请求的两段：prefill 与 decode](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0002-prefill-vs-decode.html)）＋ [进阶版「里面到底在转什么」](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0002-prefill-vs-decode-deep.html)
- **LLM 底层 · 第 3 课**（[KV Cache 与「缓存命中」是两回事](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0003-kv-cache-and-prompt-caching.html)）＋ [进阶版「三个绕人的细节」](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0003-kv-cache-and-prompt-caching-deep.html)
- **LLM 底层 · 第 4 课**（[一趟装满的卡车](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0004-batching.html)）＋ [进阶版「批从哪来、拐点、工业界的招」](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0004-batching-deep.html)
- **LLM 底层 · 第 5 课**（[它真的在思考吗？](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0005-reasoning-models.html)）＋ [进阶版「谁写的、怎么切的、谁收着、怎么练出来的」](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0005-reasoning-models-deep.html)
- **LLM 底层 · 第 6 课**（[量化：把模型压小，把字吐快](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0006-quantization.html)）＋ [进阶版「压法是什么、误差怎么救回来、KV 是什么精度」](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0006-quantization-deep.html)
- **LLM 底层 · 第 7 课**（[蒸馏：小模型的本事从哪来](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0007-distillation.html)）＋ [进阶版「抄什么、扣什么、怎么练」](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0007-distillation-deep.html)
- **LLM 底层 · 第 8 课**（[这件事到底是谁干的](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0008-who-does-what.html)）＋ [进阶版「在哪配、怎么验、代价是什么」](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0008-who-does-what-deep.html)
- **LLM 底层 · 第 9 课**（[后训练的几种练法](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0009-post-training-recipes.html)）＋ [进阶版「七问：差在哪、谁在打分、算法在拧什么、窄领域会不会练坏、练完改得动什么」](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0009-post-training-recipes-deep.html)

基础课和进阶版算同一课，改过一课就算这一课 `completed`。剩下的课会接着往下标。

---

## 怎么用

**完整目录在 [`lessons/index.html`](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/index.html)** —— 建议直接用浏览器打开它。

### 关于「基础课」和「进阶版」

课程分成两层：

- **基础课**（`0001-xxx.html`）面向初学者和业务人员。给结论和直觉，**不给推导和算式**。
- **进阶版**（`0001-xxx-deep.html`）面向想深究的技术读者。给数量关系、算式、机制边界。
- **进阶版里装的是「基础课没讲的理由」**，不是「基础课的加强版」。

如果你读到「（为什么必须看不到后面？）」这样的链接可以直接跳到进阶版；不想跳，忽略它也一样能读完主线。

### 怎么跑脚本

大多数脚本**只用 Python 标准库，离线就能跑**。只有 Agent 篇第 2 课要调真模型，装包、配 key 的完整步骤写在课里（[怎么跑](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/agent/0002-build-an-agent.html)）：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U openai python-dotenv
# 然后在仓库根目录建 .env，写一行：DEEPSEEK_API_KEY=sk-...
python exercises/agent/0002-build-an-agent.py --check
python exercises/agent/0002-build-an-agent.py
```

`.env` 已经在 `.gitignore` 里，不会进 git。**这一步会真的花钱**——四个问题加起来不到一分钱（DeepSeek `deepseek-flash`，2026-10-18 价目）。

脚本是**加分项，不是必修项**。主线不依赖跑代码 —— 第 2 课一边写一边讲，不跑也能读懂；跑起来才看得到 trace 和账单。

---

## 课程目录

### LLM 底层

先讲模型里面发生了什么。只讲**影响 agent 成本、延迟、设计**的机制，以及能力和失效的来源。

**基础课** —— 给初学者和业务人员，给结论和直觉，不给推导和算式。

| 课    | 标题                                                                                                                                                          |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0000 | [模型是怎么学出来的](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0000-how-models-learn.html) —— **先导课，先读这个**　<code>completed</code>               |
| 0001 | [从「token」到「下一个 token」](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0001-from-token-to-next-token.html) —— **基石课**　<code>completed</code> |
| 0002 | [一次请求的两段：prefill 与 decode](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0002-prefill-vs-decode.html) —— 为什么读长文快、写长文慢　<code>completed</code> |
| 0003 | [KV Cache 与「缓存命中」是两回事](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0003-kv-cache-and-prompt-caching.html)                                |
| 0004 | [一趟装满的卡车](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0004-batching.html) —— 排队 ＋ 拼车：一张卡怎么同时服务几十上百个人                                |
| 0005 | [它真的在思考吗？](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0005-reasoning-models.html) —— 屏幕上那段「思考」，是真在想还是演给你看 |
| 0006 | [量化：把模型压小，把字吐快](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0006-quantization.html) —— 压小＝吐字快，**但读长文一点不快**      |
| 0007 | [蒸馏：小模型的本事从哪来](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0007-distillation.html) —— **你给它什么，它就只能学到什么** |
| 0008 | [这件事到底是谁干的](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0008-who-does-what.html) —— 四层归属表：<b>哪些本事是引擎给的</b>（这条轨道到此为止）|

**进阶版** —— 给想动手验算的技术读者，装的是基础课没讲的那部分理由。

| 课       | 标题                                                                                                                                    |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| 0001 进阶 | [十一个追问](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0001-from-token-to-next-token-deep.html)　<code>completed</code> |
| 0002 进阶 | [里面到底在转什么](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0002-prefill-vs-decode-deep.html)　<code>completed</code> |
| 0003 进阶 | [三个绕人的细节](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0003-kv-cache-and-prompt-caching-deep.html)                  |
| 0004 进阶 | [批从哪来、拐点、工业界的招](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0004-batching-deep.html)                        |
| 0005 进阶 | [谁写的、怎么切的、谁收着、怎么练出来的](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0005-reasoning-models-deep.html)                          |
| 0006 进阶 | [压法是什么、误差怎么救回来、KV 是什么精度](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0006-quantization-deep.html)                          |
| 0007 进阶 | [抄什么、扣什么、怎么练](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0007-distillation-deep.html)                          |
| 0008 进阶 | [在哪配、怎么验、代价是什么](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/0008-who-does-what-deep.html)                          |

### Agent 原理篇

模型怎么「想」、怎么「伸手」做事 —— 直接服务「做出自己的 agent」这个目标。

| 课    | 标题                                                                                                                                      |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------- |
| 0001 | [Agent 是什么：循环、工具、记忆](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/agent/0001-what-is-an-agent.html) —— 纯理论：循环怎么转、什么时候停，工具从哪来，记忆按产品怎么存 |
| 0002 | [手写一个 agent](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/agent/0002-build-an-agent.html) —— 从装包、配 key 开始，用真模型跑通循环     |
| 0003 | [工具长出两个新形状：MCP 与 Skill](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/agent/0003-mcp-and-skills.html) —— MCP 管「怎么接」，Skill 管「怎么做」 |
| 0004 | [写一个 skill、接一个 MCP](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/agent/0004-skill-and-mcp-lab.html) —— 动手版：骨架自检、配置走通「发现」 |
| 0005 | [多 agent 协作：什么时候该上、怎么分工](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/agent/0005-multi-agent.html) —— 编排者-工作者、只回结论不回流水、什么时候不该上 |
| 0006 | [编排一群 agent](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/agent/0006-orchestrate-agents.html) —— lead＋workers 跑起来：派单三件套、失败重派、上下文对账 |
| 0007 | [安全与权限：纸条攻击、沙箱、人审](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/agent/0007-safety.html) —— 提示词注入是什么；护栏三件套：少信、少能、有人管 |
| 0008 | [Harness：Agent = Model + Harness](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/agent/0008-harness.html) —— 把学过的东西全部装回壳里 |
| 0009 | [拆解 TeleAgent：一个真实的 harness](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/agent/0009-teleagent-teardown.html) —— 收尾大作业：真实产品逐块拆 |

### 技巧与工程

「怎么不翻车」的内容**按主题归轨**（2026-10-18 重构）：上下文、评估、失败自救并进 **Agent 篇**对应课；微调项目变成 **LLM 底层的附录**（[微调项目怎么不翻车](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/llm/appendix-tuning-projects.html)）；贴墙清单在 [`reference/`](reference/)。

### RAG

让模型用上手边没有的信息。只讲**机制与取舍**，不讲向量库选型和产品对比。

| 课    | 标题                                                                                                                      |
| ---- | ----------------------------------------------------------------------------------------------------------------------- |
| 0001 | [为什么得「先查资料再回答」](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/rag/0001-why-retrieval.html)                 |
| 0002 | [一条 RAG 链长什么样](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/rag/0002-rag-pipeline.html) —— 六步里只有最后一步是模型   |
| 0003 | [什么时候不该上 RAG](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/rag/0003-when-not-to-use-rag.html)             |
| 0004 | [两种典型翻车](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/rag/0004-two-failure-modes.html) —— 该来的没来 vs 来了但没用上 |

**进阶版** —— 给想动手验算的技术读者。

| 课       | 标题                                                                                                           |
| ------- | ------------------------------------------------------------------------------------------------------------ |
| 0001 进阶 | [稀疏和稠密各自在哪翻车](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/rag/0001-why-retrieval-deep.html)   |
| 0002 进阶 | [切块到底切多大](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/rag/0002-rag-pipeline-deep.html)        |
| 0004 进阶 | [RAG 到底怎么评](https://telecomshy.github.io/telecomshy-ai-lessons/lessons/rag/0004-two-failure-modes-deep.html) |

### 速查 · 课很少回看，速查会

`reference/` 里的 7 页：

| 页面                                                                                                     | 用途                                         |
| ------------------------------------------------------------------------------------------------------ | ------------------------------------------ |
| [术语表](https://telecomshy.github.io/telecomshy-ai-lessons/reference/glossary.html)                      | 全课程统一用词，课里出现的词回来对一遍                        |
| [采样参数速查](https://telecomshy.github.io/telecomshy-ai-lessons/reference/sampling-params.html)            | temperature / top_p / top_k / seed，配模型时照着抄 |
| [KV Cache 与「缓存命中」速查](https://telecomshy.github.io/telecomshy-ai-lessons/reference/prompt-caching.html) | LLM 底层第 3 课的压缩版                            |
| [一次请求，从头到尾](https://telecomshy.github.io/telecomshy-ai-lessons/reference/one-request-end-to-end.html)  | 可点逐步版 —— 看货架（KV cache）怎么一点点变满              |
| [agent 评估该问什么](https://telecomshy.github.io/telecomshy-ai-lessons/reference/agent-eval-checklist.html) | Agent 篇第 9 课「拆完怎么验」的检查单                         |
| [预算与排座次](https://telecomshy.github.io/telecomshy-ai-lessons/reference/context-budget.html)             | 上下文工程的对照表                                  |
| [权威架构图 · 对照](https://telecomshy.github.io/telecomshy-ai-lessons/reference/canonical-diagrams.html)     | 认得出英文资料里那几张图对应哪一块，当对照不当教材                  |

---

## 仓库结构

```
AGENTS.md               agent 入口：规矩在哪、目录怎么分
MISSION.md              为什么做这个（这个仓库的一切都挂在它下面）
NOTES.md                课程开发标准、约定与待办
RESOURCES.md            全部一手资料来源，注明「用来干什么」
docs/agents/            agent 技能的仓库配置（工单 · 分诊标签 · 领域文档）
docs/learning-records/  学习者已掌握的证据（teach 技能用，算 ZPD）
docs/notes/rules/       开发操作细节（联网取材 · 标 completed 的步骤），用到才读
docs/notes/history/     决策与教训存档（一节一篇），NOTES.md 第 5 节只有索引
lessons/<轨道>/         课程本体，自包含 HTML
exercises/<轨道>/       配套脚本与实际产物（如 agent/my-first-skill/）
reference/              术语表与速查（贴墙清单）
assets/                 共享样式表、测验组件、SVG 插图、演示动画（mp4 + poster）
```

想了解这个仓库是怎么被「开发」出来的，[`NOTES.md`](NOTES.md) 记着每条教学规矩本身，[`docs/notes/history/`](docs/notes/history/) 记着它们背后的原因 —— 包括不少「我一开始写错了，后来改对」的反面案例。

---

## 这些内容是怎么来的

**本教程不凭 AI 的记忆写作。** 所有知识点都来自 [`RESOURCES.md`](RESOURCES.md) 里列出的公开一手资料 —— 论文、官方文档、经典博客，逐条注明「用来干什么」，并且在每一门课里给出出处。

课程里出现的数字，都是各家文档和论文的原值，或者是我本地跑脚本实测出来的（课里贴的就是实测输出）。

### 但请仍然自己核对

这是我要诚实说明的部分：教程由 AI 辅助生成，**它会犯错，而且错得很像真的**。`teach` 技能自己的文档里也写着同一句话 —— 不要只因为出处标了链接就相信内容。

几条实用的自检提示：

- **看到具体数字，回头看它引的是哪份原文。** 转引的数字（综述里引的论文数字）我在 `RESOURCES.md` 里都标了「未读原始报告」。
- **和英文原图的措辞对一下。** [`reference/canonical-diagrams.html`](https://telecomshy.github.io/telecomshy-ai-lessons/reference/canonical-diagrams.html) 附了中英认词表。
- **觉得哪里别扭，就别别扭着。** 直觉是有效的信号，你的怀疑比我的自信更值得听。

欢迎开 [Issue](https://github.com/telecomshy/telecomshy-ai-lessons/issues) 挑错，包括错别字和措辞别扭。

---

## 基于 `teach` 技能开发

这个仓库是用 [Matt Pocock 的 `teach` 技能](https://github.com/mattpocock/skills/blob/main/docs/productivity/teach.md)（配合 OpenCode）搭建起来的。

`teach` 的设计里有两个原则，正好解释了这个仓库长什么样：

**1. 它是有状态的，靠文件而不是靠对话记忆。** 「为什么学」「资料从哪来」「课已经写到哪」「你已经掌握了什么」全都躺在目录里。所以隔三周回来开新会话说一句「下一课学什么」，课程会接着往下走，而不是从头开始。

**2. 它不让 AI 凭记忆教学。** 参数化知识被当作不可信来源 —— 先去找高可信资料，记进 `RESOURCES.md`，然后在课里引用。这就是为什么这个仓库里的每个说法都能追到出处。

`NOTES.md` 里的课程开发标准、编号规则和核验纪律（改完必须读回来、脚本必须真跑、SVG 必须渲染出来看一眼），是在 `teach` 的基础上按我女儿这个具体学习者的情况加的。

如果你也想给自己的领域建一套这样的教程，`teach` 完全可以用在非编程领域 —— 它和数学、乐器、语言、考试、乃至给八岁小孩做一本可以打印的书，都配合得上。

---

## 参与

欢迎，但有几件事请先读 [`NOTES.md`](NOTES.md) 的第 1 节 —— 那里面是硬规则，改之前先查。

- **挑错**（最欢迎）：开 Issue，指出哪一课哪个说法不对。
- **提改进**：某段太难懂了？某个类比不贴切？直接说。
- **补一手资料**：尤其是中文资料，目前几乎全是英文 —— 这一块缺口很大。

## License

本仓库的课件与脚本以 [MIT](LICENSE) 许可发布 —— 可以自由使用、改编、再分发。

一个例外：[`reference/canonical-diagrams.html`](https://telecomshy.github.io/telecomshy-ai-lessons/reference/canonical-diagrams.html) 里引用的 Jay Alammar《The Illustrated Transformer》配图是 **CC BY-NC-SA 4.0**（署名 - 非商业 - 相同方式共享）—— 那张图能引用，但不能白拿、不能改了再发，转载请带上作者名和同样的许可。
