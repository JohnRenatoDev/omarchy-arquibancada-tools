"""SVG art for the Brasileirão theme wallpapers.

Three compositions per team:
  1. arte    – abstract dynamic art in team colours
  2. escudo  – the crest as the hero
  3. mascote – the mascot as the hero
All text is vector; photos/crests are composited later in build.py.
"""
import html

W, H = 3840, 2160


def esc(s):
    return html.escape(str(s), quote=False)


def _hexrgba(c, a):
    c = c.lstrip("#")
    r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    return f"rgba({r},{g},{b},{a})"


def _doc(defs, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}"><defs>{defs}</defs>{body}</svg>'
    )


def _defs_common(t):
    return f"""
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['bg_deep']}"/>
      <stop offset="0.55" stop-color="{t['bg']}"/>
      <stop offset="1" stop-color="{_hexrgba(t['accent'], 0.10)}"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{t['accent']}" stop-opacity="0.16"/>
      <stop offset="0.55" stop-color="{t['accent']}" stop-opacity="0.05"/>
      <stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="ghost" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['ink']}" stop-opacity="0.10"/>
      <stop offset="0.75" stop-color="{t['ink']}" stop-opacity="0.03"/>
      <stop offset="1" stop-color="{t['ink']}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="vig" cx="0.5" cy="0.44" r="0.78">
      <stop offset="0" stop-color="{t['bg']}" stop-opacity="0"/>
      <stop offset="0.62" stop-color="{t['bg']}" stop-opacity="0"/>
      <stop offset="1" stop-color="{t['bg_deep']}" stop-opacity="0.62"/>
    </radialGradient>
    """


def _footer(t):
    return f"""
    <text x="3640" y="2076" text-anchor="end" font-family="JetBrainsMono Nerd Font"
          font-size="24" letter-spacing="4" fill="{t['ink']}" fill-opacity="0.42">
      OMARCHY · THEME PACK
    </text>"""


def _text_block(t):
    n = len(t["display"])
    size = 250 if n <= 7 else (215 if n <= 8 else 200)
    return f"""
    <rect x="200" y="1398" width="150" height="5" fill="{t['accent']}" opacity="0.9"/>
    <text x="196" y="1672" font-family="Anton" font-size="{size}" letter-spacing="1"
          fill="{t['ink']}">{esc(t['display'])}</text>
    <text x="200" y="1768" font-family="Oswald" font-weight="600" font-size="62"
          letter-spacing="14" fill="{t['ink_dim']}">{esc(t['subtitle'])}</text>
    <text x="203" y="1872" font-family="Oswald" font-weight="300" font-size="40"
          letter-spacing="10" fill="{t['ink_dim']}" fill-opacity="0.85">
      {esc(f"{t['nickname']} · {t['city']} · {t['year']}")}
    </text>
    <text x="203" y="1996" font-family="JetBrainsMono Nerd Font" font-size="26"
          letter-spacing="6" fill="{t['ink_dim']}" fill-opacity="0.62">
      {esc(f"CASA: {t['stadium']}")}
    </text>"""


def _ghost_monogram(t, x=3780, y=1570, size=1200, anchor="end"):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Anton" font-size="{size}" '
        f'letter-spacing="-10" fill="url(#ghost)">{esc(t["monogram"])}</text>'
    )


def _medallion_rings(t):
    """Rings that frame the circular mascot medallion (drawing-on-white mascots)."""
    if t.get("mascot_kind") != "art":
        return ""
    return f"""
    <circle cx="2700" cy="1080" r="606" fill="none" stroke="{t['accent']}" stroke-width="2" stroke-opacity="0.35"/>
    <circle cx="2700" cy="1080" r="644" fill="none" stroke="{t['accent']}" stroke-width="1.5" stroke-opacity="0.18" stroke-dasharray="10 16"/>
    """


# ---------------------------------------------------------------- motifs
def _motif_waves(t):
    """Alvinegro: ondas em branco e cinza (a cor do mar/do Peixe, sem cores extras)."""
    acc, bright, dim = t["accent"], t["accent_bright"], t["ink_dim"]
    out = [
        f'<path d="M 1500 2420 C 2200 2020 2740 1520 4010 1180 L 4010 1900 '
        f'C 3040 2020 2480 2260 2160 2660 Z" fill="url(#waveFill)" opacity="0.6"/>',
        f'<path d="M 1560 2300 C 2260 1900 2760 1460 4020 1120" fill="none" '
        f'stroke="{bright}" stroke-width="3" stroke-opacity="0.6"/>',
    ]
    for i in range(12):
        y = 120 + i * 168
        d = (f"M 1540 {y + 260} C 2150 {y - 20}, 2870 {y - 120}, 4060 {y + 90}")
        col = bright if i in (1, 4, 9) else (dim if i % 2 else acc)
        sw = 2 + (i % 3) * 4
        op = 0.20 + (i % 4) * 0.055
        out.append(
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" '
            f'stroke-opacity="{op:.2f}" stroke-linecap="round"/>'
        )
    return "".join(out)


