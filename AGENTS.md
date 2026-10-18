# AGENTS.md

这个仓库是一部中文 AI Agent 教程：课件是 `lessons/` 下自包含的 HTML，配套脚本在 `exercises/`。

## 动手前先读

- **改课、开课、标 `completed`**：先读 [`NOTES.md`](NOTES.md) 第 1 节（硬规则）；操作细节在 [`docs/notes/rules/`](docs/notes/rules/)，历史决策与教训在 [`docs/notes/history/`](docs/notes/history/)。
- **写任何知识点**：只从 [`RESOURCES.md`](RESOURCES.md) 的一手资料取，不凭模型记忆；新来源当场补进去，并注明用途。
- **学习者已掌握什么**：看 [`docs/learning-records/`](docs/learning-records/)（teach 技能的学习记录）。那是学习证据，别跟 `docs/notes/` 的开发史混。

## Agent skills

### Issue tracker

Issues 存在 GitHub Issues，仓库 `telecomshy/telecomshy-ai-lessons`，用 `gh` CLI 操作。见 [`docs/agents/issue-tracker.md`](docs/agents/issue-tracker.md)。

### Triage labels

本仓库沿用 GitHub 默认标签（`bug` / `enhancement` / `question` / `documentation` / `wontfix`）。setup 技能要求的五个 triage 角色还没有专用标签，对应关系见 [`docs/agents/triage-labels.md`](docs/agents/triage-labels.md)。

### Domain docs

Single-context：`CONTEXT.md` 在仓库根目录，ADR 在 `docs/adr/`，两者都按需懒创建。见 [`docs/agents/domain.md`](docs/agents/domain.md)。
