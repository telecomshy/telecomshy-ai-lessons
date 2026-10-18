"""Agent 篇 · 第 6 课 配套脚本：编排一群 agent（编排者-工作者）。

一个 lead（编排者）拆活、派单、汇总；三个 worker（工作者）各管一摊、只回结论。
看三件事：
    1. 派单要写清：目标 / 输出格式 / 边界（写糊了 worker 就跑偏）
    2. 只回结论、不回流水——lead 的上下文才装得下
    3. worker 会失败：重派一次的兜底要写在编排逻辑里

纯离线，假模型。真模型只要给 worker/lead 各换一个模型函数（同第 2 课）。

运行：  python exercises/agent/0006-orchestrate-agents.py
Windows 终端若中文乱码：先执行  chcp 65001
"""

# ============ 外部世界：三个玩具工具 ============
WEATHER_DB = {"北京": (31, "晴"), "青岛": (26, "多云"), "广州": (33, "雷阵雨")}
PRICE_DB = {"北京": 980, "青岛": 760, "广州": 890}          # 人均预算（元）
ACTIVITY_DB = {"北京": "故宫+胡同骑行", "青岛": "海边烧烤+帆船", "广州": "早茶+珠江夜游"}

FAILED_ONCE = {"worker-price"}        # 演示：这个 worker 第一次会失败


def get_weather(city):
    if city in WEATHER_DB:
        t, cond = WEATHER_DB[city]
        return {"city": city, "temp_c": t, "cond": cond}
    return {"error": f"查不到「{city}」"}


def get_price(city):
    if city in PRICE_DB:
        return {"city": city, "per_person_yuan": PRICE_DB[city]}
    return {"error": f"查不到「{city}」"}


def get_activity(city):
    return {"city": city, "plan": ACTIVITY_DB.get(city, "待定")}


TOOLS = {"get_weather": get_weather, "get_price": get_price, "get_activity": get_activity}

# ============ 派单：目标 / 输出格式 / 边界，三样都要写清 ============
WORKER_SPECS = [
    {"id": "worker-weather", "tool": "get_weather",
     "goal": "比较北京、青岛、广州下周的天气，挑一个最舒服的",
     "format": "一句话结论：推荐哪座城市、为什么",
     "bound": "只看天气，不要考虑价格"},
    {"id": "worker-price", "tool": "get_price",
     "goal": "查三城的人均预算，挑最划算的",
     "format": "一句话结论：推荐哪座城市、多少钱",
     "bound": "只看价格，不要考虑天气"},
    {"id": "worker-activity", "tool": "get_activity",
     "goal": "看看三城各有什么团建玩法",
     "format": "一句话结论：推荐哪座城市、玩什么",
     "bound": "只看玩什么，别替别人做决定"},
]


def run_worker(spec, city_tool_map, attempts):
    """worker 的小循环：调工具 -> 看结果 -> 只回一句结论。"""
    logs = []
    for city in city_tool_map:
        result = TOOLS[spec["tool"]](city)
        logs.append(f"{spec['tool']}({city}) -> {result}")
        if spec["id"] in FAILED_ONCE and attempts == 1 and "error" not in result:
            return {"ok": False, "logs": logs + ["ERROR 工具超时"], "verdict": None}

    # 假模型的"推理"：挑个数给结论
    if spec["tool"] == "get_weather":
        best = max(city_tool_map, key=lambda c: -WEATHER_DB[c][0])   # 气温别太高
        verdict = f"推荐{best}：{WEATHER_DB[best][0]} 度 {WEATHER_DB[best][1]}，最舒服"
    elif spec["tool"] == "get_price":
        best = min(city_tool_map, key=lambda c: PRICE_DB[c])
        verdict = f"推荐{best}：人均 {PRICE_DB[best]} 元，最划算"
    else:
        best = "青岛"
        verdict = f"推荐{best}：{ACTIVITY_DB[best]}"
    return {"ok": True, "logs": logs, "verdict": verdict}


def lead(task, cities):
    print("=" * 58)
    print(f"[lead] 收到任务：{task}")
    print("=" * 58)

    print("\n[lead] 拆活、派单（目标 / 输出格式 / 边界 三样写清）：")
    for s in WORKER_SPECS:
        print(f"  -> {s['id']}")
        print(f"     目标：{s['goal']}")
        print(f"     输出：{s['format']}   边界：{s['bound']}")

    verdicts, all_logs = [], []
    for s in WORKER_SPECS:
        for attempt in (1, 2):
            r = run_worker(s, cities, attempt)
            all_logs += r["logs"]
            if r["ok"]:
                print(f"\n[{s['id']}] " + "；".join(r["logs"]))
                print(f"[{s['id']}] 结论：{r['verdict']}")
                verdicts.append((s["id"], r["verdict"]))
                break
            print(f"\n[{s['id']}] " + "；".join(r["logs"]))
            print(f"[lead] {s['id']} 失败，重派一次（兜底就写在这里）")

    print("\n[lead] 收到 %d 份结论（只回结论，不回流水）：" % len(verdicts))
    for wid, v in verdicts:
        print(f"  - {wid}：{v}")

    summary = "综合推荐青岛：天气舒服、人均 760 最划算、能上海边烧烤+帆船。"
    print(f"\n[lead] 汇总：{summary}")

    flow = "\n".join(all_logs)
    print("\n" + "-" * 58)
    print("上下文对账：")
    print(f"  lead 只装结论：约 {sum(len(v) for _, v in verdicts)} 字")
    print(f"  若装全部流水：约 {len(flow)} 字（{len(flow) // max(1, sum(len(v) for _, v in verdicts))} 倍）")
    print("  这就是「只回结论不回流水」省下的钱——多 agent 的账一半在这里。")
    print("-" * 58)


if __name__ == "__main__":
    lead("给下周团建挑一个城市", ["北京", "青岛", "广州"])
    print("\n翻车提醒：任务太小别上多 agent——拆活、派单、汇总本身就要花钱，")
    print("单个 agent 三五个工具调用能干完的活，叫帮手纯属亏本。")