def _motif_tricolor(t):
    red = t["accent"]
    return f"""
    <g transform="rotate(-24 3000 1080)">
      <rect x="1400" y="-760" width="3100" height="720" fill="url(#redGrad)" opacity="0.92"/>
      <rect x="1400" y="40" width="3100" height="430" fill="url(#whiteGrad)" opacity="0.96"/>
      <rect x="1400" y="540" width="3100" height="380" fill="{t.get('secondary', t['bg_deep'])}" opacity="0.95"/>
      <rect x="1400" y="990" width="3100" height="52" fill="{red}" opacity="0.9"/>
      <rect x="1400" y="1110" width="3100" height="8" fill="{t['ink']}" opacity="0.16"/>
      <rect x="1400" y="-810" width="3100" height="6" fill="{t['ink']}" opacity="0.22"/>
    </g>
    <g opacity="0.10" stroke="{t['ink']}" stroke-width="2">
      {''.join(f'<line x1="{1400 + i*150}" y1="2200" x2="{2100 + i*150}" y2="0"/>' for i in range(18))}
    </g>
    """


def _motif_shards(t):
    out = [
        f'<path d="M 2560 2160 L 3090 -40 L 3245 -40 L 2715 2160 Z" '
        f'fill="url(#beamGrad)" opacity="0.55"/>',
    ]
    for i in range(6):
        x0 = 1680 + i * 300
        top, bot = x0 + 260, x0 - 170
        w = 150 - i * 10
        op = 0.05 + (i % 3) * 0.022
        out.append(
            f'<polygon points="{top},0 {top + w},0 {bot + w},2160 {bot},2160" '
            f'fill="url(#beamGrad)" opacity="{op:.2f}"/>'
        )
        out.append(
            f'<line x1="{top}" y1="0" x2="{bot}" y2="2160" stroke="{t["ink"]}" '
            f'stroke-width="1.5" stroke-opacity="0.10"/>'
        )
    out.append(
        f'<g opacity="0.03" stroke="{t["ink"]}" stroke-width="1.5">'
        + "".join(f'<line x1="{1500 + i*160}" y1="0" x2="{1500 + i*160}" y2="2160"/>' for i in range(15))
        + "</g>"
    )
    out.append(
        f'<line x1="1520" y1="1880" x2="3840" y2="360" stroke="{t["accent"]}" '
        f'stroke-width="2" stroke-opacity="0.35"/>'
    )
    return "".join(out)


def _motif_rings(t):
    out = [f'<circle cx="3050" cy="1020" r="1350" fill="url(#discGrad)"/>']
    for i, r in enumerate(range(300, 1560, 105)):
        op = 0.10 if i % 3 == 0 else 0.055
        out.append(
            f'<circle cx="3050" cy="1020" r="{r}" fill="none" stroke="{t["accent"]}" '
            f'stroke-width="{2 if i % 3 else 3}" stroke-opacity="{op}"/>'
        )
    out.append(
        f'<circle cx="3050" cy="1020" r="860" fill="none" stroke="{t["accent_bright"]}" '
        f'stroke-width="4" stroke-opacity="0.5" stroke-dasharray="20 30"/>'
    )
    out.append(
        f'<circle cx="3050" cy="1020" r="1280" fill="none" stroke="{t["accent_bright"]}" '
        f'stroke-width="2.5" stroke-opacity="0.35" stroke-dasharray="8 46"/>'
    )
    for k in range(3):
        out.append(
            f'<path d="M 1700 {2080 - k*120} C 2300 {1350 - k*90}, 3000 {980 - k*70}, 3840 {1080 - k*90}" '
            f'fill="none" stroke="{t["accent_bright"]}" stroke-width="{8 - k}" '
            f'stroke-opacity="{0.20 - k*0.05:.2f}" stroke-linecap="round"/>'
        )
    return "".join(out)


MOTIFS = {
    "waves": _motif_waves,
    "tricolor": _motif_tricolor,
    "shards": _motif_shards,
    "rings": _motif_rings,
}


# ---------------------------------------------------------------- 1. arte
def art_svg(t):
    defs = _defs_common(t) + f"""
    <linearGradient id="waveFill" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0" stop-color="{t['accent']}" stop-opacity="0.34"/>
      <stop offset="0.7" stop-color="{t['accent']}" stop-opacity="0.08"/>
      <stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="redGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['accent']}" stop-opacity="0.95"/>
      <stop offset="1" stop-color="{_hexrgba(t['accent'], 0.55)}"/>
    </linearGradient>
    <linearGradient id="whiteGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['ink']}" stop-opacity="0.86"/>
      <stop offset="1" stop-color="{t['ink']}" stop-opacity="0.48"/>
    </linearGradient>
    <linearGradient id="beamGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{t['ink']}" stop-opacity="0.40"/>
      <stop offset="0.5" stop-color="{t['ink']}" stop-opacity="0.06"/>
      <stop offset="1" stop-color="{t['ink']}" stop-opacity="0.02"/>
    </linearGradient>
    <radialGradient id="discGrad" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{t['accent']}" stop-opacity="0.13"/>
      <stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/>
    </radialGradient>
    """
    body = f"""
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <rect width="{W}" height="{H}" fill="url(#glow)"/>
    {MOTIFS[t['motif']](t)}
    {_ghost_monogram(t)}
    {_text_block(t)}
    {_footer(t)}
    <rect width="{W}" height="{H}" fill="url(#vig)"/>
    """
    return _doc(defs, body)


