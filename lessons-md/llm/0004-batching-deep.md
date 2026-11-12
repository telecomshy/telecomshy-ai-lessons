# 批处理：批从哪来、拐点、工业界的招

> 这是 `lessons/llm/0004-batching-deep.html` 的文字稿：**直接在上面改，改完交回，我逐段映射回 HTML 并跑核验**。
> 改法与标记约定见 [README](../README.md)：✅ 标正确选项、「答对时/答错时」是小测反馈、【图】【选读框】等标记说明、小节可增删合并（节号乱了没关系，回写时重排）。

---

【meta】LLM 底层 · 第 4 课 · 进阶版
【别名（data-alias）】批从哪来、拐点、工业界的招

LLM 底层 · 第 4 课 · 进阶版

初学版讲「怎么排队、怎么拼车」，这篇答「**批从哪里来**、**它什么时候到头**、**工业界怎么绕过去**」。**按需跳读**：每条都能从[初学版](../../lessons/llm/0004-batching.html)末尾那份清单直达。

【选读框｜怎么用这篇】

只收**读完初学版仍会冒出来**的疑问；初学版讲过的（「排队 ＋ 拼车」「一趟装满 N 个包裹」「批越大越多人等越久」）这里不重复。**下面每一问都挂在同一条链上**： `请求先排队 → 每轮挑出一批 → 权重 ＋ N 份 KV 一起搬 → 批越大吞吐越高 → 但 KV 在要搬的东西里占比越来越大 → 到某个点开始算不过来 → 工业界用三招绕开`

## Q1 · 一批是怎么凑起来的？为什么半夜批小、白天批大？

**批大小不是你设的，是每一轮服务商挑出来的那几个请求决定的。**挑的是**时间上正好撞在一起**的那些：能挑几个有个上限，vLLM 里那个上限叫 `max_num_seqs`。Orca 论文管这个做法叫**迭代级调度**（iteration-level scheduling）：**每一轮重新挑一次人**，而不是等一整批跑完才换下一批。

Anyscale 测延迟的时候，请求不是一起砸进去的——它们是**隔开陆续送到的**（文档里叫「泊松到达」，给了每秒 1 个和每秒 4 个两档），所以每一轮凑出来的那一批一直在变。真实流量就是这么进来的。

跟着来两个结论：

- **人一多，系统每秒产出的字就越多**，而且会一直涨到这套机器的极限为止。原话是 "As load increases, system TPS rises until it reaches the infrastructure's maximum capacity"。所以**深夜没人用、批小、吞吐低是常态**，不是机器坏了。
- **同一个人的出字速度会随着一起算的人变多而变慢**："As concurrency increases, user TPS typically drops because the engine shares GPU and compute resources"。这就是初学版那句「多和快的拉扯」落到单个用户身上的样子。

再往后情况会反过来：**批已经坐满了，新来的请求只能排队等**。Anyscale 观察到「系统越忙，新请求能立刻插进批里的机会越少」；他们那台机器上 vLLM 大约**每秒来 8 个请求、每秒产出 1900 个字**就到顶了。

所以「慢」得先分清是哪一种：**坐在队里等的那一段**（算进「你等第一个字等了多久」），和**批里人多导致的每轮变慢**（算进「每蹦一个字花多久」）。机制不同，排查时该看的指标也不同。

（最大批多大、排多久算超时、要不要给付费用户优先，都是服务商自己定的，上面的数字只是他们那台机器上的实测。归属分界线：这一问的答案全在服务端，所以留在 LLM 轨道；「拿到一个慢的 agent」怎么量，见 [Agent 评估检查单](../../reference/agent-eval-checklist.html) 的「盯代价」那一条。）

## Q2 · 那个「拐点」长什么样？为什么批大了吞吐就不涨了？

