# Follow-up after publishing Shepherd: per-skill release information

Shepherd establishes the first per-skill version/changelog in this repository.
The remaining rollout is intentionally separate from its initial release.

- Give each skill an independent version under `metadata.version` in its
  `SKILL.md`, and bundle its own `CHANGELOG.md` with user-visible changes,
  compatibility notes and migrations.
- Show the loaded version on activation. Where a skill already has opted-in
  local state, compare the last-seen version and briefly surface relevant
  changes. Do not create user state solely for update notifications.
- Keep data schemas and independently deployed integrations distinguishable
  from skill versions. Coordinate bundled-helper versions where appropriate.
- Preserve the root changelog's historical entries. Move future skill-specific
  release information to the owning skill; root notes may describe repository
  infrastructure and point to those changelogs.
- Choose initial versions or patch/minor/major bumps from each skill's own
  release context with the user; never infer one repository-wide skill version.

This records the agreed follow-up, not completed versioning of other skills.
