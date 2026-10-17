"""Produce the two public ZhiXu packages and portable release manifests."""
import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--source-ref', required=True)
    parser.add_argument('--candidate', action='store_true', help='Label local artifacts as an unreleased candidate; does not publish')
    args = parser.parse_args()
    output = args.output_dir.resolve()
    if output.exists():
        raise ValueError('release directory already exists; keep existing assets')
    output.mkdir(parents=True)
    version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
    stem = 'zhixu-' + version + ('-candidate' if args.candidate else '')
    channel = 'candidate' if args.candidate else 'release-build'
    plugin_zip = output / (stem + '-plugin.zip')
    subprocess.run([sys.executable, '-X', 'utf8', str(ROOT / 'scripts/package_claude_plugin.py'), '--output', str(plugin_zip)], check=True)
    local_report = plugin_zip.with_suffix('.verification.json')
    local = json.loads(local_report.read_text(encoding='utf-8'))
    # Keep absolute build paths in a local subdirectory, outside public asset lists.
    (output / 'local').mkdir()
    local_report.rename(output / 'local' / local_report.name)
    with zipfile.ZipFile(plugin_zip) as archive:
        plugin_files = {name: archive.read(name) for name in archive.namelist()}
    prefix = 'skills/adaptive-personal-ai-os/'
    skill_files = {name[len(prefix):]: raw for name, raw in plugin_files.items() if name.startswith(prefix)}
    expected_skill_files = {name[len(prefix):] for name in local['file_sha256'] if name.startswith(prefix)}
    if set(skill_files) != expected_skill_files or 'SKILL.md' not in expected_skill_files:
        raise ValueError('package validation failed: standalone files differ from verified plugin manifest')
    skill_zip = output / (stem + '-skill.zip')
    with zipfile.ZipFile(skill_zip, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, raw in sorted(skill_files.items()):
            info = zipfile.ZipInfo('adaptive-personal-ai-os/' + name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, raw)
    with zipfile.ZipFile(skill_zip) as archive:
        if not (archive.testzip() is None):
            raise ValueError('package validation failed: archive.testzip() is None')
        if not (set(archive.namelist()) == {'adaptive-personal-ai-os/' + name for name in skill_files}):
            raise ValueError("package validation failed: set(archive.namelist()) == {'adaptive-personal-ai-os/' + name for name in skill_files}")
        if not (all(archive.read('adaptive-personal-ai-os/' + name) == raw for name, raw in skill_files.items())):
            raise ValueError("package validation failed: all(archive.read('adaptive-personal-ai-os/' + name) == raw for name, raw in skill_files.items())")
    manifests = []
    for kind, package, files in [('plugin', plugin_zip, plugin_files), ('skill', skill_zip, skill_files)]:
        name = stem + ('-plugin-manifest.json' if kind == 'plugin' else '-manifest.json')
        path = output / name
        write_json(path, {'version': version, 'tag': None if args.candidate else 'v' + version, 'source_ref': args.source_ref,
                         'build_channel': channel, 'publication': 'not assessed by this build command',
                         'kind': kind, 'skill_name': 'adaptive-personal-ai-os', 'license': 'MIT',
                         'archive': package.name, 'archive_sha256': sha(package.read_bytes()),
                         'file_count': len(files), 'files': {key: sha(raw) for key, raw in sorted(files.items())},
                         'scope': 'Public instruction bundle; no personal profile or chat history.'})
        manifests.append(path)
    verification = output / ('candidate-verification.json' if args.candidate else 'release-verification.json')
    write_json(verification, {'version': version, 'source_ref': args.source_ref, 'build_channel': channel,
                             'plugin_files': len(plugin_files), 'skill_files': len(skill_files),
                             'package_crc_and_per_file_readback': 'passed',
                             'relative_runtime_references_closed': local['relative_runtime_references_closed'],
                             'description_characters': local['description_characters'],
                             'desktop_install_and_activation': 'not executed',
                             'model_behavior_and_real_user_effects': 'not executed',
                             'remote_publication': 'not assessed by this build command'})
    assets = [plugin_zip, skill_zip, *manifests, verification]
    sums = output / 'SHA256SUMS'
    sums.write_text(''.join(sha(path.read_bytes()) + '  ' + path.name + '\n' for path in assets), encoding='utf-8')
    print(json.dumps({'version': version, 'build_channel': channel, 'assets': [path.name for path in assets] + [sums.name],
                      'plugin_sha256': sha(plugin_zip.read_bytes()), 'skill_sha256': sha(skill_zip.read_bytes())}, indent=2))

if __name__ == '__main__':
    main()