# ---------------------------------------------------------------- 2. escudo
def crest_svg(t):
    defs = _defs_common(t) + f"""
    <radialGradient id="crestGlow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{t['accent']}" stop-opacity="0.22"/>
      <stop offset="0.6" stop-color="{t['accent']}" stop-opacity="0.07"/>
      <stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/>
    </radialGradient>
    """
    n = len(t["display"])
    size = 205 if n <= 8 else 185
    body = f"""
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <circle cx="1250" cy="1080" r="1500" fill="url(#crestGlow)"/>
    <g>
      {''.join(f'<circle cx="1250" cy="1080" r="{r}" fill="none" stroke="{t["accent"]}" stroke-width="2" stroke-opacity="{0.06 if i % 2 else 0.10}"/>' for i, r in enumerate(range(660, 1320, 82)))}
    </g>
    {_ghost_monogram(t, x=3700, y=1700, size=900)}
    <g>
      <rect x="2210" y="560" width="4" height="1040" fill="{t['accent']}" opacity="0.75"/>
      <text x="2300" y="1092" font-family="Anton" font-size="{size}" letter-spacing="1"
            fill="{t['ink']}">{esc(t['display'])}</text>
      <text x="2304" y="1192" font-family="Oswald" font-weight="600" font-size="62"
            letter-spacing="14" fill="{t['ink_dim']}">{esc(t['subtitle'])}</text>
      <text x="2307" y="1300" font-family="Oswald" font-weight="300" font-size="40"
            letter-spacing="10" fill="{t['ink_dim']}" fill-opacity="0.85">
        {esc(f"{t['nickname']} · {t['city']}")}
      </text>
      <text x="2307" y="1692" font-family="JetBrainsMono Nerd Font" font-size="26"
            letter-spacing="6" fill="{t['ink_dim']}" fill-opacity="0.62">
        {esc(f"FUNDADO EM {t['year']} · {t['stadium']}")}
      </text>
    </g>
    {_footer(t)}
    <rect width="{W}" height="{H}" fill="url(#vig)"/>
    """
    return _doc(defs, body)


# ---------------------------------------------------------------- 3. mascote
def mascot_svg(t, photo_box_x=1450):
    n = len(t["mascot_name"])
    msize = 250 if n <= 7 else (200 if n <= 9 else 158)
    defs = _defs_common(t) + f"""
    <linearGradient id="splitGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['accent']}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="glowR" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{t['accent']}" stop-opacity="0.20"/>
      <stop offset="0.55" stop-color="{t['accent']}" stop-opacity="0.06"/>
      <stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/>
    </radialGradient>
    """
    body = f"""
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <ellipse cx="2960" cy="1180" rx="1500" ry="1350" fill="url(#glowR)"/>
    <path d="M {photo_box_x - 260} 2160 L 3840 260 L 3840 2160 Z" fill="url(#splitGrad)" opacity="0.55"/>
    {_ghost_monogram(t, x=150, y=1010, size=860, anchor="start")}
    {_medallion_rings(t)}
    <text x="200" y="222" font-family="JetBrainsMono Nerd Font" font-size="28"
          letter-spacing="8" fill="{t['ink']}" fill-opacity="0.88">
      {esc(t['nickname'])}
    </text>
    <text x="200" y="302" font-family="Oswald" font-weight="300" font-size="34"
          letter-spacing="10" fill="{t['ink_dim']}" fill-opacity="0.55">
      {esc(t['stadium'])}
    </text>
    <rect x="200" y="1540" width="150" height="5" fill="{t['accent']}" opacity="0.9"/>
    <text x="194" y="1862" font-family="Anton" font-size="{msize}" letter-spacing="1"
          fill="{t['ink']}">{esc(t['mascot_name'])}</text>
    <text x="200" y="1966" font-family="Oswald" font-weight="600" font-size="52"
          letter-spacing="16" fill="{t['ink_dim']}">{esc(t['display'])}</text>
    <text x="203" y="2056" font-family="JetBrainsMono Nerd Font" font-size="24"
          letter-spacing="6" fill="{t['ink_dim']}" fill-opacity="0.55">
      MASCOTE OFICIAL
    </text>
    {_footer(t)}
    <rect width="{W}" height="{H}" fill="url(#vig)"/>
    """
    return _doc(defs, body)


# ---------------------------------------------------------------- 4. caricatura
CAR_INK = "#101014"
CAR_SKIN = "#F6D9BC"
CAR_BALL_R = 104


def _mix(c1, c2, f):
    c1, c2 = c1.lstrip("#"), c2.lstrip("#")
    out = [round(int(c1[i:i + 2], 16) * (1 - f) + int(c2[i:i + 2], 16) * f)
           for i in (0, 2, 4)]
    return "#%02X%02X%02X" % tuple(out)


