# Triage Labels

setup 技能用五个规范角色描述 issue 状态。本仓库的 GitHub 标签目前是默认集，这五个专用标签**还没有建**。

| setup 技能角色 | 本仓库现状 | 含义 |
|---|---|---|
| `needs-triage` | 无标签（新 issue 默认） | 维护者还没评估 |
| `needs-info` | `question` | 等提问者补充信息 |
| `ready-for-agent` | 无 | 描述完整，可交给 agent 处理 |
| `ready-for-human` | `bug` / `enhancement` | 需要人来改 |
| `wontfix` | `wontfix` | 不处理 |

跑 `triage` 之前，先把缺的四个标签建出来（一次性）：

```powershell
gh label create needs-triage --description "维护者还没评估" --color FBCA04
gh label create needs-info --description "等待提问者补充信息" --color D4C5F9
gh label create ready-for-agent --description "描述完整，可交给 agent" --color 0E8A16
gh label create ready-for-human --description "需要人工实现" --color 1D76DB
```
