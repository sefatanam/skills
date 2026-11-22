---
title: "Install exported skills per project, never globally on this Mac"
author: Sefat
date: 2026-11-22
standing: true
id: l-a97bf132
scope: repo
status: active
src: init-sessions
---

## Watch out
- Recto already manages its own global copies of these skills. Installing globally from the exported repo would overwrite them.
- In the code: Run from inside the target project: `npx skills add /Users/anam/Documents/repos/sefat-skills -a claude-code --copy --skill recto ...`. Do not pass `-g`.

_From past Claude sessions here, Nov 22._
