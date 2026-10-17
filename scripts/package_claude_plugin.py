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
    'references/platforms.md', 'references/practical-life.md', 'references/provider-contract.md',
    'references/provider-descriptor.schema.json', 'references/relationships-rest.md',
    'references/research.md', 'references/templates.md', 'references/workflows.md',
)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def public_bytes(path):
    # A regular file below a symlinked directory is still an indirect read.
    # Reject the whole path, including links to private directories in ROOT.
    relative = path.relative_to(ROOT)
    current = ROOT
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError('do not follow symlinks: ' + str(current))
    if not (path.resolve().is_relative_to(ROOT.resolve())):
        raise ValueError(str(path))
    return path.read_bytes().replace(b'\r\n', b'\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise ValueError('output exists; choose a new file name')
    report_path = output.with_suffix('.verification.json')
    if report_path.exists():
        raise ValueError('verification report exists; choose a new file name')
    version = public_bytes(SKILL / 'VERSION').decode('utf-8').strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?', version):
        raise ValueError('version must be a portable semantic version')
    plugin = json.loads(public_bytes(ROOT / '.claude-plugin' / 'plugin.json'))
    if not (plugin['name'] == 'zhixu' and plugin['version'] == version):
        raise ValueError("package validation failed: plugin['name'] == 'zhixu' and plugin['version'] == version")
    if not (public_bytes(ROOT / 'VERSION').decode('utf-8').strip() == version):
        raise ValueError("package validation failed: (ROOT / 'VERSION').read_text(encoding='utf-8').strip() == version")
    text = public_bytes(SKILL / 'SKILL.md').decode('utf-8')
    header = re.match(r'\A---\n(.*?)\n---(?:\n|$)', text, re.DOTALL)
    if not header:
        raise ValueError('SKILL.md needs a complete leading frontmatter block')
    metadata_text = header.group(1)
    if not (re.search(r'(?m)^name: adaptive-personal-ai-os$', metadata_text)):
        raise ValueError("package validation failed: re.search(r'(?m)^name: adaptive-personal-ai-os$', metadata_text)")
    description_line = re.search(r'(?m)^description:[ \t]*(.+)$', metadata_text)
    if not description_line:
        raise ValueError('SKILL.md needs a JSON-quoted description')
    description = json.loads(description_line.group(1))
    if not isinstance(description, str) or not description.strip() or len(description) > 200:
        raise ValueError('description must be non-empty text of at most 200 characters')
    if not (re.search(r'(?m)^  version: "' + re.escape(version) + r'"$', metadata_text)):
        raise ValueError('package validation failed: re.search(r\'(?m)^  version: "\' + re.escape(version) + r\'"$\', text)')
    paths = [Path('skills/adaptive-personal-ai-os') / name for name in PUBLIC_RUNTIME_FILES]
    files = {}
    for relative in paths:
        name = relative.as_posix()
        if not (not {'private', '.private', '.zhixu', '.git', '__pycache__'} & set(PurePosixPath(name).parts)):
            raise ValueError("package validation failed: not {'private', '.private', '.zhixu', '.git', '__pycache__'} & set(PurePosixPath(name).parts)")
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
    if (ROOT / '.zhixu').is_symlink():
        raise ValueError('staging directory must not be a symlink')
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
            if not (resolved.is_relative_to(stage / 'skills' / 'adaptive-personal-ai-os') and resolved.is_file()):
                raise ValueError((name, target))
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, raw in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, raw)
    with zipfile.ZipFile(output) as archive:
        if not (archive.testzip() is None and set(archive.namelist()) == set(files)):
            raise ValueError('package validation failed: archive.testzip() is None and set(archive.namelist()) == set(files)')
        if not (all(archive.read(name) == raw for name, raw in files.items())):
            raise ValueError('package validation failed: all(archive.read(name) == raw for name, raw in files.items())')
    report = {'version': version, 'plugin': 'zhixu', 'skill': 'adaptive-personal-ai-os',
              'output': str(output), 'stage': str(stage), 'files': len(files), 'runtime_files': len(PUBLIC_RUNTIME_FILES),
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
