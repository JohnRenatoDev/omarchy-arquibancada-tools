# Arquibancada tools

[English](README.md) | [Português (Brasil)](README.pt-BR.md)

Artwork sources, wallpaper compositor, optional club installer and checks for
[Arquibancada](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme), the
Omarchy collection for the 20 clubs in the 2026 Brazilian Série A.

The finished theme is distributed in its own repository. These tools work with
a separate theme checkout. Generating or validating files does not activate a
theme on your desktop.

## Install the club themes

To install the default Santos variant through Omarchy, use the instructions in
the [theme repository](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme#installation).
The optional installer here adds all 20 club variants from a local checkout:

```bash
git clone https://github.com/JohnRenatoDev/omarchy-arquibancada-theme.git
git clone https://github.com/JohnRenatoDev/omarchy-arquibancada-tools.git
cd omarchy-arquibancada-tools
./install.sh --source ../omarchy-arquibancada-theme --link --menu
omarchy theme set flamengo
```

Keep the theme checkout in place when using links. The tools checkout supplies
the installer and club names; the links point to the theme checkout. `--menu`
adds missing club entries and backs up the existing menu. Running the same
command again leaves those entries alone.

Use `--copy` instead of `--link` for an independent copy. Existing local themes
stored as ordinary directories are preserved, including copies made by an earlier
run. The installer requires Bash and standard GNU file utilities; `--menu` also
requires Python 3. It runs as your normal user, without `sudo`.

## Build and review

You need Python 3.11 or newer, ImageMagick, `rsvg-convert`, and the Anton, Oswald
and JetBrains Mono fonts. Reviewed mascot images, crests and font license files
are included under `assets/`. Building uses saved artwork and needs no generator,
GPU or API token.

```bash
# Rebuild all wallpapers and previews in a separate checkout.
nice -n 19 python3 src/build.py --output-dir ../omarchy-arquibancada-theme

# Refresh only the mascot posters and previews in an existing complete checkout.
nice -n 19 python3 src/build.py --output-dir ../omarchy-arquibancada-theme --mascotes-only

# Validate the distribution and the reviewed source artwork.
nice -n 19 python3 scripts/validate.py --theme-dir ../omarchy-arquibancada-theme
nice -n 19 python3 -m unittest discover -s scripts -p 'test_*.py'
nice -n 19 python3 scripts/validate_badge_regions.py
```

Without `--output-dir`, a full build exports to the ignored `build/export/`.
A partial build needs a complete export for the clubs it does not rebuild, since
it refreshes the combined gallery. Intermediate files stay under `build/` in this
repository. Only finished visual files are written to the theme checkout.

The validator rejects programs, executable files, symlinks and workflows anywhere
in the theme distribution. It also checks all 20 palettes, exactly three 4K
wallpapers per club, the Santos root mirror and the hashes of the reviewed
illustrations and shirt emblems. The installer tests use temporary configuration
and cache directories; they do not change your desktop.

See the [build notes](docs/development.md), [art brief](docs/mascotes-brief.md) and
[shirt references](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/uniformes-2026.md).

## Contributing

Open a pull request here for changes to the compositor, installer, checks or
source artwork. Send palette and finished-wallpaper changes to the
[theme repository](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme).
Include a reference or before-and-after preview for visual changes.

The illustrations were generated with AI and reviewed for each club's identity.
None of them represents the author's club preference. The collection was made
for the Brazilian Omarchy community and supporters of every club in it.

## Rights and credits

Original code and scripts use MIT. Club names, crests, mascots and other marks
belong to their respective holders. This is an independent community project,
without endorsement from the clubs, ESPN or Omarchy. MIT does not grant rights
to those materials, including when they appear in AI-generated artwork.

Anton, Oswald and Archivo Black come from Google Fonts under SIL Open Font
License 1.1; their licenses are included in `assets/fonts/`. Source URLs and
shirt references accompany the inputs. See [LICENSE](LICENSE) and
[NOTICE.md](NOTICE.md).
