#!/usr/bin/env python3
"""Собирает страницы реализованных проектов из _template/realised.json.
Для каждого проекта: <slug>/assets/ (WebP 800/1400/2400 + LQIP + og-jpg) и <slug>/index.html
в стиле страниц портфолио (общий CSS — _template/realised_base.css, снятый со страницы посёлка).
Запуск из корня: python3 _template/tools/build_realised.py <папка с исходными фото> [slug ...]
Реестр projects.json и корневой индекс не трогает — записи добавляются отдельно, затем build_index.py."""
import sys, os, json, io, base64, html
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = sys.argv[1]; only = sys.argv[2:]
data = json.load(open(f"{ROOT}/_template/realised.json", encoding="utf-8"))
BASE_CSS = open(f"{ROOT}/_template/realised_base.css", encoding="utf-8").read()
e = html.escape

PATHS = '<path d="M52.1687 68.9595L34.5 55.6875L16.8313 68.9595H0.121479L34.5 43.1347L68.8785 68.9595H52.1687Z"/><path d="M43.1347 34.5L68.9595 0.121479V16.8313L55.6875 34.5L68.9595 52.1687V68.8785L43.1347 34.5Z"/><path d="M16.8313 0.0404053L34.5 13.3124L52.1687 0.0404053H68.8785L34.5 25.8652L0.121479 0.0404053H16.8313Z"/><path d="M25.8652 34.5L0.0404053 68.8785V52.1687L13.3124 34.5L0.0404053 16.8313V0.121479L25.8652 34.5Z"/>'
LOGO = f'<svg viewBox="0 0 69 69" aria-hidden="true">{PATHS}</svg>'

EXTRA_CSS = """
/* realised — реализованный проект */
.hero .meta .lbl:first-child:empty{display:none}
.facts{grid-column:1/-1;margin-top:clamp(40px,6vh,72px)}
.facts .row{grid-template-columns:220px 1fr;align-items:baseline}
.facts .row span:last-child{color:var(--ink72);max-width:72ch}
.facts .row:first-child{border-top:1px solid var(--ink)}
@media(max-width:900px){.facts .row{grid-template-columns:1fr;gap:4px}}
.plan .doc.portrait{aspect-ratio:4/3}
.evening .g{background:linear-gradient(90deg,rgba(2,24,37,.78) 0%,rgba(2,24,37,.45) 45%,rgba(2,24,37,.05) 100%)}
.evening .t .txt{text-shadow:0 1px 14px rgba(0,0,0,.35)}
.quote{padding-block:var(--sec)}
.quote .q{grid-column:1/11;font:400 clamp(32px,4.2vw,68px)/1.02 var(--head);text-transform:uppercase;letter-spacing:-.01em;text-wrap:balance}
.quote .q::before{content:'«'}.quote .q::after{content:'»'}
.quote .who{grid-column:1/8;margin-top:28px;display:grid;gap:6px}
.quote .who b{font:400 22px/1 var(--head);text-transform:uppercase;letter-spacing:.02em}
@media(max-width:900px){.quote .q,.quote .who{grid-column:1/-1}}
.results .head{grid-column:1/8}
.results .zones{margin-top:clamp(40px,6vh,72px)}
.gallery .head{grid-column:1/7}
.gal{grid-column:1/-1;display:grid;grid-template-columns:repeat(6,1fr);gap:clamp(20px,3vw,48px) 24px;margin-top:clamp(40px,6vh,72px)}
.gal figure{margin:0;grid-column:span 3;overflow:hidden;position:relative;background:var(--stone)}
.gal figure.w{grid-column:span 6}
.gal figure img{width:100%;aspect-ratio:3/2;object-fit:cover;transform:scale(1.05);transition:transform 1.4s cubic-bezier(.2,.6,.2,1)}
.gal figure.w img{aspect-ratio:21/10}
.gal figure:hover img{transform:scale(1)}
.gal figcaption{padding:12px 0 0}
@media(max-width:900px){.gallery .head{grid-column:1/-1}.gal figure,.gal figure.w{grid-column:span 6}.gal figure.w img{aspect-ratio:3/2}}
"""

