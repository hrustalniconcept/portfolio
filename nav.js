/* Общее меню портфолио. Подключается на каждой странице проекта: <script src="../nav.js" data-slug="<slug>" defer></script>
   и на корневом индексе: <script src="nav.js" defer></script>.
   Читает projects.json (реестр проектов), строит: бургер-меню (полноэкранная тёмно-синяя панель, проекты по категориям),
   блок «Другие проекты» ([data-more]) — соседи по категории, связанные проекты (дом ↔ посёлок) и ссылка на всё портфолио.
   Стили инжектируются здесь, чтобы страницы не редактировать. Bebas Neue / Inter, цвета JSON 2.1. */
(function () {
  const me = document.currentScript, slug = me.dataset.slug || '', root = me.getAttribute('src').replace(/nav\.js.*$/, '');
  const css = `
.nav .burger{cursor:pointer;background:none;border:0;padding:0;color:inherit}
.pmenu{position:fixed;inset:0;z-index:60;background:linear-gradient(160deg,#072F50,#021825);color:#fff;padding:clamp(24px,6vw,96px);display:grid;grid-template-rows:auto 1fr auto;opacity:0;visibility:hidden;transition:opacity .5s,visibility 0s .5s;overflow:auto;font:400 13px/1.5 Inter,Arial,sans-serif}
.pmenu.open{opacity:1;visibility:visible;transition:opacity .5s}
.pmenu .top{display:flex;justify-content:space-between;align-items:center}
.pmenu .logo{display:flex;align-items:center;gap:10px;font:400 18px/1 'Bebas Neue',Impact,sans-serif;letter-spacing:.04em;text-transform:uppercase;color:inherit;text-decoration:none}
.pmenu .logo svg{width:26px;height:26px;fill:currentColor}
.pmenu .close{background:none;border:0;color:inherit;font:400 13px/1 Inter,Arial,sans-serif;cursor:pointer;display:flex;gap:10px;align-items:center}
.pmenu .close i{display:block;width:22px;height:1px;background:currentColor;transform:rotate(45deg);position:relative}
.pmenu .close i:after{content:"";position:absolute;inset:0;background:currentColor;transform:rotate(90deg)}
.pmenu .cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:48px clamp(24px,4vw,64px);align-content:center;padding:6vh 0}
.pmenu .lbl{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,.55);display:block;margin-bottom:18px}
.pmenu .pl{display:grid;gap:14px}
.pmenu .pl a{color:inherit;text-decoration:none;font:400 clamp(28px,3.4vw,48px)/1 'Bebas Neue',Impact,sans-serif;text-transform:uppercase;display:flex;gap:16px;align-items:baseline;transition:transform .3s}
.pmenu .pl a:hover,.pmenu .pl a.cur{transform:translateX(6px)}
.pmenu .pl a.cur{text-decoration:underline;text-underline-offset:8px;text-decoration-thickness:1px}
.pmenu .pl small{font:400 12px/1 Inter,Arial,sans-serif;color:rgba(255,255,255,.55);text-transform:none}
.pmenu .pl .all{font-size:clamp(20px,2vw,26px);margin-top:10px;color:rgba(255,255,255,.75)}
.pmenu .bottom{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;border-top:1px solid rgba(255,255,255,.25);padding-top:20px}
.pmenu .bottom a{color:inherit;text-decoration:none}
.pmenu .bottom a:hover{text-decoration:underline;text-underline-offset:6px}
body.menu-open{overflow:hidden}
.pmenu .serv{display:flex;gap:6px 18px;flex-wrap:wrap;color:rgba(255,255,255,.75)}
.pmenu .serv span{color:rgba(255,255,255,.45)}
.footer .serv{display:flex;gap:6px 14px;flex-wrap:wrap;font:400 12px/1.5 Inter,Arial,sans-serif;color:#8A8A8A;width:100%;margin-top:8px}
.footer .serv a:hover,.pmenu .serv a:hover{text-decoration:underline;text-underline-offset:4px}
.more .lbl.rel{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#8A8A8A;margin:36px 0 0}
`;
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  /* Bebas Neue с кириллицей лежит на корневом сайте (у Google-версии кириллицы нет); на localhost портфолио может жить отдельно, тогда шрифт просто не подхватится */
  const ff = document.createElement('style'); ff.textContent = "@font-face{font-family:'Bebas Neue';font-weight:400 700;font-style:normal;font-display:swap;src:url(/assets/fonts/BebasNeue-Bold.woff2) format('woff2')}"; document.head.appendChild(ff);
  const LOGO = '<svg viewBox="0 0 69 69" aria-hidden="true"><path d="M52.1687 68.9595L34.5 55.6875L16.8313 68.9595H0.121479L34.5 43.1347L68.8785 68.9595H52.1687Z"/><path d="M43.1347 34.5L68.9595 0.121479V16.8313L55.6875 34.5L68.9595 52.1687V68.8785L43.1347 34.5Z"/><path d="M16.8313 0.0404053L34.5 13.3124L52.1687 0.0404053H68.8785L34.5 25.8652L0.121479 0.0404053H16.8313Z"/><path d="M25.8652 34.5L0.0404053 68.8785V52.1687L13.3124 34.5L0.0404053 16.8313V0.121479L25.8652 34.5Z"/></svg>';
  const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const href = p => root + p.slug + '/';

  const loadServices = site => fetch((site.root || '/') + 'services.json', {cache: 'no-cache'}).then(r => r.ok ? r.json() : null).catch(() => null);
  fetch(root + 'projects.json', {cache: 'no-cache'}).then(r => r.json()).then(data => loadServices(data.site).then(reg => {
    if (reg && reg.services) { data.site.services = reg.services.filter(x => !x.side).map(x => ({title: x.title, url: x.url, price: x.price})).concat([{title: 'Все услуги', url: reg.site.services}]); data.site.registry_loaded = true; }
    return data;
  })).then(data => {
    const cats = data.categories, projects = data.projects;
    const siteRoot = data.site.root || '/', svcUrl = data.site.services_url || '/uslugi/';
    /* ---- единая шапка: логотип ведёт на главную сайта, первая ссылка — Услуги ---- */
    document.querySelectorAll('.nav .logo, .footer .logo').forEach(a => { a.setAttribute('href', siteRoot); });
    document.querySelectorAll('.nav .links').forEach(nav => {
      if (!nav.querySelector('a[href="' + svcUrl + '"]')) { const a = document.createElement('a'); a.href = svcUrl; a.textContent = 'Услуги'; nav.prepend(a); }
      if (!slug && !nav.querySelector('a[href="' + root + '"]')) { const a = document.createElement('a'); a.href = root || './'; a.textContent = 'Портфолио'; nav.insertBefore(a, nav.children[1] || null); }
      nav.querySelectorAll('a[href^="https://hrustalni.com"]').forEach(a => a.remove());
    });
    const byCat = id => projects.filter(p => p.category === id);
    const cur = projects.find(p => p.slug === slug);

    /* ---- бургер-меню ---- */
    const menu = document.createElement('div'); menu.className = 'pmenu'; menu.setAttribute('role', 'dialog'); menu.setAttribute('aria-label', 'Меню портфолио');
    menu.innerHTML = `<div class="top"><a class="logo" href="${root}">${LOGO}Хрустальный</a><button class="close" type="button" aria-label="Закрыть меню">закрыть <i></i></button></div>
      <div class="cols"><div><span class="lbl">Услуги бюро</span><div class="pl">${(data.site.services||[]).filter(x => x.title !== 'Все услуги').map(x => `<a href="${x.url}">${esc(x.title)}${x.price ? `<small>${esc(x.price)}</small>` : ''}</a>`).join('')}<a class="all" href="${svcUrl}">все услуги →</a></div></div>${cats.map(c => { const list = byCat(c.id); return `<div><span class="lbl">${esc(c.title)}</span><div class="pl">${
        list.length ? list.map(p => `<a href="${href(p)}"${p.slug === slug ? ' class="cur" aria-current="page"' : ''}>${esc(p.title)}${p.year ? `<small>${p.year}</small>` : ''}</a>`).join('') : `<a class="all" href="${root}#${c.id}">скоро</a>`
      }${list.length ? `<a class="all" href="${root}#${c.id}">все ${esc(c.short.toLowerCase())} →</a>` : ''}</div></div>`; }).join('')}</div>
      <div class="bottom"><a href="${siteRoot}">Главная</a><a href="${root}">Всё портфолио</a><a href="${data.site.request}">Заявка</a><a href="${data.site.home}">hrustalni.com</a></div>`;
    document.body.appendChild(menu);
    const open = () => { menu.classList.add('open'); document.body.classList.add('menu-open'); };
    const close = () => { menu.classList.remove('open'); document.body.classList.remove('menu-open'); };
    menu.querySelector('.close').addEventListener('click', close);
    menu.querySelectorAll('a').forEach(a => a.addEventListener('click', e => { if (a.getAttribute('href').startsWith('#')) close(); }));
    addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
    document.querySelectorAll('.burger').forEach(b => { b.removeAttribute('aria-hidden'); b.setAttribute('role', 'button'); b.setAttribute('tabindex', '0'); b.setAttribute('aria-label', 'Меню портфолио'); b.addEventListener('click', open); b.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } }); });

    /* ---- подвал: hrustalni.com ссылкой + услуги бюро ---- */
    const foot = document.querySelector('.footer');
    if (foot && (data.site.services||[]).length) {
      foot.querySelectorAll('.cap').forEach(c => { if (c.textContent.trim() === 'hrustalni.com' && c.tagName !== 'A') { const a = document.createElement('a'); a.className = 'cap'; a.href = data.site.home; a.textContent = 'hrustalni.com'; c.replaceWith(a); } });
      let sv = foot.querySelector('.serv'); if (!sv) { sv = document.createElement('div'); sv.className = 'serv'; foot.appendChild(sv); }
      sv.innerHTML = '<span>Услуги бюро:</span>' + data.site.services.map(s => `<a href="${s.url}">${esc(s.title)}</a>`).join('');
    }

    /* ---- «Другие проекты» на странице проекта ---- */
    const more = document.querySelector('[data-more]');
    if (more && cur) {
      const same = byCat(cur.category), i = same.indexOf(cur);
      const next = same[(i + 1) % same.length], prev = same[(i - 1 + same.length) % same.length];
      const rel = (cur.related || []).map(s => projects.find(p => p.slug === s)).filter(Boolean);
      const seen = new Set([cur.slug]); const rows = [];
      const push = (p, n) => { if (p && !seen.has(p.slug)) { seen.add(p.slug); rows.push({p, n}); } };
      rel.forEach(p => push(p, cats.find(c => c.id === p.category).short));
      push(next, 'следующий'); push(prev, 'предыдущий');
      const item = (p, n) => `<a class="mitem" href="${href(p)}"><span class="n">${esc(n)}</span><span><span class="t">${esc(p.title)}</span><div class="cap">${p.year ? p.year + ' · ' : ''}${esc(p.meta)}</div></span><span class="a">Смотреть →</span></a>`;
      more.innerHTML = rows.map(r => item(r.p, r.n)).join('') +
        `<a class="mitem" href="${root}"><span class="n">→</span><span><span class="t">Всё портфолио</span><div class="cap">${cats.map(c => esc(c.title.toLowerCase())).join(' · ')}</div></span><span class="a"></span></a>` +
        `<a class="mitem" href="${svcUrl}"><span class="n">→</span><span><span class="t">Услуги бюро</span><div class="cap">${(data.site.services||[]).filter(x => x.title !== 'Все услуги').map(x => esc(x.title.toLowerCase())).join(' · ')}</div></span><span class="a"></span></a>`;
    }

    /* ---- корневой индекс: строки с кадром cover и вторым кадром hover (та же разметка, что у build_index.py).
       Перерисовывается только если статический список отстал от реестра; подключать как nav.js?v=<дата>, чтобы браузер не держал старую версию ---- */
    const idx = document.querySelector('[data-index]');
    const stale = idx && [...idx.querySelectorAll('a.item')].map(a => a.getAttribute('href')).join() !== projects.map(href).join();
    if (idx && stale) {
      let n = 0;
      const plural = (k, w) => k + ' ' + (k % 10 === 1 && k % 100 !== 11 ? w[0] : k % 10 >= 2 && k % 10 <= 4 && (k % 100 < 12 || k % 100 > 14) ? w[1] : w[2]);
      const ph = p => { const c = root + p.cover, h = root + (p.hover || p.cover); return `<span class="ph"><img src="${c}_s.webp" srcset="${c}_s.webp 800w, ${c}_m.webp 1400w" sizes="(max-width:640px) 34vw, 16vw" alt="" loading="lazy" decoding="async"><img class="b" src="${h}_s.webp" alt="" loading="lazy" decoding="async"></span>`; };
      idx.innerHTML = cats.map(c => { const list = byCat(c.id); return `<section class="group" id="${c.id}"><h2 class="gh"><span>${esc(c.title)}</span><small>${plural(list.length, ['проект', 'проекта', 'проектов'])}</small></h2><div class="list">${
        list.length ? list.map(p => `<a class="item rv" href="${href(p)}"><span class="n">${String(++n).padStart(2, '0')}</span>${ph(p)}<span><span class="t">${esc(p.title)}</span><div class="m">${p.year ? p.year + ' · ' : ''}${esc(p.meta)}</div></span><span class="a">Смотреть <i>→</i></span></a>`).join('')
        : `<div class="item empty"><span class="n">—</span><span class="ph"></span><span><span class="t">Первый проект раздела — скоро</span></span><span></span></div>`}</div></section>`; }).join('');
    }
  }).catch(() => {});
})();
