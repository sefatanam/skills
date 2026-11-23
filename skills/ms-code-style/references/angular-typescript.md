# Angular and TypeScript

The project paths and names are in `AGENTS.md`, and in `local.md` when present.

## Version limits

Angular 11.2, Material 11 (pre-MDC), RxJS 6.5, TypeScript 4.0.8, target ES2015, lib ES2019.

| Do not write | Write |
|---|---|
| standalone components, `loadComponent` | `NgModule` declarations, `loadChildren` |
| `inject()` | constructor injection |
| signals, `input()`, `output()`, `model()` | fields, `@Input()`, `@Output()` |
| `@if`, `@for`, `@switch` | `*ngIf`, `*ngFor`, `*ngSwitchCase` |
| `takeUntilDestroyed`, `DestroyRef` | `takeUntil(this.destroy$)` and `ngOnDestroy` |
| `new FormControl<string>('')` | `new FormControl('')` |
| `firstValueFrom`, `lastValueFrom` | `.toPromise()` |
| `satisfies`, `override` | a type annotation, no modifier |
| template literal types, mapped `as` (TS 4.1) | string unions, explicit interfaces |
| `.at()`, `replaceAll`, `Object.hasOwn` | indexing, regex `replace`, `hasOwnProperty.call` |
| `mat-mdc-*`, `@use '@angular/material'` | `mat-*`, `@import '~@angular/material/theming'` |

## Types

- **[enforced]** No `any` on new lines (a warning only in specs). Use a real type, a generic or `unknown`.
- **[project]** Use a generated DTO when one fits.
- **[project]** Service payloads are exported `type` aliases in that service file.
- **[observed]** UI models are `interface`s in the project's models folder. Closed sets are string unions, such as `'none' | 'client' | 'server'`. Variants are discriminated by a `kind` field.
- **[observed]** Name event payload types: `EventEmitter<RowEvent<T>>`, not an inline shape.
- **[observed]** Give new methods parameter types, and public ones a return type.
- **[project]** `strict` is off. Do not add `!` or null-safety edits to unrelated code.
- **[observed]** Use `??` for defaults, because `0`, `'0'`, `''` and `false` can be real values. Use `?.` for optional access.

## Components

- **[observed]** New reusable UI goes in the shared UI folder and is exported from its module. New presentational components use `OnPush`. Do not switch an existing component to `OnPush` in passing.
- **[observed]** Reusable inputs get defaults. New outputs are `readonly`. A component that acts as a form field implements `ControlValueAccessor`.
- **[observed]** Shared constants go in the project's existing constants file.
- **[project]** Subscriptions that outlive one value end in `ngOnDestroy`.

```ts
import { ChangeDetectionStrategy, Component, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-example-filter',
  templateUrl: './example-filter.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ExampleFilterComponent implements OnInit, OnDestroy {
  @Input() labelKey = '';
  @Output() readonly valueChange = new EventEmitter<string>();

  readonly control = new FormControl('');
  private readonly destroy$ = new Subject<void>();

  ngOnInit(): void {
    this.control.valueChanges.pipe(takeUntil(this.destroy$)).subscribe((value: string) => this.valueChange.emit(value));
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

## Templates

- **[project]** No method calls or getters in bindings. Use a precomputed field or map, or a pure pipe. Event handlers such as `(click)="save()"` are fine.
- **[enforced]** `strictTemplates` is on, so the AOT build rejects mistyped bindings.
- **[observed]** Reused cell `ng-template`s sit at the end of the file.
- **[observed]** CDK table header and row definitions are never behind `*ngIf`. The table throws "Missing definitions" on first render.

## Services and imports

- **[enforced]** Feature code never imports `HttpClient`. Use the project's API wrapper.
- **[project]** JSDoc on exported classes and public methods of services.
- **[enforced]** Import case matches disk.
- **[enforced]** No pre-6 RxJS or `rxjs-compat` imports.
- **[observed]** Use `src/app/...` across features and `./` beside the file.
- **[project]** Never add or edit the legacy `.js` files that sit next to `.ts`.

## Styles

- **[observed]** Scope rules to the component. Use the existing CSS variables, and define shared tokens once in the global stylesheet.
- **[observed]** A global `!important` is overridden by a scoped, more specific `!important`. Do not edit the global rule for one screen.

## Translations

- **[enforced]** A new static key goes into every supported language.
- **[project]** Do not create static keys for content the backend or database owns.

## Dates

- **[observed]** Parse known formats with strict moment: `moment(text, formats, true)`.
- **[observed]** Before reusing a date parser, check that it does not change the case of the format: `mm` is minutes, `MM` is months.

## Tests

- **[project]** Use the project's test doubles for HTTP and translation. Do not use `HttpClientTestingModule`.
- **[observed]** Test component behaviour through `TestBed` and a small host component. Name tests by behaviour: `it('shows the empty message when there are no rows')`.
- **[observed]** A bug fix gets a spec for the exact failing value.
