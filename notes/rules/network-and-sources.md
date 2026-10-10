# 联网取材：代理与可达性（NOTES 1.1 的操作细节）

> 本文件只在**要上网抓一手资料、而某个站取不到**时读。规矩本身见 [NOTES.md](../../NOTES.md) 第 1.1 节；踩坑全过见存档 [5.04](../history/5.04-verification-and-editing.md)、[5.13.4](../history/5.13-0003-deep-rework-track-boundary.md)。

## 哪些站直连不了

- **默认直连取不到**：`huggingface.co` · `raw.githubusercontent.com` · `www.reddit.com` · `wikipedia.org`（DNS 直接回 `0.0.0.0`，多半是公司策略）。
- **能直连**：`arxiv.org` · `aclanthology.org` · `www.anthropic.com` · `github.com` · `docs.vllm.ai` · substack · `martinfowler.com` · `redis.io` · `www.weka.io` · `web.stanford.edu`。

## 活路（已验证）

- **shell 显式带代理**：

  ```
  Invoke-WebRequest -Uri <url> -Proxy 'http://127.0.0.1:7890' -UseBasicParsing
  ```

- `platform.claude.com` 直连通、但部分页面回 "App unavailable in region" —— **那是地区限制，不是网络**；带上面的代理能拿到完整正文（2026-10-08 验证）。所以"抓不到"要先分清是真抓不到还是被地区挡了。
- **别猜网络**：先 `Test-NetConnection` ＋ 带/不带代理各试一次，再下结论。**实在取不到就空着——绝不凭记忆补。**

## 持久化代理（2026-09 踩过、现已设好）

- `opencode service set env HTTP_PROXY/HTTPS_PROXY/NO_PROXY`，`opencode service get env` 能查到这三个变量。
- ⚠️ **`NO_PROXY` 必须一起设**，否则 CLI 连不上本地服务。
- ⚠️ 改服务环境变量**会重启服务**；shell 里 export 的变量只有服务从那个 shell 启动时才生效 —— 这就是当初"明明设了却取不到"的根因。
- 官方文档：<https://opencode.ai/v2/docs/network>。

## 资料取回来之后

- 新用到的来源**当场补进 `RESOURCES.md`**，并注明"用来干什么"。
- **一手资料要注明是几手**：转引的数字标"未读原始报告"；分不清就明说分不清。
- **一手资料会变旧**：厂商矩阵、价目表、字段名引用前**当场再抓一次**（三例见存档 5.13.4 / 5.15.1 / 5.18.5）。
