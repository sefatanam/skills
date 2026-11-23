# ESLint and Prettier

The config files in `ClientApp` are the source of truth: `.eslintrc.new-code.json` (extends `.eslintrc.json`) and `.prettierrc.json`.

## Check changed lines as CI does

```sh
python3 -I ~/.claude/skills/ms-code-style-2/scripts/check_changed.py --repo <worktree> [--base origin/develop]
```

It is read-only, and includes uncommitted and untracked files. Exit 0 is clean, 1 means ESLint errors, 2 means the check could not run. ESLint warnings and Prettier differences are printed but do not fail, as in CI. It does not check types, templates, i18n or C#.

## ESLint on new lines

| Rule | Level |
|---|---|
| `eslint:recommended`, `@typescript-eslint/recommended` | as preset |
| `no-explicit-any` | error, warning in specs |
| `no-unused-vars` | error, `_` prefix is exempt |
| `eqeqeq` (smart, so `== null` is allowed) | error |
| `prefer-const`, `no-var` | error |
| `no-console` | error, `warn` and `error` are allowed |
| `no-eval`, `no-implied-eval`, `no-new-func`, `no-throw-literal` | error |
| `no-restricted-imports` (HttpClient, modern Angular and RxJS, rxjs-compat) | error |
| `no-non-null-assertion` | warning |
| `bypassSecurityTrust*`, `innerHTML =` | warning, justify it |

Fix the code before reaching for a disable comment. If one is unavoidable, disable one rule on one line and give the reason.

## Prettier

140 columns, 2 spaces, semicolons, single quotes, ES5 trailing commas, spaces inside braces, parentheses around every arrow parameter. Files end with a newline and have no trailing whitespace.

- **[project]** Never run `npm run lint`, `npm run format:check` or a write over the whole tree.
- **[project]** In an existing file, fix only changed lines. `eslint --fix` and `prettier --write` rewrite whole files, so use them only on files this branch created, and edit by hand otherwise.
