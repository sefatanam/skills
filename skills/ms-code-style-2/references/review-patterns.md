# What the reviewer accepts and pushes back on

Learned from the last 120 merged merge requests by Sefat on `develop`: their diffs and every human review comment. About half had comments (58 MRs; 41 had comments on specific lines). Counts are MRs where the pattern showed up, tallied by reading, so treat them as approximate. A rule seen in one MR is a hint, not a rule.

Tags: **[reviewed]** a reviewer asked for it in 3 or more MRs. **[seen]** 2 MRs, or visible in accepted diffs only. **[once]** one MR; mention it, do not enforce it.

## What an accepted change looks like

- Client-only: 109 of 120 MRs. Both client and backend: 10. Backend only: 1.
- Small: median 3 files, and 61 of 120 touch 3 files or fewer. Many CSS or template fixes are under 30 lines.
- The author changes the code in nearly every review thread and replies "applied" or "fixed". The reviewer resolves the thread. Pushback happens, with an explanation, mainly on legacy or soon-to-be-retired code, and it was accepted in about 7 MRs.
- Large features were merged too. When a backend part is big, the author asks the reviewer to look at it separately.

## What the reviewer asks for

1. **[reviewed, ~18 MRs] Do not duplicate. Reuse or extract.** Before writing a function, pipe, constant or component, search for the existing one. If the same logic exists in 2 places, extract it once: a pure function in the shared utils or common service, a pure pipe in templates, a shared component for repeated markup. If you find a sibling code path that does the same job, call it instead of copying it.
2. **[reviewed, ~12 MRs] Keep the change inside the ticket.** Unrelated refactors, typing sweeps, global CSS edits, icon removals and "while I was here" cleanups get sent back or split into their own ticket. The strongest case: a bugfix near a release that carried a refactor. The reviewer wanted less code, so it is easier to understand, cherry-pick or revert, and less likely to cause side effects. When you notice something worth fixing, name it in the handover and offer a follow-up ticket.
3. **[reviewed, ~10 MRs] Simplify.** Drop redundant checks, needless `async`, extra arrays, one-use variables, complex DOM queries, boilerplate markup. Prefer `ViewChild`/`ViewChildren` over `closest`/`getAttribute`. Prefer a plain `for...of`, optional chaining, a `switch` over a long `if` chain. Reviewers often hand over the simpler version as a suggestion block: take it.
4. **[reviewed, ~8 MRs] Type and null-safety where you touch code.** Typed dialog results, named types instead of inline shapes, a boolean flag instead of a magic string, generated DTOs instead of hand-rolled shapes, `?.` and fallbacks for parse results. No `$any`, `Partial` or casts to get around a type. Not a licence to retype untouched code (see 2).
5. **[reviewed, ~8 MRs] CSS lives in the affected component.** No edits to the app-level or global stylesheet for a local problem. Use a CSS class, not height maths in TypeScript, a timeout or a jQuery calculation. No magic numbers. It must survive resizing.
6. **[reviewed, ~8 MRs] The reviewer runs the UI.** Check overflow, scrollbars, padding, cut-off German text (long words), dialog widths, tooltips, the empty state, and the "regression" path. Attach a screenshot or short recording for visual changes. If you could not run the app, say so.
7. **[reviewed, ~5 MRs] Translations done properly.** A new key, not a string transformation of an existing one. Key names match across files. Add the key to all three language files. (Older MRs added only German and English, and the later ones add all three, which the CI parity check enforces.)
8. **[seen, 2 each]**
   - Apply the fix to every variant: all delete paths, all callers of the changed method, sibling fields.
   - Do not remove existing behaviour or a `default` branch while fixing something else.
   - Cancel stale requests and avoid races (`takeUntil`, a subject), and tear subscriptions down.
   - Do not leave dead code or a duplicate path after introducing a new one.
   - Do not put an MR explanation in a code comment, and avoid negated conditions.
   - Validate input instead of guessing. Guard against invalid or inactive configuration.
9. **[once]**
   - Subscribe to `valueChanges` in `ngOnInit` rather than using a template event handler on a form control.
   - `ngSwitchDefault` goes last.
   - Prefer an enum over a hard-coded string.
   - Use plain attributes for hard-coded strings, not property bindings.
   - Small components with inputs and outputs rather than global service state or passing a `TemplateRef`.
   - Descriptive log messages in the backend.
   - Product design questions go to the product owner.

## What CI flagged on these MRs

The review bot reported: `no-explicit-any` (mostly in specs), `no-unused-vars` (leftover imports), `eqeqeq`. These are cheap to avoid: run the changed-lines check in [lint-format.md](lint-format.md) before handover.

## Tests

- 7 of 120 MRs changed a spec, and all 7 are recent and logic-heavy (new component logic, new services, backend contracts). Small bugfixes, CSS and template fixes shipped without one, and no comment in the sample asks for one.
- The project rule still applies: write tests with the change (`AGENTS.md`). The practical reading: logic gets a spec, a pure function gets a spec, a style tweak does not need one. Say which you chose.

## Before you hand over, ask as the reviewer would

1. Is there an existing helper, pipe, constant or component I should have used? Is any logic now in two places?
2. Could this diff be smaller? Is every changed line needed for the ticket? What would I leave for a follow-up ticket?
3. Is anything more complicated than it needs to be: a check, a variable, an `async`, a DOM query, a duplicated block?
4. Did I handle every variant, caller and language?
5. Does the new code leave a subscription open, a stale request running, or a method call in a template?
6. Does it look right at a narrow width, with long German text, and in the empty and error states? If I did not see it, did I say so?
7. Does CSS stay in the component, and are there magic numbers?
8. Did I remove or change behaviour the ticket did not mention?
