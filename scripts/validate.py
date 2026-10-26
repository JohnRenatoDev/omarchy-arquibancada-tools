#!/usr/bin/env python3
"""Validate Arquibancada's native root theme and all 20 club packages offline."""
import json
import argparse
import hashlib
import re
import struct
import sys
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from badge_surface import validate_surface
REQUIRED = {'accent', 'background', 'foreground', 'red', 'yellow', 'green', 'cyan', 'blue', 'magenta'}
WALLPAPERS = ('1-arte.jpg', '2-escudo.jpg', '3-mascote.jpg')


def validate_distribution(directory):
    """Require a data-only theme tree, including nested directories."""
    result = subprocess.run(['git', '-C', str(directory), 'rev-parse', '--show-toplevel'],
                            capture_output=True, text=True)
    if result.returncode == 0 and Path(result.stdout.strip()).resolve() == directory:
        names = subprocess.check_output(
            ['git', '-C', str(directory), 'ls-files', '--cached', '--others', '--exclude-standard', '-z']
        ).decode().split('\0')
        paths = [directory / name for name in names if name]
    else:
        paths = [p for p in directory.rglob('*') if '.git' not in p.relative_to(directory).parts]
    allowed = {'.md', '.png', '.jpg', '.jpeg', '.webp', '.toml', '.theme', '.rgb', '.json'}
    for path in paths:
        name = path.relative_to(directory).as_posix()
        assert not path.is_symlink(), f'Symlink in theme distribution: {name}'
        if not path.is_file():
            continue
        assert not name.startswith('.github/workflows/'), f'Workflow in theme distribution: {name}'
        assert not path.stat().st_mode & 0o111, f'Executable file in theme distribution: {name}'
        assert path.suffix.lower() in allowed or name in {'LICENSE', '.gitignore'}, f'Non-theme file: {name}'
        with path.open('rb') as stream:
            assert not stream.read(2) == b'#!', f'Script in theme distribution: {name}'


def dimensions(path):
    with path.open('rb') as f:
        header = f.read(24)
        if header[:8] == b'\x89PNG\r\n\x1a\n':
            return struct.unpack('>II', header[16:24])
        f.seek(0)
        if f.read(2) != b'\xff\xd8':
            raise ValueError(f'Unsupported image: {path}')
        while True:
            if f.read(1) != b'\xff':
                raise ValueError(f'Invalid JPEG marker: {path}')
            marker = f.read(1)
            while marker == b'\xff':
                marker = f.read(1)
            if marker in (b'\xd8', b'\xd9', b'\x01'):
                continue
            length = struct.unpack('>H', f.read(2))[0]
            if marker[0] in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                _, height, width = struct.unpack('>BHH', f.read(5))
                return width, height
            f.seek(length - 2, 1)


def validate_theme(directory, native=False):
    assert {p.name for p in (directory / 'backgrounds').iterdir()} == set(WALLPAPERS), f'Expected exactly three wallpapers: {directory}'
    colors = tomllib.loads((directory / 'colors.toml').read_text())
    assert REQUIRED <= colors.keys(), f'Missing palette keys: {directory}'
    assert colors.get('mode') in ('dark', 'light'), f'Missing/invalid mode: {directory}'
    assert all(re.fullmatch(r'#[0-9a-fA-F]{6}', value) for key, value in colors.items() if key != 'mode'), directory
    width, height = dimensions(directory / 'preview.png')
    assert width >= 1000 and abs(width / height - 16 / 9) < 0.005, directory
    if native:
        assert width * 9 == height * 16, 'Root preview must be exactly 16:9'
    for name in WALLPAPERS:
        path = directory / 'backgrounds' / name
        assert path.is_file() and not path.is_symlink(), path
        assert dimensions(path) == (3840, 2160), path
        assert path.stat().st_size <= 50 * 1024 * 1024, path
    for name in ('icons.theme', 'keyboard.rgb', 'shell.lock.toml'):
        assert (directory / name).is_file(), directory / name


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--theme-dir', required=True, type=Path,
                        help='Separate theme checkout or exported theme directory')
    args = parser.parse_args()
    theme_root = args.theme_dir.expanduser().resolve()
    assert theme_root != ROOT, 'The tools repository is not the theme distribution'
    validate_distribution(theme_root)
    validate_theme(theme_root, native=True)
    additions = json.loads((ROOT / 'src/serie_a_2026.json').read_text())
    expected = {'santos', 'corinthians', 'palmeiras', 'sao-paulo'} | {row['slug'] for row in additions}
    actual = {path.name for path in (theme_root / 'themes').iterdir() if path.is_dir()}
    assert len(expected) == 20 and actual == expected, 'Club roster mismatch'
    layouts = json.loads((ROOT / 'src/mascotes-layout.json').read_text())
    stadiums = json.loads((ROOT / 'src/estadios.json').read_text())
    assert set(layouts) == set(stadiums) == expected, 'Every club needs an explicit badge placement and stadium source'
    for slug in sorted(expected):
        validate_theme(theme_root / 'themes' / slug)
        source = ROOT / 'assets/mascotes-generated' / f'{slug}.png'
        assert source.is_file(), slug
        assert dimensions(source) == (1672, 941), f'Badge coordinates require the reviewed source frame: {slug}'
        assert (ROOT / 'assets' / layouts[slug]['badge']).is_file(), slug
        kit = layouts[slug]
        assert kit['application'] == 'native-shirt-surface', f'Unreviewed shirt pipeline: {slug}'
        assert kit['placement'] == ('central' if slug in ('sao-paulo', 'coritiba') else 'wearer-left'), slug
        assert kit['reference'].startswith('https://') and kit['reference_image'].startswith('https://'), slug
        assert kit['verified'] == '2026-10-20' and kit['visual_review'] is True, slug
        assert hashlib.sha256(source.read_bytes()).hexdigest() == kit['source_sha256'], f'Shirt art changed since visual review: {slug}'
        badge = ROOT / 'assets' / kit['badge']
        assert hashlib.sha256(badge.read_bytes()).hexdigest() == kit['badge_sha256'], f'Badge artwork changed since review: {slug}'
        surface = kit['shirt_surface']
        assert set(surface) == {'corners', 'curve'}, f'Explicit shirt surface required: {slug}'
        validate_surface(surface)
        assert 'badge_frame' not in kit, f'Flat sticker placement is obsolete: {slug}'
        assert not {'box', 'surface', 'cloth_shading'} & kit.keys(), f'Obsolete badge overlay: {slug}'
        assert stadiums[slug]['sources'] and stadiums[slug]['verified'] == '2026-10-19', slug
    for name in WALLPAPERS:
        assert (theme_root / 'backgrounds' / name).read_bytes() == (theme_root / 'themes/santos/backgrounds' / name).read_bytes(), 'Default mirror differs from Santos'
    assert (theme_root / 'colors.toml').read_bytes() == (theme_root / 'themes/santos/colors.toml').read_bytes()
    print('PASS: data-only distribution, native root layout, exact 16:9 preview, 20 palettes, exactly 60 club wallpapers, 20 garment/native badge hashes and valid shirt projections, sourced stadiums and default Santos mirror. Visual fidelity requires the separate image review.')


if __name__ == '__main__':
    main()
