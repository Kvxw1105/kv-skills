#!/usr/bin/env python3
"""Build a portable, one-entrypoint Edge Operator Skill ZIP, using stdlib only."""
import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent.parent
EXCLUDED_DIRS = {'__pycache__', '.git', '.pytest_cache', 'dist', '.venv'}
EXCLUDED_SUFFIXES = {'.pyc', '.pyo', '.zip'}


def build(out: Path) -> int:
    skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
    if not skill.startswith('---\n') or '\nname: edge-operator\n' not in skill:
        raise ValueError('SKILL.md missing valid edge-operator frontmatter')
    files = sorted(p for p in ROOT.rglob('*') if p.is_file()
                   and not any(part in EXCLUDED_DIRS for part in p.relative_to(ROOT).parts)
                   and p.suffix not in EXCLUDED_SUFFIXES)
    out.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(out, 'w', compression=ZIP_DEFLATED, compresslevel=9) as z:
        for p in files:
            z.write(p, f'edge-operator/{p.relative_to(ROOT).as_posix()}')
    with ZipFile(out) as z:
        names = z.namelist()
        if len([n for n in names if n.endswith('/SKILL.md')]) != 1:
            raise ValueError('Archive must have exactly one skill entrypoint')
        if not z.testzip() is None:
            raise ValueError('ZIP failed integrity check')
    return len(files)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='dist/skill.zip', type=Path)
    args = parser.parse_args()
    print(f'Packaged {build(args.out)} files -> {args.out}')
