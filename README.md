# Портфолио Концепт-бюро «Хрустальный»

Статические страницы проектов для GitHub Pages. Каждый проект — своя папка с `index.html` и `assets/`.

| Проект | Раздел | Папка | Адрес |
|---|---|---|---|
| Дом в сосновом бору | Индивидуальные дома | `dom-v-sosnovom-boru/` | https://hrustalniconcept.github.io/portfolio/dom-v-sosnovom-boru/ |
| Резиденция XV | Индивидуальные дома | `rezidencia-xv/` | https://hrustalniconcept.github.io/portfolio/rezidencia-xv/ |
| Посёлок у озера | Коттеджные посёлки | `poselok-u-ozera/` | https://hrustalniconcept.github.io/portfolio/poselok-u-ozera/ |
| Лесная резиденция | Коттеджные посёлки | `lesnaya-rezidenciya/` | https://hrustalniconcept.github.io/portfolio/lesnaya-rezidenciya/ |
| Посёлок в сосновом лесу | Коттеджные посёлки | `poselok-v-sosnovom-lesu/` | https://hrustalniconcept.github.io/portfolio/poselok-v-sosnovom-lesu/ |
| Посёлок на склоне | Коттеджные посёлки | `poselok-na-sklone/` | https://hrustalniconcept.github.io/portfolio/poselok-na-sklone/ |
| Хрустальный | Реализованные проекты | `hrustalnyj/` | https://hrustalniconcept.github.io/portfolio/hrustalnyj/ |
| Aura | Реализованные проекты | `aura/` | https://hrustalniconcept.github.io/portfolio/aura/ |
| Резиденция XV | Реализованные проекты | `rezidencia-xv-poselok/` | https://hrustalniconcept.github.io/portfolio/rezidencia-xv-poselok/ |
| Villet | Реализованные проекты | `villet/` | https://hrustalniconcept.github.io/portfolio/villet/ |
| Vila | Реализованные проекты | `vila/` | https://hrustalniconcept.github.io/portfolio/vila/ |
| EcoVille | Реализованные проекты | `ecoville/` | https://hrustalniconcept.github.io/portfolio/ecoville/ |
| Хрустальный парк | Реализованные проекты | `hrustalnyj-park/` | https://hrustalniconcept.github.io/portfolio/hrustalnyj-park/ |

Добавить проект: скопировать `_template/`, заменить ассеты и тексты, добавить запись в `projects.json` (slug, название, год, категория `houses` / `settlements`, meta, `cover` и `hover` — базовые пути кадров без суффикса, related), затем `python3 _template/tools/build_index.py` — корневой индекс и эта таблица пересоберутся. Меню (бургер) и блок «Другие проекты» на всех страницах строятся из `projects.json` скриптом `nav.js` — страницы править не нужно.


Реализованные проекты (категория `built`) собираются из `_template/realised.json` генератором `python3 _template/tools/build_realised.py <папка с исходными фото> [slug]` — тексты и фото взяты со страниц hrustalni.com. После правок данных: пересобрать страницу, затем `build_index.py`.
