<#
  progress.ps1 —— 课程进度三处落点的唯一执行入口

  背景：标 completed 要改三个文件（见 NOTES 1.7），漏一处就会自相矛盾。
        2026-10-03 主页那个「N 门已定稿」就是这么被漏掉的，而且错了三个提交
        都没人发现 —— 因为没有任何东西会检查它。本脚本的 audit 模式就是补这个洞。

  用法：
    pwsh tools/progress.ps1                                        # 只审计，不改文件（默认）
    pwsh tools/progress.ps1 -Action audit
    pwsh tools/progress.ps1 -Action mark   -Lesson llm/0003-kv-cache-and-prompt-caching.html
    pwsh tools/progress.ps1 -Action unmark -Lesson llm/0003-kv-cache-and-prompt-caching.html

  退出码：0 全通过；1 有 FAIL（可直接当 CI 用）。

  约定：completed 只能由学习者明确说才标（NOTES 1.7）。本脚本只执行，不判断。
        进阶版的 README 条目不自动生成 —— 卡上标题与 README 里人写的别名不一致
        （卡上「十个问题」vs README「十个追问」），自动猜会写出另一个名字。
#>
[CmdletBinding()]
param(
  [ValidateSet('audit','mark','unmark')] [string]$Action = 'audit',
  [string]$Lesson = ''
)

$ErrorActionPreference = 'Stop'
$OutputEncoding = [Console]::OutputEncoding = [Text.Encoding]::UTF8
$root = Split-Path $PSScriptRoot -Parent
$utf8 = [Text.UTF8Encoding]::new($false)
$script:fail = 0
function Ok($m){ Write-Output "  [ok]   $m" }
function No($m){ Write-Output "  [FAIL] $m"; $script:fail++ }
function Note($m){ Write-Output "  [--]   $m" }
function ReadText($rel){ [IO.File]::ReadAllText((Join-Path $root $rel), [Text.Encoding]::UTF8) }
function WriteText($rel,$t){ [IO.File]::WriteAllText((Join-Path $root $rel), $t, $script:utf8) }

$TRACKS = @{ llm='LLM 底层'; agent='Agent 原理篇'; practice='Agent 技巧篇'; rag='RAG' }
$SITE = 'https://telecomshy.github.io/telecomshy-ai-lessons/'
$ANCHOR = '目前标为 `completed` 的是：'
# 只认 /lessons/ 前面不是连字符的（域名 telecomshy-ai-lessons/ 里那个不算）
$LESSONURL = '(?<![-\w])lessons/([a-z]+/[^\s)]+\.html)'
# 清单块 = 锚点句 + 空行 + 连续的 "- " 行
$RDPAT = '(?m)^' + [regex]::Escape($ANCHOR) + '\r?\n\r?\n(?<list>(?:[ \t]*-[^\r\n]*(?:\r\n|\n|\r))*)'

# ---------- 采集（每次都重读，改完后复用） ----------
function Load {
  $script:idx    = ReadText 'lessons/index.html'
  $script:rootI  = ReadText 'index.html'
  $script:readme = ReadText 'README.md'

  $script:cards = @()
  foreach ($m in [regex]::Matches($script:idx,
      '(?s)<div class="pillar( completed)?">\s*<h3><a href="([^"]+)">([^<]*)</a>(.*?)</h3>')) {
    $tail = $m.Groups[4].Value
    $badge = ($tail -match '<span class="badge">completed</span>')
    $script:cards += [pscustomobject]@{
      href      = $m.Groups[2].Value
      title     = $m.Groups[3].Value
      completed = $badge
      # 定稿卡的 h3 必须以 </a><span class="badge">completed</span></h3> 收尾；
      # 徽章若落进 <a> 内部、或 div 上多出引号，这里会报出来
      shapeOk   = if ($badge) {
                    ($tail -match '^\s*<span class="badge">completed</span>\s*$') -and
                    ($m.Value -notmatch '<a [^>]*>[^<]*<span class="badge">')
                  } else { $tail -notmatch '<span class="badge">' }
    }
  }
  $script:doneCards = @($script:cards | Where-Object { $_.completed })
  $script:doneHrefs = @($script:doneCards | ForEach-Object { $_.href })

  # README 清单块：锚点句 → 空行 → 连续的 "- " 行（正则定位，不靠换行符假设）
  # ⚠️ 本仓库换行符混用：README.md / lessons/index.html 是 CRLF，根 index.html 是 LF
  $script:rdHrefs = @()
  $script:rdMatch = [regex]::Match($script:readme, $script:RDPAT)
  if ($script:rdMatch.Success) {
    foreach ($m in [regex]::Matches($script:rdMatch.Groups['list'].Value, $LESSONURL)) {
      $script:rdHrefs += $m.Groups[1].Value
    }
  }

  $script:statDone = -1
  $sm = [regex]::Match($script:rootI, '<b>(\d+)</b><span>门已定稿')
  if ($sm.Success) { $script:statDone = [int]$sm.Groups[1].Value }
}

