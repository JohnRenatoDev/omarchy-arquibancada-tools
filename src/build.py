#!/usr/bin/env python3
"""Build the Brasileirão theme pack for Omarchy.

Usage:
    python3 src/build.py --output-dir ../omarchy-arquibancada-theme
    python3 src/build.py --output-dir ../omarchy-arquibancada-theme santos palmeiras

Output: <output-dir>/themes/<slug>/ and theme previews. Intermediate files and
QC sheets stay under this tools repository's build/ directory.
"""
import os
import argparse
import shutil
import subprocess
import sys
import tempfile

import art
from teams import TEAMS, team

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
BUILD = os.path.join(ROOT, "build")
OUTPUT_ROOT = os.path.join(BUILD, "export")
THEMES = os.path.join(OUTPUT_ROOT, "themes")
SVG_DIR = os.path.join(BUILD, "svg")

W, H = 3840, 2160
PHOTO_X, PHOTO_W = 1450, 2390


def run(*args, quiet=True):
    r = subprocess.run([str(a) for a in args], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(map(str, args))}\n{r.stderr[-2000:]}")
    if not quiet and r.stdout:
        print(r.stdout)
    return r.stdout


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def render_svg(svg_text, out_png):
    fd, svg_path = tempfile.mkstemp(suffix=".svg", dir=SVG_DIR)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(svg_text)
    run("rsvg-convert", "-o", out_png, svg_path)
    return out_png


# ------------------------------------------------------------------ colour utils
def _rgb(c):
    c = c.lstrip("#")
    return [int(c[i:i + 2], 16) for i in (0, 2, 4)]


def mix(c1, c2, amount):
    a, b = _rgb(c1), _rgb(c2)
    out = [round(x * (1 - amount) + y * amount) for x, y in zip(a, b)]
    return "#%02X%02X%02X" % tuple(out)


def shade(c, amount):
    return mix(c, "#000000" if amount >= 0 else "#FFFFFF", abs(amount))


# ------------------------------------------------------------------ theme files
def colors_toml(t):
    p = t["palette"]
    bg = t["bg"]
    return f"""mode = "dark"

accent = "{t['accent']}"
selection = "{p['selection']}"
muted = "{p['muted']}"

background = "{bg}"
dark_background = "{shade(bg, 0.35)}"
darker_background = "{shade(bg, 0.62)}"
lighter_background = "{mix(bg, '#FFFFFF', 0.075)}"

foreground = "{p['foreground']}"
dark_foreground = "{p['dark_foreground']}"
light_foreground = "{p['light_foreground']}"
bright_foreground = "{p['bright_foreground']}"

red = "{p['red']}"
yellow = "{p['yellow']}"
orange = "{p['orange']}"
green = "{p['green']}"
cyan = "{p['cyan']}"
blue = "{p['blue']}"
magenta = "{p['magenta']}"
brown = "{p['brown']}"

bright_red = "{p['bright_red']}"
bright_yellow = "{p['bright_yellow']}"
bright_green = "{p['bright_green']}"
bright_cyan = "{p['bright_cyan']}"
bright_blue = "{p['bright_blue']}"
bright_magenta = "{p['bright_magenta']}"
"""


def write_theme_files(t):
    out = os.path.join(THEMES, t["slug"])
    os.makedirs(os.path.join(out, "backgrounds"), exist_ok=True)
    write(os.path.join(out, "colors.toml"), colors_toml(t))
    write(os.path.join(out, "icons.theme"), t["icons"] + "\n")
    write(os.path.join(out, "keyboard.rgb"), t["accent"].lstrip("#") + "\n")
    p = t["palette"]
    write(os.path.join(out, "shell.lock.toml"), f"""text             = "{p['foreground']}"
placeholder      = "{t['ink_dim']}"
text-error       = "{p['red']}"
border           = "{t['ink_dim']}"
border-active    = "{t['accent']}"
border-error     = "{p['red']}"
""")
    return out


# ------------------------------------------------------------------ imagery
def finish_wallpaper(src_png, out_jpg, seed=7):
    # The generated illustrations already contain painted texture. Avoid an
    # expensive full-frame synthetic noise pass on every 4K export.
    run("magick", src_png,
        "-quality", "92", "-sampling-factor", "4:4:4", out_jpg)


def build_arte(t, out):
    svg = art.art_svg(t)
    png = render_svg(svg, os.path.join(BUILD, f"{t['slug']}-arte.png"))
    finish_wallpaper(png, os.path.join(out, "backgrounds", "1-arte.jpg"))


def prep_crest(t, height=1250):
    src = os.path.join(ASSETS, t["crest"])
    tmp = os.path.join(BUILD, f"{t['slug']}-crest.png")
    if src.endswith(".svg"):
        run("rsvg-convert", "-h", height, "-o", tmp, src)
        run("magick", tmp, "-trim", "+repage", tmp)
    else:
        run("magick", src, "-trim", "+repage", "-resize", f"x{height}",
            "-unsharp", "0x0.75+0.6+0.02", tmp)
    return tmp


