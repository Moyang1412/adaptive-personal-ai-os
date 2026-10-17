"""Read-only comparison of one explicitly selected Skill against a release manifest.

Does not discover host directories, inspect extra files, install, or prove activation.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath


def validate_bundle(bundle):
    bundle = Path(bundle).absolute()
    if any(part.is_symlink() for part in [bundle, *bundle.parents]):
        raise ValueError('bundle path must not contain symlinks')
    if not bundle.is_dir():
        raise ValueError('bundle must be an existing directory selected by the user')
    return bundle


def manifest_files(manifest):
    if not isinstance(manifest, dict) or manifest.get('kind') != 'skill' or manifest.get('skill_name') != 'adaptive-personal-ai-os':
        raise ValueError('expected a standalone ZhiXu skill manifest')
    files = manifest.get('files')
    count = manifest.get('file_count')
    if not isinstance(files, dict) or not files or type(count) is not int or count != len(files):
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
    return files


def file_digest(bundle, name):
    target = bundle / name
    if any(p.is_symlink() for p in [target, *target.parents]):
        return "unreadable", None
    try:
        if not target.exists():
            return "missing", None
        if not target.is_file() or target.stat().st_size > 2 * 1024 * 1024:
            return "unreadable", None
        return "read", hashlib.sha256(target.read_bytes()).hexdigest()
    except OSError:
        return "unreadable", None


def compare(bundle, manifest):
    bundle = validate_bundle(bundle)
    files = manifest_files(manifest)
    report = {'matching': [], 'different': [], 'missing': [], 'unreadable': [],
              'scope': 'Only manifest-listed paths are read for hashing, including local edits at those paths; extra files are not enumerated or read.',
              'activation': 'not assessed', 'manifest_authenticity': 'not assessed',
              'writes': 'none'}
    for name, expected in sorted(files.items()):
        state, actual = file_digest(bundle, name)
        if state != 'read':
            report[state].append(name)
        else:
            report['matching' if actual == expected else 'different'].append(name)
    report['all_listed_files_match'] = not any(report[k] for k in ('different', 'missing', 'unreadable'))
    return report


def plan_upgrade(bundle, baseline, target):
    """Classify selected files against two versions; never replace or delete files."""
    bundle = validate_bundle(bundle)
    old = manifest_files(baseline)
    new = manifest_files(target)
    groups = ('unchanged', 'replacement_candidates', 'already_target',
              'local_only_changes', 'conflicts', 'new_files', 'new_file_collisions',
              'retired_unmodified', 'retired_local_changes', 'already_absent',
              'missing', 'unreadable')
    report = {name: [] for name in groups}
    for name in sorted(old.keys() | new.keys()):
        state, actual = file_digest(bundle, name)
        if state == 'unreadable':
            category = state
        elif name not in new:
            category = 'already_absent' if state == 'missing' else 'retired_unmodified' if actual == old[name] else 'retired_local_changes'
        elif state == 'missing':
            category = 'new_files' if name not in old else 'missing'
        elif actual == new[name]:
            category = 'unchanged' if old.get(name) == new[name] else 'already_target'
        elif name not in old:
            category = 'new_file_collisions'
        elif actual == old[name]:
            category = 'replacement_candidates'
        elif old[name] == new[name]:
            category = 'local_only_changes'
        else:
            category = 'conflicts'
        report[category].append(name)
    report['needs_review'] = any(report[key] for key in groups if key not in ('unchanged', 'already_target', 'already_absent'))
    report.update({'writes': 'none', 'applied': False,
                   'scope': 'Only paths listed by the two selected manifests; extra files are not scanned.',
                   'manifest_authenticity': 'not assessed', 'activation': 'not assessed',
                   'note': 'Advisory only. Review local edits and retirement candidates; no replacement or deletion is authorized by this report.'})
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--baseline-manifest', type=Path, help='Optional old manifest for a read-only three-way upgrade plan')
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
        report = plan_upgrade(args.bundle, json.loads(args.baseline_manifest.read_text(encoding='utf-8')), manifest) if args.baseline_manifest else compare(args.bundle, manifest)
    except (OSError, ValueError) as error:
        parser.exit(2, f'Cannot compare bundle: {error}\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.baseline_manifest:
        return 1 if report['needs_review'] else 0
    return 0 if report['all_listed_files_match'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
