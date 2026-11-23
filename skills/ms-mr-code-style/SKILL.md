---
name: ms-mr-code-style
description: How a senior frontend developer on the MS project solves tickets, learned from the code of 34 of their merged Angular 11 merge requests. Covers where the fix goes, which helpers to extract, how specs are written, and which of their habits not to copy. Use when planning, writing or reviewing Angular or TypeScript client code in the MS repo (ASP.NET Core plus Angular 11, TypeScript 4.0, RxJS 6), alongside the ms-code-style skills. Not for other repositories.
metadata:
  author: sefatanam
  version: "1.0.0"
---

# MS merged-MR code style

Solve a ticket the way the reference developer's merged client changes do: a small diff at the layer that owns the problem, logic in a named pure function with its own spec, a template that only binds fields, a comment that says why.

This is evidence from code, not from review comments. It was read from the diffs of 34 merged merge requests that changed the client, over about six months. Counts below are MRs out of 34 and were tallied by reading, so treat them as approximate.

Applies only to an Angular 11 plus .NET checkout with a `ClientApp/.eslintrc.new-code.json`. Anywhere else, say so and stop. If `references/local.md` exists, read it. It is gitignored and holds the names and MR numbers behind these rules, so never copy from it into published files.

## Precedence

1. What Sefat says in this conversation.
2. The checkout's `AGENTS.md` and config files (they can change per branch).
3. `ms-code-style` or `ms-code-style-2`, if installed. They hold the lint and Angular 11 version limits. This skill adds how accepted solutions are shaped.
4. This skill.
5. The surrounding code.

Tags: **[habit]** in 10 or more of 34 MRs. **[common]** in 5 to 9. **[seen]** in 2 to 4. **[avoid]** the developer does it, but it breaks a project rule, so do not copy it.

## Where the fix goes

- **[habit, ~18]** Fix at the layer that owns the problem and keep the diff to the ticket's lines: a guard in the service, a shared loader, a shared constant, a CSS class, one flag added to an existing `[ngClass]` object. Do not patch each caller.
- **[habit, ~15]** When logic is new, put it in an exported pure function with a one-line JSDoc, in a sibling `*-utils.ts` or `*.helper.ts` file (or the project's shared utils folder), and give it its own spec. Keep the old entry point as a thin delegate that calls the new function, so callers do not change.
- **[common]** Create a new file only when the logic is reusable or isolated. Name it after its folder.
- **[common]** Replace magic numbers and keys with a module-level `const` (`PANEL_MIN_WIDTH`, a storage key).
- **[seen]** Replace several positional arguments with one typed object parameter. Remove shared mutable state in favour of an explicit `@Input` or pipe argument.
- Reuse before writing: the developer extended existing structures in most bugfixes. Search for the existing helper first.

## Templates and state

- **[habit]** Bind to precomputed fields, one handler, an extended `[ngClass]` object or a pure pipe with an argument. Unit-suffixed bindings are normal: `[style.min-height.px]="resultMinHeightPx"`.
- New templates added no method call or getter in 31 of 34 MRs. When touching old code, the developer replaced getters with fields. **[avoid]** The other 3 added `isX()` style calls to templates. Do not copy them.
- Booleans start with `is`/`has`, pixel values end in `Px`, observables end in `$`, handlers say the intent (`onWordListFanout`).
- Forms stay untyped: `new FormControl({ value, disabled })`, and `setValue(x, { emitEvent: false })` when the change must not echo. Subscribe to `valueChanges` in `ngOnInit` instead of a template handler.
- CSS: a scoped class or custom property in the component, not a global edit. When a global override is needed, extend the existing selector list and remove the `!important` it depended on.

## Null handling and types

- **[habit, ~16]** `?.`, `??`, `|| []` and early-return guards. A function returns an empty collection or empty string, not `null`. No `!` assertions.
- **[common]** Declare payload shapes as exported `type` aliases next to their use, and use generated DTOs where one fits. Use `unknown`, unions, `Record` and `Map<K, V>` before `any`.
- **[avoid]** `any` in production code (6 of 34 MRs), `==` and `!=` copied from neighbouring lines (7 of 34), a duplicated method pasted into three components, and reformatting lines the ticket did not need (4 of 34). New code uses `===` and one shared implementation.

## Subscriptions

- Long-lived streams use `takeUntil(destroy$)`, with `next()` and `complete()` in `ngOnDestroy`. Observers get `disconnect()`. Every new long-lived subscription in the sample had a teardown.
- One-shot HTTP calls may subscribe without cleanup.
- Expose a private `Subject` as a public `readonly x$` stream through `asObservable()` when other components must react to a change. See [references/idioms.md](references/idioms.md).
- **[avoid]** Duplicate operators, such as two `takeUntil` calls on the same pipe.

## Tests

- **[habit, 27 of 34]** Every functional change ships with a spec, even a small bugfix. Pure CSS, constant and config changes do not.
- Spec names are full behaviour sentences, with the edge or failure named: "keeps the default of a number field when the stored value is null", "stops listening to ticks once destroyed".
- **[common]** Test the pure helper directly. Test a component without TestBed by building it with `new Component(stubs)` and `jasmine.createSpyObj`. When Angular must be involved, use a light `TestBed` with `NO_ERRORS_SCHEMA`, `ApiService` stubbed through the repo's `testing/api.service.mock.ts`, and the repo's translate testing helper. Never `HttpClientTestingModule`.
- **[common]** Data-driven cases: `[...].forEach(x => it(\`... ${x}\`))`, with the value in the title.
- Include the cases that fail in practice: null, empty, unknown, failure, destroyed, and "does not emit when it fails".
- A destroy-then-emit spec proves teardown.
- **[avoid]** `any` in specs is widespread (about half the MRs). The review bot flags `no-explicit-any` on added spec lines, so type the stubs as `jasmine.SpyObj<T>` instead. Reaching a private member with `(component as any)` is tolerated in specs, but prefer testing through the public method.

## Comments

- **[habit]** A comment says why, or names the cause and the exit plan ("remove once we are on …"). It does not restate the code.
- JSDoc on new exported functions, service methods and exported types.
- Delete dead or commented-out code and stale comments in the lines you touch.

## Translations

New user-visible text gets a key in all three language files, nested under its screen group (`Group.Key_Name`) with real German and French text. Show it through the existing notifier or the `translate` pipe. Reuse an existing key when one fits.

## Before handover

1. Is the fix at the root, and does the diff touch only the ticket's lines?
2. Is new logic in a named pure function with a spec, and the old entry point a thin delegate?
3. Does the template only bind fields? Did I copy a method call from the old code?
4. Is every new long-lived subscription torn down?
5. Does each behaviour change have a spec with edge cases, and are the stubs typed?
6. Did I add `any`, `==`, a copy-pasted method or an unrelated reformat?
7. Is there a "why" comment, JSDoc on exports, and a key in all three language files?
