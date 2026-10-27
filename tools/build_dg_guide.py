#!/usr/bin/env python3
"""Render source-grounded DG notes into the existing Yun site."""

from __future__ import annotations

import html
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'content/notes/dg-guide'
OUTPUT = ROOT / 'notes/dg-guide'
BASE = 'https://mistysigh.github.io/notes/dg-guide/'
PAGES = (
    ('foundation', '01 · 从守恒律到 DG', '离散空间、局部弱形式与共同界面通量'),
    ('hyperbolic', '02 · 双曲问题：通量与能量', '一维输运、中心与迎风通量、离散能量估计'),
    ('nodal', '03 · 节点 DG：从公式到矩阵', '参考单元、Legendre 节点、质量矩阵与提升算子'),
    ('elliptic', '04 · 椭圆问题：SIPG 与误差', '断裂空间、内罚格式、强制性和对偶误差'),
)


def markdown(path: Path) -> str:
    return subprocess.run(
        ['pandoc', '-f', 'markdown+tex_math_dollars', '-t', 'html5',
         '--math-method=mathjax', '--wrap=none', str(path)],
        check=True, capture_output=True, text=True,
    ).stdout


def page(title: str, subtitle: str, url: str, fragment: str) -> str:
    doc = (ROOT / 'archives/index.html').read_text(encoding='utf-8')
    doc = doc.replace('<title>Archive |', f'<title>{title} |', 1)
    doc = doc.replace('content="Archive"', f'content="{html.escape(title, quote=True)}"', 1)
    doc = doc.replace('<meta property="og:title" content="Archive">',
                      f'<meta property="og:title" content="{html.escape(title, quote=True)}">', 1)
    doc = doc.replace('https://mistysigh.github.io/archives/index.html', url, 1)
    doc = doc.replace('<html lang="en">', '<html lang="zh-CN">', 1)
    doc = doc.replace('content="en_US"', 'content="zh_CN"', 1)
    doc = doc.replace('<meta property="og:type" content="website">',
                      '<meta property="og:type" content="article">', 1)
    headings = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', fragment)
    if headings:
        toc = '<nav class="study-toc" aria-label="本文目录"><h2>本文目录</h2><ol>'
        for i, (identifier, heading) in enumerate(headings, 1):
            toc += (f'<li><a href="#{html.escape(identifier, quote=True)}">'
                    f'<span>{i:02d}</span>{heading}</a></li>')
        fragment = toc + '</ol></nav>' + fragment
    fragment = re.sub(r'<h1\b[^>]*>.*?</h1>', '', fragment, count=1)
    start = doc.index('<main class="sidebar-translate" id="content">')
    end = doc.index('</main>', start) + len('</main>')
    body = (
        '<main class="sidebar-translate" id="content"><div id="post">'
        '<article class="hty-card post-block study-note dg-note" itemscope itemtype="https://schema.org/Article">'
        f'<link itemprop="mainEntityOfPage" href="{url}">'
        f'<header class="post-header"><h1 class="post-title" itemprop="name headline">{title}</h1>'
        f'<p class="study-subtitle">{subtitle}</p>'
        '<div class="post-meta"><a href="/notes/">学习笔记</a> · '
        '<a href="/notes/dg-guide/">DG 导学</a></div></header>'
        '<section class="post-body" itemprop="articleBody"><div class="post-content markdown-body">'
        f'{fragment}</div></section></article>'
        '<p class="study-back"><a href="/notes/dg-guide/">← 返回 DG 导学目录</a></p>'
        '</div></main>'
    )
    doc = doc[:start] + body + doc[end:]
    assets = (
        '<link rel="stylesheet" href="/css/study-note.css">'
        '<link rel="stylesheet" href="/css/dg-guide.css">'
        '<script>window.MathJax={tex:{inlineMath:[["\\\\(","\\\\)"]],'
        'displayMath:[["\\\\[","\\\\]"]],packages:{"[+]":["ams"]}},'
        'options:{enableMenu:false}};</script>'
        '<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>'
    )
    return doc.replace('</head>', assets + '</head>', 1)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / 'index.html').write_text(page(
        'DG 导学：从界面通量到椭圆内罚',
        '沿“局部弱形式 → 稳定性 → 节点实现 → 椭圆误差”阅读',
        BASE, markdown(SOURCE / 'index.md')), encoding='utf-8')
    for slug, title, subtitle in PAGES:
        destination = OUTPUT / slug / 'index.html'
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(page(title, subtitle, BASE + slug + '/',
                                    markdown(SOURCE / f'{slug}.md')), encoding='utf-8')
        print(f'Built {destination.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
