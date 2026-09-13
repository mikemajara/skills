# GitHub (`gh` and scripts)

Use this file when the tracker is GitHub. Procedure lives in `SKILL.md` and the phase references.

Run `gh` from the project repo, or pass `--repo owner/repo`.

## Scripts

From the installed skill (paths vary). `--format json` for machines.

```bash
node scripts/backlog-setup.mjs
node scripts/backlog-setup.mjs --dry-run
node scripts/backlog-setup.mjs --check
node scripts/backlog-setup.mjs --skip-labels --skip-scaffold --skip-agent-hint

node scripts/backlog-status.mjs
node scripts/catch-up-gather.mjs --format json
node scripts/backlog-refinement-candidates.mjs
node scripts/backlog-issue-audit.mjs 123
node scripts/backlog-dedupe.mjs --title "Repair login redirect"
node scripts/backlog-sync.mjs
node scripts/backlog-sync.mjs --repo owner/repo --state open --limit 500
```

`--check` on setup reports missing scaffold, stale agent hint, and missing labels from `labels.json` (schema 3).

## Labels

Prefer `backlog-setup.mjs` (reads `labels.json`). Manual create is `--force` upsert:

```bash
gh label create "type:feat" --color "1D76DB" --description "New behavior or capability"
# …see labels.json for the full set
```

## Review and queues

```bash
gh issue list --state open --label "status:doing" --limit 50
gh issue list --state open --label "status:open,phase:refine" --limit 50
gh issue list --state open --label "status:open,phase:implement" --limit 50
gh issue list --state open --label "status:open,phase:qa" --limit 50
gh issue list --state open --label "status:blocked" --limit 50
gh issue list --state open --label "phase:implement,priority:high" --limit 50
```

Dedupe search:

```bash
gh issue list --state all --search "<keywords>" --limit 20
gh issue view 123
```

```bash
gh issue edit 123 --add-label "status:duplicate" --remove-label "status:open,status:doing,status:blocked"
gh issue comment 123 --body "Duplicate of #456"
gh issue close 123 --reason "not planned"
```

## Claim and finish

```bash
gh issue edit 123 --remove-label "status:open" --add-label "status:doing"
gh issue edit 123 --remove-label "status:doing" --add-label "status:open"
gh issue edit 123 --remove-label "status:doing" --add-label "status:blocked"
```

Advance phase (remove the old `phase:*` first):

```bash
gh issue edit 123 --remove-label "phase:refine" --add-label "phase:implement"
```

Promote:

```bash
gh issue create \
  --title "Repair login redirect" \
  --body "Users return to the wrong page after sign-in." \
  --label "type:fix,priority:high,phase:refine,status:open"
```

```bash
gh issue list --state open --json number,title,labels,updatedAt,url --limit 100
gh issue view 123 --json number,title,body,labels,state,comments
```

If `gh` is missing, use a fresh `.backlog/issues.md` from `backlog-sync.mjs`.
