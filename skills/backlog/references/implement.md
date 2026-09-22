# Implement

`phase:implement` turns a locked plan into a reviewable change. Keep the change
inside the issue's product scope (`references/plan.md`). You own **how** the
code is written. Touch on the issue is **advisory**: extra files found in the
checkout → capture them on the issue and continue. Product behavior or a
direction-locking choice that contradicts the plan → `phase:refine` or
`status:blocked`. When a reviewable change exists, move to `phase:qa` **in the
same turn** (labels must not lag the PR). **Do not merge** — the PM merges
after QA (`references/pm.md`).

If this run was kicked off with `@cursor` (or similar), follow that comment's
mandate; it should already say not to merge (`references/spawn.md`).

## PR and issue hygiene

Overlapping implement work is a common failure mode: several draft PRs for the
same concern, then one merge that folds them — and the old drafts stay open and
go dirty vs the default branch.

Rules:

1. **One active implement PR per concern.** Before opening or continuing a PR,
   search for open PRs/issues on the same concern. Prefer updating the existing
   PR (or closing it as superseded) over starting a parallel draft.
2. **Supersede in the same turn.** When a merge (or a newer PR) folds or
   replaces older work, **close the superseded issue and PR in that same turn**.
   Comment with the winner (`Superseded by #N` / `Folded into #N`). Do not leave
   orphan drafts.
3. **No "just in case" drafts.** If the default branch already has the behavior,
   close the draft PR (and the issue if it is done). Keeping it open "for later"
   creates noise and dirty branches.
4. **Optional dirty-vs-main sweep.** On review/triage (or when asked), list open
   PRs that are behind or conflicting with the default branch and propose
   **close** (superseded / already on main) vs **rebase** (still needed). Do not
   mass-close without a one-line reason each.

These are tracker hygiene — same spirit as issue dedupe — not harness-specific.

## Done when

A reviewable change claims the issue and labels move to `phase:qa`, **or** the
work is blocked/refined with the reason on the issue, **and** any PRs/issues this
change superseded are closed with pointers.
