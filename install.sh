#!/usr/bin/env bash
# Install the separately cloned Arquibancada themes into Omarchy.
#
#   ./install.sh --source ../omarchy-arquibancada-theme --link --menu
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE=""
CONFIG_DIR="$HOME/.config/omarchy"
CACHE_ROOT="${XDG_CACHE_HOME:-$HOME/.cache}"
MODE="link"
ADD_MENU=0

usage() {
  echo "Usage: $0 --source <theme-checkout> [--link|--copy] [--menu]"
  echo "       [--config-dir <omarchy-config>] [--cache-root <cache-directory>]"
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --source)
      [ "$#" -ge 2 ] || { usage >&2; exit 1; }
      SOURCE="$2"
      shift ;;
    --config-dir)
      [ "$#" -ge 2 ] || { usage >&2; exit 1; }
      CONFIG_DIR="$2"
      shift ;;
    --cache-root)
      [ "$#" -ge 2 ] || { usage >&2; exit 1; }
      CACHE_ROOT="$2"
      shift ;;
    --copy) MODE="copy" ;;
    --link) MODE="link" ;;
    --menu) ADD_MENU=1 ;;
    --help|-h) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done

[ -n "$SOURCE" ] || { usage >&2; exit 1; }
SOURCE="$(realpath -- "$SOURCE")"
CONFIG_DIR="$(realpath -m -- "$CONFIG_DIR")"
CACHE_ROOT="$(realpath -m -- "$CACHE_ROOT")"
DEST="$CONFIG_DIR/themes"
MENU="$CONFIG_DIR/extensions/omarchy-menu.jsonc"
[ -f "$SOURCE/colors.toml" ] && [ -d "$SOURCE/themes" ] || {
  echo "not an Arquibancada theme checkout: $SOURCE" >&2; exit 1;
}
# Validate all input directories before writing into the user's configuration.
for dir in "$SOURCE"/themes/*/; do
  [ -d "$dir" ] || { echo "no club themes found in $SOURCE" >&2; exit 1; }
  slug="$(basename "$dir")"
  [[ "$slug" =~ ^[a-z0-9][a-z0-9-]*$ ]] || {
    echo "invalid club theme name: $slug" >&2; exit 1;
  }
  for required in colors.toml preview.png backgrounds/1-arte.jpg backgrounds/2-escudo.jpg backgrounds/3-mascote.jpg; do
    [ -f "$dir/$required" ] || { echo "missing theme file: $dir/$required" >&2; exit 1; }
  done
done

mkdir -p "$DEST"
count=0
for dir in "$SOURCE"/themes/*/; do
  [ -d "$dir" ] || continue
  slug="$(basename "$dir")"
  if [ -e "$DEST/$slug" ] && [ ! -L "$DEST/$slug" ]; then
    echo "skip $slug (a non-symlink theme with that name already exists)"
    continue
  fi
  if [ "$MODE" = "link" ] && [ -L "$DEST/$slug" ] && [ "$(readlink -f "$DEST/$slug")" = "$(realpath "$dir")" ]; then
    count=$((count + 1))
    continue
  fi
  rm -rf "$DEST/$slug"
  if [ "$MODE" = "copy" ]; then
    cp -r "$dir" "$DEST/$slug"
  else
    ln -s "${dir%/}" "$DEST/$slug"
  fi
  count=$((count + 1))
done

rm -rf "$CACHE_ROOT/omarchy/theme-selector"
echo "Installed $count themes into $DEST ($MODE)."

if [ "$ADD_MENU" = "1" ]; then
  python3 - "$MENU" "$ROOT" "$SOURCE" <<'PY'
import json, os, re, shutil, sys, time

menu, root, source = sys.argv[1:]
text = open(menu, encoding="utf-8").read() if os.path.exists(menu) else "{\n}\n"

themes_dir = os.path.join(source, "themes")
slugs = sorted(d for d in os.listdir(themes_dir) if os.path.isdir(os.path.join(themes_dir, d)))

rows = []
if '"clubes"' not in text:
    rows.append('"clubes": ' + json.dumps(
        {"icon": "\uf1e3", "label": "Clubes"}, ensure_ascii=True))
sys.path.insert(0, os.path.join(root, 'src'))
from teams import team
for slug in slugs:
    if json.dumps(f"clubes.{slug}") in text:
        continue
    label = team(slug)['display'].title()
    rows.append(json.dumps(f"clubes.{slug}") + ": " + json.dumps(
        {"icon": "\uf111", "label": label, "action": f"omarchy theme set {slug}"},
        ensure_ascii=True))
if not rows:
    print("Menu already contains every club theme")
    raise SystemExit(0)
block = ",\n  ".join(rows)

idx = text.rstrip().rfind("}")
if idx == -1:
    raise SystemExit("menu file has no closing brace; not touching it")

inner_raw = text[:idx].split("{", 1)[1] if "{" in text[:idx] else ""
inner = re.sub(r"//[^\n]*", "", inner_raw).strip()
lead = ",\n  " if inner else "\n  "
new = text[:idx].rstrip() + lead + block + "\n" + text[idx:]

try:
    json.loads(re.sub(r"//[^\n]*", "", new))
except json.JSONDecodeError as exc:
    raise SystemExit(f"refusing to write menu: JSONC would be invalid ({exc})")

if os.path.exists(menu):
    shutil.copy2(menu, f"{menu}.bak.{int(time.time())}")
os.makedirs(os.path.dirname(menu), exist_ok=True)
with open(menu, "w", encoding="utf-8") as f:
    f.write(new)
print(f"Added/updated {len(rows)} menu entries to {menu}")
PY
fi

echo "Try: omarchy theme set santos"
