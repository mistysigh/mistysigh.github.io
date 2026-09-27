#!/usr/bin/env python3
"""Build the Chebyshev study note from its preserved LaTeX source.

Requires Pandoc. Run from any directory with: python3 tools/build_study_note.py
"""

from __future__ import annotations

import html
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "content/notes/chebyshev-spectral-collocation.tex"
OUTPUT = ROOT / "notes/chebyshev-spectral-collocation/index.html"
TEMPLATE = ROOT / "archives/index.html"
TITLE = "从零理解 Chebyshev 谱配置法"
URL = "https://mistysigh.github.io/notes/chebyshev-spectral-collocation/"


def make_fragment() -> str:
    result = subprocess.run(
        ["pandoc", "-f", "latex", "-t", "html5", "--math-method=mathjax", "--wrap=none", str(SOURCE)],
        check=True,
        capture_output=True,
        text=True,
    )
    fragment = result.stdout
    if not fragment.strip() or "<h1" not in fragment:
        raise ValueError("Pandoc did not produce the expected study note")
    return fragment


def prepare_math(fragment: str) -> str:
    """Keep TeX math renderable and preserve numbered equation references."""
    section = 0
    equation = 0
    labels: dict[str, str] = {}
    token = re.compile(
        r'(<h1\b[^>]*>.*?</h1>)|<span class="math display">\\\[(.*?)\\\]</span>',
        re.DOTALL,
    )

    def replace(match: re.Match[str]) -> str:
        nonlocal section, equation
        if match.group(1):
            section += 1
            equation = 0
            return match.group(1)

        body = match.group(2).strip()
        label_match = re.search(r"\\label\{([^}]+)\}", body)
        label = label_match.group(1) if label_match else None
        body = re.sub(r"\\label\{[^}]+\}", "", body).strip()
        body = body.replace(r"\bm{", r"\boldsymbol{")
        numbered = False
        count = 0

        for environment in ("equation", "equation*", "align", "align*"):
            opening = rf"\begin{{{environment}}}"
            closing = rf"\end{{{environment}}}"
            if body.startswith(opening) and body.endswith(closing):
                body = body[len(opening) : -len(closing)].strip()
                numbered = not environment.endswith("*")
                if environment.startswith("align"):
                    # LaTeX align numbers each row; the web view labels its last row.
                    count = len(re.split(r"(?<!\\)\\\\", body))
                    body = rf"\begin{{aligned}}{body}\end{{aligned}}"
                else:
                    count = 1
                break

        number = None
        if numbered:
            equation += count
            number = f"{section}.{equation}"
            body += rf"\tag{{{number}}}"
        if label and number:
            labels[label] = number
        identifier = f' id="{html.escape(label, quote=True)}"' if label else ""
        return f'<span class="math display"{identifier}>\\[{body}\\]</span>'

    fragment = token.sub(replace, fragment)
    fragment = fragment.replace(r"\bm{", r"\boldsymbol{")

    def replace_ref(match: re.Match[str]) -> str:
        label = match.group(1)
        if label not in labels:
            raise ValueError(f"Unresolved equation reference: {label}")
        return f'<a href="#{html.escape(label, quote=True)}">({labels[label]})</a>'

    fragment = re.sub(
        r'<a href="#([^"]+)" data-reference-type="eqref" data-reference="[^"]+">\[[^<]+\]</a>',
        replace_ref,
        fragment,
    )
    if "data-reference-type=\"eqref\"" in fragment or r"\begin{equation}" in fragment:
        raise ValueError("An equation was not converted correctly")
    return fragment


def make_toc(fragment: str) -> str:
    items = []
    for number, match in enumerate(re.finditer(r'<h1 id="([^"]+)">(.*?)</h1>', fragment), 1):
        identifier, label = match.groups()
        label = re.sub(r"<[^>]+>", "", label)
        items.append(
            f'<li><a href="#{html.escape(identifier, quote=True)}">'
            f'<span>{number:02d}</span>{label}</a></li>'
        )
    return '<nav class="study-toc" aria-label="本文目录"><h2>本文目录</h2><ol>' + "".join(items) + "</ol></nav>"


def make_page(fragment: str) -> str:
    toc = make_toc(fragment)
    # The page title is h1; source sections and subsections follow beneath it.
    fragment = re.sub(
        r"<(/?)h([12])\b",
        lambda match: f"<{match.group(1)}h{int(match.group(2)) + 1}",
        fragment,
    )
    page = TEMPLATE.read_text(encoding="utf-8")
    page = page.replace("<title>Archive |", f"<title>{TITLE} |", 1)
    page = page.replace('content="Archive"', f'content="{TITLE}"', 1)
    page = page.replace("https://mistysigh.github.io/archives/index.html", URL, 1)
    page = page.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">', 1)
    page = page.replace("<html lang=\"en\">", "<html lang=\"zh-CN\">", 1)
    page = page.replace('<meta property="og:locale" content="en_US">', '<meta property="og:locale" content="zh_CN">', 1)

    main_start = '<main class="sidebar-translate" id="content">'
    a = page.index(main_start)
    b = page.index("</main>", a) + len("</main>")
    intro = (
        '<p class="study-lead">从节点值与 Lagrange 插值出发，推导 Chebyshev 微分矩阵，'
        '再用一维 Poisson 边值问题检验离散与程序。</p>'
        '<p class="study-route">节点值 → 全局插值 → 微分矩阵 → 边值问题 → 数值验证</p>'
    )
    body = (
        f'{main_start}<div id="post"><article class="hty-card post-block study-note" '
        'itemscope itemtype="https://schema.org/Article">'
        f'<link itemprop="mainEntityOfPage" href="{URL}">'
        '<header class="post-header">'
        f'<h1 class="post-title" itemprop="name headline">{TITLE}</h1>'
        '<p class="study-subtitle">Lagrange 插值、谱微分矩阵与一维 Poisson 边值问题</p>'
        '<div class="post-meta"><a href="/notes/">学习笔记</a> · Chebyshev 谱配置法</div>'
        '</header><section class="post-body" itemprop="articleBody">'
        f'<div class="post-content markdown-body">{intro}{toc}{fragment}</div>'
        '</section></article><p class="study-back"><a href="/notes/">← 返回学习笔记</a></p>'
        '</div></main>'
    )
    page = page[:a] + body + page[b:]
    mathjax = (
        '<link rel="stylesheet" href="/css/study-note.css">'
        '<script>window.MathJax={tex:{inlineMath:[["\\\\(","\\\\)"]],'
        'displayMath:[["\\\\[","\\\\]"]],packages:{"[+]":['
        '"ams"]}},options:{enableMenu:false}};</script>'
        '<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>'
    )
    return page.replace("</head>", mathjax + "</head>", 1)


def main() -> None:
    fragment = prepare_math(make_fragment())
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(make_page(fragment), encoding="utf-8")
    print(f"Built {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
