# Project verification

Use the repository's existing tests and application driver first. A recipe must
identify the actual build/instance, reach a usable state with disposable seeds,
exercise the changed user path, and retain observable proof after cleanup.
For a web interaction, use the authorized browser driver; for CLI/TUI work,
use its command or isolated PTY; for a parser/API, replay representative inputs.
Do not replace an unreachable required path with a convenient unit test and
call the behavior verified. Missing production access is not permission to use it.

When there is no working project recipe, the reusable pstack skills are
`create-verification-skill` (setup once) and `maintain-verification-skill` (on
demonstrated drift). Use `tdd` for a cheap defect reproduction and
`principle-test-behavior-not-implementation` when judging its assertions.
They can be used individually; enabling `poteto-mode` is not required.

Pinned source is Lauren Tan's MIT-licensed pstack at commit
`1b6d44ff26d4e242f4e8f68c391e6d2f7ca16def`:
[selected skills](https://github.com/cursor/plugins/tree/1b6d44ff26d4e242f4e8f68c391e6d2f7ca16def/pstack/skills).
Keep any installed subset external to this repo, with its references/license.
Translate only discovery paths and control tools for the harness; retain usable
readiness, seeds, isolation, side-effect checks and evidence retention. Verify
the generated recipe end to end before relying on it. Missing skills do not
block a repository that already has a proven harness.

Verification effort follows the risk and affected behavior. Do not add a design
panel, whole-app sweep, performance benchmark or new test framework to every
small issue. Record a missing baseline or prerequisite explicitly. Scheduled
checks use `scheduled-proof.md`; execution records establish what ran, while
the verifier is responsible for whether it proves the acceptance criterion.
