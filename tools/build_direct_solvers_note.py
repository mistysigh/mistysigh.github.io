#!/usr/bin/env python3
"""Build the second-chapter study note from its maintained Markdown source."""

from __future__ import annotations

import html
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'content/notes/numerical-analysis-direct-solvers.md'
OUTPUT = ROOT / 'notes/numerical-analysis-direct-solvers/index.html'
CODE_DIR = OUTPUT.parent / 'code'
TEMPLATE = ROOT / 'archives/index.html'
TITLE = '从消元代码读懂线性方程组的直接解法'
URL = 'https://mistysigh.github.io/notes/numerical-analysis-direct-solvers/'


def main() -> None:
    source = SOURCE.read_text(encoding='utf-8')
    code_blocks = re.findall(r'```matlab\n(.*?)```', source, re.DOTALL)
    functions = {}
    for code in code_blocks:
        match = re.search(r'^function\s+.*?=\s*(\w+)\(', code, re.MULTILINE)
        if match:
            functions[match.group(1)] = code
    if len(functions) != 5:
        raise ValueError(f'Expected five MATLAB functions, found {len(functions)}')
    CODE_DIR.mkdir(parents=True, exist_ok=True)
    for name, code in functions.items():
        (CODE_DIR / f'{name}.m').write_text(code, encoding='utf-8')

    fragment = subprocess.run(
        ['pandoc', '-f', 'markdown+tex_math_dollars', '-t', 'html5',
         '--math-method=mathjax', '--wrap=none', str(SOURCE)],
        check=True, capture_output=True, text=True,
    ).stdout
    headings = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', fragment)
    if len(headings) != 8:
        raise ValueError(f'Expected eight numbered sections, found {len(headings)}')
    toc = '<nav class="study-toc" aria-label="本文目录"><h2>本文目录</h2><ol>'
    for number, (identifier, title) in enumerate(headings, 1):
        toc += (f'<li><a href="#{html.escape(identifier, quote=True)}">'
                f'<span>{number:02d}</span>{title}</a></li>')
    toc += '</ol></nav>'
    fragment = re.sub(r'<h1\b[^>]*>.*?</h1>', '', fragment, count=1)

    page = TEMPLATE.read_text(encoding='utf-8')
    page = page.replace('<title>Archive |', f'<title>{TITLE} |', 1)
    page = page.replace('content="Archive"', f'content="{TITLE}"', 1)
    page = page.replace('https://mistysigh.github.io/archives/index.html', URL, 1)
    page = page.replace('<meta property="og:type" content="website">',
                        '<meta property="og:type" content="article">', 1)
    page = page.replace('<html lang="en">', '<html lang="zh-CN">', 1)
    page = page.replace('<meta property="og:locale" content="en_US">',
                        '<meta property="og:locale" content="zh_CN">', 1)
    main_open = '<main class="sidebar-translate" id="content">'
    start = page.index(main_open)
    end = page.index('</main>', start) + len('</main>')
    body = (
        f'{main_open}<div id="post"><article class="hty-card post-block study-note" '
        'itemscope itemtype="https://schema.org/Article">'
        f'<link itemprop="mainEntityOfPage" href="{URL}">'
        f'<header class="post-header"><h1 class="post-title" itemprop="name headline">{TITLE}</h1>'
        '<p class="study-subtitle">Gauss 消去、选主元、LU、Cholesky、追赶法与条件数</p>'
        '<div class="post-meta"><a href="/notes/">学习笔记</a> · 数值分析基础第二章</div>'
        '</header><section class="post-body" itemprop="articleBody">'
        f'<div class="post-content markdown-body">{toc}{fragment}</div>'
        '</section></article><p class="study-back"><a href="/notes/">← 返回学习笔记</a></p>'
        '</div></main>'
    )
    page = page[:start] + body + page[end:]
    assets = (
        '<link rel="stylesheet" href="/css/study-note.css">'
        '<script>window.MathJax={tex:{inlineMath:[["\\\\(","\\\\)"]],'
        'displayMath:[["\\\\[","\\\\]"]],packages:{"[+]":["ams"]}},'
        'options:{enableMenu:false}};</script>'
        '<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>'
    )
    page = page.replace('</head>', assets + '</head>', 1)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(page, encoding='utf-8')
    print(f'Built {OUTPUT.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
