# Refine

Get the issue to the bar in `references/plan.md`. Refine **writes the product plan**, including a rough **touch** map and any **direction-locking** library/stack choice. It does not sequence implementation or generate the implementer’s code.

## When

`phase:refine`, or research just finished. Skip a long plan file for nits and obvious fixes if the issue body already meets `plan.md`.

## Procedure

1. Claim `status:doing`.
2. Dedupe (`SKILL.md`).
3. Read `references/plan.md`. Put the spec on the **issue**. Use `.backlog/plans/PLAN-[slug].md` only as a buffer, then fold in.
4. Run **hardening** for this `type:*` (below). Skip only with an explicit note.
5. Put **touch** on the issue (rough files/repos). For `type:nit`, `touch skipped: trivial` is enough if the one-line scope already points at the change.
6. If the spec is otherwise complete but would still fork (store, mailer, auth library, …), lock **direction** on the issue or `status:blocked` with the question. Do not invent that choice.
7. Unresolved product decisions → `status:blocked` with the question on the issue. Do not invent behavior.
8. Plan done → `phase:implement` + `status:open`. Clear `doing`. Too large → split issues instead of growing one spec.

## Hardening

Walk required categories **in order**. Skip a category only with `N/A — <reason>`.

Each hit: `Scenario → expected behavior → AC | open question | out of scope`.

No shrug language (“handle errors”). For state or side effects: stop vs continue, what is persisted, what the user sees. Happy-path-only AC is not enough when this pass finds gaps.

### `type:nit` — skip

Note `hardening skipped: trivial`. Still need one-line scope + expected outcome.

### `type:fix` — light

1. Unexpected inputs / system failures
2. User error
3. Feature interactions (regression scope)

Escalate to **full** when the change is cross-cutting, data-model / migration, or external-API sensitive.

### `type:feat` — full

1. User types
2. Contexts of use
3. Unexpected inputs / system failures
4. User error
5. Feature interactions
6. Load
7. Security and privacy
8. Accessibility

## Done when

`references/plan.md` is satisfied on the issue (or skip noted). Then `phase:implement`, or `status:blocked`.
