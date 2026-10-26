"""Derive shirt variants from real club artwork, without redrawing lettering.

Only viewports, channel masks, circles and regular championship stars are added.
The source artwork and kit photographs remain separately attributable.
"""
import base64
import math
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/kit-badges'
NS = 'http://www.w3.org/2000/svg'

def uri(name):
    p = ROOT / 'assets' / name
    mime = 'image/svg+xml' if p.suffix == '.svg' else 'image/png'
    return 'data:' + mime + ';base64,' + base64.b64encode(p.read_bytes()).decode()

def star(x, y, r, color):
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        q = r if i % 2 == 0 else r * .381966
        pts.append(f'{x+q*math.cos(a):.4f},{y+q*math.sin(a):.4f}')
    return f'<polygon points="{" ".join(pts)}" fill="{color}"/>'

def image(name, x=0, y=0, w=500, h=500):
    return f'<image href="{uri(name)}" x="{x}" y="{y}" width="{w}" height="{h}"/>'

def save(name, viewbox, body):
    (OUT / name).write_text(f'<svg xmlns="{NS}" viewBox="{viewbox}">{body}</svg>\n')

def main():
    p = ET.parse(ROOT / 'assets/crests/palmeiras.svg')
    root = p.getroot()
    for parent in root.iter():
        for child in list(parent):
            if child.get('id') == 'path1':
                parent.remove(child)
    root.set('viewBox', '0 39.15834 230.98125 230.98125')
    root.set('width', '500'); root.set('height', '500')
    p.write(OUT / 'palmeiras-camisa.svg', encoding='unicode')
    gold = '#d7ad42'
    # Current shirt: one red star above a gold/red/red/gold row.
    stars = star(250, -134, 24, '#d00029')
    stars += ''.join(star(x, -55, 24, '#d00029') for x in (194, 306))
    stars += ''.join(star(x, -55, 24, gold) for x in (82, 418))
    save('sao-paulo-camisa.svg', '0 -166 500 666', stars + image('crests/sao-paulo.svg'))
    save('coritiba-camisa.svg', '0 -86 500 586', star(250, -40, 34, gold) + image('crests/coritiba.png'))
    save('flamengo-camisa.svg', '0 -95 500 571', star(250, -45, 34, gold) + image('kit-badges/flamengo-crf.svg', 0, 0, 500, 476))
    save('vitoria-camisa.svg', '0 -85 500 585', star(250, -38, 32, gold) + image('crests/vitoria.png'))
    # Preserve the original white SCI channels, excluding the institutional outer ring.
    mask = '<defs><filter id="white"><feColorMatrix type="matrix" values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 1 0 0 0"/></filter><clipPath id="inner"><circle cx="250" cy="250" r="194"/></clipPath></defs>'
    sci = f'<g clip-path="url(#inner)" filter="url(#white)">{image("crests/internacional.png")}</g>'
    stars = ''.join(star(x, y, r, gold) for x,y,r in [(250, -54, 26),(122,33,21),(203,0,21),(297,0,21),(378,33,21)])
    save('internacional-camisa.svg', '52 -82 396 528', mask + sci + stars)
    # Chape's current shirt has a round gold-edged badge, without four external stars.
    body = '<defs><clipPath id="round"><circle cx="250" cy="291" r="202"/></clipPath></defs>'
    body += f'<g clip-path="url(#round)">{image("crests/chapecoense.png")}</g><circle cx="250" cy="291" r="204" fill="none" stroke="{gold}" stroke-width="8"/>'
    save('chapecoense-camisa.svg', '40 81 420 420', body)
    # Mirassol: native green MFC letterforms, omitting the institutional ribbon.
    defs = '<defs><filter id="green" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="0 0 0 0 .025 0 0 0 0 .31 0 0 0 0 .13 -1 0 0 0 1"/></filter><clipPath id="round"><circle cx="250" cy="209" r="157"/></clipPath></defs>'
    body = f'<g clip-path="url(#round)" filter="url(#green)">{image("crests/mirassol.png")}</g><circle cx="250" cy="209" r="174" fill="none" stroke="#075c2d" stroke-width="8"/>'
    body += ''.join(star(x, y, 20, '#075c2d') for x,y in [(172,9),(250,-10),(328,9)])
    save('mirassol-camisa.svg', '69 -34 362 424', defs + body)

if __name__ == '__main__':
    main()
