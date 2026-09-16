# Портфолио Концепт-бюро «Хрустальный»

Статические страницы проектов для GitHub Pages. Каждый проект — своя папка с `index.html` и `assets/`.

| Проект | Раздел | Папка | Адрес |
|---|---|---|---|
| Дом в сосновом бору | Индивидуальные дома | `dom-v-sosnovom-boru/` | https://hrustalniconcept.github.io/portfolio/dom-v-sosnovom-boru/ |
| Резиденция XV | Индивидуальные дома | `rezidencia-xv/` | https://hrustalniconcept.github.io/portfolio/rezidencia-xv/ |
| Посёлок у озера | Коттеджные посёлки | `poselok-u-ozera/` | https://hrustalniconcept.github.io/portfolio/poselok-u-ozera/ |
| Посёлок на склоне | Коттеджные посёлки | `poselok-na-sklone/` | https://hrustalniconcept.github.io/portfolio/poselok-na-sklone/ |

Добавить проект: скопировать `_template/`, заменить ассеты и тексты, добавить запись в `projects.json` (slug, название, год, категория `houses` / `settlements`, meta, related), затем `python3 _template/tools/build_index.py` — корневой индекс и эта таблица пересоберутся. Меню (бургер) и блок «Другие проекты» на всех страницах строятся из `projects.json` скриптом `nav.js` — страницы править не нужно.
