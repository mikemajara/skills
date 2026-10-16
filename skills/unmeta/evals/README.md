# Unmeta evaluation cases

`evals.json` contains model-based behavioral checks, not executable unit tests.
They do not run automatically on install, skill use, or push, and passing them
does not prove that a harness will discover or load the skill.

## Run a comparison

1. Snapshot the previous skill before changing it.
2. For each case, give separate fresh agents the same `prompt`: one with the new
   skill and one with the snapshot. Do not show either agent the expected output
   or expectations, or let one see the other's answer.
3. Save each agent's next visible reply unchanged. For conversational cases,
   treat the turns in the prompt as the history. Do not invent the user's reply
   to a clarification question.
4. Have a separate reviewer grade every expectation using quoted evidence.
   Semantic restatements count as repetition even if the wording differs.
   An ambiguous case passes only if the agent asks before producing the affected
   content; a question inside the authored answer is a failure.
5. Compare results case by case. Investigate regressions and add new real-world
   failures as synthetic cases. Repeat runs before claiming reliable improvement.

Cases 1–3 preserve coverage from the earlier `reader-facing` skill. Cases 4–7
exercise authoring conversations: clear omission, ambiguity, explicit disclosure,
and revision feedback. The two outline cases deliberately require different
behavior: ask when intent is unclear; disclose when the user explicitly asks.

The prompts replay conversational history inside a single test request; this is
not an end-to-end multi-turn tool or document test. Behavioral runs explicitly
load the skill, so actual routing/discovery still needs a check in the user's
agent harness. Verify its loaded skill list and test a fresh session after a
rename; an existing session may retain the old name or instructions.

## Initial comparison

One fresh agent per case and configuration produced 14 replies. A separate
reviewer graded them against the 21 expectations per configuration:

| Configuration | Passed expectations |
| --- | --- |
| `unmeta` | 21/21 |
| Previous `reader-facing` | 21/21 |

The omission case produced the substantive handbook/shadowing answer without
course commentary. The ambiguous case asked whether the missing outline should
be disclosed or was background. The explicit-disclosure case kept the missing
outline in the answer. Both versions did all three correctly in this run.

This run checks intended behavior but does not demonstrate improvement over the
previous skill, reliable performance across models, or automatic activation.
The conversational history was replayed in prompts, not a live form workflow.
