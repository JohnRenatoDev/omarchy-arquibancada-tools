"""Team data for the Brasileirão theme pack.

Each entry drives: colors.toml (UI + terminal palette), wallpaper art,
preview card, icon theme and keyboard colour.
"""

FOUNDATION = {
    "santos": dict(year=1912, stadium="VILA BELMIRO", city="SANTOS · SP", nickname="O PEIXE"),
    "sao-paulo": dict(year=1930, stadium="MORUMBIS", city="SÃO PAULO · SP", nickname="O SOBERANO"),
    "corinthians": dict(year=1910, stadium="NEO QUÍMICA ARENA", city="SÃO PAULO · SP", nickname="O TIMÃO"),
    "palmeiras": dict(year=1914, stadium="NUBANK PARQUE", city="SÃO PAULO · SP", nickname="O VERDÃO"),
}

TEAMS = {
    "santos": dict(
        slug="santos",
        display="SANTOS",
        subtitle="FUTEBOL CLUBE",
        monogram="SFC",
        # Art direction — alvinegro: preto e branco. O dourado aparece apenas no
        # próprio escudo (coroa e estrelas), nunca na paleta do tema.
        accent="#F1F2F4",
        accent_bright="#FFFFFF",
        ink="#F1F1F3",
        ink_dim="#9A9DA4",
        bg="#0B0B0C",
        bg_deep="#050506",
        motif="waves",
        crest="crests/santos.png",
        crest_bg="#151210",
        mascot="mascots/santos-baleia.jpg",
        mascot_kind="photo",
        mascot_name="BALEIA",
        mascot_gravity="center",
        duo_dark="#08080a",
        duo_light="#F5F5F7",
        icons="Yaru-dark",
        # colors.toml
        palette=dict(
            foreground="#D9DADE",
            dark_foreground="#8B8E95",
            light_foreground="#EAEBEF",
            bright_foreground="#FFFFFF",
            selection="#26282D",
            muted="#4A4D54",
            red="#E06C75",
            yellow="#E5C07B",
            orange="#D19A66",
            green="#98C379",
            cyan="#56B6C2",
            blue="#82A7E0",
            magenta="#C678DD",
            brown="#9A7B5F",
            bright_red="#FF828C",
            bright_yellow="#F2D28D",
            bright_green="#B3DA96",
            bright_cyan="#6FC9D5",
            bright_blue="#9BBDF2",
            bright_magenta="#D79BE8",
        ),
    ),
    "sao-paulo": dict(
        slug="sao-paulo",
        display="SÃO PAULO",
        subtitle="FUTEBOL CLUBE",
        monogram="SPFC",
        accent="#E2374A",
        accent_bright="#FF6F7D",
        ink="#F2ECEC",
        ink_dim="#A89C9E",
        bg="#120A0B",
        bg_deep="#0A0506",
        motif="tricolor",
        crest="crests/sao-paulo.svg",
        crest_bg="#1A0D0F",
        mascot="mascots/sao-paulo-elgreco.jpg",
        mascot_kind="photo",
        mascot_name="SANTINHO",
        mascot_gravity="north",
        duo_dark="#120a0b",
        duo_light="#E9CFC9",
        icons="Yaru-red-dark",
        palette=dict(
            foreground="#E6DEDE",
            dark_foreground="#9C8F91",
            light_foreground="#F2E9E9",
            bright_foreground="#FFFFFF",
            selection="#33181C",
            muted="#6B4A50",
            red="#E5484D",
            yellow="#E5C07B",
            orange="#E08A5F",
            green="#8FBF8A",
            cyan="#5FB8C4",
            blue="#6E9FD8",
            magenta="#C678B8",
            brown="#A07A68",
            bright_red="#FF6B70",
            bright_yellow="#F2D08C",
            bright_green="#A8D6A2",
            bright_cyan="#79D0DB",
            bright_blue="#8FBBEF",
            bright_magenta="#DD93CD",
        ),
    ),
    "corinthians": dict(
        slug="corinthians",
        display="CORINTHIANS",
        subtitle="SPORT CLUB PAULISTA",
        monogram="SCCP",
        accent="#E9EBEF",
        accent_bright="#FFFFFF",
        ink="#F0F1F3",
        ink_dim="#9AA0A9",
        bg="#0A0A0C",
        bg_deep="#050506",
        motif="shards",
        crest="crests/corinthians-2026.png",
        crest_bg="#111114",
        mascot="mascots/corinthians-mosqueteiro.jpg",
        mascot_kind="photo",
        mascot_name="MOSQUETEIRO",
        mascot_gravity="north",
        duo_dark="#0a0a0c",
        duo_light="#EDEFF3",
        icons="Yaru-dark",
        palette=dict(
            foreground="#D9DADC",
            dark_foreground="#8B9098",
            light_foreground="#EBECEF",
            bright_foreground="#FFFFFF",
            selection="#24262B",
            muted="#4A4D54",
            red="#E06C75",
            yellow="#E5C07B",
            orange="#D6A97A",
            green="#9BBF8A",
            cyan="#6FB3C0",
            blue="#7EA6E8",
            magenta="#B894D6",
            brown="#9A8574",
            bright_red="#FF828C",
            bright_yellow="#F2D28D",
            bright_green="#B2D6A2",
            bright_cyan="#89CBD7",
            bright_blue="#9BBFF2",
            bright_magenta="#CFA9E8",
        ),
    ),
    "palmeiras": dict(
        slug="palmeiras",
        display="PALMEIRAS",
        subtitle="SOCIEDADE ESPORTIVA",
        monogram="SEP",
        accent="#35B36F",
        accent_bright="#63DFA2",
        ink="#EAF2EC",
        ink_dim="#93A79B",
        bg="#06110B",
        bg_deep="#030805",
        motif="rings",
        crest="crests/palmeiras.svg",
        crest_bg="#0A1B11",
        mascot="mascots/palmeiras-periquito-real1.jpg",
        mascot_kind="photo",
        mascot_name="PERIQUITO",
        mascot_gravity="center",
        duo_dark="#03150C",
        duo_light="#9FE8BE",
        icons="Yaru-prussiangreen-dark",
        palette=dict(
            foreground="#D5E2D9",
            dark_foreground="#879B8E",
            light_foreground="#E7F0E9",
            bright_foreground="#FFFFFF",
            selection="#10291B",
            muted="#3E6B52",
            red="#E06C75",
            yellow="#E3C77B",
            orange="#D79A66",
            green="#4CC38A",
            cyan="#55B8B0",
            blue="#6FA8DC",
            magenta="#B48EAD",
            brown="#8A6A4F",
            bright_red="#FF828C",
            bright_yellow="#F2D892",
            bright_green="#63DFA2",
            bright_cyan="#6BD3CB",
            bright_blue="#8BC2F2",
            bright_magenta="#CB9FC4",
        ),
    ),
}