$lessonFiles = @(Get-ChildItem (Join-Path $root 'lessons') -Recurse -File -Filter *.html | Where-Object { $_.Name -ne 'index.html' })
$nBasic   = @($lessonFiles | Where-Object { $_.Name -notmatch '-deep\.html$' }).Count
$nDeep    = @($lessonFiles | Where-Object { $_.Name -match  '-deep\.html$' }).Count
$nPy      = @(Get-ChildItem (Join-Path $root 'exercises') -Recurse -File -Filter *.py).Count
$llmBasic = @($lessonFiles | Where-Object { $_.Name -notmatch '-deep' -and $_.Directory.Name -eq 'llm' }).Count
$llmDeep  = @($lessonFiles | Where-Object { $_.Name -match  '-deep' -and $_.Directory.Name -eq 'llm' }).Count

function Audit {
  Write-Output "== A. 三处落点互相一致 =="
  if ($script:statDone -eq $script:doneCards.Count) {
    Ok "主页「$($script:statDone) 门已定稿」 == 目录页徽章 $($script:doneCards.Count) 张"
  } else { No "主页写 $($script:statDone) 门已定稿，目录页有 $($script:doneCards.Count) 张徽章" }

  $miss  = @($script:doneHrefs  | Where-Object { $script:rdHrefs -notcontains $_ })
  $extra = @($script:rdHrefs   | Where-Object { $script:doneHrefs -notcontains $_ })
  if ($script:rdHrefs.Count -eq 0) { No "README 清单一条都没解析到（锚点句或格式变了？）" }
  if (-not $miss)  { Ok "README 没漏掉任何一张已标卡（$($script:doneHrefs.Count) 张）" } else { No "README 缺: $($miss -join ', ')" }
  if (-not $extra) { Ok "README 没多出未标的课（$($script:rdHrefs.Count) 条链接）" }   else { No "README 多出: $($extra -join ', ')" }

  Write-Output "== B. 卡片形状没走样 =="
  foreach ($c in $script:doneCards) {
    if ($c.shapeOk) { Ok "$($c.href)" } else { No "$($c.href) 标了 completed 但徽章形状不对" }
  }

  Write-Output "== C. 链接指向真实文件 =="
  foreach ($h in ($script:doneHrefs + $script:rdHrefs | Select-Object -Unique)) {
    if (Test-Path (Join-Path $root "lessons/$h")) { Ok "lessons/$h" } else { No "死链 lessons/$h" }
  }

  Write-Output "== D. 主页 stats vs 实测 =="
  function ChkNum($name,$pat,$expect){
    $m = [regex]::Match($script:rootI, $pat)
    if (-not $m.Success) { No "主页找不到「$name」"; return }
    $got = [int]$m.Groups[1].Value
    if ($got -eq $expect) { Ok "$name = $got" } else { No "$name 主页写 $got，实测 $expect" }
  }
  ChkNum 'lede 基础课' '(\d+) 门基础课'                $nBasic
  ChkNum 'lede 进阶课' '(\d+) 门进阶课'                $nDeep
  ChkNum 'lede 脚本'   '，(\d+) 个能跑的 Python 脚本'    $nPy
  ChkNum 'stat 门课'   '<b>(\d+)</b><span>门课'        ($nBasic+$nDeep)
  ChkNum 'stat 脚本'   '<b>(\d+)</b><span>个脚本'       $nPy
  ChkNum 'LLM 轨道'    "$llmBasic 门基础 · (\d+) 门进阶" $llmDeep
}