def build_escudo(t, out):
    png = render_svg(art.crest_svg(t), os.path.join(BUILD, f"{t['slug']}-escudo.png"))
    crest = prep_crest(t)
    w, h = map(int, run("magick", "identify", "-format", "%w %h", crest).split())
    x, y = 1250 - w // 2, 1080 - h // 2

    glow = os.path.join(BUILD, f"{t['slug']}-crest-glow.png")
    run("magick", crest, "-channel", "A", "-blur", "0x30", "+channel",
        "-fill", t["accent"], "-colorize", "100", glow)

    merged = os.path.join(BUILD, f"{t['slug']}-escudo-merged.png")
    run("magick", png, glow, "-geometry", f"+{x - 20}+{y - 20}", "-composite",
        crest, "-geometry", f"+{x}+{y}", "-composite", merged)
    finish_wallpaper(merged, os.path.join(out, "backgrounds", "2-escudo.jpg"))


def build_mascote(t, out):
    from mascote_cartoon import render
    png = render_svg(render(t), os.path.join(BUILD, f"{t['slug']}-mascote.png"))
    finish_wallpaper(png, os.path.join(out, "backgrounds", "3-mascote.jpg"))
    # Remove the obsolete fourth entry after the replacement was exported.
    legacy = os.path.join(out, "backgrounds", "4-caricatura.jpg")
    if os.path.isfile(legacy):
        os.unlink(legacy)


def build_preview(t, out, background="3-mascote.jpg"):
    src = os.path.join(out, "backgrounds", background)
    overlay = render_svg(art.preview_overlay_svg(t),
                         os.path.join(BUILD, f"{t['slug']}-preview-overlay.png"))
    tmp = os.path.join(BUILD, f"{t['slug']}-preview-bg.png")
    run("magick", src, "-resize", "1800x1012^", "-gravity", "center",
        "-extent", "1800x1012", "-brightness-contrast", "-6x0", tmp)
    run("magick", tmp, overlay, "-geometry", "+0+0", "-composite",
        os.path.join(out, "preview.png"))


