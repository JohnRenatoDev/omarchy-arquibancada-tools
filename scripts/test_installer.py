"""Install from a separate checkout without touching the real user profile."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

INSTALLER = Path(__file__).resolve().parents[1] / 'install.sh'


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='arquibancada-install-')
        self.root = Path(self.temporary.name)
        self.source = self.root / 'theme checkout'
        self.source.mkdir()
        (self.source / 'colors.toml').write_text('mode = "dark"\n')
        for slug in ('santos', 'corinthians'):
            club = self.source / 'themes' / slug
            for name in ('colors.toml', 'preview.png', 'backgrounds/1-arte.jpg',
                         'backgrounds/2-escudo.jpg', 'backgrounds/3-mascote.jpg'):
                path = club / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f'installer fixture: {slug}/{name}\n')
        self.config = self.root / 'config'
        self.cache = self.root / 'cache'
        self.menu = self.config / 'extensions/omarchy-menu.jsonc'

    def tearDown(self):
        self.temporary.cleanup()

    def install(self, *options, source=None):
        return subprocess.run(
            ['bash', str(INSTALLER), '--source', str(source or self.source),
             '--config-dir', str(self.config), '--cache-root', str(self.cache), *options],
            capture_output=True, text=True, check=True)

    def test_external_source_links_menu_backup_and_idempotence(self):
        self.menu.parent.mkdir(parents=True)
        original = '{"existing": {"label": "Keep me"}}\n'
        self.menu.write_text(original)
        selector = self.cache / 'omarchy/theme-selector'
        selector.mkdir(parents=True)
        (selector / 'old').write_text('cache')
        self.install('--link', '--menu')
        target = self.config / 'themes/santos'
        self.assertTrue(target.is_symlink())
        self.assertEqual(target.resolve(), self.source / 'themes/santos')
        menu = json.loads(self.menu.read_text())
        self.assertIn('existing', menu)
        self.assertEqual(menu['clubes.santos']['action'], 'omarchy theme set santos')
        backups = list(self.menu.parent.glob('*.bak.*'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), original)
        self.assertFalse(selector.exists())
        before = self.menu.read_bytes()
        self.install('--link', '--menu')
        self.assertEqual(self.menu.read_bytes(), before)
        self.assertEqual(list(self.menu.parent.glob('*.bak.*')), backups)

    def test_copy_is_independent_and_existing_local_themes_are_preserved(self):
        self.install('--copy')
        target = self.config / 'themes/santos'
        self.assertFalse(target.is_symlink())
        self.assertEqual((target / 'colors.toml').read_bytes(),
                         (self.source / 'themes/santos/colors.toml').read_bytes())
        (target / 'personal.txt').write_text('keep this independent copy')
        self.install('--link')
        self.assertFalse(target.is_symlink())
        self.assertEqual((target / 'personal.txt').read_text(), 'keep this independent copy')

    def test_missing_source_is_rejected_before_configuration_changes(self):
        with self.assertRaises(subprocess.CalledProcessError):
            self.install(source=self.root / 'missing')
        self.assertFalse(self.config.exists())


if __name__ == '__main__':
    unittest.main()