Load
if ($Action -eq 'audit') {
  Audit
} else {
  if (-not $Lesson) { No "-Action $Action 需要 -Lesson <相对 lessons/ 的路径>"; exit 1 }
  $card = $script:cards | Where-Object { $_.href -eq $Lesson }
  if (-not $card) { No "目录页里找不到卡片 href=$Lesson（应形如 llm/0003-xxx.html）"; exit 1 }

  Write-Output "== 动手前先审计（状态已经不一致时不许再叠加改动）=="
  Audit
  if ($script:fail -gt 0) { No "审计没过，先修上面问题再标 completed（别在坏状态上叠改）"; exit 1 }

  if ($Action -eq 'mark'   -and $card.completed) { Ok "$Lesson 已是 completed，无需改动"; exit 0 }
  if ($Action -eq 'unmark' -and -not $card.completed) { Ok "$Lesson 本来就没标，无需改动"; exit 0 }

  $esc = [regex]::Escape($Lesson)
  Write-Output ""
  Write-Output "== 改 1/3  lessons/index.html =="
  # 分组：$1='<div class="pillar'  $2=可选的 ' completed'  $3='">' 换行 <h3><a href="目标">  $4=标题  $5='</a>'
  # 徽章必须落在 </a> 之后（对照已定稿的卡：</a><span class="badge">completed</span></h3>）
  if ($Action -eq 'mark') {
    $pat = '(<div class="pillar)( completed)?(">\s*<h3><a href="' + $esc + '">)([^<]*)(</a>)'
    $rep = '$1 completed$3$4$5<span class="badge">completed</span>'
  } else {
    $pat = '(<div class="pillar) completed(">\s*<h3><a href="' + $esc + '">)([^<]*)(</a>)\s*<span class="badge">completed</span>'
    $rep = '$1$2$3$4'
  }
  $new = [regex]::Replace($script:idx, $pat, $rep)
  if ($new -eq $script:idx) { No "目录页替换没生效（卡片形状可能变了，先看 lessons/index.html）"; exit 1 }
  WriteText 'lessons/index.html' $new; Ok "已写入"

  Write-Output "== 改 2/3  index.html（已定稿计数）=="
  $delta = if ($Action -eq 'mark') { 1 } else { -1 }
  $newR = [regex]::Replace($script:rootI, '<b>\d+</b><span>门已定稿',
          ('<b>' + ($script:doneCards.Count + $delta) + '</b><span>门已定稿'))
  if ($newR -eq $script:rootI) { No "主页计数替换没生效"; exit 1 }
  WriteText 'index.html' $newR; Ok "已写入：$($script:doneCards.Count + $delta) 门已定稿"

  Write-Output "== 改 3/3  README.md =="
  if ($Lesson -match '-deep\.html$') {
    No "进阶版的 README 条目不自动生成。"
    No "原因：卡上标题是「$($card.title)」，README 那行用的是人起的别名（0001 那行写「进阶版「十个追问」」，卡上却是「十个问题」），自动生成会写出另一个名字。"
    Note "徽章与主页计数已改好。README 请手动在对应那行末尾追加："
    Note ("＋ [进阶版「<别名>」](" + $SITE + "lessons/" + $Lesson + ")")
  } else {
    $track = $Lesson.Split('/')[0]
    $num   = [int][regex]::Match($Lesson, '(\d{4})').Groups[1].Value   # 去掉前导零：0003 -> 3
    $name  = ($card.title -split '·', 2)[1].Trim()
    if (-not $TRACKS.ContainsKey($track)) { No "不认识的轨道目录「$track」"; exit 1 }
    $line = "- **$($TRACKS[$track]) · 第 $num 课**（[$name]($SITE" + "lessons/$Lesson)）"
    if (-not $script:rdMatch.Success) { No "README 里定位不到清单块（锚点句或格式变了？）"; exit 1 }
    $lst  = $script:rdMatch.Groups['list'].Value
    $at   = $script:rdMatch.Groups['list'].Index
    $tail = $script:readme.Substring($at + $lst.Length)
    $head = $script:readme.Substring(0, $at)
    $nl   = if ($lst.EndsWith("`r`n")) { "`r`n" } elseif ($lst.EndsWith("`n")) { "`n" } else { "`r`n" }
    # 每行连同自己的换行符一起切出来。
    # ⚠️ 不要用 Split($lst,'(?<=\r\n|\n|\r)') —— 那个 lookbehind 是「或」关系，
    #    会在 \r 后和 \n 后各切一次，把每行劈成「内容+\r」和「单独一个 \n」两半。
    #    后果：删某行时连 \r 一起删掉，剩下孤立的 \n（行数对、字节不对）。
    #    用捕获组切再手工配对，行为唯一。
    $parts = [regex]::Split($lst, '(\r\n|\n|\r)')
    $rows  = @()
    for ($i = 0; $i -lt ($parts.Count - 1); $i += 2) {
      if ($parts[$i] -ne '') { $rows += ($parts[$i] + $parts[$i+1]) }
    }
    $url  = "$SITE" + "lessons/$Lesson"
    $changed = 0

    if ($Action -eq 'mark') {
      $already = @($rows | Where-Object { $_.Contains("lessons/$Lesson") }).Count
      if ($already -gt 0) { Note "README 已有这条（$already 处），跳过插入" }
      else { $rows += ($line + $nl); $changed = 1 }   # 必须自带换行，否则会粘在上一行尾巴上
    } else {
      # 删掉引用本课的行。只有这一个链接 -> 整行删；同一行还有别的链接 -> 只摘掉这一条
      $keep = @()
      foreach ($r in $rows) {
        if (-not $r.Contains("lessons/$Lesson")) { $keep += $r; continue }
        $links = ([regex]::Matches($r, [regex]::Escape($SITE) + 'lessons/[^\s)]+\.html')).Count
        if ($links -le 1) { $changed++; continue }
        $r2 = [regex]::Replace($r, '(＋\s*)?\[[^\]]*\]\(' + [regex]::Escape($url) + '\)', '')
        $r2 = $r2 -replace '（\s*）\s*$', ''          # 摘完别留空括号
        if ($r2 -notmatch [regex]::Escape($SITE)) { $changed++; continue }   # 整行没链接了 -> 删
        $keep += $r2; $changed++
      }
      $rows = $keep
    }

    if ($changed -eq 0) { No "README 清单没有可改动的行（$($rows.Count) 行清单，格式可能变了，先看 README.md）"; exit 1 }
    $newM = $head + ($rows -join '') + $tail
    WriteText 'README.md' $newM
    if ($Action -eq 'mark') { Ok "已写入：$line" } else { Ok "已摘掉本课那条" }
  }

  Write-Output ""
  Write-Output "== 写完读回来核验（NOTES 1.7）=="
  foreach ($f in 'lessons/index.html','index.html','README.md') {
    $b = [IO.File]::ReadAllBytes((Join-Path $root $f))
    $bom = ($b.Length -ge 3 -and $b[0] -eq 0xEF -and $b[1] -eq 0xBB -and $b[2] -eq 0xBF)
    $txt = [IO.File]::ReadAllText((Join-Path $root $f), [Text.Encoding]::UTF8)
    if ($bom) { No "$f 被写出 BOM" } else { Ok "$f 无 BOM" }
    if ($txt -match '�') { No "$f 出现替换字符 U+FFFD（中文写坏了）" } else { Ok "$f 无乱码字符" }
  }
  Load
  Write-Output ""
  Write-Output "== 改后重新审计 =="
  Audit
}

Write-Output ""
if ($script:fail -gt 0) { Write-Output "==== 失败 $script:fail 项 ===="; exit 1 } else { Write-Output "==== 全部通过 ====" }