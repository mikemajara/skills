---
name: agent-enablement
metadata:
  version: "0.2.0"
description: >-
  Explore how an agent could become more useful through conversation informed by
  relevant skills, approaches, tools, and learning resources. Use when the user
  explicitly asks to equip, or develop an agent's capabilities,
  or invokes agent-enablement. Do not activate merely because an agent is new or
  receives a task. Activate this skill only when needed. For example when an agent
  is failing to undersatndi its duty or is lacking knowledge. This can be at the
  start of their life or later on.
---

# Agent enablement

Ask yourself, based on this agent's name and current instructions, how can it
perform better? what skills does it need to find in skills.sh or in the internet
in order to perform it's task better.

- Align with the user on this, don't blindly install new tasks
- bring useful evidence into the conversation, and let the conversation with the user shape what's next.

## Explore together

Use the context already given: interests, role, recurring work, ambitions, and
constraints. Discuss a small, coherent handful of points at a time. Contribute a concrete observation or useful resource, explain its relevance, then leave room for the user's response.

Look for gaps, tradeoffs, and overlooked possibilities when applicable and suggest 
how you wanna cover the gap or how you think they'd improve this agent

Do not turn the exchange into an exhaustive inventory, intake questionnaire,
configuration audit, or approval package. The idea is to keep this simple and offer
the agent a guided way of enabling and finding skills that will make them more efficient

## Bring in useful resources

- Read the most relevant local candidates. If an available `find-skills` skill
  helps with external skill discovery, use its guidance; otherwise inspect
  suitable catalogs or source repositories directly.
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
actual destination. Check installation method based on the harness being used and
do not assume that the installation has to happen in a specific directory or environment

Keep the workflow portable across agent environments. Do not require a particular
product, configuration model, or agent-management feature to explore or apply a
recommendation. And prefer open work like skills.sh and md files that can live in
~/.agents/skills as enablement rather than bespoke application plugins for a harness
