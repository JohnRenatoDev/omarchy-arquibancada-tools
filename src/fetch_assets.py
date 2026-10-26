#!/usr/bin/env python3
"""Fetch crests/mascot assets and fonts for the Brasileirão theme pack.

Uses the MediaWiki API to resolve the original file URL, then downloads with a
proper User-Agent. Keeps everything under assets/ so builds are reproducible.
"""
import json
import os
import sys
import urllib.parse
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(BASE, "assets")
UA = "omarchy-brasileirao-themes/0.1 (personal theme pack; contact: local user)"

# (wiki, file title, output path relative to assets/)
FILES = [
    ("commons", "Santos Futebol Clube logo (with stars and crown).png", "crests/santos.png"),
    ("commons", "São Paulo Futebol Clube logo (2022).svg", "crests/sao-paulo.svg"),
    ("commons", "Sociedade Esportiva Palmeiras logo (1 red star).svg", "crests/palmeiras.svg"),
    ("ptwiki", "Corinthians simbolo.png", "crests/corinthians.png"),
    ("commons", "Porco-Gobatto-Palmeiras-jul-2022 (cropped).jpg", "mascots/palmeiras-porco.jpg"),
    ("commons", "Periquito-Palmeiras-jul-2022 (cropped).jpg", "mascots/palmeiras-periquito.jpg"),
    ("commons", "SPFC mascot - 02.svg", "mascots/sao-paulo.svg"),
    ("commons", "SPFC mascot - 01.jpg", "mascots/sao-paulo-photo.jpg"),
    ("commons", "Statue dArtagnan.jpg", "mascots/corinthians-dartagnan.jpg"),
    ("commons", "Monk parakeet (Myiopsitta monachus) Santiago.jpg", "mascots/palmeiras-periquito-real1.jpg"),
    ("commons", "El Greco - St. Paul - Google Art Project.jpg", "mascots/sao-paulo-elgreco.jpg"),
]

WIKIS = {
    "commons": "https://commons.wikimedia.org/w/api.php",
    "ptwiki": "https://pt.wikipedia.org/w/api.php",
}

FONTS = [
    ("https://raw.githubusercontent.com/google/fonts/main/ofl/anton/Anton-Regular.ttf", "fonts/Anton-Regular.ttf"),
    ("https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf", "fonts/Oswald.ttf"),
    ("https://raw.githubusercontent.com/google/fonts/main/ofl/archivoblack/ArchivoBlack-Regular.ttf", "fonts/ArchivoBlack-Regular.ttf"),
]


def api(wiki, params):
    params = dict(params, format="json")
    url = WIKIS[wiki] + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def original_url(wiki, title):
    d = api(wiki, {"action": "query", "titles": "File:" + title,
                   "prop": "imageinfo", "iiprop": "url|size|mime"})
    pages = d.get("query", {}).get("pages", {})
    for p in pages.values():
        ii = (p.get("imageinfo") or [{}])[0]
        if ii.get("url"):
            return ii["url"], ii.get("width", 0), ii.get("height", 0)
    return None, 0, 0


def download(url, outpath):
    dest = os.path.join(ASSETS, outpath)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
        data = r.read()
        f.write(data)
    return len(data)


def search(wiki, query, limit=10):
    d = api(wiki, {"action": "query", "generator": "search", "gsrsearch": query,
                   "gsrnamespace": 6, "gsrlimit": limit,
                   "prop": "imageinfo", "iiprop": "url|size|mime"})
    rows = []
    for p in (d.get("query") or {}).get("pages", {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        if str(ii.get("mime", "")).startswith("image/"):
            rows.append((p.get("title", ""), ii.get("width", 0), ii.get("height", 0), ii.get("url", "")))
    return rows


def main():
    only = sys.argv[1:] or None
    # fonts first (independent of API)
    for url, out in FONTS:
        if only and out not in only:
            continue
        try:
            n = download(url, out)
            print(f"font  {out}: {n//1024} KiB")
        except Exception as e:  # noqa: BLE001
            print(f"font  {out}: FAILED {e}")

    for wiki, title, out in FILES:
        if only and out not in only:
            continue
        try:
            url, w, h = original_url(wiki, title)
            if not url:
                print(f"file  {out}: not found ({title})")
                continue
            n = download(url, out)
            print(f"file  {out}: {n//1024} KiB  ({w}x{h})  {url.split('?')[0]}")
        except Exception as e:  # noqa: BLE001
            print(f"file  {out}: FAILED {e}")

    if not only:
        print("\n-- search: corinthians logo (commons) --")
        for t, w, h, u in search("commons", "Corinthians logo"):
            print(f"  {t} | {w}x{h} | {u.split('?')[0]}")
        print("\n-- search: Santos mascote/baleia (commons) --")
        for q in ("Santos FC mascote", "baleia mascote", "Santos Futebol Clube mascote"):
            print(f"  [{q}]")
            for t, w, h, u in search("commons", q, limit=6):
                print(f"    {t} | {w}x{h} | {u.split('?')[0]}")


if __name__ == "__main__":
    main()
