# 手写一个 agent

> 这是 `lessons/agent/0002-build-an-agent.html` 的文字稿：**直接在上面改，改完交回，我逐段映射回 HTML 并跑核验**。
> 改法与标记约定见 [README](../README.md)：✅ 标正确选项、「答对时/答错时」是小测反馈、【图】【选读框】等标记说明、小节可增删合并（节号乱了没关系，回写时重排）。

---

【meta】Agent 篇 · 第 2 课 · 实操

Agent 篇 · 第 2 课 · 实操

## 开场（页首框）

上一课的循环、工具、记忆，听着都对；但「听懂」和「跑起来」之间还隔着几步：装什么包、key 放哪、报错了先看什么。

这课从零把它跑起来。**所谓 agent，核心代码其实只有十几行**，就是一个循环。真正费心的是外面那圈防错和护栏。

**学完这课，你能**：从零把环境配好、跑通一个真 agent；看懂并改动它的完整代码；说清真模型会在哪出错、代码里哪一行在兜底。

## 主线（记住这一句的框）

agent 的核心就是**把一个循环转起来**：**推理**（模型说话）→ **行动**（调工具）→ **观察**（结果塞回）→ 再**推理**……直到模型认为说完了。

循环只写一遍；厂商接口的差异全关在 `model_fn` 那一层，也就是「适配层」。

（不打算真跑的话，第 1～6 节可以整节跳过——那几节是装包、配 key、验通路；从第 7 节的实跑输出接着读，第 8 节再把脚本拆开。）

## 1. 先确认 Python 能跑

这一课要用的 SDK 要求 **Python 3.10 或更高**。打开 PowerShell，先看版本：

```
python --version
```