接着[第 2 课（进阶版）· Q2](../../lessons/llm/0002-prefill-vs-decode-deep.html#q3-intensity)那把尺子往下推。**算术强度＝干多少次运算 ÷ 搬多少字节**，比值越大越划算。一批 `N` 个请求走一步：

| 要搬的（约） | 要算的（约） | 算术强度 |
|---|---|---|
| 权重 `W` ＋ `N` 份 KV | `N` × 单 token 计算量 | 随 `N` **一路涨** |
| 批小：要搬的里**权重占大头** | 要算的很少 | 比值小 → **搬不过来**（计算单元闲着一大半） |
| 批大：要搬的里**KV 才是大头** | 要算的按比例涨 | 比值涨到显卡自己的水平 → **算不过来** |

换句话说：**批小的时候卡在「搬」，批大到某个点就换成卡在「算」。**一旦算不过来，吞吐就等于显卡的算力上限：**再往上加人也涨不动了**，可每个人还在等。所以存在一个**最划算的批大小**，越过它就是纯亏。

这一节还要跟基础课那张表对一下账：**那张表跑不出这个拐点**。配套脚本只画了「搬」那一半、没算显卡的算力上限，所以它的吞吐是一路涨到撞显存为止。拐点真长什么样，只能看实测：[Databricks](https://www.databricks.com/blog/llm-inference-performance-engineering-best-practices) 那组数：批大小 64 时吞吐 14 倍、单请求延迟 4 倍，**再往上吞吐基本不涨了**。

## Q3 · 队头阻塞是什么？连续批处理怎么解决？

问题出在**「一批」这个单位是怎么定的**。

最老实的做法是：一批凑齐、一起跑，**得等最慢的那个跑完，整批才能散**，才能接下一批。于是短请求跟长请求凑成一批，短的就得陪着干等。这叫**队头阻塞**（head-of-line blocking）：**队头被一个慢的堵住，后面全跟着等**。

连续批处理只改了一件事：**把「一批」这个单位，从「一整个请求」缩到「一个字」。**

- 每走一轮就**重新挑一次人**；
- 谁跑完了**立刻下车**，空位当场坐进新请求；
- 机器不再等最慢的那个。

效果：**Orca 论文**报告同样延迟下吞吐提升 **36.9 倍**；**vLLM** 自己测是 **23 倍**。

## Q4 · PagedAttention 在解决什么问题？

这一招不碰「搬」也不碰「算」，它管的是**显存怎么摆**。

问题出在「预留」：**显存像一排连着的书架，规矩是按最长的那份给每人留一整格。**可请求有长有短，短的那个人占着一大格只用一点点，剩下的零头谁也塞不进去——**这就是碎片**。

PagedAttention 抄的是**操作系统管内存的老办法**：**把 KV 切成大小一样的小页，要用哪一页才给哪一页。**于是几乎不浪费显存，能塞进更多请求，批能开得更大。

## Q5 · 分块预填充和 prefill-decode 分离，是两件不同的事

这两件事**解决的不是同一个毛病**。

**分块预填充（chunked prefill）——同一批机器上错开。**第 2 课说过两段的脾气相反。于是有人贴一篇超长文章进来，机器会先花很久把它读完（第 1 轮那一次算完），**这段时间里正在写答案的那批人只能停着**。改法：把长文**切成几块**，**和写答案的轮次交替着跑**。代价是第一个字可能晚一点，回报是总吞吐更高。据 Weka 的综述，**Sarathi** 论文引入这一招，最多能带来 **6.9 倍**吞吐提升。

**prefill/decode 分离（disaggregated serving）更彻底：干脆把两段放到两批不同的机器上**，各用各自更擅长的硬件。据 Weka 综述，**DistServe**（OSDI 2024）报告：同样硬件能多接 **7.4 倍**的请求，或者把延迟目标（SLO）收紧到 **1/12.6** 还能达标；**Perplexity、Meta、LinkedIn、Mistral** 都已经在生产里这么跑了。

**分块预填充是「错开」，prefill/decode 分离是「分家」。**前者还在同一批卡上，后者要跨机器调度。

把这几招串起来看：**PagedAttention 抬高「能开多大的批」，连续批处理让「每一批都坐得满」，而 Q2 那个拐点决定「开到哪儿就该停」。**三件事缺一件，收益就打折。

## 检查一下你懂了没

**Q1　深夜没人用的时候，这一批会怎么变？**

- ✅ 会变小：在等的人少，挑出来的一批就小
- 不会变：批大小是机器一开始就定死的
- 会变大：没人抢，显卡算得过来了
- 不会变：批大小只由模型大小决定

答对时：对。每一轮都重新挑人，挑的是时间上正好撞在一起的那些。所以半夜批小、吞吐低是常态。
答错时：批不是配置死的，是每一轮按到达情况重新挑出来的。所以半夜批小、吞吐低是常态。

**Q2　批大小继续加大，吞吐为什么不涨了？**

- 瓶颈从算力变成了搬数据
- ✅ 瓶颈从搬数据变成了算力
- 瓶颈从显存变成了带宽
- 瓶颈从带宽变成了排队时间

答对时：对。批大到一定程度，搬运不再是瓶颈、算力用满了——再堆批量，吞吐就撞在算力上限上。
答错时：方向反了。批小的时候卡在搬数据，批大了搬运被摊薄，算力才成为瓶颈。

**Q3　一批里有个特别长的，其余都很短。一批要等齐了才散，会怎样？**

- 短请求会先跑完单独返回
- 长请求会被提前截断丢弃
- ✅ 短请求只能陪着长请求干等
- 全部重跑一遍取平均值

答对时：对。这叫「队头阻塞」——一批要等最慢的那个跑完才能散，短的全被拖着。
答错时：不会被截断，也不会先跑完。一整批一起跑、一起结束，短请求只能干等。

**Q4　PagedAttention 到底省了什么？**

- 网络延迟，让请求传得更快
- 搬运次数，让每步读得更少
- 算力开销，让矩阵乘更快
- ✅ 显存碎片，让批能开得更大

答对时：对。它管的是显存怎么摆——不再按最长的预留，于是能塞进更多请求，批就开得更大。
答错时：它不碰搬运次数，也不碰算力。它解决的是显存怎么分配：切页，用多少给多少。

## 一手资料（页脚框，一般不动）

- [Anyscale — How continuous batching enables 23x throughput](https://www.anyscale.com/blog/continuous-batching-llm-inference)：Q1 的陆续到达与到顶（每秒 8 个请求、每秒 1900 个字）、Q3 的连续批处理与 vLLM 的 23× 实测，都出自这里。
- [Anyscale — Understand LLM latency and throughput metrics](https://docs.anyscale.com/llm/serving/benchmarking/metrics)：Q1 那两句原话（系统吞吐随负载涨到上限、并发上去单个用户变慢）、以及"排队等待会算进首字延迟"。
- [Weka — Prefill and Decode: A Technical Guide](https://www.weka.io/learn/ai-ml/prefill-and-decode/)：Q5 的分块预填充（Sarathi，6.9×）、prefill/decode 分离（DistServe，7.4× / 12.6×）以及各家在生产里的用法，都出自这篇综述。
- [Orca 论文（OSDI'22）](https://www.usenix.org/system/files/osdi22-yu.pdf)：连续批处理（iteration-level scheduling）的原始论文，同样延迟下 36.9× 吞吐；Q1 的挑选单位也出自它。
- [Runpod — vLLM, PagedAttention and Continuous Batching](https://www.runpod.io/articles/guides/vllm-pagedattention-continuous-batching)：Q4 的工程落地。
- [Databricks — LLM Inference Performance Engineering](https://www.databricks.com/blog/llm-inference-performance-engineering-best-practices)：Q2 那个拐点的实测（批 64 → 吞吐 14×、延迟 4×）、"最划算的批大小"那句原话，以及 Llama2 权重 140GB、KV 占用那两张表。
- 算术强度的推导见 [第 2 课（进阶版）· Q2](../../lessons/llm/0002-prefill-vs-decode-deep.html#q3-intensity)。

## 提问框

**我是你的老师，随时打断我。**比如"每轮挑人的上限是谁定的？""'页'具体多大？""拐点能靠调参挪过去吗？""Databricks 那 14 倍是跟谁比的？"——直接问。最后一个尤其值得追。

## 页尾互链（一般不动）

- **回初学版**：[LLM 底层 · 第 4 课 · 一趟装满的卡车](../../lessons/llm/0004-batching.html)
- **前置**：[第 2 课 · 一次请求的两段](../../lessons/llm/0002-prefill-vs-decode.html)（本文的拐点从那课的算术强度推出来）· [第 2 课（进阶版）· Q2](../../lessons/llm/0002-prefill-vs-decode-deep.html#q3-intensity)
- **你会用到**：[Agent 评估检查单](../../reference/agent-eval-checklist.html)（agent 慢的时候，先把它的耗时按步量开）
- **顺着往下**：[Agent 原理篇 · 第 1 课 · Agent 到底是什么](../../lessons/agent/0001-what-is-an-agent.html)
- 术语表：[批处理](../../reference/glossary.html#batching) · [批大小](../../reference/glossary.html#batch-size) · [排队](../../reference/glossary.html#queueing) · [吞吐](../../reference/glossary.html#throughput) · [连续批处理](../../reference/glossary.html#continuous-batching) · [算术强度](../../reference/glossary.html#arithmetic-intensity)
