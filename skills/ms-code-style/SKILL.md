---
name: ms-code-style
description: Sefat's code style and engineering rules for the MS project, an ASP.NET Core plus Angular 11 repo (TypeScript 4.0, RxJS 6, ESLint, Prettier) with a ClientApp/.eslintrc.new-code.json. Use before planning, writing, fixing, refactoring, testing, reviewing or committing code in any branch or worktree of that repo, including small fixes and tickets, and whenever Sefat asks for "my code style". Not for other repositories.
metadata:
  author: sefatanam
  version: "1.0.0"
---

# MS code style

Write code that passes CI and that Sefat would have written.

This applies only to an Angular 11 plus .NET checkout with a `ClientApp/.eslintrc.new-code.json`. Anywhere else, say so and stop.

If `references/local.md` exists, read it now. It holds the project's names, paths and exceptions, and is gitignored. This skill is published, so never copy from the `local*` files into its other files.

## Precedence

1. What Sefat says in this conversation.
2. The checkout's `AGENTS.md` and its config files. They can change per branch, so if one disagrees with this skill, follow it and mention the drift.
3. This skill.
4. The surrounding code.
5. Generic Angular or TypeScript advice and skills. These usually assume modern versions that do not compile here.

Rules carry a tag, so you know how hard to hold them:

- **[enforced]** a compiler or CI fails without it.
- **[project]** written in `AGENTS.md`.
- **[stated]** Sefat said it.
- **[observed]** inferred from Sefat's commits or past sessions. A default: depart from it with a reason.

## Read what the change needs

| Changing | Read first |
|---|---|
| `.ts`, `.html`, `.css`, specs, i18n | [references/angular-typescript.md](references/angular-typescript.md) |
| `.cs`, SQL scripts, API contracts | [references/backend.md](references/backend.md) |
| Before handing over client changes, or any lint question | [references/lint-format.md](references/lint-format.md) |

## Solving an issue

1. If `trail` is installed, run `trail ask "<ticket words>" --source`. Earlier sessions may have ruled out the obvious fix.
2. Find the cause before editing. If reading cannot prove it, say what runtime evidence is needed. A value that looks empty may be valid: `'0'` can be a real selection.
3. Check the callers of anything shared.
4. Look for an existing helper, constant, component or type, and check that it is correct for this input before reusing it.
5. Make the change under the rules below.

## How Sefat wants code shaped

- **[stated]** Prefer a short inline read over a new state field that mirrors it. This does not license method calls in templates.
- **[stated]** Reusable helpers live in a util folder, not beside the component.
- **[observed]** Use the project's existing utils folder. Do not create a second utils root. A helper with a single consumer can stay a private method of that component.
- **[observed]** Fix at the narrowest point that owns the problem: the subscriber before the shared emitter, scoped CSS before `styles.css`.
- **[observed]** A rule used in several places gets one pure function and a spec.
- **[observed]** Loaders load. They do not set defaults or overwrite saved user choices.
- **[observed]** Several small readable templates beat one generic template with a switch and a bag of optional inputs.
- **[observed]** Use guard clauses with braces, descriptive names and few comments. A comment explains why.
- **[observed]** In a legacy file, match its naming (`_service` or `service`) and layout. Do not modernise or reformat lines the ticket does not need.

## Shipping

- **[project]** The branch is the ticket key alone, cut from `develop`. The commit subject is `<KEY> <ticket title in the ticket's language>`, with no colon after the key. Changes land by MR, and nothing is force pushed.
- **[project]** Write tests with the change. Run the build and test commands in `AGENTS.md`.
- **[observed]** Each commit compiles by itself. Stage by explicit path, because config files often hold local-only edits.
- Commit, push or open an MR only when asked. Run `trail check` first if it is installed.

## Handing over

Report in a few lines:

- what changed and why there;
- which checks ran, with results, and which did not;
- any rule you departed from, and why;
- anything that still needs a check in the browser.

When Sefat corrects the style, offer to add the correction as **[stated]**: general rules here, project details in `references/local.md`.
