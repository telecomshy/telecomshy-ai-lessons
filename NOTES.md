# NOTES.md

学习者的偏好与教学约定。

> 依据 teach 技能：`NOTES.md` 记用户的偏好和约定，设计与学习者协作时回来参考。**开发流程、写作标准、操作手册都不在这里**——它们各有唯一落点，见下表。
>
> 2026-11-17 瘦身：流程纪律移到 [`internal/standards/PROCESS.md`](internal/standards/PROCESS.md)，历史索引移到 [`internal/history/INDEX.md`](internal/history/INDEX.md)，过期待办清出（下一步只看 [`NEXT-SESSION.md`](NEXT-SESSION.md)）。本文件只留「这个学习者是谁、怎么教他」。

## 1. 学习者的画像

**分两层**（2026-09-30 定）：技术层读者（学习者本人）是 LLM 轨 deep 的标准；LLM 轨基础课、Agent 篇与 RAG 轨的理论课面向初学者和业务人员，标准是「学完能听懂技术对话」。下面「会追问机制、会自己验算」这些特征只对 deep 与实操课成立，薄层课别按它写。

- 编程基础：有。用过 LLM API（调接口、写 prompt），未系统构建过 agent。
- **会追问机制的精确性**：不接受停在类比上（曾指出「标签卡／内容卡」站不住、「每蹦一个字就是一次调用」不严谨）。类比之后必须补上真实机制。⚠ 这条管的是机制正文，不是比喻本身：比喻要生动优先，不必逐句对应机制；精确性由「类比之后补的那段真实机制」承担，两层不许互相挤。
- **对「机制＋数量关系」敏感**：会自己推公式（已独立推出 `N(N+1)/2`）。讲取舍时带出量级计算。
- **会用「这个信息从哪来、用完去哪」质疑机制**：讲任何机制时显式标注每个量的来源与生命周期（LR-0005 推进一层：不只来源，还要消费方与时机）。
- **会自己拆解自己建的错误模型**：他能判断「我把两件事当一步了，所以产生了矛盾」（LR-0005）。具备自查能力，缺的是课件把隐含依赖显式写出来。
- **同一卡点会换四种问法反复问**（LR-0005）：遇到与上次相似的问题，先确认问的是不是同一层意思，别急着按字面答。
- **文字讲不通就配图**：跨层、跨位置的数据流向，文字版连卡三次，画成一张「跟踪某一行往下走」的图之后一次通。
- **把「LLM 底层原理」与「agent 应用」视为两件事**，要求分开组织；后来又要求把技巧单独成篇。讲课时要说清「这属于哪条轨道、为什么」。
- 动机：搞懂原理＋满足好奇，同时想要「能动手做出来」的掌握感。
- 偏好：项目驱动、边做边学；每课要有可动手且有即时反馈的部分。
- 语言：中文讲解；一手资料多为英文，接受。
- 自评方向：全都要，先建全景，再按需深入。

## 2. 教学偏好（八条）

2026-10-21 学习者定；文字怎么执行见 [`internal/standards/ARTICLE-STYLE.md`](internal/standards/ARTICLE-STYLE.md)。

1. 开场接上一课刚做的事，再连问几个日常问题；不编故事。
2. 新课从上一课的具体机制里长出来。
3. 机制讲到底层实现，不停在类比。
4. 概念先给两条路的对比，再下定义。
5. 实操给全路径：去哪找、配置长什么样、依赖什么、有没有捷径。
6. 生态信息要给：鉴权、收费、SDK。
7. 提示类内容大幅精简。
8. 口语连接词照用；中英文之间加空格。

## 3. 其它约定

- 学习者每周可投入的时间还没收集，排期别按固定节奏估。
- 学习者说「改课」按整课重过，不做局部打补丁；证据与流程见 [`internal/standards/REVISION.md`](internal/standards/REVISION.md)。
- 课程里的个人疑问只在它真的进入公共知识时留着；单个学习者的临时困惑不进课件。

## 4. 各类文档去哪找

| 你要什么 | 去哪 |
|---|---|
| 当前进度、下一步、待确认 | [`NEXT-SESSION.md`](NEXT-SESSION.md) |
| 开发流程、取材、交付核验 | [`internal/standards/PROCESS.md`](internal/standards/PROCESS.md) |
| 页面零件、课型、讲法、互链、交付检查单 | [`internal/standards/COURSE-STANDARD.md`](internal/standards/COURSE-STANDARD.md) |
| 正文文章体 | [`internal/standards/ARTICLE-STYLE.md`](internal/standards/ARTICLE-STYLE.md) |
| 改课／精修流程 | [`internal/standards/REVISION.md`](internal/standards/REVISION.md) |
| 分版、受众、课型标识、脚本分层 | `internal/standards/tracks/<轨道>.md` |
| 联网、改课件、学习审计的具体做法 | [`internal/playbooks/`](internal/playbooks/) |
| 当初为什么这么定、踩过什么坑 | [`internal/history/INDEX.md`](internal/history/INDEX.md) |
| 学习者已经掌握了什么 | [`internal/learning-records/`](internal/learning-records/) |

> AI生成
