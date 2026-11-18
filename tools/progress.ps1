<#
  progress.ps1 —— 课程库只读审计

  用途：课程库没有数据库，一致性只能靠脚本在「入口」处兜住。
        本脚本检查：卡片链接、主页统计、RAG 三链、deep 别名与问数、
        标准/历史文档的存在与体量、md 相对链接。

  用法：
    pwsh tools/progress.ps1            # 审计，不改任何文件

  退出码：0 全通过；1 有 FAIL（可直接当 CI 用）。

  约定：课程不再维护 completed 标记，也不再维护「已定稿」计数。
        进阶版别名以 data-alias 为唯一落点，卡片 / <title> / 审计核一致性。
#>
[CmdletBinding()]
param(
  [ValidateSet('audit')] [string]$Action = 'audit'
)

$ErrorActionPreference = 'Stop'
$OutputEncoding = [Console]::OutputEncoding = [Text.Encoding]::UTF8
$root = Split-Path $PSScriptRoot -Parent
$script:fail = 0
function Ok($m){ Write-Output "  [ok]   $m" }
function No($m){ Write-Output "  [FAIL] $m"; $script:fail++ }
function Note($m){ Write-Output "  [--]   $m" }
function ReadText($rel){ [IO.File]::ReadAllText((Join-Path $root $rel), [Text.Encoding]::UTF8) }

# 进阶版的别名 = lesson-meta 上的 data-alias（唯一落点）。
function Get-Alias($rel){
  $p = Join-Path $root "lessons/$rel"
  if (-not (Test-Path $p)) { return $null }
  $t = [IO.File]::ReadAllText($p, [Text.Encoding]::UTF8)
  $m = [regex]::Match($t, '<div class="lesson-meta"[^>]*\bdata-alias="([^"]*)"')
  if ($m.Success) { return $m.Groups[1].Value }
  return $null
}

# 中文数字 -> 整数，认到九十九。认不出返回 $null（让调用方去提示人肉确认，别硬猜）。
$CNNUM = @{ '零'=0; '〇'=0; '一'=1; '二'=2; '两'=2; '三'=3; '四'=4; '五'=5; '六'=6; '七'=7; '八'=8; '九'=9 }
function ConvertFrom-CnNum([string]$s){
  if ($s -match '^十([一二三四五六七八九])$') { return 10 + $script:CNNUM[$Matches[1]] }
  if ($s -eq '十') { return 10 }
  if ($s -match '^([二三四五六七八九])十([一二三四五六七八九])?$') {
    $n = $script:CNNUM[$Matches[1]] * 10
    if ($Matches[2]) { $n += $script:CNNUM[$Matches[2]] }
    return $n
  }
  if ($s -match '^[一二两三四五六七八九]$') { return $script:CNNUM[$s] }
  return $null
}

# ---------- 采集（每次都重读） ----------
function Load {
  $script:idx   = ReadText 'lessons/index.html'
  $script:rootI = ReadText 'index.html'

  # 只采集「已经写出来的课」：普通 pillar 卡；planned 卡链接可空，不查。
  $script:cards = @()
  foreach ($m in [regex]::Matches($script:idx,
      '(?s)<div class="pillar">\s*<h3><a href="([^"]+)">([^<]*)</a>')) {
    $script:cards += [pscustomobject]@{
      href  = $m.Groups[1].Value
      title = $m.Groups[2].Value
    }
  }
  $script:ragCards = @($script:cards | Where-Object { $_.href -match '^rag/' })
}

$lessonFiles = @(Get-ChildItem (Join-Path $root 'lessons') -Recurse -File -Filter *.html |
                 Where-Object { $_.Name -ne 'index.html' -and $_.Name -notmatch '^appendix-' })
$nBasic   = @($lessonFiles | Where-Object { $_.Name -notmatch '-deep\.html$' }).Count
$nDeep    = @($lessonFiles | Where-Object { $_.Name -match  '-deep\.html$' }).Count
$nPy      = @(Get-ChildItem (Join-Path $root 'exercises') -Recurse -File -Filter *.py |
              Where-Object { $_.Name -notmatch '^appendix-' }).Count
