import hashlib
import tempfile
import unittest
from pathlib import Path
from scripts.compare_skill_bundle import compare

class BundleComparisonTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.bundle = self.root / 'bundle'
        self.bundle.mkdir()
        (self.bundle / 'SKILL.md').write_bytes(b'public core')
        self.manifest = {'kind': 'skill', 'skill_name': 'adaptive-personal-ai-os', 'file_count': 1,
                         'files': {'SKILL.md': hashlib.sha256(b'public core').hexdigest()}}

    def test_match_does_not_read_or_change_private_files(self):
        private = self.bundle / 'private.md'
        private.write_bytes(b'not in manifest')
        before = {p.name: p.read_bytes() for p in self.bundle.iterdir()}
        report = compare(self.bundle, self.manifest)
        self.assertTrue(report['all_listed_files_match'])
        self.assertNotIn('private.md', str(report))
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.bundle.iterdir()})

    def test_changed_missing_and_directory(self):
        target = self.bundle / 'SKILL.md'
        target.write_bytes(b'local changes')
        self.assertEqual(compare(self.bundle, self.manifest)['different'], ['SKILL.md'])
        target.unlink()
        self.assertEqual(compare(self.bundle, self.manifest)['missing'], ['SKILL.md'])
        target.mkdir()
        self.assertEqual(compare(self.bundle, self.manifest)['unreadable'], ['SKILL.md'])

    def test_unsafe_manifest_rejected(self):
        for name in ('../secret', '/secret', 'C:/secret', 'a\\secret', './SKILL.md', 'a//b', 'a/../b'):
            with self.subTest(name=name):
                bad = {**self.manifest, 'files': {name: '0' * 64}}
                with self.assertRaises(ValueError): compare(self.bundle, bad)
        for patch in ({'kind':'plugin'}, {'file_count':2}, {'files':{'SKILL.md':'bad'}}):
            with self.assertRaises(ValueError): compare(self.bundle, {**self.manifest, **patch})

    def test_symlink_not_followed(self):
        outside = self.root / 'outside'
        outside.write_bytes(b'public core')
        target = self.bundle / 'SKILL.md'
        target.unlink()
        target.symlink_to(outside)
        self.assertEqual(compare(self.bundle, self.manifest)['unreadable'], ['SKILL.md'])
        alias = self.root / 'alias'
        alias.symlink_to(self.bundle, target_is_directory=True)
        with self.assertRaises(ValueError): compare(alias, self.manifest)

    def test_large_file_not_hashed(self):
        (self.bundle / 'SKILL.md').write_bytes(b'x' * (2 * 1024 * 1024 + 1))
        self.assertEqual(compare(self.bundle, self.manifest)['unreadable'], ['SKILL.md'])

if __name__ == '__main__': unittest.main()
