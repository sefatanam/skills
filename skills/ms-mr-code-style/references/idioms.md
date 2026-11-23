# Idioms seen in accepted client changes

Short patterns that recur in the sampled merge requests. Names are placeholders. The version limits in `ms-code-style` still apply: no `inject()`, signals, typed forms or `@if`.

## Pure helper with a thin delegate

```ts
/** Wraps every match of `term` in a highlight span; the text is escaped first. */
export function highlightMatches(text: string, term: string): string { /* ... */ }

// the old entry point stays, so callers do not change
createViewOnlySpan(text: string, term: string): string {
  return highlightMatches(text, term);
}
```

## Long-lived subscription teardown

```ts
private readonly destroy$ = new Subject<void>();

ngOnInit(): void {
  this.control.valueChanges.pipe(takeUntil(this.destroy$)).subscribe(value => this.apply(value));
}

ngOnDestroy(): void {
  this.destroy$.next();
  this.destroy$.complete();
}
```

## Change notification from a service

```ts
private readonly changedSubject = new Subject<void>();
readonly changed$: Observable<void> = this.changedSubject.asObservable();

save(): Observable<Result> {
  return this.api.post(...).pipe(tap(() => this.changedSubject.next()));
}
```

A consumer reloads on `changed$` with `takeUntil(destroy$)`.

## Null handling

```ts
const doc = frame.contentWindow?.document;
if (!doc) {
  return;
}
return event?.snapshot.firstChild?.data ?? null;
(items || []).filter(item => item.isActive);
```

## Template state: field, class object, pure pipe

```html
<div [ngClass]="{ dirty: row.isDirty, 'row-readonly': !row.isEditable }"></div>
<span [style.min-height.px]="resultMinHeightPx"></span>
<span [innerHTML]="text | searchHighlight: searchText"></span>
```

## Spec without TestBed

```ts
describe('SidenavListComponent', () => {
  let menuService: jasmine.SpyObj<MenuService>;
  let component: SidenavListComponent;

  beforeEach(() => {
    menuService = jasmine.createSpyObj<MenuService>('MenuService', ['load']);
    menuService.load.and.returnValue(of([]));
    component = new SidenavListComponent(menuService, {} as Router /* unused deps */);
  });

  it('keeps the selected node when the menu reloads without it', () => {
    // ...
  });
});
```

A comment on why the TestBed is skipped ("it would need a dozen unrelated dependencies") is the accepted form.

## Data-driven spec

```ts
[null, undefined, ''].forEach(value => {
  it(`returns an empty string for ${JSON.stringify(value)}`, () => {
    expect(formatValue(value)).toBe('');
  });
});
```

## Service spec

```ts
TestBed.configureTestingModule({
  providers: [{ provide: ApiService, useValue: createApiServiceSpy() }],
});
service = TestBed.inject(FeatureService);
```
