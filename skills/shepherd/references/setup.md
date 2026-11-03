# Optional setup

Use this path only after the user chooses setup or explicitly requests it.
Bare activation ends at the welcome choice in [SKILL.md](../SKILL.md).
Setup never inventories agents, reads transcripts, or produces an automatic brief.

## Ask once, together

Discover cwd, whether it is a Git worktree, and any existing answers first; use
cwd as the proposed setup root. Omit the Git question outside a repository and
explain that Git protection does not apply; do not initialize one automatically.
Do not ask for a directory or preference already supplied. Use one native
questionnaire if it supports multiple fields; otherwise send one compact message:

> Set this up in `<current directory>` (or tell me another directory):
> - Follow **all agents in this session**, or **a selected group**?
> - Remember selected work for next time: **yes / no**? This saves short context,
>   next steps and recovery pointers, not transcripts or an automatic agent roster.
> - Clickable agent names to jump straight to them: **yes / no**? This enables
>   navigation on this machine across Herdr sessions.
> - Git: **keep everything local (default)**, or **share instructions only**?
>   Shared instructions can contain your scope and preferences; saved work stays local.

Include only unanswered fields, together, rather than a turn per choice. Do not
inventory agents to populate the scope question. A selected group can be described
by projects, names or exclusions without inspection; ask a follow-up only for a
dependent ambiguity (for example, which group after choosing “selected group”).
Resolve a different root before deriving its Git paths. No answer is not consent
to write; the Git default is a proposal, not permission.

Summarize the chosen scope, root, files/content to save, exact local exclude edit,
and any machine-wide navigation effect; obtain confirmation before writes.
Review proposed shared instructions with the user: omit private paths, session
IDs, credentials, work context and other sensitive material. “Share” only makes
instructions eligible for a later deliberate Git action, not automatically public.
Remembering work is independent of standing instructions; “no” creates no checkpoint
and does not delete existing data. Follow [recovery](recovery.md) for minimal data,
scoped helper writes and existing-file preservation, and [navigation](navigation.md)
for approved registration and verification. Do not replace another plugin copy.

## Privacy gate before saving

Perform read-only checks before sensitive configuration or runtime writes. Never
assume ignores protect files already in Git's index. For the confirmed `root`:

1. Determine whether it is inside a Git worktree with `git -C "$root" rev-parse
   --show-toplevel`. Distinguish a genuine nonrepo from command/permission errors.
   Outside Git, local setup is allowed after explaining there is **no Git ignore
   guarantee**; do not initialize a repo. Sharing is unavailable there.
2. Inside Git, derive `repo` and the selected root's repo-relative prefix. Use
   literal pathspecs and quoted argv; do not interpolate paths into shell code.
   Stop on uncertain containment, symlink redirection or path interpretation.
3. **PRECHECK:** from `repo`, run the following with `relative` equal to
   `.shepherd` at repo root or, for example, `team/app/.shepherd` for a nested root:

   ```sh
   git -C "$repo" ls-files --cached --full-name -z -- ":(top,literal)$relative"
   ```

   Check command success and parse NUL-delimited paths. In local mode, **any tracked
   path** under that directory blocks setup. In share mode, only the exact
   `$relative/instructions.md` may be tracked; any runtime or unknown tracked path
   blocks setup. Stop before sensitive writes, report paths without their contents,
   and let the user decide remediation. Never automatically untrack, stage, commit,
   push or force-add anything. Ignores do not remove tracked content or history.
4. Resolve the local exclusion file through Git, not by assuming `.git` is a directory:

   ```sh
   git -C "$root" rev-parse --path-format=absolute --git-path info/exclude
   ```

   A linked worktree's `.git` may be a file. Git normally resolves `info/exclude`
   to a common file across linked worktrees: explain that these repo-relative
   patterns affect matching paths in those worktrees too, not just this directory.
   Confirm that effect before editing; stop on resolution/read/write errors.

Append only the chosen block to the resolved `info/exclude`, preserving unrelated
bytes and rules (insert a separating newline if needed). If absent, create that
file and its metadata parent only as part of the confirmed edit. Do not rewrite
the file or automatically modify any shared `.gitignore`. Here `{prefix}` is empty at repo
root, or the selected root's repo-relative path **with a trailing slash**, such as
`team/app/`. Replace it, retaining the leading `/` anchoring to the repo root.
Escape Git-ignore metacharacters in each prefix component (`\`, `*`, `?`, `[` and
`]`; handle whitespace/line boundaries correctly), or stop if uncertain. Shell
quoting alone does not escape ignore syntax. Reject newline-bearing paths if they
cannot be represented safely. These blocks cover future, unknown runtime names.

### Keep everything local

```gitignore
/{prefix}.shepherd/
```

### Share instructions only

```gitignore
!/{prefix}.shepherd/
/{prefix}.shepherd/*
!/{prefix}.shepherd/instructions.md
```

The first negation opens the directory; the wildcard ignores every child except
the single reviewed instructions file. All runtime files and directories stay
ignored, including `threads.json`, `threads.lock`, `.threads-*.tmp`, backups and
unknown future names. A directory named `instructions.md` is not a shareable file:
stop if that path is a directory or symlink. Do not relax the runtime rule.

## Verify before data writes

After the approved exclude append, but **before** creating/changing instructions,
initializing a checkpoint or writing any sensitive data, check each path separately:

```sh
git -C "$repo" check-ignore --no-index -q -- "$path"
```

Use repo-relative literal paths, not glob-expanded lists. Exit **0** means ignored,
**1** means not ignored, **128** means error; any other error also blocks setup.
Do not mistake a nonzero result for success. Use `check-ignore --no-index -v --
"$path"` for diagnostics, not as a boolean: a matching negation can print a rule
while leaving the path unignored. `--no-index` checks rules even for tracked files;
it does not replace the tracked precheck.

Require instructions ignored in local mode and not ignored in share mode. Require
every existing runtime path plus planned writes ignored in both modes; also probe
`threads.json`, `threads.lock`, `.threads-probe.tmp`, an unknown file and an unknown
directory/child. Check without creating sensitive probe content. Higher-priority
`.gitignore` rules can keep instructions ignored (including an excluded ancestor)
or re-include runtime data despite `info/exclude`. On any mismatch, **stop before
sensitive data writes**, explain the conflicting rule and ask the user to resolve
it or choose another root/mode; never silently edit `.gitignore`. Preserve existing
data and report any already-applied exclude change. Repeat the tracked precheck
and ignore checks immediately before later sensitive writes; concurrent changes
can invalidate an earlier check.

Ignore rules reduce accidental Git inclusion; they are not access control,
encryption, protection against force-add, or removal from Git history/backups.
After verified setup, report only what was saved/enabled and any blockers. Offer
to check agents next, then wait for an explicit request; do not start a brief.

Run the [privacy tests](../tests/test_setup_privacy.py) from the skill repo root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/shepherd/tests -p 'test_setup_privacy.py' -v
```

These stdlib tests exercise this recipe in temporary real Git repositories only;
they do not configure a user's Shepherd, initialize their repo or install anything.