# ------------------------------------------------------------------ QC sheet
def palette_sheet(slugs):
    cards = []
    for slug in slugs:
        t = team(slug)
        p = t["palette"]
        colors = [t["accent"], p["red"], p["yellow"], p["green"], p["cyan"],
                  p["blue"], p["magenta"], p["bright_foreground"]]
        w, h = 760, 210
        blocks = "".join(
            f'<rect x="{40 + i*86}" y="96" width="70" height="72" rx="6" fill="{c}"/>'
            for i, c in enumerate(colors)
        )
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">
          <rect width="{w}" height="{h}" fill="{t['bg']}"/>
          <rect x="0" y="0" width="10" height="{h}" fill="{t['accent']}"/>
          {blocks}
          <text x="40" y="58" font-family="Anton" font-size="40" fill="{t['ink']}">{t['display']}</text>
          <text x="{w-40}" y="58" text-anchor="end" font-family="JetBrainsMono Nerd Font"
                font-size="18" fill="{t['ink_dim']}">{slug}</text>
        </svg>"""
        png = render_svg(svg, os.path.join(BUILD, f"qc-{slug}.png"))
        cards.append(png)
    out = os.path.join(BUILD, "palettes.png")
    run("magick", *cards, "-append", out)
    return out


def contact_sheet(slug):
    out = os.path.join(THEMES, slug, "backgrounds")
    files = [os.path.join(out, f) for f in
             ("1-arte.jpg", "2-escudo.jpg", "3-mascote.jpg")]
    sheet = os.path.join(BUILD, f"contact-{slug}.png")
    run("magick", *files, "-resize", "900x", "+append", sheet)
    return sheet


def build(slug):
    t = team(slug)
    print(f"→ {t['display']} ({slug})")
    out = write_theme_files(t)
    build_arte(t, out)
    build_escudo(t, out)
    build_mascote(t, out)
    build_preview(t, out)
    contact_sheet(slug)
    print(f"  ok: {out}")


def build_docs():
    """Refresh all mascot reviews and the three-wallpaper catalogue per club."""
    from mascote_cartoon import ORDER
    docs = os.path.join(OUTPUT_ROOT, "docs")
    os.makedirs(docs, exist_ok=True)
    # Resize inputs before montage: holding sixty full 4K frames at once would
    # waste several gigabytes during a documentation-only operation.
    thumbs = os.path.join(BUILD, 'docs-thumbnails')
    os.makedirs(thumbs, exist_ok=True)
    posters, catalogue, uniforms = [], [], []
    for slug in ORDER:
        for name in ('1-arte.jpg', '2-escudo.jpg', '3-mascote.jpg'):
            source = os.path.join(THEMES, slug, 'backgrounds', name)
            small = os.path.join(thumbs, f'{slug}-{name}')
            if name == '3-mascote.jpg':
                poster = os.path.join(thumbs, f'{slug}-poster.jpg')
                run('magick', source, '-resize', '960x540', '-quality', '92',
                    '-write', poster, '-resize', '640x360', small)
                posters.append(poster)
                detail = os.path.join(thumbs, f'{slug}-shirt.jpg')
                run('magick', source, '-resize', '1672x941!', '-crop', '480x370+920+150',
                    '+repage', '-background', '#141414', '-fill', 'white', '-font', 'Oswald',
                    '-gravity', 'south', '-splice', '0x28', '-pointsize', '20',
                    '-annotate', '+0+4', slug, '-quality', '94', detail)
                uniforms.append(detail)
            else:
                run('magick', source, '-resize', '640x360', '-quality', '92', small)
            catalogue.append(small)
    run("magick", "montage", *posters, "-tile", "4x", "-geometry", "960x540+8+8",
        "-background", "#08090b", '-depth', '8', os.path.join(docs, "mascotes-cartoon.png"))
    run("magick", "montage", *catalogue, "-tile", "3x", "-geometry", "640x360+8+8",
        "-background", "#08090b", '-depth', '8', os.path.join(docs, "preview.png"))
    run("magick", "montage", *uniforms, "-tile", "4x5", "-geometry", "480x398+5+5",
        '-background', '#08090b', '-quality', '94', os.path.join(docs, 'uniformes-revisao.jpg'))
    run("magick", os.path.join(docs, "mascotes-cartoon.png"), "-resize", "2800x",
        "-quality", "91", os.path.join(docs, "mascotes-serie-a-2026.jpg"))
    run("magick", os.path.join(docs, "mascotes-cartoon.png"), "-resize", "1800x",
        os.path.join(docs, "cover.png"))
    run("magick", os.path.join(docs, "preview.png"), "-resize", "1600x",
        "-quality", "90", os.path.join(docs, "catalogo-serie-a-2026.jpg"))
    sync_default_theme()


def sync_default_theme():
    """Keep the native Omarchy root entry point in sync with default Santos."""
    source = os.path.join(THEMES, 'santos')
    backgrounds = os.path.join(OUTPUT_ROOT, 'backgrounds')
    os.makedirs(backgrounds, exist_ok=True)
    for name in ('colors.toml', 'icons.theme', 'keyboard.rgb', 'shell.lock.toml'):
        shutil.copy2(os.path.join(source, name), os.path.join(OUTPUT_ROOT, name))
    for name in ('1-arte.jpg', '2-escudo.jpg', '3-mascote.jpg'):
        shutil.copy2(os.path.join(source, 'backgrounds', name), os.path.join(backgrounds, name))
    legacy = os.path.join(backgrounds, '4-caricatura.jpg')
    if os.path.isfile(legacy):
        os.unlink(legacy)
    run('magick', os.path.join(backgrounds, '3-mascote.jpg'),
        '-resize', '1920x1080', '-strip', os.path.join(OUTPUT_ROOT, 'preview.png'))


def main():
    global OUTPUT_ROOT, THEMES
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=OUTPUT_ROOT,
                        help="Theme checkout or export directory (default: build/export)")
    parser.add_argument("--mascotes-only", "--caricaturas-only", dest="mascotes_only", action="store_true",
                        help="Update mascot posters and previews; preserve wallpapers 1–2")
    parser.add_argument("slugs", nargs="*")
    args = parser.parse_args()
    OUTPUT_ROOT = os.path.realpath(os.path.expanduser(args.output_dir))
    if OUTPUT_ROOT == ROOT:
        parser.error("Use a separate theme checkout or export directory, not the tools root")
    THEMES = os.path.join(OUTPUT_ROOT, "themes")
    slugs = args.slugs or list(TEAMS)
    unknown = set(slugs) - TEAMS.keys()
    if unknown:
        parser.error(f"Unknown teams: {', '.join(sorted(unknown))}")
    # Every build refreshes the complete gallery. A partial build therefore
    # needs an existing export for the clubs it will not render.
    for slug in TEAMS:
        required = ('1-arte.jpg', '2-escudo.jpg') if args.mascotes_only and slug in slugs else ()
        if slug not in slugs:
            required = ('1-arte.jpg', '2-escudo.jpg', '3-mascote.jpg')
        for name in required:
            path = os.path.join(THEMES, slug, 'backgrounds', name)
            if not os.path.isfile(path):
                parser.error(f"Existing export required for a partial build: {path}")
    for slug in slugs:
        source = os.path.join(ASSETS, "mascotes-generated", f"{slug}.png")
        if not os.path.isfile(source):
            parser.error(f"Generated mascot required: {source}")
    for d in (BUILD, SVG_DIR, THEMES):
        os.makedirs(d, exist_ok=True)
    for slug in slugs:
        if args.mascotes_only:
            t = team(slug)
            out = os.path.join(THEMES, slug)
            build_mascote(t, out)
            build_preview(t, out)
            contact_sheet(slug)
            print(f"  updated mascote: {slug}")
        else:
            build(slug)
    build_docs()
    sheet = palette_sheet(slugs)
    print(f"\npalette sheet: {sheet}")


if __name__ == "__main__":
    main()
