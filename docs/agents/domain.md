# Domain Docs

本仓库用 single-context 布局。领域文档分两层，别混。

## 先读什么

- `GLOSSARY.md`（仓库根目录，懒创建）：**仓库/课程开发领域的术语表**——轨道、课号、基础课/进阶版、别名、`completed` 这类词的口径。只放术语定义和 `_Avoid_`，不写实现细节、决策或不变量。mattpocock 的 `domain-modeling` 技能读取和更新它。
- `docs/adr/`（懒创建）：架构与结构决策记录；带取舍的跨课决策、不变量写这里，或写进 `NOTES.md` 第 1 节。
- [`reference/glossary.html`](../../reference/glossary.html)：**课程内容术语**（Agent、KV cache、prefill/decode 等），也是学习者看到的术语表；课里的术语链接都指向它。

## 两层怎么分工

- **课程内容术语** → `reference/glossary.html`。新术语先进这里，课里的说法以它为准。
- **仓库/课程开发术语** → `GLOSSARY.md`。`GLOSSARY.md` 提到课程内容术语时，链到 `reference/glossary.html#...`，不要复制定义。
- 同一术语两层都出现时，**定义只写一处**：课程含义在 HTML，仓库用法在 `GLOSSARY.md` 里链过去。
- 新术语先判断属于哪一层，再决定写哪里。拿不准时，先问学习者。

## 边界

- 学习者的掌握情况 → `docs/learning-records/`，不是领域文档。
- 课程开发规矩 → `NOTES.md`，不是领域文档。
- 找不到 `GLOSSARY.md` / `docs/adr/` 就静默继续，别为了「齐全」先建空文件（setup 技能的懒创建约定）。
