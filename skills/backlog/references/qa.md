# QA

Judge a change against the **product plan** on the issue (`references/plan.md`).
Not a restatement of how to open a PR. The QA worker is the **role**, not a
named persona — do not call it Quinn or any other bot name.

## When

`phase:qa` — a reviewable change exists that claims this issue.

## Procedure

1. Claim `status:doing`.
2. Read the issue (canonical plan, including the QA checklist) and the linked change.
3. Execute that checklist. Do not drop checks. Add relevant regression checks
   when the diff or observed behavior reveals a gap; explain the evidence.
   Judge from the issue, the diff, and CI. Do not run `agent-browser` or any
   other browser automation unless the human explicitly enabled browser QA
   for this work. Implementation extras that are not in the plan are either
   out of scope (fail) or a plan hole (back to refine).
4. Write the **verdict on the issue** (not only the PR), naming the PR URL,
   exact tested head SHA, commands/scenarios actually run and their results.
   Use a plain line `QA verdict: pass`, `QA verdict: implement-again`, or
   `QA verdict: refine-again` so the scheduled runner can recognize the verdict.
   A changed PR head invalidates the pass; run QA on the new head.
   For scheduled review delivery, include a JSON code block with a
   `backlog_qa` object: `verdict`, `pr_url`, `head_sha`,
   `acceptance_results` (each has the literal `criterion`, `result`, and
   `evidence`), and `validations` (each has `command`, `result`, and
   `evidence`). Include every acceptance criterion and actual validation.
   A pass needs nonempty evidence and passing results in both lists.
   Later verdicts on the same head supersede earlier ones.
   For scheduled review delivery, copy canonical AC into an issue body/comment
   list under `## Acceptance criteria` if they currently exist only in a plan
   file. Receipt criteria must match that list's text; the runner checks coverage.
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
| Tested head SHA matches the current linked PR head; validation evidence recorded | Not a current pass |
| Verdict on the **issue**: `pass`, `implement-again`, or `refine-again` | Not a pass |
| **Every** AC listed as `pass`, `fail`, or `not-reached` | Not a pass |
| No in-scope AC is `fail` | `implement-again` |
| For `type:fix`, the **repro** AC is `pass` (not `not-reached`) | `implement-again` or `status:blocked` |
| When a PM split the roles, QA ran in a **different session** from the implementer. A single agent walking every phase may QA here, and still must write this verdict | Not QA when roles were split |
| Linked PR (`Fixes #N` / `Closes #N`); required CI green when CI exists | Not merge-ready |

`not-reached` on an in-scope AC the change claims to fix is **not** a pass.
Write `status:blocked` with the missing check (for example signed-in repro)
when the QA worker cannot reach it.

Self-QA by the implementer (PR comment, local smoke without the repro) does
not satisfy this bar.

## Done when

That written verdict exists, with AC cited, and labels match it.
