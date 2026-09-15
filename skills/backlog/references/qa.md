# QA

`phase:qa` is where the backlog pipeline **checks the change against the plan**.
Earlier phases already defined the product intent: research (if any), then refine
locked the plan — problem, goal, in/out of scope, and **acceptance criteria**
(`references/plan.md`). QA does not invent new product criteria; it verifies
those.

## Goal

1. **Validate every acceptance criterion** with concrete evidence.
2. **Check for regressions** in what the change touches (and happy paths the AC
   imply).
3. **Guard scope** — behavior outside the plan fails or goes back to refine.

Do not turn QA into open-ended exploratory testing unless the issue asks for it.

## Inputs (from earlier phases)

| Source | Use |
| ------ | --- |
| Issue (canonical) | Goal, in/out, AC; open questions should be empty or answered |
| Change under review | Diff, CI/checks, preview only if the project usually has one |
| `.backlog/plans/…` | Only if still a draft buffer — the issue wins when both exist |

If AC are missing or not testable, that is a **refine** gap: send the issue back;
do not invent criteria.

## Standards

### Acceptance criteria

- Walk AC **one by one**. Each needs a short evidence line (test name, CLI
  output, check run, or a precise diff/pointer).
- Prefer the project's **automated tests and CLI** when they can show the AC.
- Manual checks only when an AC cannot be shown otherwise — keep them minimal
  and tied to named criteria.

### Regressions

- Exercise or inspect coverage for **touched** paths and their obvious callers.
- A broken happy path in a touched area is a fail even when AC did not spell it
  out.
- Stay out of unrelated product areas.

### Scope

- Extras not in the plan: **FAIL** (out of scope) or back to **refine** (plan
  hole). Say which.

## Verdict

Leave a short written verdict that cites AC. Prefer the PR when the project uses
pull requests; otherwise comment on the issue.

```text
### QA: PASS | FAIL | BLOCKED

AC:
- [x] <criterion> — <one-line evidence>
- [ ] <criterion> — <why it fails / blocked>

Regressions: <touched paths checked / gaps>
Next: <ready for human ship | back to implement | back to refine | waiting>
```

| Verdict | Meaning | Labels |
| ------- | ------- | ------ |
| **PASS** | AC met; no blocking in-scope regressions | Leave `phase:qa` (or project “ready”); clear `doing` → `status:open`. Agent QA does **not** merge or close — shipping stays with the human / project convention. |
| **FAIL** | Bug in the change | `phase:implement` + `status:open` |
| Plan wrong | Product/AC hole | `phase:refine` + `status:open` (or `blocked`) |
| **BLOCKED** | No clear change, no access, or needs a human call | Comment why; `status:blocked` when waiting |

Harness-specific rules (repo allowlists, how to find PRs, which review button to
click) belong in the harness or persona — not in this shared file.

## Procedure

1. Claim `status:doing` while `phase:qa`.
2. Identify **one** reviewable change for this issue. If none or ambiguous:
   **BLOCKED**.
3. Read the inputs above; list the AC you will check.
4. Validate AC, then regressions, at the standards above.
5. Record the verdict; move labels; clear `doing`.

## Done when

Every AC has an evidence line, in-scope regressions were considered, and the
issue has a clear next step (or a human handoff on PASS).
