# Research

Product research: gather facts so a plan can be written without guessing. This is not refine and not implementation.

Scheduled adapter runs use `scheduled-proof.md`: PM owns the claim and labels;
publish the structured proposed outcome instead of applying the transitions below.

## When

Issue is `phase:research`, or `phase:refine` but facts are still thin (repro, current behavior, constraints unclear). Skip when the issue already has enough signal to shape a plan.

## Procedure

1. Claim `status:doing`.
2. Dedupe lightly. If it is the same work as another issue, stop and mark duplicate (see `SKILL.md`).
3. Investigate: code and config as evidence of **what is true today**, `memory.md`, related issues.
4. Write a **research brief** as an **issue comment** (required). Optional file `.backlog/research/RESEARCH-[slug].md` if there is a checkout — still comment a pointer on the issue.
5. List open questions. Do **not** invent acceptance criteria, in/out of scope, or file lists.
6. Enough to plan → `phase:refine` + `status:open`. Need a human → `status:blocked` with the question on the issue. Clear `doing`.

## Done when

Facts and constraints are stated with evidence. Open questions are explicit. A refiner can write a plan without discovering the same unknowns again.

## Brief shape

```markdown
## Research brief

### Facts
- …

### Evidence
- (links, paths, commands — as citations, not as an implementation plan)

### Open questions
- …
```
