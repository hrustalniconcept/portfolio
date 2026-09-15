# Промт-инструкция: горизонтальные кадры 16:9 для портфолио бюро
Версия 1.0 · 2026-09-15 · выведена на пилоте «Дом в сосновом бору»

Вставлять в начало сессии целиком. Ниже — что положить в папку, как работать, какие промты давать моделям и по какому чек-листу принимать. Всё, что здесь запрещено, уже стоило лишних генераций на пилоте.

---

## 0. Что мне нужно (одним абзацем)

Пять–семь горизонтальных кадров 16:9 в 4K для страницы портфолио: максимальный фотореализм «как живая съёмка» при **полном сохранении архитектуры и планировки**. Дом — тот же, что в исходных рендерах, до последнего окна. Кадры раскрывают сильные стороны именно этого дома. Если для дома уже сделан вертикальный ролик — все узлы (вход, витраж, терраса, камин) должны совпадать с принятыми вертикальными кадрами. На странице обязательна подпись «концепция · визуализация».

---

## 1. Папка проекта

```
<дом>/
  00_source/exterior/   рендеры фасадов (A фронт, B три четверти, C задний, D терраса, E вход)
  00_source/whitebox/   белые болванки интерьера (если есть)
  00_source/plan/       планировка
  00_source/approved_vertical/   принятые вертикальные стиллы ролика (если ролик был)
  06_portfolio/stills/  результат, 4K PNG, имена P01_front_approach.png …
  06_portfolio/rejected/
  _log.md
```

Ничего в `00_source/` не трогать. Каждая генерация — строка в `_log.md`: дата, кадр, модель, попытка, что поменяли, результат, кредиты.

---

## 2. Пайплайн (не менять порядок)

**Экстерьер, есть рендер нужного ракурса:**
1. `outpaint_image` исходника до 16:9 (дорисовка полей, здание не трогается).
2. `gpt_image_2_5`, 16:9, 2k, quality high, референс — результат шага 1. Промт из §4.1. Задача модели — **фотопасс, а не перекомпоновка**.
3. `upscale_image` (bytedance) до 4K.
4. Приёмка по §5. Не прошёл — правка точечным промтом «ONE change only» (§4.4), не перегенерация с нуля.

**Экстерьер, нужен ракурс, которого нет в рендерах:** сначала вертикальный/квадратный стилл по канону ролика (Nano Banana Pro с двумя референсами: ближайший рендер + принятый стилл), затем шаги 1–3. Такой кадр — отдельная приёмка, он самый рискованный.

**Интерьер:** `nano_banana_pro` или `gpt_image_2_5`, 16:9, два референса: болванка (геометрия) + принятый одетый стилл (материалы и мебель). Промт §4.2. Потом апскейл.

**Почему так.** Nano Banana Pro при переводе квадрата в 16:9 перекомпоновывает и «придумывает» другой дом (на пилоте: другой скат, другие окна). GPT Image 2.5 держит исходник, но хуже в фактуре — поэтому сначала дорисовка полей, потом фотопасс, потом апскейл за деталью.

**Не делать:** генерировать 16:9 напрямую из квадратного рендера; просить модель «улучшить» без перечисления, что именно; ставить ночь и сумерки (кадр уходит в черноту); оставлять машины из рендеров.

---

## 3. Список ракурсов (база — 5, расширение — до 8)

| № | Кадр | База | Что раскрывает | Свет |
|---|---|---|---|---|
| P01 | Фронтальный подъезд: вход, гараж, главный витраж | A | композиция объёмов | низкое солнце сбоку, длинные тени на подъезде |
| P02 | Три четверти против солнца: силуэт кровли | B | пластика кровли, лента верхнего света | контражур, естественный блик в кронах |
| P03 | Задний фасад сквозь стволы | C | приватность, природа у стекла | боковое вечернее солнце |
| P04 | Главный интерьер на витраж | W1 + одетый стилл | двусветный объём | боковое солнце, тени переплётов на полу |
| P05 | Терраса / очаг у стены | D | вечерняя жизнь | **золотой час** — солнце над горизонтом, небо светлое |
| P06 | Деталь: кромка кровли / стык материалов | E | материалы | косой свет |
| P07 | Второй интерьер (камин / кухня) | W2 + одетый стилл | ядро дома | тёплый вечерний |
| P08 | Дом-фонарь в сумерках | B/C | финал галереи | синий час, но окна и фасад читаются |

Порядок на странице: от общих к деталям, от дня к вечеру. Время суток внутри серии меняется только в одну сторону.

---

## 4. Промты

### 4.1 Экстерьер — фотопасс (GPT Image 2.5, референс = дорисованный до 16:9 исходник)

```
Edit this image so it looks like a real photograph taken on location, but DO NOT change anything about the building: same camera, same roof geometry and overhangs, same number, size and position of windows, same chimney, same volumes and proportions. Remove any car.
MATERIALS (name them exactly): [smooth dark-stained horizontal timber boards with fine straight grain — NOT charred, NOT shou sugi ban, no silver streaks] / [dark brick with mortar joints and slight irregularities] / [anthracite matte frames]. Transparent glass with warm interior visible and subtle sky reflections.
GROUND: [gravel with individual stones and dust, corten edging with real rust] / [uneven moss with brown patches, dry pine needles, dead twigs, dry grass tufts with seed heads, lichen on granite boulders — no uniform CG lawn]. Flaking bark on the trunks.
LIGHT: [low afternoon sun, long trunk shadows across the ground, warm patch on the wall] — true dynamic range, open shadows, soft haze between the trunks, faint lens vignetting, fine natural grain. Shot on a Sony A7R IV, [24mm tilt-shift | 35mm | 50mm], f/[5.6–8], ISO 100, RAW.
No HDR, no plastic CG smoothness, no oversaturated greens, no people, no text.
```

