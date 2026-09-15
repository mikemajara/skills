# Catch-up

**Read-only.** Do not claim issues, change labels, edit `.backlog/`, or
recommend what to do next. After the brief, stop — do not continue into
review → triage → claim.

If this chat is already the **PM**, skip this file and use `references/pm.md`.
Parallel work / collision while PM is a wake, not catch-up.

The user was away or is walking in with their own task. They need a short
map of leftover work and live collision—then they drill down.

## Effort

Medium. Recent activity plus a small always-include set. Not an exhaustive
search, not every open issue.

1. Run `scripts/catch-up-gather.mjs` from the project cwd. Prefer
   `--format json`. If the script is missing, use the bounded commands below.
2. Skim `AGENTS.md` (or `CLAUDE.md`) for the project goal—not the whole file.
   Optionally the tail of `.backlog/memory.md` if it exists. Do not dump it.
3. Reconcile using this skill’s labels. Write a **brief natural summary**.
   Stop.

Skip GitHub only if `gh` fails; say so. Local git is this machine and will
differ from other laptops—label it **this machine**.

## What belongs in the brief

Always:

- What recent commits suggest has actually been happening, against the
  stated project goal (tracking, drifting, or chores).
- `status:doing` and `status:blocked` (usually tiny; include even if quiet).
- Drift, for example:
  - issue `status:doing` but a PR already exists
  - issue closed/done but a worktree or branch is still **this machine**
  - branch/PR moving while the issue is still `status:open` in an early phase
- **This machine:** current branch, dirty tree, worktrees, unpushed or
  behind/ahead vs upstream when cheap to see.

Then, only if it has been moving in recent commits, branches, or PRs: other
pending work (anything not done/closed: `phase:implement` unstarted, qa,
refine, …). Quiet pending work is a **count** (and maybe the dominant
phase), not a list.

Do not list the full open backlog. Do not end with a recommended next issue.

## Output

A short briefing the user can scan in seconds. Prose first; bullets only for
the live threads. Rough shape:

```text
<2–4 sentences: recent work vs project goal, where agents/you left off>

Live / claimed:
- #N … (phase/status; PR or quiet; drift if any)

This machine:
- … (or “clean, one worktree” — skip if nothing)

Pending otherwise: N open issues (mostly phase:…); not listing quiet ones.
```

Name issue numbers. Mark local-only leftovers as local. If gather data is
thin, say what you could not see.

## Bounded gather

Same limits as `scripts/catch-up-gather.mjs`. Do not paginate past these.

```bash
node scripts/catch-up-gather.mjs --format json

git rev-parse --abbrev-ref HEAD
git status -sb
git log -15 --pretty=format:%h%x09%ad%x09%s --date=short
git worktree list --porcelain
git for-each-ref --format='%(refname:short) %(upstream:track)' refs/heads | head -40

gh pr list --state open --limit 20 --json number,title,headRefName,url,updatedAt,isDraft
gh issue list --state open --label "status:doing" --limit 50 --json number,title,labels,updatedAt,url
gh issue list --state open --label "status:blocked" --limit 50 --json number,title,labels,updatedAt,url
gh issue list --state open --limit 50 --json number,title,labels,updatedAt,url
```

Issue numbers in branch names (`#12`, `issue-12`, `12-foo`):

```bash
gh issue view 12 --json number,title,state,labels,url
```

Cap at a handful of views. Do not `gh issue list` closed issues in bulk.

## Rules

- Brief over complete.
- Recency of git/GitHub is the main signal of “what was going on.”
- Claimed and blocked are not optional just because they are quiet.
- GitHub is shared; worktrees and dirty trees are this checkout.
- No triage, no claim, no “you should continue on #N.”
