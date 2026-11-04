# Shepherd

A human-directed coordination skill for agents already running in the current
Herdr session. Version **0.2.0** — [changes and limits](CHANGELOG.md).

```sh
npx skills add mikemajara/skills --skill shepherd -g --agent universal -y
```

Start any supported agent inside Herdr, then say:

> Use the $shepherd skill. Review the agents in this Herdr session and tell me
> what needs my attention.

Or simply say "Be my Shepherd". By default, the greeting waits for your choice
between checking agents now and setting things up, without reading every pane.

For recurring use, ask Shepherd to save this line in your local
`.shepherd/instructions.md` during [setup](references/setup.md#default-mode):

```yaml
default_mode: check
```

Then each activation checks the configured agents' work directly and returns a
read-only brief, without asking again. Use `default_mode: ask` to restore the
welcome. Missing or invalid settings use `ask`; explicit requests for the current
run override either mode. A separately configured runner can instead include
`default_mode: check` in each invocation. It must run inside the intended Herdr
session; this setting does not create a schedule or authorize agent messages.
Setup does not automatically launch a summary afterward.

No special pane name or directory is required. A requested brief is numbered;
reply with “push item 2,” “park this thread,” or “help me wrap this up.” Inspection
alone does not authorize messages to agents.

- [Batched setup and Git privacy choices](references/setup.md): everything local
  by default, or share instructions only; saved work always remains local.
- [Optional standing configuration and active/parked checkpoints](references/recovery.md).
- [Optional clickable pane/workspace navigation](references/navigation.md).
- [Operating instructions](SKILL.md) and [Herdr adapter](references/herdr.md).

No cron, autonomous nudging, team creation, or implementation takeover.
