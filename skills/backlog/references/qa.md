# QA

Judge a change against the **product plan** on the issue (`references/plan.md`).
Not a restatement of how to open a PR. Do **not** merge PRs or close issues on
pass — that stays with the human owner.

## When

`phase:qa` — a reviewable change exists that claims this issue.

## Scope

Default: the issue's own repo (or the repo the human named for this QA).

If this harness or project defines a **repo allowlist** (persona, `AGENTS.md`, or
a local scope skill), respect it. Outside that list: **BLOCKED** — comment why
and ping the human; do not review. Do **not** put private or org-specific repo
names in this shared file.

## Find the change (PR ↔ issue)

Resolve **one** reviewable change before judging. Prefer, in order:

1. PR body / commits with `Fixes #N`, `Closes #N`, or `Resolves #N` for this issue.
2. PR linked from the issue (Development / linked pull requests).
3. Search open PRs in the same repo for the issue number or clear title match
   (`gh pr list --search "<N>"` / issue URL).
4. If still none (or several ambiguous): **BLOCKED** — comment what you tried;
   ask the human or implementer to link the PR. Do not invent a change to review.

Diff is enough to start; use a preview/deploy URL when the issue or PR provides
one (or the project usually has one).

## Depth

Default bar: **plan / AC compliance** on the claimed change.

Also check:

- Obvious regressions in **touched** paths (broken happy path, clearly broken
  related UI/API in the diff).
- Edge cases **only when AC or in/out implies them**.

Do **not** turn QA into open-ended exploratory testing unless the issue asks.
Prefer preview when available; otherwise judge from the PR diff + checks.

Prefer using the test suite and/or CLI. If you have to use the browser or the
computer manually because a test suite and/or CLI are not available, always ask
for HITL authorization first.

Extras in the change that are not in the plan: **FAIL** (out of scope) or send
back to **refine** (plan hole) — say which.

## Verdict comment (on the PR)

Always leave a short comment on the **PR** (required). Use this shape:

```text
### QA: PASS | FAIL | BLOCKED
Repo: <owner/name>  PR: <#n or none>  Preview: <url or n/a>

AC:
- [x] <criterion> — <one-line evidence>
- [ ] <criterion> — <why it fails / blocked>

Notes: <optional, ≤3 lines>
Next: <merge-ready for human | back to implement | back to refine | waiting on human>
```

## GitHub PR review actions

- On the PR, submit a review matching the verdict:
  - **PASS** → Approve (do **not** merge, do **not** close the issue).
  - **FAIL** → Request changes.
  - **BLOCKED** → Comment on the PR (no approve); leave issue `status:blocked` or
    open with a clear wait reason.
- Label moves are on the **issue**, not a substitute for the comment.

## HITL (when to ping the human)

Ping the human when:

- **PASS** — ready for them to merge/ship (QA does not merge).
- Product judgment call (ambiguous AC, scope dispute, "is this good enough?").
- Repo outside a configured allowlist, missing/ambiguous PR, or security /
  data-loss risk.

Otherwise decide yourself: **FAIL** → `phase:implement` + `status:open`;
plan hole → `phase:refine` + `status:open` (or `blocked`); clear **BLOCKED**
with reason on the issue.

## Procedure

1. If a harness/project repo allowlist applies, confirm the repo is in scope (or
   the human explicitly authorized you). Else BLOCKED + ping.
2. Claim `status:doing` (while `phase:qa`).
3. Find the change (section above). Else BLOCKED.
4. Read the issue (canonical plan) and the change (diff; preview if available).
5. Check AC and in/out of scope at the depth above.
6. Verdict on the PR (template). Submit the matching PR review action above.
7. **PASS** — leave issue open at `phase:qa` (or project "ready to merge"
   convention); clear `doing` → `status:open`; **do not** close or merge;
   ping human that it is merge-ready.
8. **FAIL (bug in the change)** — `phase:implement` + `status:open`; clear `doing`.
9. **Plan wrong / product hole** — `phase:refine` + `status:open` (or `blocked`);
   clear `doing`.
10. **BLOCKED** — comment + ping as needed; `status:blocked` when waiting on human.

## Done when

A written verdict on the PR (PASS / FAIL / BLOCKED) with AC cited, matching PR
review action when a PR exists, and issue labels updated — without merging or
closing on pass.
