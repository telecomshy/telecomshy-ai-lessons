# -*- coding: utf-8 -*-
"""
html2md.py —— 把 lessons/ 下的课件 HTML 转成 markdown 文字稿（lessons-md/，结构与 lessons/ 一致）。

用途：学习者直接在 md 上改，主代理再按 internal/drafts/agent-0003-f5-markdown.md 的既定约定
逐段映射回 HTML 并跑核验。标记约定（✅ / 答对时 / 答错时 / 【图】 / 【选读框】……）
见 lessons-md/README.md。

用法：
    python tools/html2md.py            # 全量转换 lessons/*.html -> lessons-md/
    python tools/html2md.py --check    # 转换后做一致性校验（题数/标记数/链接可达）

只读 lessons/，不改任何课件；输出只进 lessons-md/。
"""
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / 'lessons'
OUT = ROOT / 'lessons-md'

VOID = {'img', 'br', 'meta', 'link', 'col', 'hr', 'input', 'source', 'wbr'}

# ---------------------------------------------------------------- DOM


class El:
    def __init__(self, tag, attrs=None):
        self.tag = tag
        self.attrs = dict(attrs or {})
        self.children = []  # El | str

    @property
    def cls(self):
        return self.attrs.get('class', '')

    def iter(self):
        for c in self.children:
            if isinstance(c, El):
                yield c
                yield from c.iter()

    def raw_text(self):
        out = []
        for c in self.children:
            if isinstance(c, str):
                out.append(c)
            else:
                out.append(c.raw_text())
        return ''.join(out)


