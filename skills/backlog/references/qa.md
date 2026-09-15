# QA

Judge a change against the **product plan** on the issue (`references/plan.md`).
Not a restatement of how to open a PR. The QA worker is the **role**, not a
named persona — do not call it Quinn or any other bot name.

## When

`phase:qa` — a reviewable change exists that claims this issue.

## Procedure

1. Claim `status:doing`.
2. Read the issue (canonical plan) and the linked change.
3. Check acceptance criteria and in/out of scope. Implementation extras that
   are not in the plan are either out of scope (fail) or a plan hole (back to
   refine).
4. Write the **verdict on the issue** (not only the PR).
5. Labels:
   - **Pass** — leave `phase:qa`. Clear `doing` → `status:open`. **Do not
     merge.** The PM merges (`references/pm.md`).
   - **Bug in the change** — `phase:qa` → `phase:implement`,
     `status:doing` → `status:open`.
   - **Plan was wrong / product hole** — `phase:qa` → `phase:refine`,
     `status:doing` → `status:open` (or `status:blocked` with the question).

## Pass (binary)

A comment that says “PASS” is not a pass. All of the following must hold:

| Required | If missing |
| -------- | ---------- |
| Verdict on the **issue**: `pass`, `implement-again`, or `refine-again` | Not a pass |
| **Every** AC listed as `pass`, `fail`, or `not-reached` | Not a pass |
| No in-scope AC is `fail` | `implement-again` |
| For `type:fix`, the **repro** AC is `pass` (not `not-reached`) | `implement-again` or `status:blocked` |
| QA ran in a **different session** from the implementer | Not QA |
| Linked PR (`Fixes #N` / `Closes #N`); required CI green when CI exists | Not merge-ready |

`not-reached` on an in-scope AC the change claims to fix is **not** a pass.
Write `status:blocked` with the missing check (for example signed-in repro)
when the QA worker cannot reach it.

Self-QA by the implementer (PR comment, local smoke without the repro) does
not satisfy this bar.

## Done when

That written verdict exists, with AC cited, and labels match it.
