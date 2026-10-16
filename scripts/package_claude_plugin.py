"""Build a local Claude plugin ZIP from the one shared public Skill."""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'adaptive-personal-ai-os'
PUBLIC_RUNTIME_FILES = (
    'SKILL.md', 'VERSION', 'LICENSE', 'agents/openai.yaml',
    'references/daily-life.md', 'references/health-habits.md',
    'references/learning.md', 'references/life.md', 'references/memory.md',
    'references/money-career.md', 'references/planning-decisions.md',
    'references/platforms.md', 'references/provider-contract.md',
    'references/provider-descriptor.schema.json', 'references/relationships-rest.md',
    'references/research.md', 'references/templates.md', 'references/workflows.md',
)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def public_bytes(path):
    assert not path.is_symlink(), 'do not follow symlinks: ' + str(path)
    assert path.resolve().is_relative_to(ROOT.resolve()), str(path)
    return path.read_bytes().replace(b'\r\n', b'\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    assert not output.exists(), 'output exists; choose a new file name'
    report_path = output.with_suffix('.verification.json')
    assert not report_path.exists(), 'verification report exists; choose a new file name'
    version = (SKILL / 'VERSION').read_text(encoding='utf-8').strip()
    plugin = json.loads((ROOT / '.claude-plugin' / 'plugin.json').read_text(encoding='utf-8'))
    assert plugin['name'] == 'zhixu' and plugin['version'] == version
    assert (ROOT / 'VERSION').read_text(encoding='utf-8').strip() == version
    text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    assert re.search(r'(?m)^name: adaptive-personal-ai-os$', text)
    description = json.loads(re.search(r'(?m)^description:\s*(.+)$', text).group(1))
    assert len(description) <= 200
    assert re.search(r'(?m)^  version: "' + re.escape(version) + r'"$', text)
    paths = [Path('skills/adaptive-personal-ai-os') / name for name in PUBLIC_RUNTIME_FILES]
    files = {}
    for relative in paths:
        name = relative.as_posix()
        assert not {'private', '.private', '.zhixu', '.git', '__pycache__'} & set(PurePosixPath(name).parts)
        files[name] = public_bytes(ROOT / relative)
    files['.claude-plugin/plugin.json'] = public_bytes(ROOT / '.claude-plugin' / 'plugin.json')
    files['LICENSE'] = public_bytes(ROOT / 'LICENSE')
    files['README.md'] = (
        '# ZhiXu / 智序 — Claude plugin\n\n'
        'Plugin: zhixu; Skill: adaptive-personal-ai-os; Version: ' + version + '.\n\n'
        'In Claude Desktop or Cowork, open Customize > Plugins, choose the custom plugin upload option, '
        'upload this ZIP and enable ZhiXu. Check the skill menu in a new conversation before claiming activation.\n\n'
        'Add marketplace Moyang1412/adaptive-personal-ai-os and install the zhixu plugin, '
        'or upload this ZIP through the custom plugin option. '
        'The package contains public instructions only; personal memory, chat history, hooks and MCP services are not included. '
        'Use either the standalone Skill or this plugin in a given host to avoid duplicate entries.\n\n'
        'Source: https://github.com/Moyang1412/adaptive-personal-ai-os\n'
        'License: MIT.\n'
    ).encode('utf-8')
    # Stage only the exact public files; do not copy the repository or local data.
    stage_base = ROOT / '.zhixu' / ('claude-plugin-' + version)
    stage = stage_base
    suffix = 2
    while stage.exists():
        stage = stage_base.with_name(stage_base.name + '-' + str(suffix))
        suffix += 1
    stage.mkdir(parents=True)
    for name, raw in files.items():
        destination = stage / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw)
    # Every local Markdown file reference in the runtime package must resolve inside it.
    for name, raw in files.items():
        if not name.startswith('skills/') or not name.endswith('.md'):
            continue
        for target in re.findall(r'\]\(([^)]+)\)', raw.decode('utf-8')):
            target = target.split('#', 1)[0]
            if not target or '://' in target or target.startswith('mailto:'):
                continue
            resolved = (stage / name).parent.joinpath(target).resolve()
            assert resolved.is_relative_to(stage / 'skills' / 'adaptive-personal-ai-os') and resolved.is_file(), (name, target)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, raw in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, raw)
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None and set(archive.namelist()) == set(files)
        assert all(archive.read(name) == raw for name, raw in files.items())
    report = {'version': version, 'plugin': 'zhixu', 'skill': 'adaptive-personal-ai-os',
              'output': str(output), 'stage': str(stage), 'files': len(files), 'runtime_files': 18,
              'description_characters': len(description), 'zip_sha256': sha(output.read_bytes()),
              'zip_bytes': output.stat().st_size, 'crc_and_files_match': True,
              'relative_runtime_references_closed': True,
              'file_sha256': {name: sha(raw) for name, raw in files.items()},
              'desktop_upload_and_activation': 'not executed', 'publication': 'not assessed by this packaging command'}
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({key: value for key, value in report.items() if key != 'file_sha256'}, ensure_ascii=False, indent=2))
    print('REPORT', report_path)

if __name__ == '__main__':
    main()
