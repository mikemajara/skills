# Spawn

Handoffs live in `references/pm.md`. Herdr commands live in
`references/herdr.md`.

Open `herdr.md` only when `test "${HERDR_ENV:-}" = 1` succeeds. Otherwise do
not run `herdr` and do not look for another terminal harness. Tell the human
the next role and wait.
