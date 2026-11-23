---
title: "Recto's own skills stay local in this public collection until Recto permits redistribution"
author: Sefat
date: 2026-11-22
branch: main
cost: { minutes: 1, tokens: 1302 }
id: l-9bde45d5
scope: repo
status: active
src: agent
touches:
  - AGENTS.md
---

## Decided
Keep the eight exported Recto skills installable from the local checkout but excluded from git. They are Recto's work (copyright 2026 Recto), no redistribution license was found, and this repo is public under MIT.

## Tried and ruled out
Byte-for-byte copies alone: two upstream descriptions are invalid strict YAML, so the installer would not discover them. Only those two lines are quoted.

## Watch out
Do not force-add them or list them in the public README without written permission from Recto. If permission arrives, the global gitignore also hides AGENTS.md, which two of the skills need. A fresh export from the app brings the YAML problem back.

In the code: skills/recto and skills/recto-*, excluded in .git/info/exclude; quoted description in skills/recto-animation/SKILL.md and skills/recto-slides/SKILL.md.
