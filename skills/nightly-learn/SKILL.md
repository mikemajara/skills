---
name: nightly-learn
metadata:
  version: "0.1.0"
description: >-
  Use when running a periodic (e.g. nightly) pass to turn sticky how-to facts
  out of agent memory into skills — or when unsure whether something belongs
  in memory vs a skill. Harness-agnostic; each agent runs it on its own memory.
---

# Nightly learn

Agents often stash **procedures** in memory because the user said "remember…".
That is fine short-term. This skill is the **promotion path**: review recent
memory, decide what is really a skill (or a patch to an existing skill), and
land it in the right place.

Like sleep for humans: overnight (or on a schedule) the day's how-to stick and
get filed where they belong.

Harness-agnostic: works wherever the agent has memory and a skills library.
Each agent runs this on **its own** memory (optional: shared user memory). Do
not scrape other agents' private memories as the architecture.

## Memory vs skill (gate)

| Keep as **memory** | Promote to **skill** (or skill patch) |
| --- | --- |
| Who the user is, prefs, names, one-off decisions | How to do a recurring task |
| Transient state ("blocked on X until Friday") | Rules that should apply every time that task runs |
| Facts that do not change a procedure | Steps, tags, formats, checklists |

**Canonical miss:** user says "when looking through Todoist, shopping/Amazon
tasks need tag `shop` / Amazon and a search permalink in the description."
Storing that only in memory is wrong long-term — it belongs in the Todoist (or
shopping) skill so every agent that runs that playbook sees it.

Rule of thumb: if another agent (or tomorrow's run) needs the **procedure**, it
is a skill. If they only need to **know a fact**, it is memory.

## When to run

- On a **schedule** (nightly / weekly) — preferred.
- On demand when the user asks to "clean up memory" or "turn this into a skill."
- After a burst of "remember when doing X…" corrections in chat.

The schedule is a **routine** in the harness (one per agent); this skill is the
recipe the routine runs. Do not hard-code cron syntax here.

## Procedure

1. **Collect candidates** from recent **own** agent memory / logs (and optional
   user-shared memory): lines that sound like steps, tags, formats,
   "always/never when doing X".
2. **Classify** each with the gate above. Skip pure profile facts and ephemeral
   state.
3. **Match target skill**
   - Existing skill that owns that domain (e.g. Todoist playbook) → propose a
     **minimal patch**.
   - No owner and the pattern is reusable across harnesses → propose a **new
     thin skill** (shared lane if connector-agnostic).
   - Harness-only quirks → local / harness-only skill, not the shared repo.
4. **Draft the change** as skill text (what to add/change), not a dump of chat.
5. **HITL for shared contracts** — do not silently rewrite shared upstream
   skills. Present the proposal (diff / review doc / chat) and wait for owner
   approval.
6. **Apply** after approval: update upstream or local skill per the project's
   skills-routing rules; then drop or rewrite the memory fact so it no longer
   duplicates the skill ("promoted to skill X on DATE").
7. **Report** briefly: promoted N, left in memory M, skipped K — with
   links/ids.

## What not to do

- Do not invent product features or large new playbooks unasked.
- Do not fork a shared skill locally "just for tonight."
- Do not delete user memory without leaving a pointer that it moved into a
  skill.
- Do not treat every "remember" as a new skill — only sticky how-to.

## Out of scope

- Connector install or auth.
- Cross-agent private memory scraping.
