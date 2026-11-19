# AGENTS.md

This repo is a collection of agent skills, installed with the `skills` CLI (`npx skills add sefatanam/sefat-skills --skill <name>`). The CLI finds every `skills/<name>/SKILL.md` on its own, so a new skill installs as soon as its folder exists.

## Adding a skill

1. Create `skills/<name>/SKILL.md`. Use a kebab-case `<name>`, and make the frontmatter `name` exactly match the folder name; otherwise `--skill <name>` won't find it.
   ```markdown
   ---
   name: <name>
   description: <What it does>. Use when <the distinct situations that should trigger it>.
   metadata:
     author: sefatanam
     version: "1.0.0"
   ---
   ```
2. Keep `SKILL.md` to the steps the agent takes. Put detailed reference material in `skills/<name>/references/` and link to it from `SKILL.md`, because only `SKILL.md` is loaded when the skill fires. Put scripts in `skills/<name>/scripts/`.
3. Add the skill to a group in `skills.sh.json` (this controls its grouping on skills.sh), and add a section to `README.md` under **Available skills**.
4. Check that it's discovered: `npx skills add . --list`.

Bump `metadata.version` whenever a skill's behaviour changes.