def _rg(id_, c0, c1, cx=0.36, cy=0.30, r=1.05):
    return (f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}">'
            f'<stop offset="0" stop-color="{c0}"/>'
            f'<stop offset="1" stop-color="{c1}"/></radialGradient>')


def _lg(id_, c0, c1, x1=0, y1=0, x2=0, y2=1):
    return (f'<linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{c0}"/>'
            f'<stop offset="1" stop-color="{c1}"/></linearGradient>')


def _ball(x, y, r=None, dark=CAR_INK, light="#FAFAFC"):
    import math
    r = r or CAR_BALL_R
    pent = " ".join(
        f"{x + r * 0.36 * math.cos(math.radians(-90 + 72 * k)):.0f},"
        f"{y + r * 0.36 * math.sin(math.radians(-90 + 72 * k)):.0f}"
        for k in range(5))
    return f"""
    <circle cx="{x}" cy="{y}" r="{r}" fill="{light}"/>
    <polygon points="{pent}" fill="{dark}"/>
    <g stroke="{dark}" stroke-width="{int(r * 0.07)}">
      {''.join(f'<line x1="{x + r * 0.36 * math.cos(math.radians(-90 + 72 * k)):.0f}" y1="{y + r * 0.36 * math.sin(math.radians(-90 + 72 * k)):.0f}" x2="{x + r * 0.97 * math.cos(math.radians(-90 + 72 * k)):.0f}" y2="{y + r * 0.97 * math.sin(math.radians(-90 + 72 * k)):.0f}"/>' for k in range(5))}
    </g>
    <circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{dark}" stroke-width="9"/>"""


def _badge(x, y, w, h, fill, label, tcolor):
    return f"""
    <path d="M {x} {y} L {x + w} {y} L {x + w} {y + h * 0.45}
             C {x + w} {y + h * 0.72} {x + w / 2} {y + h} {x + w / 2} {y + h}
             C {x + w / 2} {y + h} {x} {y + h * 0.72} {x} {y + h * 0.45} Z"
          fill="{fill}" stroke="{CAR_INK}" stroke-width="9"/>
    <text x="{x + w / 2}" y="{y + h * 0.56}" font-family="Anton" font-size="{h * 0.30:.0f}"
          text-anchor="middle" fill="{tcolor}" letter-spacing="2">{label}</text>"""


def _eye(x, y, rx=34, ry=44, iris="#1C1D22"):
    return f"""
    <ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#FFFFFF"/>
    <ellipse cx="{x - 5}" cy="{y + 7}" rx="{rx * 0.52:.0f}" ry="{ry * 0.55:.0f}" fill="{iris}"/>
    <circle cx="{x - 9}" cy="{y + 2}" r="{rx * 0.22:.0f}" fill="#0C0D10"/>
    <circle cx="{x - 16}" cy="{y - 15}" r="{rx * 0.24:.0f}" fill="#FFFFFF"/>
    <circle cx="{x + 8}" cy="{y + 28}" r="{rx * 0.10:.0f}" fill="#FFFFFF" opacity="0.85"/>"""


def _mouth(x, y, w=132, h=88):
    return f"""
    <path d="M {x - w / 2} {y} A {w / 2} {h} 0 0 0 {x + w / 2} {y} Z"
          fill="#43121E" stroke="{CAR_INK}" stroke-width="8"/>
    <rect x="{x - w / 2 + 9}" y="{y - 3}" width="{w - 18}" height="20" rx="9" fill="#FFFFFF"/>
    <path d="M {x - w * 0.26} {y + h * 0.55} A {w * 0.28} {h * 0.32} 0 0 0 {x + w * 0.26} {y + h * 0.55} Z"
          fill="#E26D7A"/>"""


def _limb(x1, y1, x2, y2, color, w=54):
    """Membro cartoon: traço grosso com contorno escuro."""
    return (f'<path d="M {x1} {y1} L {x2} {y2}" fill="none" stroke="{CAR_INK}" '
            f'stroke-width="{w + 13}" stroke-linecap="round"/>'
            f'<path d="M {x1} {y1} L {x2} {y2}" fill="none" stroke="{color}" '
            f'stroke-width="{w}" stroke-linecap="round"/>')


def _particles(t, pts):
    out = []
    for (x, y, r) in pts:
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{t["accent"]}" opacity="0.14"/>')
        out.append(f'<circle cx="{x}" cy="{y}" r="{r * 0.38:.0f}" fill="{t["accent_bright"]}" opacity="0.85"/>')
    return "".join(out)