def build_assets(p, outdir):
    os.makedirs(outdir, exist_ok=True); lq = {}; names = []
    items = [(f"p{i+1:02d}", f, alt) for i, (f, alt) in enumerate(p["photos"])] + [(f"mp{i+1}", f, alt) for i, (f, alt, _) in enumerate(p.get("plans", []))]
    for name, f, _ in items:
        path = f"{src}/{f}"
        if not os.path.exists(path): sys.exit(f"нет файла {path}")
        im = Image.open(path).convert("RGB"); wide = im.width >= im.height
        for suf, w, q in [("_s", 800, 72), ("_m", 1400, 74), ("", 2400, 74)]:
            out = f"{outdir}/{name}{suf}.webp"
            if not os.path.exists(out):
                c = im.copy(); c.thumbnail((w, w if wide else int(w * 1.2)), Image.LANCZOS); c.save(out, "WEBP", quality=q, method=6)
        if name == "p01" and not os.path.exists(f"{outdir}/p01.jpg"):
            c = im.copy(); c.thumbnail((1600, 1600)); c.save(f"{outdir}/p01.jpg", "JPEG", quality=80)
        t = im.copy(); t.thumbnail((40, 40)); b = io.BytesIO(); t.save(b, "WEBP", quality=40)
        lq[name] = "data:image/webp;base64," + base64.b64encode(b.getvalue()).decode()
        names.append((name, im.width, im.height))
    return lq, dict((n, (w, h)) for n, w, h in names)

def img(name, alt, sizes, lazy=True, extra=""):
    return (f'<img data-lqip="{name}" {"data-src" if lazy else "src"}="assets/{name}.webp" {"data-srcset" if lazy else "srcset"}="assets/{name}_s.webp 800w, assets/{name}_m.webp 1400w, assets/{name}.webp 2400w" '
            f'sizes="{sizes}" alt="{e(alt)}"{" loading=lazy" if lazy else " fetchpriority=high"}{extra}>')

def img_eager(name, alt, sizes):
    return f'<img data-lqip="{name}" src="assets/{name}.webp" srcset="assets/{name}_s.webp 800w, assets/{name}_m.webp 1400w, assets/{name}.webp 2400w" sizes="{sizes}" alt="{e(alt)}" loading="lazy">'

