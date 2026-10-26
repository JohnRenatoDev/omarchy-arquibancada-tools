"""Lay out reviewed raster posters with club identity and theme typography.

SVG is only the container: characters, stadium and lighting are generated PNGs.
Missing art is an error, never a fallback to the old vector prototypes.
Shirt artwork uses native club assets over a clean, unbranded garment raster.
"""
import base64
import html
import json
from pathlib import Path
from teams import TEAM_ORDER

ROOT = Path(__file__).resolve().parents[1]
W, H = 3840, 2160
ORDER = TEAM_ORDER
LAYOUT = json.loads(Path(__file__).with_name('mascotes-layout.json').read_text())


def _uri(path):
    path = Path(path)
    mime = 'image/svg+xml' if path.suffix == '.svg' else 'image/png'
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()


def shirt_badge(slug):
    """Use the native emblem on this mascot's reviewed shirt surface."""
    from badge_surface import render as render_badge
    kit = LAYOUT[slug]
    if kit['application'] != 'native-shirt-surface':
        raise ValueError(f'Reviewed shirt surface required: {slug}')
    return render_badge(ROOT / 'assets' / kit['badge'], kit['shirt_surface'])


def render(t, source_override=None, caption='MASCOTE · PÔSTER CINEMATOGRÁFICO'):
    """Contain the entire illustration in 4K without stretching or cropping."""
    slug = t['slug']
    source = Path(source_override) if source_override else ROOT / 'assets' / 'mascotes-generated' / f'{slug}.png'
    if not source.is_file():
        raise FileNotFoundError(f'Generated mascot required: {source}')
    crest = _uri(ROOT / 'assets' / t['crest'])
    esc = lambda value: html.escape(str(value), quote=True)
    name = 'SANTO PAULO' if slug == 'sao-paulo' else t['mascot_name']
    title_size = min(210, 1900 / max(len(name), 1))
    return f'''<svg xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}"
      viewBox="0 0 {W} {H}">
      <defs>
        <linearGradient id="caption-shade" x1="0" x2="1" y1="0" y2="0">
          <stop offset="0" stop-color="{t['bg_deep']}" stop-opacity="0.52"/>
          <stop offset="0.36" stop-color="{t['bg_deep']}" stop-opacity="0.18"/>
          <stop offset="0.57" stop-color="{t['bg_deep']}" stop-opacity="0"/>
        </linearGradient>
      </defs>
      <rect width="{W}" height="{H}" fill="{t['bg_deep']}"/>
      <image width="{W}" height="{H}" preserveAspectRatio="xMidYMid meet"
        xlink:href="{_uri(source)}"/>
      <svg width="{W}" height="{H}" viewBox="0 0 1672 941"
        preserveAspectRatio="xMidYMid meet">{shirt_badge(slug)}</svg>
      <rect width="{W}" height="{H}" fill="url(#caption-shade)"/>
      <text x="202" y="220" font-family="JetBrainsMono Nerd Font" font-size="28"
        letter-spacing="8" fill="{t['ink']}">{esc(t['nickname'])}</text>
      <text x="202" y="299" font-family="Oswald" font-weight="300" font-size="34"
        letter-spacing="{min(10, 160 / len(t['stadium']))}" fill="{t['ink_dim']}">{esc(t['stadium'])}</text>
      <path d="M202 350 H380" stroke="{t['accent']}" stroke-width="5"/>
      <image x="202" y="424" width="210" height="250"
        preserveAspectRatio="xMinYMin meet" xlink:href="{crest}"/>
      <text x="184" y="1150" font-family="Anton" font-size="600"
        letter-spacing="-8" fill="{t['ink']}" opacity="0.055">{esc(t['monogram'])}</text>
      <path d="M202 1505 H352" stroke="{t['accent']}" stroke-width="5"/>
      <text x="196" y="1740" font-family="Anton" font-size="{title_size}"
        fill="{t['ink']}">{esc(name)}</text>
      <text x="202" y="1840" font-family="Oswald" font-weight="600" font-size="48"
        letter-spacing="13" fill="{t['accent']}">{esc(t['display'])}</text>
      <text x="205" y="1930" font-family="JetBrainsMono Nerd Font" font-size="22"
        letter-spacing="5" fill="{t['ink_dim']}">{esc(caption)}</text>
    </svg>'''