看到 `Python 3.12.9` 这样的输出就对了。没有 `python` 命令、或者一输就弹出微软商店，说明 Python 没装好或没进 PATH（PATH 是系统按名字找命令的那张清单）：去 [python.org/downloads](https://www.python.org/downloads/) 重新装，安装第一屏记得勾上 **Add python.exe to PATH**。

Windows 上也可以换 `py` 启动器，效果一样：

```
py -3.12 --version
```

## 2. 建一个干净的实验环境

接下来的包装在项目自己的虚拟环境里，不污染系统 Python。先进入仓库根目录，再建环境、激活：

```
cd E:\code\my_projects\learn-ai-agents   # 换成你自己的仓库路径
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

激活成功后，命令行前面会多一个 `(.venv)`。以后每次新开窗口跑这一课的脚本，都要先激活一次。macOS / Linux 的激活命令是 `source .venv/bin/activate`。

**如果报「无法加载文件，因为在此系统上禁止运行脚本」**：这是 PowerShell 的执行策略，不是环境坏了。对当前窗口放行一次，再激活：

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

`-Scope Process` 只影响这个窗口，关掉就恢复，不会改系统设置。`.venv/` 已经在 `.gitignore` 里，不会进 git。

## 3. 装两个包

环境建好了，但里面还空着——把两个包装进去，脚本才连得上模型。确认 `(.venv)` 还在，然后：

```
python -m pip install -U openai python-dotenv
```

卡在 `Resolving dependencies` 超过两三分钟，就 Ctrl+C 停掉，换国内镜像重试，例如清华源：`python -m pip install -U openai python-dotenv -i https://pypi.tuna.tsinghua.edu.cn/simple`。

两个包各管一件事：

- **`openai`** —— OpenAI 官方 SDK。替我们拼请求、解析 `tool_calls`、处理重试和超时。不用它也能手写 HTTP，但那些坑没必要在学循环时踩。
- **`python-dotenv`** —— 从 `.env` 文件里读 key，这样 key 不写进代码。

装完验一下版本：

```
python -c "import openai, dotenv; print(openai.__version__)"
```

本机实测输出 `3.35.1`（2026-10-18）。你装到更新的版本也行，这一课只用最稳定的 Chat Completions 接口（OpenAI 家对话接口的名字）。

## 4. 申请一个 API key

两个包装好了，但要连模型，还得先有 key。这一课默认用 DeepSeek 的 `deepseek-flash`：它兼容 OpenAI 的接口格式，价格低，文档有中文。步骤：

1. 打开 [platform.deepseek.com](https://platform.deepseek.com/)，注册 / 登录。
2. 进 **API keys** 页面，点创建，把 key 复制下来——**它只完整显示这一次**。
3. 去 **充值** 页充一点。这一步绕不过：余额为 0 时接口返回 402。

**key 等于密码 + 钱包**：不要写进代码、不要贴进聊天记录、不要截图发出去。下面把它放进一个不会进 git 的文件。

## 5. 把 key 放进 .env，而不是代码里

在仓库根目录新建一个文件，名字就叫 `.env`（注意不是 `.env.txt`），里面只写一行：

```
DEEPSEEK_API_KEY=sk-你的key
```

三条格式要求：**不要引号**、**等号两边不要空格**、**保存成 UTF-8**。多一个空格，读出来就是错的 key。

确认它被 git 忽略：

```
git check-ignore -v .env
```

能打印出 `.gitignore` 里那一行就对了。代码里用 `load_dotenv()` 读它，所以 key 永远不会出现在源码里——这份代码可以放心分享、提交。

**也可以不开文件，直接设环境变量**（`$env:DEEPSEEK_API_KEY = "sk-..."`），但它只在当前窗口有效，关掉就没了；用 `setx` 能永久保存，但要新开窗口才生效。日常学习推荐 `.env`。

**三个变量名是这份脚本自己约定的**，不是 DeepSeek 规定的：`DEEPSEEK_API_KEY`（必填）、`DEEPSEEK_MODEL`（默认 `deepseek-flash`）、`DEEPSEEK_BASE_URL`（默认 `https://api.deepseek.com`）。后两个写进 `.env` 也能覆盖。

## 6. 先花小钱验通路

正式跑之前，先做一次很小的调用：只发一句话、只让它回两个字，key 对不对、网络通不通、模型名对不对，一次全验掉：

```
python exercises/agent/0002-build-an-agent.py --check
```

本机实测输出：

```
模型：deepseek-flash   接口：https://api.deepseek.com
回复：收到
用掉 token：输入 9 / 输出 1，耗时 1.2 秒
通路正常，可以跑正式的了：python exercises/agent/0002-build-an-agent.py
```

看到「通路正常」再往下（耗时会随着网络和模型负载变，差一两秒正常）。报错的话照下面几种查（DeepSeek 官方错误码）：

- **401 认证失败**：key 不对或已失效，先查 `.env` 里有没有引号、空格，再确认这个 key 没被删。
- **402 余额不足**：去平台充值。
- **429 限流**：等一会儿，或看余额与并发。
- **500 / 503**：服务端的事，等一会儿重试。
- **连不上**：检查网络或代理，`DEEPSEEK_BASE_URL` 别多写斜杠。

还有一个最常见的坑：**`.env` 放错了地方**。脚本会从自己所在目录（`exercises/agent/`）逐级往上找 `.env`，所以放在仓库根目录能读到；放到别的盘或别的项目里就读不到了。

## 7. 跑起来

```
python exercises/agent/0002-build-an-agent.py
```

四个问题，本机实测输出：

```
模型：deepseek-flash   接口：https://api.deepseek.com

==========================================================
真模型（deepseek-flash）：同一个 run_agent，看它怎么走
==========================================================

──────────────────────────────────────────────────────────
用户问：北京今天多少度？
──────────────────────────────────────────────────────────
  [1] 调工具：get_weather({'city': '北京'}) -> {"city": "北京", "temp_c": 26, "cond": "晴"}
  [2] 完成：北京今天气温 **26°C**，天气晴朗 ☀️
  >> done，共走 2 步，耗时 2.0 秒

──────────────────────────────────────────────────────────
用户问：上海比北京热多少？
──────────────────────────────────────────────────────────
  [1] 调工具：get_weather({'city': '上海'}) -> {"city": "上海", "temp_c": 28, "cond": "多云"}
  [1] 调工具：get_weather({'city': '北京'}) -> {"city": "北京", "temp_c": 26, "cond": "晴"}
  [2] 完成：上海今天比北京热 **2°C**：
      
      | 城市 | 气温 | 天气 |
      |---|---|---|
      | 上海 | 28°C | 多云 |
      | 北京 | 26°C | 晴 |
  >> done，共走 2 步，耗时 2.0 秒

──────────────────────────────────────────────────────────
用户问：有哪些城市能查？
──────────────────────────────────────────────────────────
  [1] 调工具：list_cities({}) -> {"cities": ["上海", "北京", "广州"]}
  [2] 完成：目前可以查天气的城市有 3 个：**上海、北京、广州**。
      
      需要我帮你查其中某个城市的天气吗？
  >> done，共走 2 步，耗时 1.5 秒

──────────────────────────────────────────────────────────
用户问：魔都今天多少度？
──────────────────────────────────────────────────────────
  [1] 调工具：get_weather({'city': '上海'}) -> {"city": "上海", "temp_c": 28, "cond": "多云"}
  [2] 完成：魔都（上海）今天 **28°C**，多云 ☁️
  >> done，共走 2 步，耗时 2.0 秒

==========================================================
这几次调用一共花掉了：
  输入 token：2969   输出 token：279
  按空闲时段价估算：约 0.00409 元（缓存命中会更便宜）
==========================================================
```

（token＝模型数着计费、计长度的字词单位；耗时和 token 数每次会有少量出入，下面的账单按当次实算。）

先看第二个问题：它出现了两条 `[1]`。不是打印错了——模型在**同一轮**里一次要了两个工具。只看别人写好的 demo，最容易漏掉这一点；第 8、9 节都会回到它。

「魔都」它也认得出。脚本里没有「魔都＝上海」这条规则，是模型自己从语义里认出来的。

答案里还有 `**` 和 `|`。模型爱用 Markdown 排版，终端不渲染，星号和竖线就原样露出来——接进网页或聊天框才好看。

四个问题各花了 1.5～2.0 秒，里面每一步都是一次网络往返——这就是「真模型要等」的字面意思，不是本地算出来的。

还有一处输出里看不出来的：四个问题各转各的循环——`run_agent` 每次都新建一份 `messages`，问题之间不共享历史。

## 8. 脚本拆开，只有四块

这份脚本就是上一课说的壳，最小号的那种：转循环、执行工具、装护栏，全是它的活。先看一次工具调用的完整来回：

【图】../../assets/tool-call-roundtrip.svg（图片文件不动）

替代文字（alt）：两栏时序图：左边是模型，只会吐字；右边是你的程序和外部世界。工具清单与用户问题送进去，模型回一段「我要调 get_weather(city=北京)」的文字；程序解析这段文字、真的去查天气库，把结果作为 tool_result 塞回对话；模型再输出人话。底部注明：模型的输出永远是文字，真正动手的是程序

图注：**一次工具调用 = 五步走完一个来回**：清单和问题送进去 → 模型写「要调什么」 → 程序真的去调 → 结果塞回 → 模型再说人话。图里画的是一个工具；真模型一步要两个时，就是「② 写两条、③ 调两次、④ 塞回两条」。

### 第一块：工具（agent 能对外做的事）

两个玩具工具，背后是个写死的小「天气库」：

```python
def get_weather(city):
    if city in WEATHER_DB:
        return {"city": city, **WEATHER_DB[city]}
    return {"error": f"查不到「{city}」的天气"}
```

return 里那个 `**` 是 Python 的字典合并写法，把气温、天气并进同一个结果。再往下是**工具清单**——上一课说的「名字＋一句话说明＋参数」三件套，模型照着它挑工具、填参数：

```
TOOL_LIST = [
    {"type": "function",
     "function": {
         "name": "get_weather",
         "description": "查某个城市今天的天气。返回气温（摄氏度）和天气状况。",
         "parameters": {"type": "object",
                        "properties": {"city": {"type": "string", "description": "城市名，例如「北京」"}},
                        "required": ["city"]}}},
    ...
]
```

注意外面多包了一层 `{"type": "function", "function": {...}}`——这是接口要求的信封，名字、说明、参数装在里面。真正执行时用的是另一个字典 `TOOLS`：名字 → 函数。两张表要同步改，漏一个就多一种出错方式（第 10 节有练习）。

### 第二块：model_fn——把接口适配成循环要的形状

循环不关心 OpenAI 还是 DeepSeek。它只认两种回话：`text`（说完了）或 `tool_use`（要调工具）。把所有接口细节翻译成这两种形状的，就是 `model_fn`：

```python
def model_fn(messages, tools):
    m = call_model(messages, tools)

    if m.tool_calls:
        calls = [{"name": tc.function.name,
                  "input": json.loads(tc.function.arguments or "{}"),
                  "tool_msg": (lambda tid: lambda result: {
                      "role": "tool", "tool_call_id": tid,
                      "content": json.dumps(result, ensure_ascii=False)})(tc.id)}
                 for tc in m.tool_calls]
        return {"type": "tool_use", "calls": calls,
                "history": [m.model_dump(exclude_none=True)]}

    return {"type": "text", "text": (m.content or "").strip()}
```

循环对 `model_fn` 的约定，落在这几处细节上：

- **`m.tool_calls` 是个列表**：可能一条，也可能好几条。这里**全部接住**，每条都带着自己的 `id`（`tool_call_id`）。
- **`history` 把模型说的那句话原样放回对话**。`model_dump(exclude_none=True)` 把 SDK 对象转成字典，顺手去掉空字段。这条助手消息里带着 `tool_calls`，下一轮必须原样出现——接口靠它把结果和请求对上。
- **结果必须带 `tool_call_id` 挂回去**。少了它，接口不知道这条结果是回答哪一次调用的，直接 400。打包结果用的 `json.dumps(result, ensure_ascii=False)`，末尾那个参数是让中文原样保留、不转成转义符。

那行两层 `lambda` 是全脚本最绕的写法：外层先把这一次调用的 `id` 固定下来，内层等结果到手，把结果带上这个 `id` 打包成一条 `role:"tool"` 的消息。语法读不懂可以先跳过，拆开就是「固定编号、等结果、打包塞回」三步。参数也是它处理的：模型发回的参数是一段 JSON 文本，`json.loads` 把它变回字典，空的就补 `{}`。

还有一处藏在真正发请求的 `call_model` 里（本课没贴它，脚本里能看到）：请求带了 `extra_body={"thinking": {"type": "disabled"}}`。**DeepSeek 的思考模式默认是开的**，而带工具时，接口要求把历次思考内容原样传回，否则 400。本课只看循环，关掉最省事——想了解思考模式，见 [LLM 底层 · 第 5 课](../../lessons/llm/0005-reasoning-models.html)。

### 第三块：run_agent——agent 的全部核心代码

```python
def run_agent(question, model_fn, max_steps=6):
    messages = [
        {"role": "system", "content": "你可以使用下列工具来回答问题。"},
        {"role": "user", "content": question},
    ]
    trace = []

    for step in range(1, max_steps + 1):
        reply = model_fn(messages, TOOL_LIST)         # ① 推理

        if reply["type"] == "text":                   # 模型认为说完了 → 停
            trace.append((step, "完成", reply["text"]))
            return {"status": "done", "answer": reply["text"], "steps": step, "trace": trace}

        messages += reply["history"]                  # ③ 观察（上半）：它说的那句

        for call in reply["calls"]:                   # ② 行动：模型一次可能要调好几个工具
            fn = TOOLS.get(call["name"])
            if fn is None:                            # 真模型真会编出不存在的工具
                result = {"error": f"没有这个工具：{call['name']}"}
            else:
                try:
                    result = fn(**call["input"])      # 真模型真会填错参数
                except Exception as e:
                    result = {"error": f"工具执行出错：{e}"}

            trace.append((step, "调工具",
                          f"{call['name']}({call['input']}) -> {json.dumps(result, ensure_ascii=False)}"))
            messages.append(call["tool_msg"](result))   # ③ 观察（下半）：结果逐条塞回

    return {"status": "hit_max_steps", "answer": None, "steps": max_steps, "trace": trace}   # 护栏
```

循环还是上一课那个循环，注释里的 ①②③ 就是推理、行动、观察：推理＝把整个 `messages` 交给 `model_fn`，换回一个动作（一步就是问一次模型，一轮里要两个工具也只算一步）；行动＝你的程序真的去调工具，一个动作可能带好几条调用，代码里是挨个执行；观察＝先把它说的那句放回去，再把**每条**结果挂回去——**顺序反了或漏了一条，接口就报 400**。

messages 开头那条 `role:"system"`，就是上一课说的系统提示。这份代码里真正新的，是兜底和护栏：两个兜底（`fn is None`、`try/except`）不是摆设，真模型真会编工具、填错参数；`max_steps` 走满还没完，最后的 `return` 强制停，就是上一课说的最大步数护栏。

### 第四块：打印 trace 和账单

`run_stage()` 把每次的 `trace` 打印出来，`print_bill()` 把 token 记成钱。**想调试 agent，第一件事就是打印 trace**——它走了几步、调了什么、拿到了什么，全在里面。

## 9. 真模型会在哪里出错

这份脚本的第一版是按「一次只回一个工具」写的，第一次真跑就报了一个错：

```
接口报错 400：Error code: 400 - {'error': {'message': "An assistant message with 'tool_calls' must be followed by tool messages responding to each 'tool_call_id'. (insufficient tool messages following tool_calls message)", ...}}
```

原因就在上一节：问「上海比北京热多少」时，模型**一轮里要了两个工具**，而第一版只执行了第一个，却把整条含两个 `tool_calls` 的助手消息放回了历史。接口一看：两个调用只收到一条结果，非法。

报这个错的根子，是**真模型的行为不由你设想**。它可能：

- **一次要多个工具**——就是上面这条。代码要按列表处理，每条都执行、每条都回。
- **认语义，不认关键词**——「魔都」它知道是上海。好处是不用把用户会怎么问全写进 if；代价是它的「理解」你预测不了。
- **编出清单里没有的工具、填错参数**——这次没遇到，但随时会。所以 `fn is None` 和 `try/except` 从第一天就在。
- **绕圈、中途放弃、提前收工**——可能查了一家就下结论，也可能一直「再查一家」。`max_steps` 是最后一道闸。
- **花钱、要等**——每一步都是一次网络往返＋真金白银（第 11 节算账）。
- **接口格式由厂商定**——`tool_call_id` 怎么挂、思考模式怎么关、并行调用支不支持，各家不一样。这就是适配层存在的理由。

**真 agent 的代码，很多是在防模型出错。**这不是不信任模型，是承认它按概率说话——概率偶尔会给你一个你没写过的形状。

## 10. 改一改：亲手制造三次失败

要摸清兜底和护栏装在哪，最快的办法是亲手把失败造出来。**每跑一次不到一分钱**，改完记得改回去。

1. **把护栏拧到 1 步**，再跑同样的四个问题： `python exercises/agent/0002-build-an-agent.py --max-steps 1` 本机实测第一问的输出变成： `用户问：北京今天多少度？
──────────────────────────────────────────────────────────
 [1] 调工具：get_weather({'city': '北京'}) -> {"city": "北京", "temp_c": 26, "cond": "晴"}
 >> hit_max_steps，共走 1 步，耗时 1.1 秒` 工具调到了、结果也拿到了，就是没机会说人话——这就是护栏强制收工的现场。生产里这个数字设多大，是钱和安全的取舍。
2. **删掉一个城市再问**：把 `WEATHER_DB` 里的 `"北京"` 整个删掉，再问「北京今天多少度」。工具会返回 `{"error": "查不到「北京」的天气"}`，观察它接下来怎么处理这条错误——如实说查不到，还是换个城市硬答？
3. **加一个「只写了一半」的工具**：在 `TOOL_LIST` 里加一条 `get_air_quality`（名字、说明、参数都写），但**不**往 `TOOLS` 里加实现。再问「北京空气质量怎么样」。模型很可能真去调它，然后触发 `没有这个工具` 的兜底——这就是「清单和实现不同步」的现场。

## 11. 成本、延迟与护栏：这一课的账

这次跑四个问题，账单是 **2969 输入 token ＋ 279 输出 token**。按 DeepSeek 官方价目（2026-10-18 查），`deepseek-flash` 的价格是：

```
                        空闲时段        高峰时段
输入（缓存未命中）      ¥1 / 百万       ¥2 / 百万
输入（缓存命中）        ¥0.02 / 百万    ¥0.04 / 百万
输出                    ¥4 / 百万       ¥8 / 百万
```

按全价估：`2969 ÷ 1,000,000 × 1 ＋ 279 ÷ 1,000,000 × 4 ≈ 0.0041 元`。所以脚本打出来「约 0.00409 元」——**四个问题不到半分钱**。高峰时段（工作日的白天）翻倍；缓存命中还会更便宜。

**但便宜不等于无脑跑。**每一步都要把**之前的全部对话**再送一遍，所以这笔账输入占大头；问题越长、工具清单越大，输入 token 涨得越快。这也是为什么缓存在 agent 里特别值钱，机制见 [LLM 底层第 3 课 · KV Cache 与「缓存命中」](../../lessons/llm/0003-kv-cache-and-prompt-caching.html)。工程上至少配三道护栏：**最大步数**、**超时**、**预算上限**。

## 12. 检查一下你懂了没

**Q1　`--check` 报 401，第一步先查什么？**

- 模型名是不是写错，或根本不存在
- ✅ .env 里的 key 有没有引号或空格
- 网络是不是不通，必须先挂上代理
- 账户余额是不是不够，或者已经欠费

答对时：对。401 是认证失败，先盯 key 本身：多一个空格、多一对引号都会错。
答错时：401 是「你是谁」这一步没过——先查 key 的写法，余额是 402，网络是连不上。

**Q2　循环里把观察那一步整个漏掉——模型说的那句和工具结果都不放回对话，会发生什么？**

- 程序会直接报错，循环根本起不来
- 上下文会越用越小，最后溢出
- ✅ 模型看不到工具结果，下一步全靠猜
- 工具会被重复调用，直到步数耗尽

答对时：对。两边都不放回，历史里就没有悬着的 tool_calls，接口不报错——但模型什么都没看见。
答错时：报 400 的是另一种漏法：模型说的那句放回了历史、结果却没跟着回。整个漏掉反而不报错，模型只是看不到结果。

**Q3　模型一步返回了两条 `tool_calls`，代码应该怎么处理？**

- 只执行第一条，第二条直接丢掉不管
- 重新发一次请求，要求它一次只给一条
- 把两条合成一条，只回一个合并结果
- ✅ 两条都执行，各回一条带自己 id 的结果

答对时：对。模型要几个就执行几个，每个 tool_call_id 都要有对应的结果，否则 400。
答错时：少回任何一条，接口都会报 insufficient tool messages——这一课第一版就是这么报错的。

**Q4　跑完发现 `>> hit_max_steps`，下一步先做什么？**

- ✅ 看 trace：卡在哪一步、反复在调什么
- 换个更贵的模型，原样再跑一遍看结果
- 把 max_steps 调大十倍，再跑一次
- 把工具全部删掉，然后再从头跑一次

答对时：对。trace 是 agent 的体检报告：先看它卡在哪，再决定动护栏还是动提示词。
答错时：盲目调大步数只是让烧钱烧得更久——先看 trace。

**Q5　为什么 key 要放在 `.env`，而不是直接写进脚本？**

- 放在单独的文件里，读起来会更快一点
- ✅ 代码可以分享、提交，key 不会跟着泄露
- 写进脚本，接口就会不认这个 key
- .env 里的 key 不会被计费，能省钱

答对时：对。key 是密码也是钱：源码进 git、发给别人时，.env 留在本机。
答错时：读取速度和计费都跟放哪无关；区别只有一个——key 会不会跟着代码泄露。

**Q6　换一家模型供应商，接口的差异被关在哪一层，循环本身不用动？**

- run_agent：每一步重新问一次模型，天然兼容各家接口
- 工具清单：把参数格式写进清单，跟厂商对齐
- ✅ model_fn：把厂商各自的回复翻译成 text 或 tool_use 两种形状
- 系统提示：在提示里写明用的是哪家的接口

答对时：对。循环只认 text 和 tool_use 两种回话；厂商差异全关在 model_fn 那一层。
答错时：循环和工具都不用动——把新接口的回复翻译成两种形状的活，是 model_fn 在干。

## 一手资料（页脚框，一般不动）

- [DeepSeek — Tool Calls（官方文档）](https://api-docs.deepseek.com/zh-cn/guides/tool_calls)：`tools` 的定义、`tool_calls` 的返回、`tool_call_id` 怎么挂回去，以及非思考模式那个 `extra_body` 写法。
- [OpenAI Python SDK（PyPI）](https://pypi.org/project/openai/)：`pip install openai`、`OpenAI(base_url=...)`、错误类型与默认重试。
- [ReAct: Synergizing Reasoning and Acting in Language Models（Yao et al., ICLR 2023）](https://arxiv.org/abs/2210.03629)——本课这个「推理 → 行动 → 观察」循环的原始论文。

## 提问框

**我是你的老师，随时打断我。**比如「为什么要用 SDK，不直接用 requests？」「tool_call_id 这个编号是谁生成的？」「模型一步要两个工具，我能并行执行吗？」「max_steps 设多少才合适？」——直接问我。搞不懂就往下学，是最贵的学费。

## 页尾互链（一般不动）

- **前置**：[Agent 篇 · 第 1 课 · Agent 是什么：循环、工具、记忆](../../lessons/agent/0001-what-is-an-agent.html)（循环、工具、记忆都是那课讲过的，这里写成能跑的代码）
- **顺着往下**：[Agent 篇 · 第 3 课 · MCP：给工具定一个统一插口](../../lessons/agent/0003-mcp.html)（工具的新形状）→ [第 4 课 · Skill：把做法打包成文件](../../lessons/agent/0004-skill.html)（做法的新形状）
- **LLM 底层**：[第 3 课 · KV Cache 与「缓存命中」](../../lessons/llm/0003-kv-cache-and-prompt-caching.html)（工具清单每一轮都原样重发，正好吃上缓存）
- 术语表：[Agent 循环](../../reference/glossary.html#loop) · [工具](../../reference/glossary.html#tool) · [观察](../../reference/glossary.html#observation) · [护栏](../../reference/glossary.html#guardrail) · [轨迹](../../reference/glossary.html#trace)
