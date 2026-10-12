# Scheduled outcome contract

Applies only when the PM provides a dispatch adapter. Workers propose phase
changes; the adapter validates the durable issue outcome, and the PM applies
labels. Runtime registry and evidence live outside product branches. Do not
commit `.backlog/autonomous-*` files. Never spawn native subagents or another
coding CLI; every model worker must be admitted by the adapter.

Before implementation/QA, promote the full product specification into the issue
body, including `## Acceptance criteria` and `## QA checklist` lists. Each
check names the action/input, expected observable result and environment.
Nits need one short AC and check. The body is authoritative; comment copies are
context only. Product questions must be resolved before implementation.

The adapter appends the runner path, context path, issue, run ID and worker ID
to the mandate. Get current bindings with:

```sh
python3 <runner> --worker-info --context <run.json>
```

This returns the canonical issue-body `spec_sha256` and registered identity.
Implementation/QA cannot change the specification mid-phase. Read the full
current issue before relying on its hash.

Run validation through the recorder, without shell interpolation of credentials:

```sh
python3 <runner> --record-check --context <run.json> -- <program> <arguments>
python3 <runner> --record-check --context <run.json> --artifact <worktree-file> -- <program> <arguments>
```

It captures actual command output and optional screenshots/files, their hashes,
exit status, head/base, spec digest and verifier session. Evidence IDs identify
those records. Keep diagnostics that fail; do not label them pass. Secrets and
real customer data must not enter commands or captured artifacts. Use fixtures.
The command runs with the worker's permissions; this is not a new sandbox.
Commit the product/test changes before capture. Tracked/index changes or
untracked product inputs are rejected before, during and after a check. Keep
mandates/receipts under `.backlog/autonomous-*.md|json|lock`; generated evidence
files must be explicitly named with `--artifact`, then removed from the checkout
before handoff if untracked. Ignored dependencies/build outputs and external
seeded environments still depend on the project verification recipe; the
recorder is not an immutable or hostile-host execution environment.

Publish one JSON code block on the issue with `backlog_phase`:

```json
{"backlog_phase":{"run_id":"<run>","worker_id":"<worker>","issue":1,"phase":"refine","spec_sha256":"<digest>","outcome":"ready","summary":"<durable result>","open_product_questions":[]}}
```

Additional phase evidence:

- Research ready: nonempty `facts` and `sources` lists. Next phase is refine.
- Refine ready: the canonical body has Problem, Goal, In scope, Out of scope,
  AC and QA checklist. Open product questions must be empty. Next is implement.
- Implement ready: `pr_url` and nonempty `evidence_ids` of passing self-checks
  at the current PR head/base. The PR must link this issue. Next is QA.
- Blocked: `outcome: blocked` plus `blocker` containing `kind: product | validation | dependency`,
  the exact `question`, and `resume_when`. Retain phase. A shared process/startup
  failure belongs to the infrastructure handoff, not this product blocker.
- QA defect/plan hole: `outcome: rework`, `next_phase: implement | refine`,
  `reason`, and a corresponding `backlog_qa` verdict. Keep failed/unreached AC
  evidence honest. Next worker gets the concrete failure and reproduction.

QA ready also publishes `QA verdict: pass`, the head SHA, and `backlog_qa`:

```json
{"backlog_qa":{"run_id":"<run>","worker_id":"<worker>","issue":1,"spec_sha256":"<digest>","verdict":"pass","pr_url":"<actual URL>","head_sha":"<tested head>","base_sha":"<tested base>","acceptance_results":[{"criterion":"<literal issue-body AC>","result":"pass","evidence_id":"<record ID>","evidence":"<action and observed result>"}],"validations":[{"check":"<literal QA checklist item>","result":"pass","evidence_id":"<record ID>"}]}}
```

Every AC needs a passing recorded check and explanation. Every canonical QA
check needs a required passing validation; extra passing checks may be included.
Diagnostic failures use `required: false`, `result: fail`, and `reason`; they
cannot substitute for required proof. For rework, use verdict `implement-again`
or `refine-again`, list every AC as pass/fail/not-reached, and explain the gap.
Structured negative QA verdicts also supersede older passes, even without the
plain verdict line. A later prose-only pass cannot resurrect an older receipt.

PM records verified PRs with `issue`, `pr_url`, `head_sha`, `run_id`, `worker_id`
and a short evidence summary. A changed head/base/body or later negative verdict
invalidates the pass. Required CI must be green, with expected check names
configured when absence must block. Existing PRs can be verified by a fresh
registered QA session starting at their head; external authorship cannot be
reconstructed from the shared GitHub account. The registry establishes session
separation for implementation workers it dispatched, not historical provenance.

Pending/failing required CI, unresolved mergeability/conflicts or requested
reviews are issue-local delivery holds, not successful delivery or shared
runtime failure. The adapter retains valid behavioral proof and publishes a
dependency blocker with a resume condition. PM parks it in QA, clears the lane
and continues. On a later wake, unchanged head/base/body proof may be reused
only after current delivery checks pass, no newer negative QA exists and the
PM restores `phase:qa/status:open` for human review. Changed bindings require
fresh QA. Cancellation revokes that run's receipts; after human reconciliation,
use fresh QA rather than accepting late or historical cancelled-run results.

The final report must match live labels: verified PRs are `phase:qa/status:open`,
newly parked issues match the accepted blocker and retained phase, and advanced
issues match their accepted destination. Already parked issues may be listed
as pre-existing blockers; they do not count as newly validated work.

Recorded exits/hashes are execution proof, not proof that an assertion is good.
The independent QA worker still judges scenario relevance and inspects the diff.
These receipts are not tamper-resistant against a process with host write access.
