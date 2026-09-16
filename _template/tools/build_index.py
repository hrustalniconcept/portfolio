#!/usr/bin/env python3
"""Пересобирает корневой index.html (статический список по категориям) и таблицу в README.md из projects.json.
Запуск из корня репозитория: python3 _template/tools/build_index.py"""
import json, re, html
d = json.load(open("projects.json", encoding="utf-8")); e = html.escape
n = 0; groups = []
for c in d["categories"]:
    items = [p for p in d["projects"] if p["category"] == c["id"]]
    rows = "".join(f'    <a class="item" href="{p["slug"]}/"><span class="n">{(n:=n+1):02d}</span><span><span class="t">{e(p["title"])}</span><div class="m">{p["year"]} · {e(p["meta"])}</div></span><span class="a">Смотреть →</span></a>\n' for p in items) \
        or '    <div class="item empty"><span class="n">—</span><span><span class="t">Первый проект раздела — скоро</span></span><span></span></div>\n'
    groups.append(f'  <section class="group" id="{c["id"]}"><h2 class="gh">{e(c["title"])}</h2><div class="list">\n{rows}  </div></section>\n')
s = open("index.html", encoding="utf-8").read()
s = re.sub(r'(<div class="groups" data-index>\n).*?(</div>\n<p class="cap">)', lambda m: m.group(1) + "".join(groups) + m.group(2), s, count=1, flags=re.S)
open("index.html", "w", encoding="utf-8").write(s)
r = open("README.md", encoding="utf-8").read()
table = "| Проект | Раздел | Папка | Адрес |\n|---|---|---|---|\n" + "".join(
    f'| {p["title"]} | {next(c["title"] for c in d["categories"] if c["id"]==p["category"])} | `{p["slug"]}/` | https://hrustalniconcept.github.io/portfolio/{p["slug"]}/ |\n' for p in d["projects"])
r = re.sub(r'\| Проект \|.*?\n(?=\n|Добавить)', table, r, count=1, flags=re.S)
open("README.md", "w", encoding="utf-8").write(r); print("index.html и README.md обновлены:", n, "проектов")
