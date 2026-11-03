# Per-skill release information

Each skill has its own `metadata.version` in `SKILL.md` and a bundled
`CHANGELOG.md`. Shepherd started at 0.1.0; the other skills received their
first independent version, 0.1.0, on 2026-11-03. These initial versions are
baselines, not claims that earlier root changelog entries were independently
versioned releases.

- Record user-visible behavior changes, compatibility notes, and migrations in
  the owning skill's changelog. Choose later patch/minor/major bumps from that
  skill's release context, not a repository-wide version.
- Keep data schemas and independently deployed integrations distinguishable
  from skill versions. Coordinate bundled-helper versions where appropriate.
- Preserve the [root changelog](../CHANGELOG.md) as historical repository
  context. Future root notes may cover repository infrastructure and link to
  skill-specific changelogs rather than duplicate their histories.
- A version in metadata does not require an activation-time announcement or
  user-state tracking. Shepherd's activation behavior is specific to Shepherd.
