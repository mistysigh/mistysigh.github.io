#!/usr/bin/env python3
"""Refresh the learning-notes and life-record sections in the static site."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
MAIN_OPEN = '<main class="sidebar-translate" id="content">'
STYLESHEET = '<link rel="stylesheet" href="/css/study-note.css">'
NOTE_URL = '/notes/chebyshev-spectral-collocation/'
DIRECT_SOLVERS_URL = '/notes/numerical-analysis-direct-solvers/'
LEVEQUE_URL = '/notes/leveque-finite-difference/'
LIFE_URL = '/2025/02/16/%E4%B9%99%E5%B7%B3%E8%9B%87%E5%B9%B4%E6%98%A5%E8%8A%82/'


def replace_main(page: str, main: str) -> str:
    start = page.index(MAIN_OPEN)
    end = page.index('</main>', start) + len('</main>')
    return page[:start] + main + page[end:]


def add_stylesheet(page: str) -> str:
    if STYLESHEET not in page:
        page = page.replace('</head>', STYLESHEET + '</head>', 1)
    return page


def listing_page(title: str, icon: str, description: str, item: str, slug: str) -> str:
    page = (ROOT / 'archives/index.html').read_text(encoding='utf-8')
    page = page.replace('<title>Archive |', f'<title>{title} |', 1)
    page = page.replace('content="Archive"', f'content="{title}"', 1)
    page = page.replace('https://mistysigh.github.io/archives/index.html',
                        f'https://mistysigh.github.io/{slug}/', 1)
    page = page.replace('<html lang="en">', '<html lang="zh-CN">', 1)
    page = page.replace('<meta property="og:locale" content="en_US">',
                        '<meta property="og:locale" content="zh_CN">', 1)
    main = (
        f'{MAIN_OPEN}<div class="hty-card" id="page"><header class="post-header">'
        f'<h1 class="post-title"><span class="icon iconify" data-icon="{icon}"></span>{title}</h1>'
        f'</header><div class="study-note-list"><p>{description}</p>{item}</div></div></main>'
    )
    return add_stylesheet(replace_main(page, main))


def refresh_sidebar(page: str) -> str:
    for old, new_url, title, old_icon, new_icon in (
        ('categories', '/notes/', '学习笔记', 'ri:folder-2-line', 'ri:book-open-line'),
        ('tags', '/life/', '生活记录', 'ri:price-tag-3-line', 'ri:camera-line'),
    ):
        pattern = rf'<a href="/{old}/" title="[^"]+">.*?</a>'
        match = re.search(pattern, page, re.DOTALL)
        if match:
            anchor = match.group(0)
            anchor = re.sub(rf'href="/{old}/" title="[^"]+"',
                            f'href="{new_url}" title="{title}" aria-label="{title}"',
                            anchor, count=1)
            anchor = anchor.replace(f'data-icon="{old_icon}"', f'data-icon="{new_icon}"', 1)
            count = '3' if old == 'categories' else '1'
            anchor = re.sub(r'<span class="site-state-item-count">\d+</span>',
                            f'<span class="site-state-item-count">{count}</span>',
                            anchor, count=1)
            page = page[:match.start()] + anchor + page[match.end():]
    page = re.sub(
        r'(<a href="/notes/" title="学习笔记"[^>]*>.*?'
        r'<span class="site-state-item-count">)\d+(</span></a>)',
        r'\g<1>3\2', page, count=1, flags=re.DOTALL,
    )
    return page


def main() -> None:
    note_item = (
        '<article class="note-entry"><h2><a href="' + NOTE_URL + '">从零理解 Chebyshev 谱配置法</a></h2>'
        '<p>Lagrange 插值、谱微分矩阵、一维 Poisson 边值问题与 MATLAB 验证。</p>'
        '<p>按照“节点值 → 插值 → 求导 → 离散求解”的路线阅读；文内有目录、公式、代码和练习。</p>'
        '</article>'
        '<article class="note-entry"><h2><a href="' + DIRECT_SOLVERS_URL + '">从消元代码读懂线性方程组的直接解法</a></h2>'
        '<p>《数值分析基础》第二章：Gauss 消去、选主元、LU、Cholesky、追赶法、五点差分与条件数。</p>'
        '<p>以 MATLAB 代码串联公式、数组索引、可复算例题和误差诊断。</p>'
        '</article>'
        '<article class="note-entry"><h2><a href="' + LEVEQUE_URL + '">LeVeque 有限差分方法：前三章导读</a></h2>'
        '<p>从差分权重走向一维边值问题与二维椭圆方程，分三章推导截断误差、稳定性与收敛。</p>'
        '<p>以理论为主，补充边界层、高阶格式及稀疏线性代数的关键判断。</p>'
        '</article>'
    )
    life_item = (
        '<article class="note-entry"><h2><a href="' + LIFE_URL + '">乙巳蛇年春节记录[一]</a></h2>'
        '<p>2025-02-16 · 包饺子的家庭片段。</p></article>'
    )
    (ROOT / 'notes/index.html').parent.mkdir(exist_ok=True)
    (ROOT / 'life/index.html').parent.mkdir(exist_ok=True)
    (ROOT / 'notes/index.html').write_text(
        listing_page('学习笔记', 'ri:book-open-line',
                     '从基础问题出发，按推导、实现和验证整理可逐步阅读的学习手册。', note_item, 'notes'),
        encoding='utf-8',
    )
    (ROOT / 'life/index.html').write_text(
        listing_page('生活记录', 'ri:camera-line',
                     '生活记录集中放在这里，按时间浏览。', life_item, 'life'),
        encoding='utf-8',
    )

    home = (ROOT / 'index.html').read_text(encoding='utf-8')
    home_intro = (ROOT / 'content/home-intro.html').read_text(encoding='utf-8')
    home_main = (
        f'{MAIN_OPEN}{home_intro}'
        '<section class="hty-card study-section-card" aria-labelledby="home-notes">'
        '<header class="post-header"><h1 class="post-title" id="home-notes">'
        '<span class="icon iconify" data-icon="ri:book-open-line"></span>学习笔记</h1></header>'
        '<p>从公式的来处读起，走到可复算的数值实验。</p>'
        f'<ul><li><a href="{NOTE_URL}">从零理解 Chebyshev 谱配置法</a>：'
        'Lagrange 插值、微分矩阵与一维 Poisson 问题</li>'
        f'<li><a href="{DIRECT_SOLVERS_URL}">从消元代码读懂线性方程组的直接解法</a>：'
        '选主元、三角分解、稀疏系统与误差诊断</li>'
        f'<li><a href="{LEVEQUE_URL}">LeVeque 有限差分方法：前三章导读</a>：'
        '差分近似、一维边值问题和二维椭圆方程</li></ul>'
        '<p><a href="/notes/">查看学习笔记栏目 →</a></p></section>'
        '<section class="hty-card study-section-card" aria-labelledby="home-life">'
        '<header class="post-header"><h2 class="post-title" id="home-life">'
        '<span class="icon iconify" data-icon="ri:camera-line"></span>生活记录</h2></header>'
        '<p>日常片段集中在一个栏目。</p>'
        f'<ul><li><a href="{LIFE_URL}">乙巳蛇年春节记录[一]</a></li></ul>'
        '<p><a href="/life/">查看生活记录栏目 →</a></p></section>'
        '<p class="study-back"><a href="/archives/">浏览旧文章归档 →</a></p>'
        '</main>'
    )
    (ROOT / 'index.html').write_text(add_stylesheet(replace_main(home, home_main)), encoding='utf-8')

    categories = ROOT / 'categories/index.html'
    page = categories.read_text(encoding='utf-8')
    page = replace_main(page, (
        f'{MAIN_OPEN}<div class="hty-card" id="page"><header class="post-header">'
        '<h1 class="post-title">栏目</h1></header><div class="study-note-list">'
        '<p><a href="/notes/">学习笔记</a> · 3 篇</p>'
        '<p><a href="/life/">生活记录</a> · 1 篇</p>'
        '</div></div></main>'
    ))
    categories.write_text(add_stylesheet(page), encoding='utf-8')

    life_article = ROOT / '2025/02/16/乙巳蛇年春节/index.html'
    page = life_article.read_text(encoding='utf-8')
    page = page.replace('<div class="post-classify"></div>',
                        '<div class="post-classify"><a href="/life/">生活记录</a></div>', 1)
    life_article.write_text(page, encoding='utf-8')

    for path in ROOT.rglob('*.html'):
        if '.git' in path.parts:
            continue
        page = path.read_text(encoding='utf-8')
        refreshed = refresh_sidebar(page)
        if refreshed != page:
            path.write_text(refreshed, encoding='utf-8')
    print('Built study-note and life-record sections')


if __name__ == '__main__':
    main()