$llmBasic = @($lessonFiles | Where-Object { $_.Name -notmatch '-deep' -and $_.Directory.Name -eq 'llm' }).Count
$llmDeep  = @($lessonFiles | Where-Object { $_.Name -match  '-deep' -and $_.Directory.Name -eq 'llm' }).Count
$ragFiles = @($lessonFiles | Where-Object { $_.Directory.Name -eq 'rag' })
$ragPy    = @(Get-ChildItem (Join-Path $root 'exercises/rag') -File -Filter *.py)

function Audit {
  Write-Output "== A. 课程卡片指向真实文件 =="
  if ($script:cards.Count -eq 0) {
    No "目录页一张课程卡都没解析到（卡片形状变了？）"
  } else {
    foreach ($c in $script:cards) {
      $full = [IO.Path]::GetFullPath((Join-Path (Join-Path $root 'lessons') $c.href))
      if ($full.StartsWith($root, [StringComparison]::OrdinalIgnoreCase) -and (Test-Path -LiteralPath $full)) {
        Ok "$($c.href)"
      } else {
        No "死链 $($c.href)（目录页卡片指向不存在的文件）"
      }
    }
  }

  Write-Output "== B. 主页 stats vs 实测 =="
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

  Write-Output "== C. RAG 轨：卡片 ↔ 课文件 ↔ 脚本 =="
  $ragFileHrefs = @($ragFiles | ForEach-Object { "rag/" + $_.Name })
  $ragCardHrefs = @($script:ragCards | ForEach-Object { $_.href })
  if ($script:ragCards.Count -eq $ragFiles.Count) {
    Ok "RAG 卡片 $($script:ragCards.Count) 张 == 课文件 $($ragFiles.Count) 个"
  } else {
    No "RAG 目录有 $($ragFiles.Count) 个课文件，目录页只有 $($script:ragCards.Count) 张卡"
  }
  $ragNoCard = @($ragFileHrefs | Where-Object { $ragCardHrefs -notcontains $_ })
  if ($ragNoCard.Count -eq 0) { Ok "RAG 每个课文件都有目录卡" } else { No "RAG 课文件没有卡: $($ragNoCard -join ', ')" }
  $ragDead = @($ragCardHrefs | Where-Object { -not (Test-Path (Join-Path $root ("lessons/" + $_))) })
  if ($ragDead.Count -eq 0) { Ok "RAG 每张卡都指向真实文件" } else { No "RAG 死链: $($ragDead -join ', ')" }
  $ragScriptOrphans = @($ragPy | Where-Object { $script:idx -notmatch [regex]::Escape($_.Name) })
  if ($ragScriptOrphans.Count -eq 0) {
    Ok "RAG $($ragPy.Count) 个脚本都至少被目录页引用一次"
  } else {
    No "RAG 脚本没进目录页: $(($ragScriptOrphans | ForEach-Object { $_.Name }) -join ', ')"
  }

  Write-Output "== D. 进阶版：别名三处一致 ＋ Q 编号连续 ＋ 问数对得上 =="
  $deepCards = @($script:cards | Where-Object { $_.href -match '-deep\.html$' })
  if ($deepCards.Count -eq 0) { Note "目录页里还没有进阶版卡片" }
  foreach ($c in $deepCards) {
    $bad = 0
    $txt = ReadText ("lessons/" + $c.href)
    $al  = Get-Alias $c.href
    if (-not $al) { No "$($c.href) 的 lesson-meta 上没有 data-alias"; $bad++ }

    # (1) 三处一致：data-alias / 目录页卡片 / <title> 尾段
    if ($al) {
      $cardAlias = ($c.title -replace '^\s*\d+\s*进阶\s*[·・]\s*', '').Trim()
      if ($cardAlias -ne $al) { No "$($c.href) 卡片写「$cardAlias」，data-alias 是「$al」"; $bad++ }
      $tt = [regex]::Match($txt, '(?s)<title>(.*?)</title>')
      $tail = if ($tt.Success) { ($tt.Groups[1].Value -split '·')[-1].Trim() } else { '' }
      if ($tail -ne $al) { No "$($c.href) <title> 尾段是「$tail」，data-alias 是「$al」"; $bad++ }
    }

    # (2) Q 编号必须连续 1..N
    $nums = @([regex]::Matches($txt, '<h2 id="q[^"]*"[^>]*>\s*Q(\d+)') | ForEach-Object { [int]$_.Groups[1].Value })
    if ($nums.Count -gt 0 -and (Compare-Object (1..$nums.Count) $nums)) {
      No "$($c.href) 的 Q 编号断了：$($nums -join ',')（应为 1..$($nums.Count)）"; $bad++
    }

    # (3) 别名以中文数字开头 = 带编号的问数
    if ($al) {
      $mn = [regex]::Match($al, '^([零〇一二两三四五六七八九十]+)')
      if ($mn.Success) {
        $claim = ConvertFrom-CnNum $mn.Groups[1].Value
        if ($null -eq $claim) {
          Note "$($c.href) 别名开头「$($mn.Groups[1].Value)」认不出是几，人肉确认一下"
        } elseif ($claim -ne $nums.Count) {
          No "$($c.href) 别名说「$($mn.Groups[1].Value)」＝ $claim 个问，带编号的 Q 只有 $($nums.Count) 个"; $bad++
        }
      }
    }
    if ($bad -eq 0) { Ok "$($c.href) = $al（带编号 Q $($nums.Count) 个）" }
  }

  # deep 是 LLM 轨专属
  $nonLlmDeep = @($lessonFiles | Where-Object { $_.Name -match '-deep\.html$' -and $_.Directory.Name -ne 'llm' })
  if ($nonLlmDeep.Count -eq 0) {
    Ok "deep 页只在 LLM 轨（RAG/Agent 无 deep）"
  } else {
    No "非 LLM 轨出现 deep 页: $(($nonLlmDeep | ForEach-Object { $_.FullName.Substring($root.Length + 1) }) -join ', ')"
  }
  $nonLlmDeepCards = @($script:cards | Where-Object { $_.href -match '-deep\.html$' -and $_.href -notmatch '^llm/' })
  if ($nonLlmDeepCards.Count -eq 0) {
    Ok "目录页没有非 LLM 轨的 deep 卡"
  } else {
    No "目录页出现非 LLM 轨 deep 卡: $(($nonLlmDeepCards | ForEach-Object { $_.href }) -join ', ')"
  }

  Write-Output "== E. 文档卫生：标准/流程/历史各就各位 =="
  # 1) completed 退役后不许回潮
  if ($script:idx -match 'completed|class="badge"') {
    No "lessons/index.html 仍有 completed 徽章或 badge 标记（2026-11-17 已退役）"
  } else {
    Ok "目录页没有完成徽章"
  }
  if ($script:rootI -match '门已定稿') {
    No "根 index.html 仍有「门已定稿」计数（2026-11-17 已退役）"
  } else {
    Ok "主页没有「门已定稿」计数"
  }
  if (Test-Path (Join-Path $root 'internal/rules')) {
    No "internal/rules/ 仍在（操作手册已迁 internal/playbooks/）"
  } else {
    Ok "旧 internal/rules/ 已清"
  }

  # 2) 核心文档存在与体量
  $docs = @(
    @{ rel='NOTES.md'; max=120; name='NOTES.md（学习者偏好）' },
    @{ rel='internal/standards/PROCESS.md'; max=160; name='PROCESS.md（开发流程）' },
    @{ rel='internal/standards/COURSE-STANDARD.md'; max=200; name='COURSE-STANDARD.md（课程标准）' },
    @{ rel='internal/standards/ARTICLE-STYLE.md'; max=200; name='ARTICLE-STYLE.md（文章体）' },
    @{ rel='internal/standards/REVISION.md'; max=140; name='REVISION.md（改课标准）' },
    @{ rel='internal/history/INDEX.md'; max=200; name='history/INDEX.md（历史索引）' }
  )
  foreach ($d in $docs) {
    $p = Join-Path $root $d.rel
    if (-not (Test-Path $p)) {
      No "$($d.name) 不存在"
    } else {
      $lines = @((ReadText $d.rel) -split '\r?\n')
      if ($lines.Count -gt $d.max) {
        No "$($d.name) 已 $($lines.Count) 行（阈值 $($d.max)）：先把历史/细节挪出去，再加新规矩"
      } else {
        Ok "$($d.name) $($lines.Count) 行（阈值 $($d.max)）"
      }
    }
  }
  foreach ($t in 'agent','llm','rag') {
    $tp = Join-Path $root "internal/standards/tracks/$t.md"
    if (-not (Test-Path $tp)) {
      No "internal/standards/tracks/$t.md 不存在（轨道标准）"
    } else {
      $tl = @((ReadText "internal/standards/tracks/$t.md") -split '\r?\n')
      if ($tl.Count -gt 120) {
        No "internal/standards/tracks/$t.md 已 $($tl.Count) 行（阈值 120）"
      } else {
        Ok "internal/standards/tracks/$t.md $($tl.Count) 行（阈值 120）"
      }
    }
  }
  foreach ($pb in 'learner-audit.md','modify-lessons.md','network-and-sources.md') {
    if (Test-Path (Join-Path $root "internal/playbooks/$pb")) { Ok "playbooks/$pb" } else { No "internal/playbooks/$pb 不存在" }
  }

  # 3) 历史索引 <-> internal/history/ 双向一致（INDEX.md 自己不算一篇）
  $histDir = Join-Path $root 'internal/history'
  if (-not (Test-Path $histDir)) {
    No "internal/history/ 不存在（历史存档目录）"
  } else {
    $files = @(Get-ChildItem $histDir -File -Filter '*.md' |
               Where-Object { $_.Name -ne 'INDEX.md' } |
               Select-Object -ExpandProperty Name | Sort-Object)
    $indexTxt = ReadText 'internal/history/INDEX.md'
    $linked = @([regex]::Matches($indexTxt, '\]\((5\.\d{2}-[^)]+\.md)\)') |
                ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique)
    foreach ($f in $files)  { if ($linked -notcontains $f) { No "internal/history/$f 存在，但 INDEX.md 里没有它的链接" } }
    foreach ($l in $linked) { if ($files -notcontains $l) { No "INDEX.md 链到 internal/history/$l，文件不存在" } }
    if ($files.Count -gt 0 -and $linked.Count -eq $files.Count) { Ok "INDEX 与 internal/history/ 双向一致（$($files.Count) 篇）" }
  }

  Write-Output "== F. md 链接断链扫描 =="
  $draftsDir = Join-Path $root 'internal/drafts'
  $mdFiles = @(Get-ChildItem (Join-Path $root 'internal') -Recurse -File -Filter *.md |
               Where-Object { -not $_.FullName.StartsWith($draftsDir, [StringComparison]::OrdinalIgnoreCase) }) +
              @(Get-ChildItem $root -File -Filter *.md)
  if (Test-Path (Join-Path $root 'docs')) {
    $mdFiles += @(Get-ChildItem (Join-Path $root 'docs') -File -Filter *.md)
  }
  $gChecked = 0; $gBad = 0
  foreach ($md in $mdFiles) {
    $rel = $md.FullName.Substring($root.Length + 1).Replace('\', '/')
    $txt = ReadText $rel
    $txt = [regex]::Replace($txt, '(?s)```.*?```', '```CODE```')
    $txt = [regex]::Replace($txt, '`[^`]*`', '')
    $baseDir = $md.DirectoryName
    foreach ($m in [regex]::Matches($txt, '!?\[[^\]\n]*\]\(([^)\n]+)\)')) {
      $url = $m.Groups[1].Value.Trim()
      if ($url -match '^(https?://|mailto:|tel:|#)') { continue }
      $path = ($url -split '#')[0]
      if ($path -eq '') { continue }
      $path = [Uri]::UnescapeDataString($path)
      $full = [IO.Path]::GetFullPath((Join-Path $baseDir $path))
      if (-not $full.StartsWith($root, [StringComparison]::OrdinalIgnoreCase)) {
        No "死链: $($md.Name) -> $path（$rel）逃逸出仓库根（解析到 $full）"; $gBad++; continue
      }
      $gChecked++
      if (-not (Test-Path -LiteralPath $full)) { No "死链: $($md.Name) -> $path（$rel）"; $gBad++ }
    }
  }
  if ($gChecked -eq 0) {
    No "F 段一条 md 相对链接都没扫到（文件列表或正则变了？）"
  } elseif ($gBad -eq 0) {
    Ok "F 段 $gChecked 条 md 相对链接全部指向真实文件"
  }
}

Load
Audit

Write-Output ""
if ($script:fail -gt 0) { Write-Output "==== 失败 $script:fail 项 ===="; exit 1 } else { Write-Output "==== 全部通过 ====" }
