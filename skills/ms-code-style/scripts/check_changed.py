#!/usr/bin/env python3
"""Lint the lines a branch adds, with the config CI uses. Never writes to the repo."""
import argparse
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

CONFIG = '.eslintrc.new-code.json'
HUNK = re.compile(r'^@@ -\S+ \+(\d+)(?:,(\d+))? @@', re.MULTILINE)


def fail(message):
    print(f'CHECK NOT RUN: {message}', file=sys.stderr)
    sys.exit(2)


def run(args, cwd, ok=(0,), stdin=None):
    try:
        result = subprocess.run(args, cwd=cwd, input=stdin, capture_output=True, encoding='utf-8')
    except OSError as error:
        fail(str(error))
    if result.returncode not in ok:
        fail(result.stderr.strip() or f'{args[0]} exited {result.returncode}')
    return result.stdout


def find_app(root):
    found = run(['git', 'ls-files', '-z', '--', f':(glob)**/{CONFIG}'], root).split('\0')
    apps = [Path(path).parent.as_posix() for path in found if path]
    if len(apps) != 1:
        fail(f'expected one tracked {CONFIG}, found {len(apps)}: wrong repo, or the branch needs develop merged in')
    return apps[0]


def changed_lines(root, app_path, base):
    merge_base = run(['git', 'merge-base', base, 'HEAD'], root).strip()
    scope = f'{app_path}/src'
    tracked = run(['git', 'diff', '-z', '--name-only', '--diff-filter=AMR', merge_base, '--', scope], root)
    untracked = run(['git', 'ls-files', '-z', '--others', '--exclude-standard', '--', scope], root)

    def wanted(path):
        return path.endswith('.ts') and '/services/generated/' not in path

    changed = {}
    for path in filter(wanted, tracked.split('\0')):
        diff = run(['git', 'diff', '--no-ext-diff', '--no-color', '-U0', merge_base, '--', path], root)
        lines = set()
        for start, count in HUNK.findall(diff):
            lines.update(range(int(start), int(start) + int(count or 1)))
        if lines:
            changed[path] = lines
    for path in filter(wanted, untracked.split('\0')):
        count = len((root / path).read_text(encoding='utf-8').splitlines())
        changed[path] = set(range(1, count + 1))
    return changed


def eslint(root, app_path, changed):
    app = root / app_path
    args = ['node', 'node_modules/eslint/bin/eslint.js', '-c', CONFIG, '--no-eslintrc', '--format', 'json']
    report = json.loads(run(args + [path[len(app_path) + 1:] for path in changed], app, ok=(0, 1)))
    errors = warnings = 0
    for entry in report:
        path = Path(entry['filePath']).resolve().relative_to(root).as_posix()
        for item in entry['messages']:
            if not item.get('fatal') and item.get('line') not in changed.get(path, ()):
                continue
            is_error = item['severity'] == 2
            errors += is_error
            warnings += not is_error
            level = 'error' if is_error else 'warning'
            print(f"{level:8} {path}:{item.get('line', 1)} {item.get('ruleId')} {item['message']}")
    return errors, warnings


def prettier(root, app_path, changed):
    app = root / app_path
    count = 0
    for path, lines in changed.items():
        source = (root / path).read_text(encoding='utf-8')
        args = ['node', 'node_modules/prettier/bin-prettier.js', '--stdin-filepath', path[len(app_path) + 1:]]
        formatted = run(args, app, ok=(0, 2), stdin=source)
        # Exit 2 with no output is a syntax error, which ESLint already reported.
        if not formatted:
            continue
        matcher = difflib.SequenceMatcher(None, source.splitlines(), formatted.splitlines(), autojunk=False)
        for op, start, end, _, _ in matcher.get_opcodes():
            if op == 'equal':
                continue
            touched = lines.intersection(range(start + 1, max(end, start + 1) + 1))
            if touched:
                count += 1
                print(f'format   {path}:{min(touched)} differs from Prettier')
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default='.', help='any path inside the worktree')
    parser.add_argument('--base', default='origin/develop')
    options = parser.parse_args()

    root = Path(run(['git', 'rev-parse', '--show-toplevel'], options.repo).strip()).resolve()
    app_path = find_app(root)
    changed = changed_lines(root, app_path, options.base)
    if not changed:
        print('No changed TypeScript lines.')
        return 0
    if not (root / app_path / 'node_modules').exists():
        fail('ClientApp/node_modules is missing')

    errors, warnings = eslint(root, app_path, changed)
    formatting = prettier(root, app_path, changed)
    print(f'{len(changed)} files: {errors} errors, {warnings} warnings, {formatting} formatting differences')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
