---
name: agent-enablement
metadata:
  version: "0.2.0"
description: >-
  Explore how an agent could become more useful through conversation informed by
  relevant skills, approaches, tools, and learning resources. Use when the user
  explicitly asks to discuss, enable, equip, or develop an agent's capabilities,
  or invokes agent-enablement. Do not activate merely because an agent is new or
  receives a task.
---

# Agent enablement

Be a thinking partner about what an agent could do and what would help it do
that well. Start from the user's direction, bring useful evidence into the
conversation, and let their responses shape what to explore next. A defined
task, named agent, or formal learning plan is not required.

## Explore together

Use the context already given: interests, role, recurring work, ambitions, and
constraints. Discuss a small, coherent handful of points at a time, usually one
to three. Contribute a concrete observation or useful resource, explain its
relevance, then leave room for the user's response. Ask a focused question only
when the answer would change the discussion.

Look for gaps, tradeoffs, and overlooked possibilities without replacing the
user's direction. Keep unresolved threads in context and revisit them as useful.
Do not turn the exchange into an exhaustive inventory, intake questionnaire,
configuration audit, or approval package. Offer a synthesis or learning path
when the user asks for one; do not declare the exploration finished for them.

## Bring in useful resources

Treat relevant existing local skills as part of the baseline. Check the local
catalog for useful candidates before looking for additional skills, without
requiring a per-agent assignment check. Verify actual access only when a concrete
recommendation depends on it or the user asks about availability.

Follow the question beyond skills: useful additions may include methods,
official documentation, tutorials, examples, tools, domain knowledge, or expert
input. Research what would advance the current discussion rather than compiling
a catalog of everything the agent might ever need.

- Read the most relevant local candidates. If an available `find-skills` skill
  helps with external skill discovery, use its guidance; otherwise inspect
  suitable catalogs or source repositories directly.
- Read [research.md](references/research.md) when external research would help.
  Use a focused first pass, stop when there is enough evidence for the current
  question, and adapt further research to the conversation or the user's budget.
- Link inspected resources and explain what each adds and why it fits. Judge
  skills by their instructions, provenance, dependencies, and maintenance;
  popularity alone does not establish suitability. Mark inaccessible candidates
  as unverified rather than presenting them as ready to use.
- Separate reusable instructions from knowledge, tool access, and expert
  judgment. A skill cannot silently supply missing credentials, connections, or
  professional qualifications. Reading a resource does not prove competence.

Surface a few relevant findings naturally, with material uncertainties. Do not
require research counts, a prescribed report, or a complete learning path for
every conversational turn.

## Turn discussion into action when requested

When the user asks for a plan, organize the useful additions by practical value
and prerequisites. Explain what each adds, its source, any dependencies, and a
small exercise or observable result that could demonstrate useful application.
Reuse existing resources where they fit.

When the user requests implementation, use the environment's actual supported
mechanisms and the scope already authorized. Confirm the specific selection if
it is ambiguous; do not treat exploration or enthusiasm as authorization to
install resources, change standing instructions, or begin unrelated work.
Recheck external skill content before installation and verify changes at their
actual destination. Describe any refresh needed and distinguish verified results
from pending work. Use practice exercises within the authorized scope.

Keep the workflow portable across agent environments. Do not require a particular
product, configuration model, or agent-management feature to explore or apply a
recommendation.
