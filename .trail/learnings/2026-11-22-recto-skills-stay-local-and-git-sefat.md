---
title: "Recto skills stay local and git-excluded, never published in the public skills repo"
author: Sefat
date: 2026-11-22
standing: true
id: l-f3b2efb0
scope: repo
status: active
src: init-sessions
---

## Decided
- The Recto skills were exported into the skills repo for installation, but they are not the owner's to publish. They were deliberately excluded from git, and a note was recorded so later sessions don't force-add them.
- In the code: Keep the recto* skill folders under /Users/anam/Documents/repos/sefat-skills/skills/ git-excluded. Do not use `git add -f` on them or commit/push them. Only the learning file in .trail/learnings is tracked.

_From past Claude sessions here, Nov 22._
