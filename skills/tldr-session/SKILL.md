---
name: tldr-session
description: >
  Produce a concise session TL;DR in four parts: how it started, how it is
  going, what was achieved, and what is pending. Use when the user runs
  /tldr-session, asks for a session summary, recap, status check, "where are
  we?", or a quick catch-up on the current conversation.
---

# TL;DR Session

Summarize the current session from conversation history. Stay thin and factual.

Do not start new work, propose plans, or run tools unless you need them to
verify a claim already visible in the session.

## Output

Reply with exactly these four sections:

### 1. How it started
- What the user asked for or what kicked off the session
- Any starting context that shaped the work (repo, branch, constraint, error)

### 2. How it is going
- Current state in one or two sentences
- Whether work is active, blocked, waiting on the user, or done

### 3. What was achieved
- Concrete outcomes only: files changed, commands run, decisions made, bugs
  fixed, answers given
- Skip process narration and tool play-by-play

### 4. What's pending
- Open questions, unfinished tasks, follow-ups, or blockers
- If nothing is pending, say so explicitly

## Rules

- Be brief. Prefer bullets over paragraphs.
- Do not invent facts. If something is unclear, say "unclear" or "not yet done."
- Prefer the current session over older context unless it still matters.
- Do not commit, push, or change files unless the user asks beyond this summary.