def render(p, lq, dims, all_projects):
    photos = p["photos"]; n = len(photos)
    hero = [i for i in p["hero"] if 1 <= i <= n][:5] or [1]
    ev = p.get("evening", 1)
    is_photo = p.get("kind", "photo") == "photo"
    capword = ("реализация" + (f", {p['year']}" if p.get("year") else "")) if is_photo else "концепция · визуализация"
    plans = p.get("plans", [])
    year = p.get("year", "")
    place = p.get("place", "")
    meta2 = " · ".join(x for x in [p["type"], place] if x)
    caps = [photos[i-1][1] for i in hero]

    # hero
    slides = ""
    for k, i in enumerate(hero):
        name = f"p{i:02d}"; alt = photos[i-1][1]
        if k == 0:
            slides += f'<div class="sl on"><img data-lqip="{name}" src="assets/{name}.webp" srcset="assets/{name}_s.webp 800w, assets/{name}_m.webp 1400w, assets/{name}.webp 2400w" sizes="(max-width:900px) 100vw, 92vw" alt="{e(alt)}" fetchpriority="high"></div>'
        else:
            slides += f'<div class="sl">{img(name, alt, "(max-width:900px) 100vw, 92vw")}</div>'
    dots = "".join(f'<button{" class=on" if k == 0 else ""} type="button" aria-label="Кадр {k+1}"></button>' for k in range(len(hero)))
    counter = f'<div class="counter" data-line><div class="n"><span id="slnum">01</span><small>/ {len(hero):02d}</small></div><div class="dots" role="tablist" aria-label="Кадры">{dots}</div></div>' if len(hero) > 1 else ""
    slnav = '<button class="slnav prev" type="button" aria-label="Предыдущий кадр">←</button><button class="slnav next" type="button" aria-label="Следующий кадр">→</button><div class="slbar"><i></i></div>' if len(hero) > 1 else ""
    first_link = "#plan" if plans else "#facts"

    # metrics
    metrics = ""
    if p.get("metrics"):
        cells = "".join(f'<div class="metric"><div class="n">{e(v)}{f"<small>{e(u)}</small>" if u else ""}</div><div class="cap">{e(c)}</div></div>' for v, u, c in p["metrics"])
        metrics = f'<div class="metrics" data-stagger>{cells}</div>'

    facts = "".join(f'<div class="row"><span>{e(k)}</span><span>{e(v)}</span></div>' for k, v in p["facts"])

    # plan section
    plan_sec = ""
    if plans:
        w, h = dims["mp1"]; portrait = h > w * 0.9
        imgs = "".join(f'<img data-layer-img="mp{i+1}" class="{"on" if i == 0 else ""}" {"src" if i == 0 else "data-src"}="assets/mp{i+1}.webp" {"srcset" if i == 0 else "data-srcset"}="assets/mp{i+1}_s.webp 800w, assets/mp{i+1}_m.webp 1400w, assets/mp{i+1}.webp 2400w" sizes="92vw" alt="{e(alt)}" loading="lazy">' for i, (_, alt, _) in enumerate(plans))
        tog = ("".join(f'<button class="pill" type="button" data-layer="mp{i+1}" aria-pressed="{"true" if i == 0 else "false"}">{e(lbl)}</button>' for i, (_, _, lbl) in enumerate(plans))) if len(plans) > 1 else ""
        plan_sec = f'''<section class="sec plan stone" id="plan"><div class="wrap grid">
  <div class="head"><span class="lbl rv">Генплан</span><h2 class="h2 rv" style="margin-top:14px">Как устроен <em>посёлок</em></h2></div>
  <div class="tog rv">{tog}</div>
  <div class="doc rv{" portrait" if portrait else ""}" style="{"" if portrait else f"aspect-ratio:{w}/{h}"}">{imgs}<span class="cap" data-state-cap>{e(plans[0][2])}</span></div>
  <div class="facts rv" id="facts">{facts}</div>
</div></section>'''
    else:
        plan_sec = f'''<section class="sec plan stone" id="facts"><div class="wrap grid">
  <div class="head"><span class="lbl rv">Проект в фактах</span><h2 class="h2 rv" style="margin-top:14px">Участок, форматы, <em>ограничения</em></h2></div>
  <div class="facts rv">{facts}</div>
</div></section>'''

    # evening
    evn = f"p{ev:02d}"
    evening = f'''<section class="evening" id="challenge">
  <div class="bg" data-parallax>{img_eager(evn, photos[ev-1][1], "100vw")}</div>
  <div class="g"></div>
  <div class="t"><span class="lbl rv" style="color:rgba(255,255,255,.6)">С чем пришлось столкнуться</span><p class="txt rv" style="margin-top:18px;max-width:52ch;font-size:clamp(17px,1.4vw,21px);color:#fff">{e(p["challenge"])}</p></div>
</section>'''

    quote = f'''<section class="quote dark"><div class="wrap grid">
  <p class="q rv">{e(p["quote"])}</p>
  <div class="who rv"><b>Кристина Яковенко</b><span class="cap">сооснователь, продуктолог концепт-бюро «Хрустальный»</span></div>
</div></section>'''

    zones = "".join(f'<div class="zone"><div class="h3">{e(k)}</div><p class="txt">{e(v)}</p></div>' for k, v in p["results"])
    results = f'''<section class="sec results" id="results"><div class="wrap grid">
  <div class="head"><span class="lbl rv">Результаты</span><h2 class="h2 rv" style="margin-top:14px">Что <em>получилось</em></h2></div>
  <div class="zones" data-stagger>{zones}</div>
</div></section>'''

    # gallery — все кадры, кроме полноэкранного
    figs = ""
    k = 0
    for i, (f, alt) in enumerate(photos, 1):
        if i == ev and n > 1: continue
        wide = (k % 5 == 0)
        figs += f'<figure class="{"w" if wide else ""}">{img(f"p{i:02d}", alt, "(max-width:900px) 100vw, 46vw" if not wide else "92vw")}<figcaption class="cap">{e(alt)} · {e(capword)}</figcaption></figure>'
        k += 1
    gallery = f'''<section class="sec gallery stone" id="gallery"><div class="wrap grid">
  <div class="head"><span class="lbl rv">{"Фотографии" if is_photo else "Визуализации"}</span><h2 class="h2 rv" style="margin-top:14px">{"Как это <em>построено</em>" if is_photo else "Как это <em>задумано</em>"}</h2></div>
  <div class="gal" data-stagger>{figs}</div>
</div></section>''' if k else ""

    # other projects (static fallback; nav.js replaces)
    others = [q for q in all_projects if q["slug"] != p["slug"]][:2]
    more = "".join(f'<a class="mitem" href="../{q["slug"]}/"><span class="n">реализовано</span><span><span class="t">{e(q["title"])}</span><div class="cap">{e(q["index_meta"])}</div></span><span class="a">Смотреть →</span></a>' for q in others)

    nav_links = f'<a href="../">Портфолио</a><a href="{first_link}">{"Генплан" if plans else "Факты"}</a><a href="#gallery">{"Фото" if is_photo else "Кадры"}</a><a href="#results">Результаты</a>'
    foot_cap = "Фотографии построенного посёлка · реализация" if is_photo else "Все изображения на странице — концепция · визуализация"
    desc = p["description"].split(". ")[0].rstrip(".") + "."
    caps_js = json.dumps(caps, ensure_ascii=False)

    return f'''<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p["title"])}</title>
<meta name="description" content="{e(desc)} Концепт-бюро «Хрустальный»: реализованные проекты.">
<meta property="og:title" content="{e(p["title"])} — Концепт-бюро «Хрустальный»">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="assets/p01.jpg">
<meta property="og:type" content="article">
<link rel="preload" as="image" href="assets/p{hero[0]:02d}.webp" imagesrcset="assets/p{hero[0]:02d}_s.webp 800w, assets/p{hero[0]:02d}_m.webp 1400w, assets/p{hero[0]:02d}.webp 2400w" imagesizes="(max-width:900px) 100vw, 92vw">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
<style>
{BASE_CSS}{EXTRA_CSS}</style>

<header class="nav" id="nav">
  <a class="logo" href="../">{LOGO}Хрустальный</a>
  <nav class="links" aria-label="Разделы">{nav_links}</nav>
  <div class="right"><a href="#contact">Заявка</a><button class="burger" type="button" aria-label="Меню портфолио"><i></i><i></i><i></i></button></div>
</header>

<section class="hero" id="top">
  <div class="meta"><span class="lbl" data-line>{e(year) if year else "Реализовано"}</span><span class="lbl" data-line>{e(meta2)}</span></div>
  <h1 class="h1 title" data-line>{e(p["title"])}</h1>
  {counter}
  <a class="arrow see" href="{first_link}" data-line>Смотреть проект <i>→</i></a>
  <div class="photo" data-hero-photo{" data-slider" if len(hero) > 1 else ""}>
    {slides}
    {slnav}
    <span class="cap" id="slcap">{e(caps[0])} · {e(capword)}</span>
  </div>
</section>

<section class="sec thought" id="thought"><div class="wrap grid">
  <div class="head" style="grid-column:1/8"><h2 class="h2 rv">{p["thesis"]}</h2><div class="rule rv"></div><p class="txt rv">{e(p["description"])}</p></div>
  {metrics}
</div></section>

{plan_sec}

{evening}

{quote}

{results}

{gallery}

<section class="sec cta dark" id="contact"><div class="wrap grid">
  <div class="l">
    <h2 class="h2 rv">Есть участок и межевание? Покажем, <em>что на нём продавать</em></h2>
    <div class="rule rv"></div>
    <p class="txt rv">Пришлите кадастровую схему или просто границы участка. Мы сами девелоперы: считаем продукт так, как потом будем его продавать, а построенное обслуживает своя гарантийная служба.</p>
  </div>
  <form id="leadForm" novalidate class="rv">
    <div class="f"><label for="f-name">Имя</label><input id="f-name" name="name" type="text" autocomplete="name" placeholder="Как к вам обращаться"><span class="msg" aria-live="polite"></span></div>
    <div class="f"><label for="f-phone">Телефон</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="+7"><span class="msg" aria-live="polite"></span></div>
    <div><button class="btn" type="submit">Обсудить участок <span aria-hidden="true">→</span></button></div>
    <p class="consent">Нажимая кнопку, вы соглашаетесь с политикой обработки персональных данных.</p>
  </form>
</div></section>

<section class="sec more" id="more"><div class="wrap">
  <span class="word rv">Другие проекты</span>
  <div class="mlist rv" data-more>
    {more}
    <a class="mitem" href="../"><span class="n">→</span><span><span class="t">Всё портфолио</span><div class="cap">реализованные проекты, дома и посёлки бюро</div></span><span class="a"></span></a>
  </div>
</div></section>

<footer class="footer">
  <a class="logo" href="#top" style="display:flex;align-items:center;gap:10px;font:400 18px/1 var(--head);text-transform:uppercase;letter-spacing:.04em"><svg viewBox="0 0 69 69" style="width:22px;height:22px;fill:currentColor" aria-hidden="true">{PATHS}</svg>Хрустальный</a>
  <span class="cap">{foot_cap}</span>
  <span class="cap">hrustalni.com</span>
</footer>

<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script>
(function(){{
  const LQ={json.dumps(lq)};
  document.querySelectorAll('img[data-lqip]').forEach(im=>{{ const par=im.parentElement; par.style.backgroundImage=`url(${{LQ[im.dataset.lqip]}})`; par.style.backgroundSize='cover'; par.style.backgroundPosition='center'; im.classList.add('ld'); const done=()=>im.classList.add('in'); if(im.complete && im.naturalWidth) done(); else im.addEventListener('load',done,{{once:true}}); }});
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasGsap = typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined';
  const hydrateAll = root => root.querySelectorAll('img[data-src]').forEach(im=>{{ im.src=im.dataset.src; if(im.dataset.srcset) im.srcset=im.dataset.srcset; im.removeAttribute('data-src'); im.removeAttribute('data-srcset'); }});
  /* ленивые кадры галереи и полосы — по приближению */
  if ('IntersectionObserver' in window) {{ const io = new IntersectionObserver(es=>es.forEach(en=>{{ if(en.isIntersecting){{ hydrateAll(en.target); io.unobserve(en.target); }} }}),{{rootMargin:'600px 0px'}}); document.querySelectorAll('.gal figure,.evening,.plan .doc').forEach(el=>io.observe(el)); }} else hydrateAll(document);

  /* слои генплана */
  const layers = [...document.querySelectorAll('[data-layer-img]')], stateCap = document.querySelector('[data-state-cap]');
  const capOf = {json.dumps({f"mp{i+1}": lbl for i, (_, _, lbl) in enumerate(plans)}, ensure_ascii=False)};
  document.querySelectorAll('[data-layer]').forEach(b=>b.addEventListener('click',()=>{{ const k=b.dataset.layer;
    layers.forEach(im=>{{ if (im.dataset.src){{ im.src=im.dataset.src; im.srcset=im.dataset.srcset; im.removeAttribute('data-src'); }} im.classList.toggle('on', im.dataset.layerImg===k); }});
    document.querySelectorAll('[data-layer]').forEach(x=>x.setAttribute('aria-pressed', x===b)); if (stateCap) stateCap.textContent = capOf[k]||''; if (hasGsap) ScrollTrigger.refresh(); }}));

  /* hero slider */
  const sld = document.querySelector('[data-slider]');
  if (sld) {{
    const slides = [...sld.querySelectorAll('.sl')], dots = [...document.querySelectorAll('.hero .dots button')], num = document.getElementById('slnum'), cap = document.getElementById('slcap'), bar = sld.querySelector('.slbar i');
    const caps = {caps_js}, capword = {json.dumps(capword, ensure_ascii=False)};
    let i = 0, timer = null, paused = false;
    const show = k => {{ i = (k + slides.length) % slides.length; slides.forEach((x,j)=>x.classList.toggle('on', j===i)); dots.forEach((d,j)=>d.classList.toggle('on', j===i)); num.textContent = String(i+1).padStart(2,'0'); cap.textContent = caps[i] + ' · ' + capword; bar.classList.remove('run'); void bar.offsetWidth; bar.classList.add('run'); }};
    const start = () => {{ clearInterval(timer); timer = setInterval(()=>{{ if(!paused) show(i+1); }}, 6000); }};
    dots.forEach((d,j)=>d.addEventListener('click',()=>{{ show(j); start(); }}));
    sld.querySelector('.next').addEventListener('click',e=>{{ e.stopPropagation(); show(i+1); start(); }});
    sld.querySelector('.prev').addEventListener('click',e=>{{ e.stopPropagation(); show(i-1); start(); }});
    sld.addEventListener('click',()=>{{ show(i+1); start(); }});
    sld.addEventListener('mouseenter',()=>paused=true); sld.addEventListener('mouseleave',()=>paused=false);
    let tx=null; sld.addEventListener('touchstart',e=>tx=e.touches[0].clientX,{{passive:true}}); sld.addEventListener('touchend',e=>{{ if(tx===null) return; const dx=e.changedTouches[0].clientX-tx; if(Math.abs(dx)>40){{ show(dx<0?i+1:i-1); start(); }} tx=null; }});
    addEventListener('keydown',e=>{{ if(e.key==='ArrowRight'){{show(i+1);start();}} if(e.key==='ArrowLeft'){{show(i-1);start();}} }});
    setTimeout(()=>hydrateAll(sld), 1200);
    if (!reduced) {{ bar.classList.add('run'); start(); }}
  }}

  const form = document.getElementById('leadForm');
  form.addEventListener('submit', e=>{{ e.preventDefault(); let ok = true;
    const set = (inp,msg)=>{{ const f = inp.closest('.f'); f.classList.toggle('err', !!msg); f.querySelector('.msg').textContent = msg||''; if(msg) ok=false; }};
    set(form.name, form.name.value.trim().length<2 ? 'Напишите имя' : ''); set(form.phone, form.phone.value.replace(/\\D/g,'').length<10 ? 'Нужен номер из 10–11 цифр' : '');
    if(!ok) return; window.dataLayer = window.dataLayer || []; dataLayer.push({{event:'form_submit', form_id:'final'}});
    /* TODO: GETCOURSE_FORM_ACTION — fetch(url,{{method:'POST',body:new FormData(form)}}) */
    form.innerHTML = '<div class="success"><h2 class="h2">Спасибо. <em>Перезвоним</em> в течение рабочего дня</h2><div class="rule"></div><p class="txt">А пока пришлите кадастровую схему участка на почту бюро — так разговор начнётся с конкретики.</p></div>'; }});

  /* nav colour on photo / dark */
  const nav = document.getElementById('nav');
  const darks = [...document.querySelectorAll('.dark,.evening')];
  const upd = ()=>{{ const on = darks.some(b=>{{ const r=b.getBoundingClientRect(); return r.top<=40 && r.bottom>40; }}); nav.classList.toggle('onphoto', on); }};
  addEventListener('scroll', upd, {{passive:true}}); upd();

  if (reduced || !hasGsap) return;
  gsap.registerPlugin(ScrollTrigger);
  ScrollTrigger.config({{ ignoreMobileResize: true }});
  addEventListener('load', ()=>ScrollTrigger.refresh());
  document.querySelectorAll('img').forEach(im=>im.addEventListener('load', ()=>ScrollTrigger.refresh(), {{once:true}}));
  document.querySelectorAll('a[href^="#"]').forEach(a=>a.addEventListener('click',e=>{{ const t=document.querySelector(a.getAttribute('href')); if(t){{ e.preventDefault(); window.scrollTo({{top: t.getBoundingClientRect().top + scrollY - 10, behavior:'smooth'}}); }} }}));
  gsap.from('.hero [data-line]', {{ y: 30, opacity: 0, duration: 1.2, stagger: 0.1, ease: 'power3.out', delay: 0.2 }});
  gsap.from('[data-hero-photo]', {{ clipPath: 'inset(0 0 100% 0)', duration: 1.6, ease: 'power3.inOut', delay: 0.5, clearProps: 'clipPath' }});
  gsap.to('[data-hero-photo] .sl', {{ yPercent: 8, ease: 'none', scrollTrigger: {{ trigger: '.hero', start: 'top top', end: 'bottom top', scrub: 0.6 }} }});
  gsap.utils.toArray('.rv').forEach(el => gsap.from(el, {{ y: 22, opacity: 0, duration: 1.1, ease: 'power2.out', scrollTrigger: {{ trigger: el, start: 'top 90%', once: true }} }}));
  gsap.utils.toArray('[data-stagger]').forEach(g => gsap.from(g.children, {{ y: 22, opacity: 0, duration: 1.0, stagger: 0.14, ease: 'power2.out', scrollTrigger: {{ trigger: g, start: 'top 85%', once: true }} }}));
  gsap.utils.toArray('[data-parallax]').forEach(el => gsap.fromTo(el, {{ yPercent: -6 }}, {{ yPercent: 6, ease: 'none', scrollTrigger: {{ trigger: el.parentElement, scrub: 0.6, start: 'top bottom', end: 'bottom top' }} }}));
}})();
</script>
<script src="../nav.js?v=20260916b" data-slug="{p["slug"]}" defer></script>
'''

for p in data["projects"]:
    if only and p["slug"] not in only: continue
    outdir = f"{ROOT}/{p['slug']}"
    lq, dims = build_assets(p, f"{outdir}/assets")
    open(f"{outdir}/index.html", "w", encoding="utf-8").write(render(p, lq, dims, data["projects"]))
    print(p["slug"], "—", len(p["photos"]), "фото,", len(p.get("plans", [])), "схем →", f"{p['slug']}/index.html")