# ------------------------------------------------------------------ santos
def _car_santos(t):
    ink = "#101014"
    white = "#FDFDFD"
    body_c0, body_c1 = "#2C2F36", "#131419"
    defs = (_rg("wBody", body_c0, body_c1)
            + _lg("wBelly", "#FFFFFF", "#C6CBD4")
            + _lg("wGloss", "#FFFFFF", "#FFFFFF", 0, 0, 0, 1))
    gloss = f"""
    <ellipse cx="360" cy="470" rx="180" ry="110" fill="url(#wGloss)"
             opacity="0.12" transform="rotate(-14 360 470)"/>"""
    body = f"""
    <path d="M 660 1180 C 762 1120 852 1140 872 1232 C 884 1300 822 1342 742 1330 Z" fill="{ink}"/>
    <path d="M 680 1262 C 782 1262 852 1302 852 1382 C 842 1424 780 1424 718 1382 Z" fill="{ink}"/>
    <ellipse cx="500" cy="790" rx="340" ry="490" fill="url(#wBody)"/>
    <clipPath id="carClip"><ellipse cx="500" cy="790" rx="340" ry="490"/></clipPath>
    <g clip-path="url(#carClip)">
      <ellipse cx="500" cy="1075" rx="262" ry="240" fill="url(#wBelly)"/>
      <ellipse cx="392" cy="580" rx="182" ry="132" fill="#FDFDFD"/>
      <rect x="352" y="756" width="308" height="330" rx="64" fill="#FDFDFD"/>
      <clipPath id="carBib"><rect x="352" y="756" width="308" height="330" rx="64"/></clipPath>
      <g clip-path="url(#carBib)">
        <g fill="none" stroke="{ink}" stroke-width="40">
          <path d="M 386 750 C 380 900 380 1060 386 1090"/>
          <path d="M 462 748 C 456 900 456 1060 462 1090"/>
          <path d="M 538 748 C 532 900 532 1060 538 1090"/>
          <path d="M 614 750 C 608 900 608 1060 614 1090"/>
        </g>
      </g>
      {gloss}
    </g>
    <ellipse cx="500" cy="790" rx="340" ry="490" fill="none" stroke="{ink}" stroke-width="18"/>
    {_badge(448, 836, 116, 140, ink, "SFC", "#FFFFFF")}
    {_eye(368, 452, rx=40, ry=49)}
    {_eye(596, 452, rx=40, ry=49)}
    <path d="M 500 330 C 478 260 512 220 496 152" fill="none" stroke="#FDFDFD"
          stroke-width="14" stroke-linecap="round"/>
    <circle cx="462" cy="140" r="14" fill="#FDFDFD"/>
    <circle cx="540" cy="120" r="10" fill="#FDFDFD"/>
    <circle cx="500" cy="96" r="7" fill="#FDFDFD"/>
    {_mouth(500, 618, w=142, h=92)}
    <path d="M 332 806 C 278 848 246 916 250 984 C 252 1024 290 1034 310 998
             C 328 958 334 896 360 838 Z" fill="url(#wBody)" stroke="{ink}" stroke-width="13"/>
    {_ball(250, 1218)}
    """
    return defs, body


# ------------------------------------------------------------------ sao paulo
def _car_saopaulo(t):
    ink = "#101014"
    red = t["accent"]
    robe = "#FDFDFD"
    hair = "#5B4128"
    defs = (_rg("wSkin", "#FFE3C4", "#E3AC80")
            + _lg("wRobe", "#FFFFFF", "#CDD0D7")
            + _lg("wGloss", "#FFFFFF", "#FFFFFF", 0, 0, 0, 1))
    body = f"""
    <ellipse cx="500" cy="128" rx="148" ry="38" fill="#FDFDFD" stroke="{ink}" stroke-width="13"/>
    <ellipse cx="500" cy="128" rx="148" ry="38" fill="none" stroke="#FDFDFD" stroke-width="30" opacity="0.16"/>
    <circle cx="500" cy="408" r="214" fill="url(#wSkin)" stroke="{ink}" stroke-width="16"/>
    <path d="M 288 390 C 294 258 380 194 500 194 C 620 194 706 258 712 390
             C 640 316 360 316 288 390 Z" fill="{hair}" stroke="{ink}" stroke-width="10"/>
    <path d="M 334 512 C 358 660 642 660 666 512 C 618 584 382 584 334 512 Z"
          fill="{hair}" stroke="{ink}" stroke-width="10"/>
    {_eye(432, 396, rx=32, ry=42)}
    {_eye(568, 396, rx=32, ry=42)}
    <path d="M 392 342 Q 432 326 472 340" fill="none" stroke="{ink}" stroke-width="11" stroke-linecap="round"/>
    <path d="M 528 340 Q 568 326 608 342" fill="none" stroke="{ink}" stroke-width="11" stroke-linecap="round"/>
    <path d="M 442 536 Q 500 584 558 536" fill="none" stroke="{ink}" stroke-width="12" stroke-linecap="round"/>
    <path d="M 500 664 C 388 692 350 844 332 1300 L 668 1300 C 650 844 612 692 500 664 Z"
          fill="url(#wRobe)" stroke="{ink}" stroke-width="16"/>
    <path d="M 452 686 L 566 1300 L 646 1300 L 520 680 Z" fill="{red}" stroke="{ink}" stroke-width="9"/>
    <rect x="332" y="1266" width="336" height="34" fill="{red}" stroke="{ink}" stroke-width="8"/>
    <path d="M 420 900 C 436 1010 432 1120 416 1240" fill="none" stroke="{ink}" stroke-width="8" opacity="0.12"/>
    <path d="M 600 880 C 616 1000 620 1120 608 1240" fill="none" stroke="{ink}" stroke-width="8" opacity="0.12"/>
    {_limb(628, 746, 772, 540, robe, w=54)}
    <circle cx="786" cy="522" r="45" fill="url(#wSkin)" stroke="{ink}" stroke-width="10"/>
    {_limb(374, 758, 306, 956, robe, w=54)}
    <circle cx="296" cy="972" r="45" fill="url(#wSkin)" stroke="{ink}" stroke-width="10"/>
    {_badge(446, 862, 112, 134, "#FFFFFF", "SPFC", red)}
    <ellipse cx="438" cy="1306" rx="64" ry="28" fill="#5B4128" stroke="{ink}" stroke-width="8"/>
    <ellipse cx="576" cy="1306" rx="64" ry="28" fill="#5B4128" stroke="{ink}" stroke-width="8"/>
    {_ball(262, 1234)}
    """
    return defs, body


