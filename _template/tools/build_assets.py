#!/usr/bin/env python3
"""Готовит ассеты страницы: WebP в трёх размерах (800/1400/2400) + LQIP-заглушки.
Вход: папка с PNG/JPG мастерами (имена файлов = имена ассетов, латиница, напр. p01_front.png).
Выход: assets/<name>_s.webp, <name>_m.webp, <name>.webp и lqip.json (data-URI 40px).
Запуск: python3 tools/build_assets.py <папка_мастеров> <папка_assets>"""
import sys, os, glob, io, base64, json
from PIL import Image
src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True); lq = {}
for f in sorted(glob.glob(f"{src}/*.png") + glob.glob(f"{src}/*.jpg")):
    name = os.path.splitext(os.path.basename(f))[0]; im = Image.open(f).convert("RGB"); wide = im.width >= im.height
    for suf, w, q in [("_s", 800, 72), ("_m", 1400, 74), ("", 2400, 74)]:
        c = im.copy(); c.thumbnail((w, w if wide else int(w * 1.2)), Image.LANCZOS); c.save(f"{out}/{name}{suf}.webp", "WEBP", quality=q, method=6)
    t = im.copy(); t.thumbnail((40, 40)); b = io.BytesIO(); t.save(b, "WEBP", quality=40)
    lq[name] = "data:image/webp;base64," + base64.b64encode(b.getvalue()).decode()
    print(name, [os.path.getsize(f"{out}/{name}{s}.webp") // 1024 for s in ("_s", "_m", "")], "KB")
json.dump(lq, open(f"{out}/../lqip.json", "w")); print("lqip.json — вставить в index.html как const LQ={...}")
