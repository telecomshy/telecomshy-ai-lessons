"""Agent 篇 · 第 4 课 配套脚本：给 agent 接一个 MCP 工具（离线演示）。

MCP＝工具的统一插口。接一个 MCP server 分三步：
    1. 写配置（mcpServers JSON：command / args / env）
    2. 连上后先「发现」：问它「你能干什么？」
    3. 把它公布的工具清单交给模型（清单会算进上下文）

这个脚本离线模拟这三步：读一份配置 → 校验字段 → 模拟发现往返 → 打印清单。
不连真 server，不调 API。

运行：  python exercises/agent/0004-mcp-config.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

import json
import re

# ---- 第 1 步：配置长什么样（真实 harness 都是读这样一份 JSON） ----
CONFIG = {
    "mcpServers": {
        "weather-server": {
            "command": "npx",
            "args": ["-y", "@example/weather-mcp"],
            "env": {"API_KEY": "sk-demo"},
        }
    }
}

# ---- 模拟 server 公布的工具（真实场景里，这一步是连上后问出来的） ----
SERVER_CATALOG = {
    "weather-server": [
        {"name": "get_weather",
         "description": "查某个城市今天的天气。返回气温（摄氏度）和天气状况。",
         "parameters": {"type": "object",
                        "properties": {"city": {"type": "string", "description": "城市名，例如「北京」"}},
                        "required": ["city"]}},
        {"name": "get_forecast",
         "description": "查某个城市未来三天的天气趋势。返回每天的气温和天气状况。",
         "parameters": {"type": "object",
                        "properties": {"city": {"type": "string", "description": "城市名"}},
                        "required": ["city"]}},
    ]
}


def validate(config):
    """配置校验——最常见的翻车就这几条。返回 (问题列表, 服务名列表)。"""
    problems = []
    servers = config.get("mcpServers")
    if not isinstance(servers, dict) or not servers:
        return ["顶层必须是 mcpServers 对象，且至少有一个服务"], []

    names = []
    for name, cfg in servers.items():
        names.append(name)
        if not re.fullmatch(r"[a-z0-9-]+", name):
            problems.append(f"服务名 {name!r} 只能用小写字母、数字、连字符")
        if not isinstance(cfg, dict):
            problems.append(f"{name}：配置必须是对象")
            continue
        if not isinstance(cfg.get("command"), str) or not cfg.get("command"):
            problems.append(f"{name}：缺 command（启动命令，如 npx / python / node）")
        if not isinstance(cfg.get("args"), list):
            problems.append(f"{name}：args 必须是数组（没有参数就写 []）")
        if "env" in cfg and not isinstance(cfg["env"], dict):
            problems.append(f"{name}：env 必须是对象（键值对）")
    return problems, names


def main():
    print("=" * 58)
    print("MCP 接入演示：配置 → 校验 → 发现 → 清单")
    print("=" * 58)

    print("\n[第 1 步] 配置（真实 harness 读的就是这样一份 JSON）：")
    print(json.dumps(CONFIG, ensure_ascii=False, indent=2))

    problems, names = validate(CONFIG)
    print("\n[第 2 步] 校验字段：")
    if problems:
        for p in problems:
            print(f"  BAD  {p}")
    else:
        for n in names:
            print(f"  OK   {n}：command/args 齐了，env 可选")
        print("  （字段口径：command 必填；args 必填可空；env 可选，放 API key 这类）")

    print("\n[第 3 步] 发现：连上先问「你能干什么？」")
    print("  client -> server： 你能干什么？")
    for n in names:
        for t in SERVER_CATALOG[n]:
            print(f"  server -> client： {t['name']} —— {t['description']}")

    tools = [t for n in names for t in SERVER_CATALOG[n]]
    print(f"\n[第 4 步] 清单就绪：{len(tools)} 个工具，交给模型的是「名字＋说明＋参数」：")
    for t in tools:
        req = ",".join(t["parameters"].get("required", [])) or "（无必填）"
        print(f"  {t['name']:<14} 参数必填：{req}")

    print("\n" + "=" * 58)
    print("记住三件事：① 照抄配置容易翻在字段上，先校验；")
    print("② 接上先「发现」，别硬编码工具；③ 清单会被算进上下文——")
    print("工具不是越多越好，用不上的别挂。")
    print("=" * 58)


if __name__ == "__main__":
    main()
