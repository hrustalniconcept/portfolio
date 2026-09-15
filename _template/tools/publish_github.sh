#!/usr/bin/env bash
# Публикация страницы проекта в hrustalniconcept/portfolio (GitHub Pages).
# Использование: bash tools/publish_github.sh <slug> <папка_сайта_с_index.html_и_assets>
# Нужен .env рядом со скриптом или в корне проекта: GITHUB_TOKEN=... (Contents: Read and write)
set -e
SLUG="$1"; SITE="$2"; [ -n "$SLUG" ] && [ -d "$SITE" ] || { echo "usage: publish_github.sh <slug> <site_dir>"; exit 1; }
[ -f .env ] && source .env; [ -n "$GITHUB_TOKEN" ] || { echo "нет GITHUB_TOKEN"; exit 1; }
REPO=hrustalniconcept/portfolio; W=$(mktemp -d)
git clone -q "https://x-access-token:${GITHUB_TOKEN}@github.com/${REPO}.git" "$W"
mkdir -p "$W/$SLUG"; rm -rf "$W/$SLUG/assets"; cp -R "$SITE/index.html" "$SITE/assets" "$W/$SLUG/"; find "$W" -name .DS_Store -delete
cd "$W" && git config user.name "Hrustalniconcept" && git config user.email "hrustalni.concept@gmail.com"
git add -A && (git commit -q -m "$SLUG: страница и ассеты" || true) && git push -q origin main
echo "https://hrustalniconcept.github.io/portfolio/${SLUG}/"
echo "Не забыть: добавить строку проекта в корневой index.html и README.md репозитория."