# ------------------------------------------------------------------ corinthians
def _car_corinthians(t):
    ink = "#101014"
    skin = CAR_SKIN
    defs = (_rg("wSkin", "#FFE3C4", "#E3AC80")
            + _lg("wGloss", "#FFFFFF", "#FFFFFF", 0, 0, 0, 1))
    body = f"""
    <path d="M 614 700 C 772 782 852 962 842 1210 L 692 1152 C 708 1002 670 862 576 778 Z"
          fill="{ink}"/>
    {_ball(262, 1236, r=106)}
    <path d="M 470 1030 L 322 1116" fill="none" stroke="{ink}" stroke-width="66" stroke-linecap="round"/>
    <ellipse cx="300" cy="1130" rx="92" ry="38" transform="rotate(-14 300 1130)" fill="{ink}"/>
    <rect x="552" y="1000" width="78" height="296" rx="32" fill="{ink}"/>
    <ellipse cx="596" cy="1312" rx="90" ry="38" fill="{ink}"/>
    <rect x="410" y="656" width="302" height="392" rx="82" fill="{ink}"/>
    <path d="M 448 664 L 548 762 L 648 664 Z" fill="#FDFDFD" stroke="{ink}" stroke-width="9"/>
    <rect x="424" y="984" width="274" height="26" rx="13" fill="#FDFDFD" stroke="{ink}" stroke-width="8"/>
    {_badge(452, 800, 108, 130, "#FDFDFD", "SCCP", ink)}
    {_limb(652, 736, 786, 566, ink, w=56)}
    <circle cx="800" cy="550" r="46" fill="url(#wSkin)" stroke="{ink}" stroke-width="10"/>
    <line x1="814" y1="526" x2="916" y2="284" stroke="{ink}" stroke-width="13" stroke-linecap="round"/>
    <line x1="918" y1="286" x2="898" y2="308" stroke="#FDFDFD" stroke-width="6" stroke-linecap="round"/>
    <line x1="852" y1="356" x2="912" y2="384" stroke="{ink}" stroke-width="10" stroke-linecap="round"/>
    {_limb(416, 740, 328, 862, ink, w=56)}
    <circle cx="318" cy="878" r="46" fill="url(#wSkin)" stroke="{ink}" stroke-width="10"/>
    <circle cx="500" cy="432" r="208" fill="url(#wSkin)" stroke="{ink}" stroke-width="16"/>
    <ellipse cx="500" cy="254" rx="266" ry="52" fill="{ink}"/>
    <path d="M 378 252 C 388 150 612 150 622 252 Z" fill="{ink}"/>
    <path d="M 640 236 C 744 170 784 100 772 38 C 728 86 672 162 620 224 Z"
          fill="#FDFDFD" stroke="{ink}" stroke-width="10"/>
    {_eye(436, 414, rx=30, ry=38)}
    {_eye(564, 414, rx=30, ry=38)}
    <path d="M 396 366 Q 436 350 476 362" fill="none" stroke="{ink}" stroke-width="11" stroke-linecap="round"/>
    <path d="M 524 362 Q 564 350 604 366" fill="none" stroke="{ink}" stroke-width="11" stroke-linecap="round"/>
    <path d="M 500 510 C 452 486 412 502 404 530 C 430 536 464 534 500 526 Z"
          fill="#4A3623" stroke="{ink}" stroke-width="7"/>
    <path d="M 500 510 C 548 486 588 502 596 530 C 570 536 536 534 500 526 Z"
          fill="#4A3623" stroke="{ink}" stroke-width="7"/>
    <path d="M 476 566 C 486 622 514 622 524 566 C 508 578 492 578 476 566 Z"
          fill="#4A3623" stroke="{ink}" stroke-width="7"/>
    {_particles(t, [(950, 330, 24), (1050, 720, 18), (890, 1140, 22)])}
    """
    return defs, body


