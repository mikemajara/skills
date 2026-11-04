# Shepherd

A human-directed coordination skill for agents already running in the current
Herdr session. Version **0.2.0** — [changes and limits](CHANGELOG.md).

```sh
npx skills add mikemajara/skills --skill shepherd -g --agent universal -y
```

Start any supported agent inside Herdr, then say:

> Use the $shepherd skill. Review the agents in this Herdr session and tell me
> what needs my attention.

Or simply say "Be my Shepherd" to choose between checking agents now and setting
things up for next time. That greeting waits for your choice without reading every
pane. Setup does not automatically launch a summary afterward.

No special pane name or directory is required. A requested brief is numbered;
reply with “push item 2,” “park this thread,” or “help me wrap this up.” Inspection
alone does not authorize messages to agents.

- [Batched setup and Git privacy choices](references/setup.md): everything local
  by default, or share instructions only; saved work always remains local.
- [Optional standing configuration and active/parked checkpoints](references/recovery.md).
- [Optional clickable pane/workspace navigation](references/navigation.md).
- [Operating instructions](SKILL.md) and [Herdr adapter](references/herdr.md).

No cron, autonomous nudging, team creation, or implementation takeover.
