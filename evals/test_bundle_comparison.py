import hashlib
import tempfile
import unittest
from pathlib import Path
from scripts.compare_skill_bundle import compare, plan_upgrade
from unittest.mock import patch
import json
import subprocess
import sys

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

class UpgradePlanTests(unittest.TestCase):
    setUp = BundleComparisonTests.setUp
    @staticmethod
    def make_manifest(contents):
        return {'kind':'skill','skill_name':'adaptive-personal-ai-os','file_count':len(contents),
                'files':{name:hashlib.sha256(value.encode()).hexdigest() for name,value in contents.items()}}

    def test_three_way_categories_preserve_local_work(self):
        old={'same.md':'old','update.md':'old','done.md':'old','personal.md':'old','conflict.md':'old','retire.md':'old','retire-local.md':'old','gone.md':'old','missing.md':'old'}
        new={k:'new' for k in ['update.md','done.md','conflict.md','missing.md','new.md','collision.md']}
        new.update({'same.md':'old','personal.md':'old'})
        installed={'same.md':'old','update.md':'old','done.md':'new','personal.md':'mine','conflict.md':'mine','retire.md':'old','retire-local.md':'mine','collision.md':'private collision','extra-private.md':'never inspect'}
        for name,value in installed.items():(self.bundle/name).write_text(value)
        from scripts import compare_skill_bundle as tool
        with patch.object(tool,'file_digest',wraps=tool.file_digest) as reads:
            report=plan_upgrade(self.bundle,self.make_manifest(old),self.make_manifest(new))
        expected={'unchanged':['same.md'],'replacement_candidates':['update.md'],'already_target':['done.md'],'local_only_changes':['personal.md'],'conflicts':['conflict.md'],'new_files':['new.md'],'new_file_collisions':['collision.md'],'retired_unmodified':['retire.md'],'retired_local_changes':['retire-local.md'],'already_absent':['gone.md'],'missing':['missing.md'],'unreadable':[]}
        for key,value in expected.items():self.assertEqual(report[key],value,key)
        self.assertEqual(reads.call_count,len(old.keys()|new.keys()))
        self.assertNotIn('extra-private.md',[call.args[1] for call in reads.call_args_list])
        self.assertFalse(report['applied'])
        for name,value in installed.items():self.assertEqual((self.bundle/name).read_text(),value)

    def test_both_manifests_validated_before_any_file_read(self):
        valid=self.make_manifest({'SKILL.md':'public core'})
        unsafe=self.make_manifest({'../outside':'secret'})
        with patch('scripts.compare_skill_bundle.file_digest') as reads:
            for old,new in [(valid,unsafe),(unsafe,valid)]:
                with self.assertRaises(ValueError):plan_upgrade(self.bundle,old,new)
            reads.assert_not_called()

    def test_plan_does_not_follow_symlinks(self):
        target=self.bundle/'linked.md';target.symlink_to(self.root/'outside')
        manifest=self.make_manifest({'SKILL.md':'public core','linked.md':'new'})
        self.assertEqual(plan_upgrade(self.bundle,manifest,manifest)['unreadable'],['linked.md'])

    def test_cli_plan_reports_without_applying(self):
        old=self.root/'old.json';new=self.root/'new.json'
        old.write_text(json.dumps(self.make_manifest({'SKILL.md':'public core'})))
        new.write_text(json.dumps(self.make_manifest({'SKILL.md':'next core'})))
        script=Path(__file__).resolve().parents[1]/'scripts/compare_skill_bundle.py'
        result=subprocess.run([sys.executable,str(script),'--bundle',str(self.bundle),'--manifest',str(new),'--baseline-manifest',str(old)],capture_output=True,text=True)
        self.assertEqual(result.returncode,1,result.stderr)
        report=json.loads(result.stdout);self.assertEqual(report['replacement_candidates'],['SKILL.md']);self.assertFalse(report['applied'])
        self.assertEqual((self.bundle/'SKILL.md').read_bytes(),b'public core')

if __name__ == '__main__': unittest.main()
