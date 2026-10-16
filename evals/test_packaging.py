"""Offline package regressions, including Python optimized mode."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '.zhixu', '__pycache__'))
        self.output = Path(self.temp.name) / 'plugin.zip'

    def package(self, optimized=False):
        return subprocess.run([sys.executable, *(['-O'] if optimized else []),
            str(self.root / 'scripts/package_claude_plugin.py'), '--output', str(self.output)],
            text=True, capture_output=True)

    def test_package_is_reproducible(self):
        first = self.package()
        self.assertEqual(first.returncode, 0, first.stderr)
        original = self.output.read_bytes()
        self.output.unlink()
        self.output.with_suffix('.verification.json').unlink()
        second = self.package(optimized=True)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(original, self.output.read_bytes())
        with zipfile.ZipFile(self.output) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(len(archive.namelist()), 21)

    def test_version_mismatch_rejected_in_optimized_mode(self):
        (self.root / 'VERSION').write_text('999.0.0\n')
        result = self.package(optimized=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())

    def test_symlinked_runtime_parent_is_rejected(self):
        refs = self.root / 'skills/adaptive-personal-ai-os/references'
        private = self.root / 'private-references'
        refs.rename(private)
        try:
            refs.symlink_to(private, target_is_directory=True)
        except OSError:
            self.skipTest('directory symlinks unavailable')
        result = self.package(optimized=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('do not follow symlinks', result.stderr)
        self.assertFalse(self.output.exists())

    def test_symlinked_stage_is_rejected(self):
        stage = self.root / '.zhixu'
        external = Path(self.temp.name) / 'external'
        external.mkdir()
        try:
            stage.symlink_to(external, target_is_directory=True)
        except OSError:
            self.skipTest('directory symlinks unavailable')
        result = self.package(optimized=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(external.iterdir()), [])

    def test_broken_runtime_link_rejected_in_optimized_mode(self):
        skill = self.root / 'skills/adaptive-personal-ai-os/SKILL.md'
        with skill.open('a') as stream:
            stream.write('\n[missing](references/not-shipped.md)\n')
        result = self.package(optimized=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())

    def test_non_text_or_blank_description_rejected(self):
        skill = self.root / 'skills/adaptive-personal-ai-os/SKILL.md'
        original = skill.read_text()
        import re
        for value in ['[]', 'null', '"   "']:
            skill.write_text(re.sub(r'(?m)^description:.*$', 'description: ' + value, original))
            result = self.package(optimized=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('description must be', result.stderr)
            self.assertFalse(self.output.exists())

    def test_body_text_cannot_supply_missing_frontmatter_metadata(self):
        skill = self.root / 'skills/adaptive-personal-ai-os/SKILL.md'
        original = skill.read_text()
        import re
        for index, pattern in enumerate([r'^name:.*$', r'^description:.*$', r'^  version:.*$']):
            with self.subTest(pattern=pattern):
                self.output = Path(self.temp.name) / f'metadata-{index}.zip'
                line = re.search(pattern, original, re.MULTILINE).group(0)
                skill.write_text(re.sub(pattern, '', original, count=1, flags=re.MULTILINE)
                                 + '\n' + line + '\n')
                result = self.package(optimized=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(self.output.exists())

    def test_nonportable_version_rejected_before_packaging(self):
        (self.root / 'skills/adaptive-personal-ai-os/VERSION').write_text('../outside')
        result = self.package(optimized=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('portable semantic version', result.stderr)
        self.assertFalse(self.output.exists())

    def test_existing_report_preserved_in_optimized_mode(self):
        report = self.output.with_suffix('.verification.json')
        report.write_text('keep existing evidence')
        result = self.package(optimized=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(report.read_text(), 'keep existing evidence')
        self.assertFalse(self.output.exists())

    def test_release_output_preserved_in_optimized_mode(self):
        output = Path(self.temp.name) / 'release'
        output.mkdir()
        marker = output / 'keep.txt'
        marker.write_text('existing release')
        result = subprocess.run([sys.executable, '-O',
            str(self.root / 'scripts/package_release.py'), '--output-dir', str(output),
            '--source-ref', 'test-only'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(output.iterdir()), [marker])


if __name__ == '__main__':
    unittest.main()
