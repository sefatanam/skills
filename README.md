# sefat-skills

My personal collection of skills for AI coding agents (Claude Code, Cursor, Codex, and others). Skills follow the [Agent Skills](https://agentskills.io/) format and install with the [`skills`](https://github.com/vercel-labs/skills) CLI.

## Install

```sh
# See what's in the collection
npx skills add sefatanam/sefat-skills --list

# Install one skill
npx skills add sefatanam/sefat-skills --skill act

# Install several skills
npx skills add sefatanam/sefat-skills --skill act --skill <other-skill>

# Install every skill
npx skills add sefatanam/sefat-skills --all
```

Add `-a claude-code` to install for a single agent only, and `-g` to install globally (user scope) instead of into the current project:

```sh
npx skills add sefatanam/sefat-skills --skill act -a claude-code -g
```

## Available skills

### act

Run GitHub Actions workflows locally in Docker with [nektos/act](https://github.com/nektos/act). The skill checks that act and Docker are set up, scopes the run to a single job, passes secrets, variables and event data, does a dry run first, and works out whether a failure is a real bug or a gap between act and GitHub.

**Use when:**

- "Run this workflow locally"
- "Test my CI without pushing"
- "Why does this job fail in CI?"

**Requires:** `act` (`brew install act`) and Docker.

## Adding a skill

See [AGENTS.md](AGENTS.md).

## License

MIT