# Verified 2026 league expansion. Copy base palette structures so clubs do not
# share mutable terminal colour dictionaries. Existing four entries stay intact.
import copy
import json
from pathlib import Path

EXPANSION = json.loads(Path(__file__).with_name('serie_a_2026.json').read_text())
for spec in EXPANSION:
    slug = spec['slug']
    entry = copy.deepcopy(TEAMS[spec['template']])
    entry.update({k: v for k, v in spec.items() if k not in ('template', 'espn_id')})
    entry.update(
        crest=f'crests/{slug}.png',
        mascot=f'mascotes-generated/{slug}.png',
        mascot_kind='generated', mascot_gravity='center',
        bg_deep=spec['bg'], crest_bg=spec['bg'], duo_dark=spec['bg'],
        duo_light=spec['ink'], accent_bright=spec['ink'],
    )
    def blend(a, b, amount):
        x = [int(a[i:i+2],16) for i in (1,3,5)]
        y = [int(b[i:i+2],16) for i in (1,3,5)]
        return '#' + ''.join(f'{round(u*(1-amount)+v*amount):02X}' for u,v in zip(x,y))
    entry['ink_dim'] = blend(spec['bg'], spec['ink'], 0.62)
    entry['palette'].update(foreground=spec['ink'], light_foreground=spec['ink'],
                            bright_foreground='#FFFFFF',
                            selection=blend(spec['bg'],spec['accent'],0.20),
                            muted=blend(spec['bg'],spec['ink'],0.35))
    if spec['template'] == 'corinthians':
        entry['icons'] = 'Yaru-dark'
    TEAMS[slug] = entry
    FOUNDATION[slug] = {k: spec[k] for k in ('year', 'stadium', 'city', 'nickname')}

# Stadium labels and primary-source checks live in one maintained manifest.
STADIUMS = json.loads(Path(__file__).with_name('estadios.json').read_text())
for slug, stadium in STADIUMS.items():
    FOUNDATION[slug]['stadium'] = stadium['label']


# First four remain at the front to keep their familiar preview order.
TEAM_ORDER = ('santos', 'corinthians', 'palmeiras', 'sao-paulo') + tuple(
    spec['slug'] for spec in EXPANSION)


def team(slug):
    t = dict(TEAMS[slug])
    t.update(FOUNDATION[slug])
    t["theme_name"] = slug.replace("-", " ").title()
    return t


def slug_to_title(slug):
    return slug.replace("-", " ").title()
