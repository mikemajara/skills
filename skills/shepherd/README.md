# Shepherd

A human-directed coordination skill for agents already running in the current
Herdr session. Version **0.1.0** — [changes and limits](CHANGELOG.md).

```sh
npx skills add mikemajara/skills --skill shepherd -g --agent universal -y
```

Start any supported agent inside Herdr, then say:

> Use the $shepherd skill. Review the agents in this Herdr session and tell me
> what needs my attention.

No special pane name or directory is required. The first brief is numbered;
reply with “push item 2,” “park this thread,” or “help me wrap this up.” Inspection
alone does not authorize messages to agents.

- [Optional standing configuration and active/parked checkpoints](references/recovery.md).
- [Optional clickable pane/workspace navigation](references/navigation.md).
- [Operating instructions](SKILL.md) and [Herdr adapter](references/herdr.md).

No cron, autonomous nudging, team creation, or implementation takeover.
