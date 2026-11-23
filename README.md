# skills

My personal collection of skills for AI coding agents (Claude Code, Cursor, Codex, and others). Skills follow the [Agent Skills](https://agentskills.io/) format and install with the [`skills`](https://github.com/vercel-labs/skills) CLI.

## Install

```sh
# See what's in the collection
npx skills add sefatanam/skills --list

# Install one skill
npx skills add sefatanam/skills --skill act

# Install several skills
npx skills add sefatanam/skills --skill act --skill <other-skill>

# Install every skill
npx skills add sefatanam/skills --all
```

Add `-a claude-code` to install for a single agent only, and `-g` to install globally (user scope) instead of into the current project:

```sh
npx skills add sefatanam/skills --skill act -a claude-code -g
```

## Available skills

### act

Run GitHub Actions workflows locally in Docker with [nektos/act](https://github.com/nektos/act). The skill checks that act and Docker are set up, scopes the run to a single job, passes secrets, variables and event data, does a dry run first, and works out whether a failure is a real bug or a gap between act and GitHub.

**Use when:**

- "Run this workflow locally"
- "Test my CI without pushing"
- "Why does this job fail in CI?"

**Requires:** `act` (`brew install act`) and Docker.

### ms-code-style

My code style for the MS project, an ASP.NET Core and Angular 11 codebase: TypeScript 4.0, RxJS 6, ESLint and Prettier. It includes a read-only checker that lints only changed lines. Project-specific details live in gitignored `references/local*.md` files.

**Use when:**

- "Implement this ticket in my code style"
- "Review this branch against my code style"
- "Will my changed lines pass lint?"

**Requires:** Python 3, and a checkout with a `.eslintrc.new-code.json` and installed `node_modules` for the checker.

### ms-code-style-2

A variant of `ms-code-style` kept side by side for comparison. It adds a reference on what the reviewer accepts and sends back, learned from 120 merged merge requests, and a self-review checklist for handover. Project-specific details live in gitignored `references/local*.md` files.

**Use when:** the same prompts as `ms-code-style`.

**Requires:** the same as `ms-code-style`.

### ms-mr-code-style

How a senior frontend developer on the MS project solves tickets, read from the code of 34 merged Angular 11 merge requests: where the fix goes, which helpers to extract, how specs are written, and which habits not to copy. It is meant to be used next to `ms-code-style`. Names and MR numbers live in a gitignored `references/local.md`.

**Use when:**

- "Solve this ticket the way the team's accepted merge requests do"
- "How would a senior developer shape this change?"

**Requires:** a checkout with a `ClientApp/.eslintrc.new-code.json`.

## Adding a skill

See [AGENTS.md](AGENTS.md).

## License

MIT