Квадратные скобки — заменить под материалы конкретного дома. Материалы называть точно: на пилоте «dark timber cladding» без уточнения превратилось в обожжённое дерево.

### 4.2 Интерьер (два референса: болванка + одетый стилл)

```
A real interior photograph, 16:9 horizontal.
GEOMETRY: exactly as in the first reference (the white-box render): same ceiling slope, same glazing pattern and mullions, same wall positions and room depth. Single storey, no mezzanine, no stairs.
DRESSING AND MATERIALS: exactly as in the second reference — [floor], [walls], [frames], [furniture and its placement по плану: e.g. the dining table for eight along the glass, three chairs each long side, one at each end; the island along the left wall; the fireplace on the right wall].
OUTSIDE THE GLASS: [real Siberian pine forest, trunks close to the glass, moss floor, muted greens. No birches].
Shot on a Sony A7R IV, 24mm tilt-shift, f/8, ISO 400, natural light only: low side sun, long mullion shadows across the floor, dust in the beam, gently blown highlights outside, wood grain and plaster texture visible, fine natural grain.
No HDR, no CG smoothness, no people, no text.
```

Расстановка мебели — только из планировки; ориентацию стола, острова, камина прописывать словами, не надеяться на референс (на пилоте стол дважды разворачивали).

### 4.3 Терраса / вечер

Всегда **golden hour**, не ночь:

```
… at golden hour — sun just above the horizon, sky still bright, everything clearly visible, NOT dark, NOT night. Warm low sun raking across the brick so the mortar joints read clearly; every window glowing warm from inside with the interior visible; a small wood fire in the fire bowl …
```

### 4.4 Точечная правка (когда кадр почти принят)

```
Edit the first image with ONE change only: make [the entrance / the roof edge / the window ribbon] identical to the [second image] — [перечислить элементы: anthracite steel portal frame around the recessed entrance, glazed door with a top light, two warm wall-washer lights, a wooden bench, a stack of firewood, a granite step with a corten edge, one dark bollard]. Keep everything else in the first image exactly the same: camera, roof geometry, glazing, cladding, ground, forest and light. Photographic, no HDR, no people, no text.
```

Так согласуются узлы между горизонталью и вертикалью. Второй референс — принятый вертикальный стилл того же узла.

### 4.5 Анимация для hero-блоков сайта (если нужна)

Стилл → `veo3_1` (8 с, фактура как съёмка, отдаёт 720p) → `upscale_video` Topaz 2160p. Промт: одно движение камеры, «smooth gimbal, no shake, the architecture stays rigid», звук — только ветер/огонь, без музыки. Kling 3.0 pro — дешевле вдвое, но текстуры глаже.

---

## 5. Приёмка (каждый кадр, до апскейла)

- [ ] Рядом с исходником: кровля, свесы, число и размер окон, дымоход, объёмы — совпадают.
- [ ] Материалы названы правильно и выглядят как названы (планкен ровный, кирпич со швами).
- [ ] Нет машин, людей, текста, лишних построек и проёмов.
- [ ] Узлы совпадают с принятыми вертикальными кадрами (вход, витраж, терраса).
- [ ] Интерьер: скат и переплёты по болванке, мебель по плану, этаж один, за стеклом — правильный лес.
- [ ] Свет: время суток видно, фасад и фактуры читаются (вечерние кадры не ушли в черноту).
- [ ] Земля живая: неровный мох, сухая трава, хвоя, лишайник, а не ровный газон.
- [ ] Нет HDR-свечения, «пластика», кислотной зелени.

Не прошёл один пункт — точечная правка §4.4. Не прошли два и больше — вернуться на шаг назад (дорисовка исходника), а не тянуть промтом.

---

## 6. Стоимость (Higgsfield, сентябрь 2026)

| Операция | Кредиты |
|---|---|
| Nano Banana Pro, стилл 2k/4k | 2 |
| GPT Image 2.5, 2k high | 3 |
| Outpaint исходника | ≈2 |
| Апскейл 4K (bytedance) | ≈2–3 |
| Kling 3.0 pro, 5 с со звуком | 12,5 |
| Veo 3.1, 8 с | 22 |
| Topaz 2160p | 5 |

Пять базовых кадров с правками — **≈40–60 кредитов**. Пакет с анимацией пяти hero-клипов — ещё ≈135. Смету показывать до запуска.

---

## 7. Что подчёркивать в подписях на странице

Не «дом 273 м²», а что в нём решено: моноскат и лента верхнего света; двусветный витраж в торце; дом прячется в бору — ни одного срубленного ствола; один этаж и три крыла — приватность спален; кухня в кармане, ядро на 82 м². Площади — только из экспликации проекта, не выдумывать.