# ------------------------------------------------------------------ palmeiras
def _car_palmeiras(t):
    ink = "#101014"
    g1, g2, light = "#0E7A44", "#0B5A31", "#E7F6EC"
    defs = (_rg("wBody", "#3FAE72", "#0E5A34")
            + _lg("wBelly", light, "#9CCBAF")
            + _lg("wBeak", "#F4BE4E", "#D3861A")
            + _lg("wGloss", "#FFFFFF", "#FFFFFF", 0, 0, 0, 1))
    body = f"""
    <path d="M 622 1072 C 742 1132 812 1222 832 1322 L 720 1292 C 700 1212 670 1152 616 1108 Z"
          fill="{g2}" stroke="{ink}" stroke-width="12"/>
    <path d="M 598 1112 C 698 1182 738 1256 746 1332 L 656 1308 C 654 1232 632 1172 588 1128 Z"
          fill="{g1}" stroke="{ink}" stroke-width="12"/>
    {_ball(252, 1300, r=104)}
    <path d="M 470 1140 L 330 1216" fill="none" stroke="{ink}" stroke-width="30" stroke-linecap="round"/>
    <ellipse cx="308" cy="1222" rx="54" ry="23" transform="rotate(-13 308 1222)"
             fill="#E8A33C" stroke="{ink}" stroke-width="8"/>
    <path d="M 556 1140 L 596 1276" fill="none" stroke="{ink}" stroke-width="30" stroke-linecap="round"/>
    <ellipse cx="602" cy="1290" rx="54" ry="23" fill="#E8A33C" stroke="{ink}" stroke-width="8"/>
    <ellipse cx="500" cy="970" rx="246" ry="302" fill="url(#wBody)"/>
    <clipPath id="carClip"><ellipse cx="500" cy="970" rx="246" ry="302"/></clipPath>
    <g clip-path="url(#carClip)">
      <ellipse cx="500" cy="1090" rx="176" ry="200" fill="url(#wBelly)"/>
      <path d="M 444 676 L 500 748 L 556 676 Z" fill="{light}"/>
      <ellipse cx="330" cy="760" rx="120" ry="200" fill="#FFFFFF" opacity="0.08"/>
    </g>
    <ellipse cx="500" cy="970" rx="246" ry="302" fill="none" stroke="{ink}" stroke-width="18"/>
    {_badge(444, 782, 112, 134, "#FDFDFD", "SEP", g1)}
    <path d="M 338 820 C 300 892 286 992 300 1072 C 306 1118 342 1124 358 1088
             C 382 1020 394 908 398 826 Z" fill="{g2}" stroke="{ink}" stroke-width="13"/>
    {_limb(652, 806, 830, 590, g2, w=52)}
    <path d="M 796 560 C 776 512 800 480 836 496 C 868 512 862 566 826 594 Z"
          fill="{g2}" stroke="{ink}" stroke-width="10"/>
    <circle cx="500" cy="392" r="224" fill="url(#wBody)" stroke="{ink}" stroke-width="16"/>
    <ellipse cx="500" cy="500" rx="150" ry="106" fill="{light}"/>
    <path d="M 396 250 C 382 172 432 144 462 212 Z" fill="{g2}" stroke="{ink}" stroke-width="10"/>
    <path d="M 480 236 C 478 152 532 152 524 232 Z" fill="{t['accent']}" stroke="{ink}" stroke-width="10"/>
    <path d="M 546 244 C 570 166 624 176 614 250 Z" fill="{g1}" stroke="{ink}" stroke-width="10"/>
    {_eye(420, 404, rx=33, ry=43)}
    {_eye(580, 404, rx=33, ry=43)}
    <path d="M 380 344 Q 420 328 460 340" fill="none" stroke="{ink}" stroke-width="10" stroke-linecap="round"/>
    <path d="M 540 340 Q 580 328 620 344" fill="none" stroke="{ink}" stroke-width="10" stroke-linecap="round"/>
    <path d="M 452 512 C 536 496 568 526 548 570 C 528 606 462 604 444 558
             C 438 534 442 514 452 512 Z" fill="url(#wBeak)" stroke="{ink}" stroke-width="10"/>
    <circle cx="492" cy="532" r="9" fill="#8A5A18"/>
    {_particles(t, [(950, 310, 24), (1050, 700, 18), (890, 1120, 22)])}
    """
    return defs, body


CARICATURES = {
    "santos": _car_santos,
    "sao-paulo": _car_saopaulo,
    "corinthians": _car_corinthians,
    "palmeiras": _car_palmeiras,
}


