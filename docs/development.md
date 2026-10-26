# Artwork and build notes

[README](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/../README.md) | [English](development.md) | [Português (Brasil)](development.pt-BR.md)

File paths below are relative to the repository root.

## Three wallpapers per club

The stadium names were checked against primary sources on October 19, 2026.
[docs/estadios.md](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/estadios.md) has the references and notes on temporary home
venues. Palmeiras uses Nubank Parque; São Paulo uses MorumBIS. The captions for
Palmeiras, São Paulo, Bahia and Mirassol have the updated stadium names.

All 20 kits were reviewed using photographs of the 2026 shirts, listed in
[docs/uniformes-2026.md](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/uniformes-2026.md). The October 20 review uses original
badge artwork projected onto each shirt's surface, following the chest's
perspective and curvature with fabric texture and lighting. Letters and stars
keep their original shapes. Placement, scale and spacing were reviewed for every
club. São Paulo and Coritiba have centered badges; the others use the wearer's
left chest. Flamengo uses the CRF monogram, Cruzeiro its five stars and Vasco the
cross inside the white sash. The surrounding wallpaper design uses the full club crest.

Internacional's Saci keeps his single leg planted on the grass and holds the ball
in his arm. Athletico uses Fura-Cão; Botafogo uses Bira; Bahia uses Homem
de Aço; Fluminense uses Guerreiro. The lions, birds and human characters have
their own kits, anatomy and colors. The shirts follow photographs of current
designs, and their symbols use separate original artwork. No sponsors were added.

## Files and previews

- `<output-dir>/themes/<slug>/`: palette, three JPEGs, preview and additional Omarchy files.
- `assets/mascotes-generated/<slug>.png`: 20 independent base illustrations.
- `assets/mascotes-generated/prompts.json`: prompts for the first four clubs.
- `assets/mascotes-generated/serie-a-2026-prompts.json`: prompts for the other 16
  clubs and framing corrections for Atlético-MG, Chapecoense, Cruzeiro and Fluminense.
- `assets/mascotes-generated/uniformes-2026-prompts.json`: prompts and references
  for all 20 shirt edits made with the integrated `image_gen` tool.
- `assets/crests/serie-a-2026-sources.json`: source URLs for the 16 added crests.
- `assets/kit-badges/`: shirt emblem variants, with sources in `sources.json`.
- `src/badge_surface.py`: projects the original emblem onto the shirt surface.
- `src/mascotes-layout.json`: kit model, anatomical placement, sources and hashes
  of each club's artwork and emblem, plus four shirt surface points and curvature
  values for projecting the original design to match the pose.
- [Current kits and review references](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/uniformes-2026.md).
- [Stadiums and official sources](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/estadios.md).
- [Close-up shirt review](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/uniformes-revisao.jpg).
- [All 20 posters](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/mascotes-cartoon.png).
- [All 60 wallpapers](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/preview.png), with one row per club and three columns.
- [Status and review](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/mascotes-status.md).
- [Integrity checks](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/serie-a-2026-verificacao.json).
- [Club identity sources](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/serie-a-2026-fontes.md).

## AI generation and resolution

The illustrations were generated with the integrated `image_gen` tool, using the
approved Santos artwork as a shared reference for style, camera angle and
lighting. The service does not expose its seed, step count or internal model
version. The native PNGs are 1672×941; the 3840×2160 JPEGs are proportional
upscales that keep the whole image in the frame. They are not native 4K generations.

Typography and crests in the wallpaper layout are composed separately at the
final resolution. Shirt emblems also use original artwork on a separate layer.
The base PNGs in `assets/mascotes-generated/` contain the shirt fabric without a
badge; the compositor produces the final wallpaper.

## Build the package

You need Python 3, ImageMagick, `rsvg-convert` and the Anton, Oswald and JetBrains
Mono fonts. The generated artwork is included, so the build needs no image
generator, GPU or token. A missing illustration produces an error; there is no
simplified SVG fallback.

```bash
nice -n 19 python3 src/build.py --output-dir ../omarchy-arquibancada-theme --mascotes-only  # só pôsteres e previews dos 20
nice -n 19 python3 src/build.py --output-dir ../omarchy-arquibancada-theme flamengo gremio    # todos os wallpapers desses clubes
nice -n 19 python3 src/build.py --output-dir ../omarchy-arquibancada-theme  # pacote completo
```

`src/teams.py` keeps the data for the original four clubs and loads the others from
`src/serie_a_2026.json`. To add a club, include its data, actual crest and a
separately generated and reviewed mascot illustration. Recoloring another club's
mascot is not enough.

The contact sheets use intermediate thumbnails so the build does not load all
60 4K wallpapers into memory at once. Exports preserve the illustrations' painted
texture without adding heavy synthetic noise.

## Separate source and theme repositories

This repository holds the programs, reviewed source images and fonts. The
[theme repository](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme) holds the finished palettes, wallpapers and
previews. The build writes only those outputs to `--output-dir`; intermediates
stay in this repository's ignored `build/` directory. The default export path is
`build/export`. A partial build needs an existing complete export for the gallery.

The theme root is the Santos variant. The 20 club variants are in
`<output-dir>/themes/<slug>/`. Building does not install or activate a theme.

To validate a separate checkout:

```bash
nice -n 19 python3 scripts/validate.py --theme-dir ../omarchy-arquibancada-theme
nice -n 19 python3 -m unittest discover -s scripts -p 'test_*.py'
nice -n 19 python3 scripts/validate_badge_regions.py
```

`install.sh --source <theme-checkout>` installs from the separate distribution.
Its `--menu` option needs Python 3. Link mode follows changes in the theme checkout.
Copy mode creates an independent snapshot; rerunning preserves an existing copy.
The installer tests use explicit temporary config and cache paths and leave the
real user profile alone.
