"""Regression checks for the gallery's data-only distribution requirement."""
import tempfile
import unittest
from pathlib import Path

from validate import validate_distribution


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='arquibancada-data-')
        self.root = Path(self.temporary.name)
        (self.root / 'colors.toml').write_text('mode = "dark"\n')

    def tearDown(self):
        self.temporary.cleanup()

    def test_plain_theme_data_is_accepted(self):
        (self.root / 'README.md').write_text('Theme installation instructions.\n')
        validate_distribution(self.root)

    def test_code_is_rejected_in_nested_directories(self):
        nested = self.root / 'tools' / 'nested'
        nested.mkdir(parents=True)
        (nested / 'installer.py').write_text('print("not theme data")\n')
        with self.assertRaisesRegex(AssertionError, 'Non-theme file'):
            validate_distribution(self.root)

    def test_workflows_are_rejected(self):
        workflows = self.root / '.github' / 'workflows'
        workflows.mkdir(parents=True)
        (workflows / 'validate.yml').write_text('name: Validation\n')
        with self.assertRaisesRegex(AssertionError, 'Workflow'):
            validate_distribution(self.root)

    def test_scripts_cannot_be_disguised_as_documentation(self):
        (self.root / 'installer.md').write_text('#!/bin/sh\ntrue\n')
        with self.assertRaisesRegex(AssertionError, 'Script'):
            validate_distribution(self.root)

    def test_executables_and_symlinks_are_rejected(self):
        readme = self.root / 'README.md'
        readme.write_text('Documentation\n')
        readme.chmod(0o755)
        with self.assertRaisesRegex(AssertionError, 'Executable'):
            validate_distribution(self.root)
        readme.chmod(0o644)
        (self.root / 'linked.md').symlink_to(readme)
        with self.assertRaisesRegex(AssertionError, 'Symlink'):
            validate_distribution(self.root)


if __name__ == '__main__':
    unittest.main()
