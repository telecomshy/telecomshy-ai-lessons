# Domain Docs

本仓库用 single-context 布局。

## 先读什么

- `CONTEXT.md`（仓库根目录，懒创建）：跨课共享的领域术语、口径、不变量。
- `docs/adr/`（懒创建）：架构与结构决策记录。
- `reference/glossary.html`：已经存在的术语单一落点。**新术语先进这里**；只有当一条术语跨多课、且术语表装不下（要带取舍与不变量）时，才在 `CONTEXT.md` 里立条目并链回术语表。

## 边界

- 学习者的掌握情况 → `docs/learning-records/`，不是领域文档。
- 课程开发规矩 → `NOTES.md`，不是领域文档。
- 找不到 `CONTEXT.md` / `docs/adr/` 就静默继续，别为了「齐全」先建空文件（setup 技能的懒创建约定）。