def caricatura_svg(t, photo_box_x=1450):
    """Mascote cartoon de clube: badge circular + personagem padronizado."""
    n = len(t["mascot_name"])
    msize = 250 if n <= 7 else (200 if n <= 9 else 158)
    extra_defs, character = CARICATURES[t["slug"]](t)
    disc0 = _mix("#FFFFFF", t["accent"], 0.10)
    disc1 = _mix("#FFFFFF", t["accent"], 0.34)
    defs = _defs_common(t) + f"""
    <linearGradient id="splitGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['accent']}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="glowR" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{t['accent']}" stop-opacity="0.22"/>
      <stop offset="0.55" stop-color="{t['accent']}" stop-opacity="0.07"/>
      <stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="discGrad" cx="0.38" cy="0.30" r="1.05">
      <stop offset="0" stop-color="{disc0}"/><stop offset="1" stop-color="{disc1}"/>
    </radialGradient>
    {extra_defs}
    """
    body = f"""
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <ellipse cx="2900" cy="1120" rx="1500" ry="1400" fill="url(#glowR)"/>
    <path d="M {photo_box_x - 260} 2160 L 3840 260 L 3840 2160 Z" fill="url(#splitGrad)" opacity="0.55"/>
    {_ghost_monogram(t, x=150, y=1010, size=860, anchor="start")}
    <text x="200" y="222" font-family="JetBrainsMono Nerd Font" font-size="28"
          letter-spacing="8" fill="{t['ink']}" fill-opacity="0.88">
      {esc(t['nickname'])}
    </text>
    <text x="200" y="302" font-family="Oswald" font-weight="300" font-size="34"
          letter-spacing="10" fill="{t['ink_dim']}" fill-opacity="0.55">
      {esc(t['stadium'])}
    </text>
    <ellipse cx="2700" cy="1806" rx="560" ry="48" fill="#000000" opacity="0.40"/>
    <circle cx="2700" cy="1130" r="630" fill="url(#discGrad)"/>
    <circle cx="2700" cy="1130" r="630" fill="none" stroke="{t['accent']}" stroke-width="10" opacity="0.9"/>
    <circle cx="2700" cy="1130" r="594" fill="none" stroke="{t['accent']}" stroke-width="3" opacity="0.35"/>
    <g transform="translate(2200,470)">{character}</g>
    <rect x="200" y="1540" width="150" height="5" fill="{t['accent']}" opacity="0.9"/>
    <text x="194" y="1862" font-family="Anton" font-size="{msize}" letter-spacing="1"
          fill="{t['ink']}">{esc(t['mascot_name'])}</text>
    <text x="200" y="1966" font-family="Oswald" font-weight="600" font-size="52"
          letter-spacing="16" fill="{t['ink_dim']}">{esc(t['display'])}</text>
    <text x="203" y="2056" font-family="JetBrainsMono Nerd Font" font-size="24"
          letter-spacing="6" fill="{t['ink_dim']}" fill-opacity="0.55">
      CARICATURA · MASCOTE
    </text>
    {_footer(t)}
    <rect width="{W}" height="{H}" fill="url(#vig)"/>
    """
    return _doc(defs, body)


def fade_svg(t, photo_x=1450, photo_w=2390):
    bg = t["bg"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">
      <defs>
        <linearGradient id="fl" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="{bg}" stop-opacity="1"/>
          <stop offset="0.42" stop-color="{bg}" stop-opacity="0.55"/>
          <stop offset="1" stop-color="{bg}" stop-opacity="0"/>
        </linearGradient>
        <linearGradient id="fb" x1="0" y1="1" x2="0" y2="0">
          <stop offset="0" stop-color="{bg}" stop-opacity="1"/>
          <stop offset="0.35" stop-color="{bg}" stop-opacity="0.7"/>
          <stop offset="1" stop-color="{bg}" stop-opacity="0"/>
        </linearGradient>
        <linearGradient id="ft" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="{bg}" stop-opacity="0.85"/>
          <stop offset="1" stop-color="{bg}" stop-opacity="0"/>
        </linearGradient>
      </defs>
      <rect x="{photo_x}" y="0" width="{photo_w}" height="{H}" fill="url(#fl)"/>
      <rect x="{photo_x}" y="1420" width="{photo_w}" height="740" fill="url(#fb)"/>
      <rect x="{photo_x}" y="0" width="{photo_w}" height="360" fill="url(#ft)"/>
    </svg>"""


# ---------------------------------------------------------------- preview
def preview_overlay_svg(t):
    pw, ph = 1800, 1012
    chips = [t["accent"], t["palette"]["red"], t["palette"]["yellow"],
             t["palette"]["green"], t["palette"]["blue"], t["palette"]["magenta"]]
    chip_svg = "".join(
        f'<rect x="{92 + i*78}" y="112" width="64" height="12" rx="4" fill="{c}" opacity="0.95"/>'
        for i, c in enumerate(chips)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{pw}" height="{ph}">
      <defs>
        <linearGradient id="pv" x1="0" y1="1" x2="0" y2="0">
          <stop offset="0" stop-color="{t['bg_deep']}" stop-opacity="0.72"/>
          <stop offset="0.42" stop-color="{t['bg_deep']}" stop-opacity="0.18"/>
          <stop offset="1" stop-color="{t['bg_deep']}" stop-opacity="0"/>
        </linearGradient>
      </defs>
      <rect width="{pw}" height="{ph}" fill="url(#pv)"/>
      <text x="1712" y="66" text-anchor="end" font-family="JetBrainsMono Nerd Font"
            font-size="22" letter-spacing="6" fill="{t['ink']}" fill-opacity="0.72">
        {esc(t['nickname'].upper())}
      </text>
      {chip_svg}
    </svg>"""


# The fourth wallpaper embeds generated raster art; SVG only lays out real
# club crests and typography. Missing generated art is an explicit error.
def caricatura_svg(t, photo_box_x=1450):
    from mascote_cartoon import render

    return render(t)
