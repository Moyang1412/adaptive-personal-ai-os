"""Read-only comparison of one explicitly selected Skill against a release manifest.

Does not discover host directories, inspect extra files, install, or prove activation.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath


def compare(bundle, manifest):
    bundle = Path(bundle).absolute()
    if any(part.is_symlink() for part in [bundle, *bundle.parents]):
        raise ValueError('bundle path must not contain symlinks')
    if not bundle.is_dir():
        raise ValueError('bundle must be an existing directory selected by the user')
    if not isinstance(manifest, dict) or manifest.get('kind') != 'skill' or manifest.get('skill_name') != 'adaptive-personal-ai-os':
        raise ValueError('expected a standalone ZhiXu skill manifest')
    files = manifest.get('files')
    if not isinstance(files, dict) or not files or manifest.get('file_count') != len(files):
        raise ValueError('invalid manifest file list')
    # Validate the entire list before reading any target file.
    for name, digest in files.items():
        if not isinstance(name, str) or '\\' in name or ':' in name or '\x00' in name:
            raise ValueError('unsafe manifest path')
        path = PurePosixPath(name)
        if path.is_absolute() or any(p in ('', '.', '..') for p in name.split('/')):
            raise ValueError('unsafe manifest path')
        if not isinstance(digest, str) or not re.fullmatch('[0-9a-f]{64}', digest):
            raise ValueError('invalid SHA-256 digest')
    report = {'matching': [], 'different': [], 'missing': [], 'unreadable': [],
              'scope': 'Only manifest-listed files; extra/private files are not enumerated or read.',
              'activation': 'not assessed', 'manifest_authenticity': 'not assessed',
              'writes': 'none'}
    for name, expected in sorted(files.items()):
        target = bundle / name
        chain = [target, *target.parents]
        if any(p.is_symlink() for p in chain):
            report['unreadable'].append(name)
            continue
        try:
            if not target.exists():
                report['missing'].append(name)
            elif not target.is_file():
                report['unreadable'].append(name)
            elif target.stat().st_size > 2 * 1024 * 1024:
                report['unreadable'].append(name)
            else:
                actual = hashlib.sha256(target.read_bytes()).hexdigest()
                report['matching' if actual == expected else 'different'].append(name)
        except OSError:
            report['unreadable'].append(name)
    report['all_listed_files_match'] = not any(report[k] for k in ('different', 'missing', 'unreadable'))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    args = parser.parse_args()
    try:
        report = compare(args.bundle, json.loads(args.manifest.read_text(encoding='utf-8')))
    except (OSError, ValueError) as error:
        parser.exit(2, f'Cannot compare bundle: {error}\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['all_listed_files_match'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
