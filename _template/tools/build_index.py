#!/usr/bin/env python3
"""Пересобирает корневой index.html (список по категориям с кадрами cover/hover из реестра) и таблицу в README.md из projects.json.
Запуск из корня репозитория: python3 _template/tools/build_index.py"""
import json, re, html
d = json.load(open("projects.json", encoding="utf-8")); e = html.escape
n = 0; groups = []
for c in d["categories"]:
    items = [p for p in d["projects"] if p["category"] == c["id"]]
    def row(p):
        c, h = p["cover"], p.get("hover") or p["cover"]
        ph = (f'<span class="ph"><img src="{c}_s.webp" srcset="{c}_s.webp 800w, {c}_m.webp 1400w" sizes="(max-width:640px) 34vw, 16vw" alt="" loading="lazy" decoding="async">'
              f'<img class="b" src="{h}_s.webp" alt="" loading="lazy" decoding="async"></span>')
        return f'    <a class="item rv" href="{p["slug"]}/"><span class="n">{n:02d}</span>{ph}<span><span class="t">{e(p["title"])}</span><div class="m">{p["year"]} · {e(p["meta"])}</div></span><span class="a">Смотреть <i>→</i></span></a>\n'
    rows = ""
    for p in items: n += 1; rows += row(p)
    rows = rows or '    <div class="item empty"><span class="n">—</span><span class="ph"></span><span><span class="t">Первый проект раздела — скоро</span></span><span></span></div>\n'
    cnt = len(items); word = "проект" if cnt % 10 == 1 and cnt % 100 != 11 else "проекта" if 2 <= cnt % 10 <= 4 and not 12 <= cnt % 100 <= 14 else "проектов"
    groups.append(f'  <section class="group" id="{c["id"]}"><h2 class="gh"><span>{e(c["title"])}</span><small>{cnt} {word}</small></h2><div class="list">\n{rows}  </div></section>\n')
s = open("index.html", encoding="utf-8").read()
s = re.sub(r'(<div class="groups" data-index>\n).*?(</div>\n<p class="cap">)', lambda m: m.group(1) + "".join(groups) + m.group(2), s, count=1, flags=re.S)
open("index.html", "w", encoding="utf-8").write(s)
r = open("README.md", encoding="utf-8").read()
table = "| Проект | Раздел | Папка | Адрес |\n|---|---|---|---|\n" + "".join(
    f'| {p["title"]} | {next(c["title"] for c in d["categories"] if c["id"]==p["category"])} | `{p["slug"]}/` | https://hrustalniconcept.github.io/portfolio/{p["slug"]}/ |\n' for p in d["projects"])
r = re.sub(r'\| Проект \|.*?\n(?=\n|Добавить)', table, r, count=1, flags=re.S)
open("README.md", "w", encoding="utf-8").write(r); print("index.html и README.md обновлены:", n, "проектов")