class Dom(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = El('#root')
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        el = El(tag, attrs)
        self.stack[-1].children.append(el)
        if tag not in VOID:
            self.stack.append(el)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(El(tag, attrs))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        if data:
            self.stack[-1].children.append(data)


def parse(html_text: str) -> El:
    dom = Dom()
    dom.feed(html_text)
    return dom.root


def find(el: El, tag: str, cls: str = None):
    for d in el.iter():
        if d.tag == tag and (cls is None or cls in d.cls.split()):
            return d
    return None


# ---------------------------------------------------------------- inline 渲染


class Ctx:
    """转换上下文：源 html 路径 + 输出 md 路径（用于重写相对链接）"""

    def __init__(self, src: Path, md: Path):
        self.src = src
        self.md = md
        self.goal_seen = False  # 每课第一个 goal 框＝开场，其余 goal 样式框走【goal 框】标记


def rewrite_link(href: str, ctx: Ctx) -> str:
    if href.startswith(('http://', 'https://', 'mailto:')):
        return href
    base, _, frag = href.partition('#')
    frag = f'#{frag}' if (frag or '#' in href) else ''
    if not base:
        return href  # 纯页内锚点
    target = (ctx.src.parent / base).resolve()
    # 课程目录页 -> lessons-md/index.md
    if target.name == 'index.html' and target.parent == LESSONS:
        rel = os.path.relpath((OUT / 'index.md').resolve(), ctx.md.parent.resolve())
        return rel.replace('\\', '/') + frag
    rel = os.path.relpath(target, ctx.md.parent.resolve()).replace('\\', '/')
    return rel + frag


def esc_cell(s: str) -> str:
    return s.replace('|', '\\|')


def inline(node, ctx: Ctx) -> str:
    """行内内容 -> markdown。block 级子节点（不应出现在行内）按纯文本兜底。"""
    if isinstance(node, str):
        s = re.sub(r'\s+', ' ', node)
        # 正文里真实写出的标签（如 <think>）要转义，否则 GFM 会当未知 HTML 吞掉
        return re.sub(r'<(?=[a-zA-Z/!])', r'\\<', s)
    if not isinstance(node, El):
        return ''
    tag = node.tag
    if tag in ('b', 'strong'):
        inner = inline_all(node.children, ctx).strip()
        return f'**{inner}**' if inner else ''
    if tag == 'code':
        inner = node.raw_text()
        if '`' in inner:
            return f'`` {inner} ``'
        return f'`{inner.strip()}`'
    if tag == 'a':
        href = node.attrs.get('href', '')
        text = inline_all(node.children, ctx).strip() or href
        if not href:
            return text
        return f'[{text}]({rewrite_link(href, ctx)})'
    if tag == 'br':
        return '<br>'
    if tag in ('sub', 'sup', 'small'):
        return f'<{tag}>{inline_all(node.children, ctx)}</{tag}>'
    if tag == 'span':
        cls = node.cls
        if cls == 'badge':  # 目录页 completed 徽章
            inner = inline_all(node.children, ctx).strip()
            return f'（{inner}）' if inner else ''
        return inline_all(node.children, ctx)
    if tag in VOID:
        return ''
    # 兜底：未知行内标签，递归其子节点
    return inline_all(node.children, ctx)


def inline_all(children, ctx: Ctx) -> str:
    parts = [inline(c, ctx) for c in children]
    s = ''.join(parts)
    return re.sub(r'[ \t]+', ' ', s)


def split_br(el: El):
    """按 <br> 把子节点切成若干段。"""
    segs, cur = [], []
    for c in el.children:
        if isinstance(c, El) and c.tag == 'br':
            segs.append(cur)
            cur = []
        else:
            cur.append(c)
    segs.append(cur)
    return segs


# ---------------------------------------------------------------- block 渲染


def render_para(el: El, ctx: Ctx) -> str:
    return inline_all(el.children, ctx).strip()


def render_h(el: El, level: int, ctx: Ctx) -> str:
    return '#' * level + ' ' + inline_all(el.children, ctx).strip()


def render_list(el: El, ctx: Ctx, indent='') -> list:
    ordered = el.tag == 'ol'
    lines = []
    idx = 0
    for li in el.children:
        if not (isinstance(li, El) and li.tag == 'li'):
            continue
        idx += 1
        bullet = f'{idx}.' if ordered else '-'
        # li 内部：行内部分 + 特殊 span（.in/.to/.note-line）+ 嵌套列表
        flow, nested = [], []
        for c in li.children:
            if isinstance(c, El) and c.tag in ('ul', 'ol'):
                nested.append(c)
            elif isinstance(c, El) and c.tag == 'span' and c.cls in ('in', 'to', 'note-line'):
                nested.append(c)
            else:
                flow.append(c)
        head = inline_all(flow, ctx).strip()
        lines.append(f'{indent}{bullet} {head}'.rstrip())
        for n in nested:
            if isinstance(n, El) and n.tag in ('ul', 'ol'):
                lines.extend(render_list(n, ctx, indent + '   '))
            else:
                txt = render_special_span(n, ctx).strip()
                if txt:
                    lines.append(f'{indent}   - {txt}')
    return lines


def render_special_span(el: El, ctx: Ctx) -> str:
    cls = el.cls
    if cls == 'to':  # 详见：<链接>；<链接>
        segs = [inline_all(s, ctx).strip() for s in split_br(el)]
        segs = [s for s in segs if s]
        if segs and segs[0].rstrip('：:').endswith('详见'):
            return '详见：' + '；'.join(segs[1:])
        return '；'.join(segs)
    return inline_all(el.children, ctx).strip()


def render_table(el: El, ctx: Ctx) -> list:
    thead = find(el, 'thead')
    tbody = find(el, 'tbody')
    rows = []
    if thead:
        tr = find(thead, 'tr')
        if tr:
            rows.append([inline_all(th.children, ctx).strip()
                         for th in tr.children if isinstance(th, El) and th.tag in ('th', 'td')])
    body_rows = []
    if tbody:
        for tr in tbody.children:
            if isinstance(tr, El) and tr.tag == 'tr':
                body_rows.append([inline_all(td.children, ctx).strip()
                                  for td in tr.children if isinstance(td, El) and td.tag in ('th', 'td')])
    if not rows and body_rows:
        rows, body_rows = body_rows[0:1], body_rows[1:]
    lines = []
    if rows:
        ncol = max(len(r) for r in rows + body_rows) if (rows or body_rows) else 0
        header = rows[0] + [''] * (ncol - len(rows[0]))
        lines.append('| ' + ' | '.join(esc_cell(c) for c in header) + ' |')
        lines.append('|' + '---|' * ncol)
        for r in body_rows:
            r = r + [''] * (ncol - len(r))
            lines.append('| ' + ' | '.join(esc_cell(c) for c in r) + ' |')
    return lines


def render_pre(el: El, ctx: Ctx) -> str:
    code = find(el, 'code')
    text = (code or el).raw_text().strip('\n')
    fence = '```'
    while fence in text:
        fence += '`'
    lang = ''
    stripped = text.lstrip()
    if stripped.startswith(('{', '[')):
        lang = 'json'
    elif re.search(r'^(import |from \S+ import |def |class |print\(|>>> )', stripped, re.M):
        lang = 'python'
    return f'{fence}{lang}\n{text}\n{fence}'


def render_figure(el: El, ctx: Ctx) -> list:
    lines = []
    img = find(el, 'img')
    video = find(el, 'video')
    if img is not None:
        src = img.attrs.get('src', '')
        alt = img.attrs.get('alt', '').strip()
        lines.append(f'【图】{src}（图片文件不动）')
        if alt:
            lines.append('')
            lines.append(f'替代文字（alt）：{alt}')
    elif video is not None:
        src = video.attrs.get('src', '')
        poster = video.attrs.get('poster', '')
        extra = f'；海报图 {poster}' if poster else ''
        lines.append(f'【视频】{src}（视频文件不动{extra}）')
        fallback = video.raw_text().strip()
        if fallback:
            lines.append('')
            lines.append(f'视频替代文字：{fallback}')
    cap = find(el, 'figcaption')
    if cap is not None:
        lines.append('')
        lines.append('图注：' + inline_all(cap.children, ctx).strip())
    return lines


def render_quiz(el: El, ctx: Ctx) -> list:
    lines = []
    q = find(el, 'p', 'q')
    num_el = find(q, 'span', 'num') if q else None
    num = num_el.raw_text().strip() if num_el else 'Q?'
    rest = ''
    if q is not None:
        rest_children = [c for c in q.children if not (isinstance(c, El) and c.cls == 'num')]
        rest = inline_all(rest_children, ctx).strip()
    lines.append(f'**{num}　{rest}**')
    lines.append('')
    for btn in el.children:
        if isinstance(btn, El) and btn.tag == 'button':
            mark = '✅ ' if btn.attrs.get('data-correct') else ''
            lines.append(f'- {mark}{inline_all(btn.children, ctx).strip()}')
    fb = find(el, 'p', 'feedback')
    if fb is not None:
        ok = fb.attrs.get('data-ok', '').strip()
        no = fb.attrs.get('data-no', '').strip()
        lines.append('')
        lines.append(f'答对时：{ok}')
        lines.append(f'答错时：{no}')
    return lines


def render_note(el: El, ctx: Ctx, mainline: bool) -> list:
    label_el = find(el, 'span', 'label')
    label = label_el.raw_text().strip() if label_el else ''
    lines = []
    if mainline:
        lines.append('## 主线（记住这一句的框）')
    elif label:
        lines.append(f'【选读框｜{label}】')
    else:
        lines.append('【提示框】')
    lines.append('')
    for c in el.children:
        if isinstance(c, El) and c.cls == 'label':
            continue
        if isinstance(c, El) and c.tag == 'p':
            lines.append(render_para(c, ctx))
            lines.append('')
        elif isinstance(c, El) and c.tag in ('ul', 'ol'):
            lines.extend(render_list(c, ctx))
            lines.append('')
        elif isinstance(c, El) and c.tag == 'table':
            lines.extend(render_table(c, ctx))
            lines.append('')
        elif isinstance(c, El) and c.tag == 'pre':
            lines.append(render_pre(c, ctx))
            lines.append('')
    while lines and lines[-1] == '':
        lines.pop()
    return lines


def render_goal(el: El, ctx: Ctx) -> list:
    label_el = find(el, 'span', 'label')
    label = label_el.raw_text().strip() if label_el else ''
    head = '## 开场（页首框）' if not label else f'## 开场（页首框｜{label}）'
    lines = [head, '']
    for c in el.children:
        if isinstance(c, El) and c.cls == 'label':
            continue
        if isinstance(c, El) and c.tag == 'p':
            lines.append(render_para(c, ctx))
            lines.append('')
        elif isinstance(c, El) and c.tag in ('ul', 'ol'):
            lines.extend(render_list(c, ctx))
            lines.append('')
    while lines and lines[-1] == '':
        lines.pop()
    return lines


def render_goal_box(el: El, ctx: Ctx) -> list:
    """课文中间的 goal 样式框（白底重点框／课程地图框）。"""
    label_el = find(el, 'span', 'label')
    label = label_el.raw_text().strip() if label_el else ''
    lines = [f'【goal 框｜{label}】' if label else '【goal 框】', '']
    for c in el.children:
        if isinstance(c, El) and c.cls == 'label':
            continue
        if isinstance(c, El) and c.tag in ('p', 'ul', 'ol'):
            if c.tag in ('ul', 'ol'):
                lines.extend(render_list(c, ctx))
                lines.append('')
            else:
                lines.append(render_para(c, ctx))
                lines.append('')
    while lines and lines[-1] == '':
        lines.pop()
    return lines


def render_pillars(el: El, ctx: Ctx) -> list:
    lines = ['【三柱框】', '']
    for p in el.children:
        if not (isinstance(p, El) and 'pillar' in p.cls.split()):
            continue
        for c in p.children:
            if not isinstance(c, El):
                continue
            if c.tag in ('h2', 'h3', 'h4'):
                lines.append('**' + inline_all(c.children, ctx).strip() + '**')
                lines.append('')
            elif c.tag == 'p':
                lines.append(render_para(c, ctx))
                lines.append('')
    while lines and lines[-1] == '':
        lines.pop()
    return lines


def render_loop(el: El, ctx: Ctx) -> list:
    """页内 HTML 画的流程图（loop-node / loop-arrow / loop-back）拍平成一行箭头图。"""
    nodes = []
    back = ''
    for c in el.children:
        if not isinstance(c, El):
            continue
        if 'loop-node' in c.cls:
            small = find(c, 'small')
            if small is not None:
                main = c.raw_text().replace(small.raw_text(), '').strip()
                nodes.append(f'{main}（{small.raw_text().strip()}）')
            else:
                nodes.append(c.raw_text().strip())
        elif 'loop-back' in c.cls:
            back = inline_all(c.children, ctx).strip()
    lines = ['【页内图｜流程】（HTML 排版，回写时按原结构还原；下面的文字可改）', '']
    lines.append(' → '.join(nodes))
    if back:
        lines.append('')
        lines.append(back)
    return lines


def render_phase_item_li(li: El, ctx: Ctx, indent='') -> list:
    return render_list(_fake_list([li]), ctx, indent)


def _fake_list(lis):
    ul = El('ol')
    ul.children = list(lis)
    return ul


def render_phases_block(el: El, ctx: Ctx, kind: str) -> list:
    """0002-deep 的 phases / shared 总图。"""
    lines = []
    if kind == 'phases':
        lines.append('【页内图｜总图】（HTML 排版，回写时按原结构还原；下面的文字可改）')
        lines.append('')
        blocks = list(el.children)
    else:  # shared
        h = find(el, 'p', 'shared-h')
        head = inline_all(h.children, ctx).strip() if h is not None else ''
        lines.append(f'【共用框｜{head}】')
        lines.append('')
        blocks = [c for c in el.children if not (isinstance(c, El) and c.cls == 'shared-h')]
    for b in blocks:
        if not isinstance(b, El):
            continue
        if 'phase' in b.cls and b.tag == 'div':
            ph_h = find(b, 'p', 'phase-h')
            if ph_h is not None:
                sub = find(ph_h, 'span', 'sub')
                main_t = inline_all([c for c in ph_h.children
                                     if not (isinstance(c, El) and c.cls == 'sub')], ctx).strip()
                sub_t = sub.raw_text().strip() if sub is not None else ''
                lines.append(f'**{main_t}**（{sub_t}）' if sub_t else f'**{main_t}**')
                lines.append('')
            for c in b.children:
                if isinstance(c, El) and c.tag in ('ol', 'ul'):
                    lines.extend(render_list(c, ctx))
                    lines.append('')
                elif isinstance(c, El) and 'feed' in c.cls:
                    cost = find(c, 'span', 'cost')
                    main_t = inline_all([x for x in c.children
                                         if not (isinstance(x, El) and x.cls == 'cost')], ctx).strip()
                    line = main_t
                    if cost is not None:
                        line += '（' + inline_all(cost.children, ctx).strip() + '）'
                    lines.append(line)
                    lines.append('')
        elif isinstance(b, El) and b.tag in ('ol', 'ul'):
            lines.extend(render_list(b, ctx))
            lines.append('')
        elif isinstance(b, El) and b.tag == 'p':
            lines.append(render_para(b, ctx))
            lines.append('')
    while lines and lines[-1] == '':
        lines.pop()
    return lines


def render_details(el: El, ctx: Ctx) -> list:
    summary = find(el, 'summary')
    head = inline_all(summary.children, ctx).strip() if summary is not None else ''
    lines = [f'【折叠框｜{head}】', '']
    for c in el.children:
        if not isinstance(c, El):
            continue
        if c.tag == 'summary':
            continue
        lines.extend(render_block(c, ctx))
        lines.append('')
    while lines and lines[-1] == '':
        lines.pop()
    return lines


def render_source(el: El, ctx: Ctx) -> list:
    lines = ['## 一手资料（页脚框，一般不动）', '']
    segs = split_br(el)
    start = 0
    # 第一段若不带链接，是盒子标题（「这节课的一手资料：」），标题已表达，不进 md；
    # 其余段即使不带链接（纯注释行）也保留。
    if segs and not any(isinstance(c, El) and c.tag == 'a' for c in segs[0]):
        start = 1
    for seg in segs[start:]:
        text = inline_all(seg, ctx).strip()
        if not text:
            continue
        lines.append(f'- {text}')
    return lines


def render_next(el: El, ctx: Ctx) -> list:
    lines = ['## 页尾互链（一般不动）', '']
    for seg in split_br(el):
        text = inline_all(seg, ctx).strip()
        if text:
            lines.append(f'- {text}')
    return lines


def render_ask_teacher(el: El, ctx: Ctx) -> list:
    return ['## 提问框', '', render_para(el, ctx)]


def render_generic(el: El, ctx: Ctx, mainline_note_used=None) -> list:
    """未知标签/无类容器的兜底：没有块级子节点就当行内内容，否则逐块递归（文本节点不丢）。"""
    BLOCK = {'p', 'h1', 'h2', 'h3', 'h4', 'ul', 'ol', 'table', 'pre', 'figure', 'details', 'div', 'blockquote'}
    if not any(isinstance(c, El) and c.tag in BLOCK for c in el.children):
        txt = inline_all(el.children, ctx).strip()
        return [txt] if txt else []
    out = []
    for c in el.children:
        if isinstance(c, El):
            out.extend(render_block(c, ctx, mainline_note_used))
        elif isinstance(c, str) and c.strip():
            out.append(inline(c, ctx).strip())
    return out


def render_block(el: El, ctx: Ctx, mainline_note_used=None) -> list:
    """渲染一个顶层块，返回行列表。mainline_note_used: [bool] 可变标记（主线 note 只认第一个）。"""
    tag, cls = el.tag, el.cls
    if tag in ('h1',):
        return []  # h1 已在文件头
    if tag == 'h2':
        return [render_h(el, 2, ctx)]
    if tag == 'h3':
        return [render_h(el, 3, ctx)]
    if tag == 'h4':
        return [render_h(el, 4, ctx)]
    if tag == 'p':
        if 'subtitle' in cls:
            return [render_para(el, ctx)]
        if 'next' in cls:
            return render_next(el, ctx)
        return [render_para(el, ctx)]
    if tag == 'div':
        if 'goal' in cls:
            if not ctx.goal_seen:
                ctx.goal_seen = True
                return render_goal(el, ctx)
            return render_goal_box(el, ctx)
        if 'note' in cls:
            has_label = find(el, 'span', 'label') is not None
            if not has_label and mainline_note_used is not None and not mainline_note_used[0]:
                mainline_note_used[0] = True
                return render_note(el, ctx, mainline=True)
            return render_note(el, ctx, mainline=False)
        if 'ask-teacher' in cls:
            return render_ask_teacher(el, ctx)
        if 'pillars' in cls:
            return render_pillars(el, ctx)
        if 'loop' in cls:
            return render_loop(el, ctx)
        if 'phases' in cls:
            return render_phases_block(el, ctx, 'phases')
        if 'shared' in cls:
            return render_phases_block(el, ctx, 'shared')
        if 'quiz' in cls:
            return render_quiz(el, ctx)
        if 'source' in cls:
            return render_source(el, ctx)
        # 未知容器：没有块级子节点就当行内内容渲染，否则逐块递归（文本节点也不丢）
        return render_generic(el, ctx, mainline_note_used)
    if tag == 'figure':
        return render_figure(el, ctx)
    if tag == 'details':
        return render_details(el, ctx)
    if tag in ('ul', 'ol'):
        return render_list(el, ctx)
    if tag == 'table':
        return render_table(el, ctx)
    if tag == 'pre':
        return [render_pre(el, ctx)]
    if tag in ('footer', 'script', 'style'):
        return []
    # 兜底：未知标签/无类容器
    return render_generic(el, ctx, mainline_note_used)


# ---------------------------------------------------------------- 文件级


def file_header(src_rel: str, md: Path) -> list:
    readme = os.path.relpath(OUT / 'README.md', md.parent.resolve()).replace('\\', '/')
    return [
        f'> 这是 `{src_rel}` 的文字稿：**直接在上面改，改完交回，我逐段映射回 HTML 并跑核验**。',
        f'> 改法与标记约定见 [README]({readme})：✅ 标正确选项、「答对时/答错时」是小测反馈、【图】【选读框】等标记说明、小节可增删合并（节号乱了没关系，回写时重排）。',
    ]


def convert_file(src: Path, md_path: Path) -> str:
    html_text = src.read_text(encoding='utf-8')
    dom = parse(html_text)
    wrap = find(dom, 'div', 'wrap')
    body_children = wrap.children if wrap is not None else dom.children

    h1 = find(dom, 'h1')
    title = inline_all(h1.children, Ctx(src, md_path)).strip() if h1 else src.stem

    ctx = Ctx(src, md_path)
    lines = [f'# {title}', '']
    lines += file_header(str(src.relative_to(ROOT)).replace('\\', '/'), md_path)
    lines += ['', '---', '']

    meta = find(dom, 'div', 'lesson-meta')
    if meta is not None:
        lines.append('【meta】' + meta.raw_text().strip())
        alias = meta.attrs.get('data-alias', '').strip()
        if alias:
            lines.append('【别名（data-alias）】' + alias)
        lines.append('')

    flow, mainline_used = [], [False]
    # 「收尾段」：最后一个 quiz 之后、source/ask-teacher 之前的普通块
    top = [c for c in body_children if isinstance(c, El)]
    quiz_seen = False
    closing_buf = []
    for el in top:
        is_quiz = el.tag == 'div' and 'quiz' in el.cls
        is_tail = (el.tag == 'div' and ('source' in el.cls or 'ask-teacher' in el.cls)) or \
                  (el.tag == 'p' and 'next' in el.cls)
        if quiz_seen and not is_quiz and not is_tail and el.tag not in ('footer',):
            closing_buf.append(el)
            continue
        if closing_buf and (is_quiz or is_tail):
            if not any(c.tag == 'h2' for c in closing_buf):
                flow.append('## 收尾段（小测后面）')
                flow.append('')
            for c in closing_buf:
                flow.extend(render_block(c, ctx, mainline_used))
                flow.append('')
            closing_buf = []
        if is_quiz:
            quiz_seen = True
        flow.extend(render_block(el, ctx, mainline_used))
        flow.append('')
    if closing_buf:
        if not any(c.tag == 'h2' for c in closing_buf):
            flow.append('## 收尾段（小测后面）')
            flow.append('')
        for c in closing_buf:
            flow.extend(render_block(c, ctx, mainline_used))
            flow.append('')

    lines.extend(flow)
    # 收尾：去掉多余空行
    out, prev_blank = [], False
    for ln in lines:
        blank = (ln.strip() == '')
        if blank and prev_blank:
            continue
        out.append(ln.rstrip())
        prev_blank = blank
    while out and out[-1] == '':
        out.pop()
    return '\n'.join(out) + '\n'


def md_for(src: Path) -> Path:
    rel = src.relative_to(LESSONS)
    return OUT / rel.parent / (src.stem + '.md')


def convert_all(check: bool) -> int:
    OUT.mkdir(exist_ok=True)
    srcs = sorted(LESSONS.rglob('*.html'))
    errors = 0
    for src in srcs:
        md_path = md_for(src)
        md_path.parent.mkdir(parents=True, exist_ok=True)
        text = convert_file(src, md_path)
        md_path.write_text(text, encoding='utf-8', newline='\n')
        print(f'ok  {md_path.relative_to(ROOT)}')
    print(f'\n共转换 {len(srcs)} 个文件 -> lessons-md/')
    if check:
        errors = validate()
    return errors


# ---------------------------------------------------------------- 校验


def validate() -> int:
    print('\n== 校验 ==')
    errs = 0
    tot_quiz = tot_correct = tot_img = tot_video = 0
    link_fail = 0
    loss_total = 0

    def norm(s: str) -> str:
        """只留字母数字与 CJK，两侧同口径，用于包含性检查。"""
        return re.sub(r'[^0-9A-Za-z\u4e00-\u9fff]+', '', s)

    for src in sorted(LESSONS.rglob('*.html')):
        md_path = md_for(src)
        if not md_path.exists():
            print(f'[FAIL] 缺文件 {md_path}')
            errs += 1
            continue
        html_t = src.read_text(encoding='utf-8')
        md_t = md_path.read_text(encoding='utf-8')
        hq = html_t.count('class="quiz"')
        hc = html_t.count('data-correct="true"')
        himg = html_t.count('<img ')
        hvid = html_t.count('<video ')
        mq = len(re.findall(r'^\*\*Q\d+　', md_t, re.M))
        mc = md_t.count('\n- ✅ ')
        mok = md_t.count('答对时：')
        mno = md_t.count('答错时：')
        mimg = len(re.findall(r'^【图】', md_t, re.M))
        mvid = len(re.findall(r'^【视频】', md_t, re.M))
        tot_quiz += hq; tot_correct += hc; tot_img += himg; tot_video += hvid
        bad = []
        if hq != mq:
            bad.append(f'quiz {hq}->{mq}')
        if hc != mc:
            bad.append(f'✅ {hc}->{mc}')
        if hq != mok or hq != mno:
            bad.append(f'反馈 {hq}/{mok}/{mno}')
        if himg != mimg:
            bad.append(f'图 {himg}->{mimg}')
        if hvid != mvid:
            bad.append(f'视频 {hvid}->{mvid}')
        # 残留 HTML（允许 sub/sup/small/br）＋ 链接可达（都在代码块外判）
        in_fence = False
        for i, ln in enumerate(md_t.splitlines(), 1):
            if ln.startswith('```'):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            scan_ln = re.sub(r'`[^`]*`', '', ln)  # 行内代码里的 <xxx> 是安全的
            for m in re.finditer(r'</?([a-zA-Z][a-zA-Z0-9]*)[ >]', scan_ln):
                if m.group(1).lower() not in ('sub', 'sup', 'small', 'br'):
                    bad.append(f'L{i} 残留标签 <{m.group(1)}>')
                    break
            for m in re.finditer(r'\]\(([^)]+)\)', scan_ln):
                href = m.group(1)
                if href.startswith(('http://', 'https://', 'mailto:')):
                    continue
                base, _, frag = href.partition('#')
                if not base:
                    continue  # 页内锚点（HTML 原件上有，md 不锚）
                target = (md_path.parent / base).resolve()
                if not target.exists():
                    bad.append(f'死链 {href}')
                    link_fail += 1
        # 全文本丢失检查：HTML 的每个文本片段（footer 除外）都必须能在 md 里找到
        dom = parse(html_t)
        wrap_el = find(dom, 'div', 'wrap')
        chunks = []

        def collect(el):
            for c in el.children:
                if isinstance(c, str):
                    if len(norm(c)) >= 8:
                        chunks.append(c)
                elif isinstance(c, El) and c.tag != 'footer':
                    collect(c)

        collect(wrap_el if wrap_el is not None else dom)
        md_norm = norm(md_t)
        # 有意不进 md 的盒子标题（标题行已表达）：白名单
        drop_labels = {norm('这节课的一手资料'), norm('这篇用到的一手资料')}
        missing = [c for c in chunks if norm(c) not in md_norm and norm(c) not in drop_labels]
        loss_total += len(missing)
        for c in missing:
            bad.append(f'丢文本 {c.strip()[:40]!r}')
        if bad:
            errs += 1
            print(f'[FAIL] {md_path.relative_to(ROOT)}: ' + '；'.join(bad))
        else:
            print(f'[ok] {md_path.relative_to(ROOT)}（quiz {hq} ✅ {hc}）')
    print(f'\n合计：quiz {tot_quiz}（✅ {tot_correct}）· 图 {tot_img} · 视频 {tot_video} · 死链 {link_fail} · 丢文本片段 {loss_total}')
    print('校验通过' if errs == 0 else f'校验失败：{errs} 个文件有问题')
    return errs


if __name__ == '__main__':
    sys.exit(convert_all('--check' in sys.argv))
