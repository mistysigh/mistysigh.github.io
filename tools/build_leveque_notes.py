#!/usr/bin/env python3
"""Render the LeVeque chapters from maintained Markdown into Yun-themed pages."""

from __future__ import annotations

import html
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'content/notes/leveque-finite-difference'
OUTPUT = ROOT / 'notes/leveque-finite-difference'
TEMPLATE = ROOT / 'archives/index.html'
BASE_URL = 'https://mistysigh.github.io/notes/leveque-finite-difference/'
PAGES = (
    ('ch01', '第一章：有限差分近似', 'Taylor 展开、差分权重与局部精度'),
    ('ch02', '第二章：一维边值问题', '边界条件、稳定性、Green 函数与奇异摄动'),
    ('ch03', '第三章：二维椭圆方程', '五点与九点格式、谱稳定性及稀疏求解'),
)


def render_page(title: str, subtitle: str, url: str, fragment: str, toc: bool = True) -> str:
    page = TEMPLATE.read_text(encoding='utf-8')
    page = page.replace('<title>Archive |', f'<title>{title} |', 1)
    page = page.replace('content="Archive"', f'content="{title}"', 1)
    page = page.replace('https://mistysigh.github.io/archives/index.html', url, 1)
    page = page.replace('<meta property="og:type" content="website">',
                        '<meta property="og:type" content="article">', 1)
    page = page.replace('<html lang="en">', '<html lang="zh-CN">', 1)
    page = page.replace('<meta property="og:locale" content="en_US">',
                        '<meta property="og:locale" content="zh_CN">', 1)
    if toc:
        headings = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', fragment)
        contents = '<nav class="study-toc" aria-label="本文目录"><h2>本文目录</h2><ol>'
        for number, (identifier, heading) in enumerate(headings, 1):
            contents += (f'<li><a href="#{html.escape(identifier, quote=True)}">'
                         f'<span>{number:02d}</span>{heading}</a></li>')
        contents += '</ol></nav>'
        fragment = contents + fragment
    fragment = re.sub(r'<h1\b[^>]*>.*?</h1>', '', fragment, count=1)
    main_open = '<main class="sidebar-translate" id="content">'
    start = page.index(main_open)
    end = page.index('</main>', start) + len('</main>')
    body = (
        f'{main_open}<div id="post"><article class="hty-card post-block study-note" '
        'itemscope itemtype="https://schema.org/Article">'
        f'<link itemprop="mainEntityOfPage" href="{url}">'
        f'<header class="post-header"><h1 class="post-title" itemprop="name headline">{title}</h1>'
        f'<p class="study-subtitle">{subtitle}</p>'
        '<div class="post-meta"><a href="/notes/">学习笔记</a> · '
        '<a href="/notes/leveque-finite-difference/">LeVeque 有限差分方法</a></div>'
        '</header><section class="post-body" itemprop="articleBody">'
        f'<div class="post-content markdown-body">{fragment}</div>'
        '</section></article><p class="study-back"><a href="/notes/leveque-finite-difference/">'
        '← 返回本系列目录</a></p></div></main>'
    )
    page = page[:start] + body + page[end:]
    assets = (
        '<link rel="stylesheet" href="/css/study-note.css">'
        '<script>window.MathJax={tex:{inlineMath:[["\\\\(","\\\\)"]],'
        'displayMath:[["\\\\[","\\\\]"]],packages:{"[+]":["ams"]}},'
        'options:{enableMenu:false}};</script>'
        '<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>'
    )
    return page.replace('</head>', assets + '</head>', 1)


def render_markdown(path: Path) -> str:
    return subprocess.run(
        ['pandoc', '-f', 'markdown+tex_math_dollars', '-t', 'html5',
         '--math-method=mathjax', '--wrap=none', str(path)],
        check=True, capture_output=True, text=True,
    ).stdout


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    hub = (
        '<p class="study-lead">依据 R. J. LeVeque, <em>Finite Difference Methods for Ordinary '
        'and Partial Differential Equations</em>（SIAM, 2007）及提供的中文 TeX 稿，'
        '重写前三章的理论推导。按“构造差分 → 边值问题稳定性 → 二维椭圆系统”阅读。</p>'
        '<div class="study-note-list">'
        '<article class="note-entry"><h2><a href="ch01/">第一章：有限差分近似</a></h2>'
        '<p>Taylor 展开、中心与单侧公式、非均匀网格、一般差分权重。</p></article>'
        '<article class="note-entry"><h2><a href="ch02/">第二章：一维边值问题</a></h2>'
        '<p>截断误差与全局误差、谱稳定性、Green 函数、Neumann 条件、'
        '非线性、边界层和高阶方法。</p></article>'
        '<article class="note-entry"><h2><a href="ch03/">第三章：二维椭圆方程</a></h2>'
        '<p>五点与九点格式、块稀疏矩阵、二维误差证明、通量与求解成本。</p>'
        '</article></div>'
        '<p>原中文稿中个别式子存在转写不一致；正文在相关推导处给出可代入检查的校正。'
        '这份笔记是学习性改写，不替代原书。</p>'
    )
    hub_page = render_page('LeVeque 有限差分方法：前三章导读',
                           '以理论推导为主线的一维与二维差分笔记', BASE_URL, hub, False)
    (OUTPUT / 'index.html').write_text(hub_page, encoding='utf-8')
    for slug, title, subtitle in PAGES:
        fragment = render_markdown(SOURCE / f'{slug}.md')
        out = OUTPUT / slug / 'index.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_page(title, subtitle, BASE_URL + slug + '/', fragment),
                       encoding='utf-8')
        print(f'Built {out.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
