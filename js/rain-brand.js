/* 雨落成海 — progressive homepage enhancement; preserves every original article URL. */
(()=>{
 function mount(){
  const main=document.querySelector('body.is-home main#content');
  if(!main||main.querySelector('.rain-header'))return;
  const header=document.createElement('header');header.className='rain-header';
  header.innerHTML='<a class="rain-brand" href="/" aria-label="雨落成海，返回首页"><img class="rain-brand-icon" src="/images/rain-to-sea-logo.svg" alt="" width="62" height="62"><img class="rain-brand-title" src="/images/rain-calligraphy.svg" alt="雨落成海" width="151" height="40"><img class="rain-brand-seal" src="/images/rain-dragon-seal.svg" alt="草书龙字印章" width="29" height="36"><img class="rain-brand-signature" src="/images/rain-signature.svg" alt="Misty Sigh" width="118" height="31"></a><nav class="rain-nav" id="rain-primary-nav" aria-label="主导航"><a href="/" aria-current="page">首页</a><a href="/notes/">学术笔记</a><a href="/life/">日常生活</a><a href="/archives/">文章归档</a><a href="/about/">关于我</a></nav><div class="rain-controls"><button type="button" class="rain-search-toggle" aria-label="搜索本页文章" aria-expanded="false" aria-controls="rain-search">⌕</button><button type="button" class="rain-mode-toggle" aria-label="切换深浅色模式">◐</button><button type="button" class="rain-menu-toggle" aria-label="展开导航菜单" aria-expanded="false" aria-controls="rain-primary-nav">☰</button></div>';
  main.prepend(header);
  const hero=document.createElement('section');hero.className='rain-hero';hero.setAttribute('aria-label','欢迎来到雨落成海');
  hero.innerHTML='<span class="rain-hero-kicker">RESEARCH · NOTES · EVERYDAY LIFE</span><h1>在研究、学习与日常之间，<br>记录思考，整理知识，分享生活。</h1><p>心与行并，渐行渐远，且慢且慢。</p><div class="rain-hero-actions"><a href="/notes/">开始阅读　↗</a><a href="/life/">生活随笔　↗</a></div>';
  header.after(hero);
  const sections=[...main.querySelectorAll('.study-section-card')];
  if(!sections.length)return;
  const discover=document.createElement('section');discover.className='rain-discover';discover.id='rain-discover';discover.setAttribute('aria-label','阅读与记录');
  discover.innerHTML='<div class="rain-discover-head"><div><h2>阅读与记录</h2><span class="rain-discover-note">在数字与文字之间，收藏值得回望的片刻。</span></div><div class="rain-filter" role="group" aria-label="文章分类"><button type="button" data-rain-filter="all" aria-pressed="true">全部</button><button type="button" data-rain-filter="notes" aria-pressed="false">学术笔记</button><button type="button" data-rain-filter="life" aria-pressed="false">日常生活</button></div></div><input id="rain-search" class="rain-search" type="search" placeholder="搜索首页文章标题与摘要" aria-label="搜索首页文章" hidden><div class="rain-articles"></div><p class="rain-empty" hidden>没有找到匹配的文章。</p>';
  sections[0].before(discover);
  const grid=discover.querySelector('.rain-articles');
  sections.forEach((s,i)=>{s.dataset.rainCategory=i===0?'notes':'life';grid.append(s)});
  const input=discover.querySelector('input'),empty=discover.querySelector('.rain-empty');let current='all';
  function filter(){const query=input.value.trim().toLocaleLowerCase();let shown=0;
   for(const s of sections){const group=current==='all'||s.dataset.rainCategory===current;const lis=[...s.querySelectorAll('li')];let matches=0;
    for(const li of lis){const ok=!query||li.textContent.toLocaleLowerCase().includes(query);li.hidden=!ok;if(ok)matches++}
    s.hidden=!group||(query!==''&&matches===0);if(!s.hidden)shown++;
   }empty.hidden=shown>0;
  }
  discover.querySelectorAll('[data-rain-filter]').forEach(b=>b.addEventListener('click',()=>{current=b.dataset.rainFilter;discover.querySelectorAll('[data-rain-filter]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));filter()}));
  input.addEventListener('input',filter);
  header.querySelector('.rain-search-toggle').addEventListener('click',e=>{input.hidden=!input.hidden;e.currentTarget.setAttribute('aria-expanded',String(!input.hidden));if(input.hidden){input.value='';filter()}else{input.focus();discover.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth',block:'start'})}});
  header.querySelector('.rain-menu-toggle').addEventListener('click',e=>{const nav=header.querySelector('.rain-nav'),open=nav.dataset.open!=='true';nav.dataset.open=String(open);e.currentTarget.setAttribute('aria-expanded',String(open))});
  header.querySelector('.rain-mode-toggle').addEventListener('click',()=>{const yun=document.querySelector('#toggle-mode-btn');if(yun){yun.click()}else{const dark=document.documentElement.classList.toggle('dark');try{localStorage.setItem('darken-mode',dark?'dark':'light')}catch(_){}}});
  filter();
 }
 document.addEventListener('DOMContentLoaded',mount);
 document.addEventListener('pjax:success',mount);
 if(document.readyState!=='loading')mount();
})();