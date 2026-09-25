# Evidence record

Use an evidence record for any claim that changes project status, closes a milestone, resolves a blocker, or justifies a high-cost decision. The record should be short enough to maintain and specific enough to reproduce or challenge.

## Record shape

```yaml
id: EVID-YYYYMMDD-###
claim: string
source: test | build | runtime | inspection | user_acceptance | external_system
scope:
  version: string
  environment: string
  scenarios: [string]
observed_at: YYYY-MM-DD or timestamp
result: pass | partial | fail | inconclusive
limitations: [known gaps, excluded scenarios, or measurement error]
recheck_when: [code, interface, dependency, configuration, or requirement changes]
related_nodes: [stable project-map ids]
```

`source` says how the observation was obtained; it does not prove that the observation satisfies the goal. Keep the requirement or acceptance criterion beside the claim so a reviewer can compare them.

## The three checks

For important work, ask these separately:

1. **Implementation check** — did the system produce the observed result?
2. **Requirement check** — does the observed result satisfy the user’s requirement and constraints?
3. **Evaluation check** — could the test or benchmark pass while missing a meaningful failure, scenario, or quality dimension?

A passing test generated from the same mistaken assumption as the implementation is evidence for the first check only. Mark the node `UNKNOWN` or `AT RISK` until the other checks have a credible basis.

## Evidence lifecycle

Create the record before or during verification, link it from the map node, and review its `recheck_when` list after changes. Re-verify evidence after a changed interface, dependency, configuration, environment, or requirement. When a record is no longer valid, mark it stale and create a new verification step.

## Acceptance examples

For behavior that is easy to express, prefer a reviewed fixture containing input, expected result, and relevant side effects. Keep the fixture readable and stable; the implementation may regenerate actual output, but a human or independent rule must approve changes to the expected result. For visual, workflow, or protocol behavior, a compact scenario file can be more reviewable than a large assertion suite.

## Conflict reporting

When the current behavior conflicts with the requirement, report both facts:

```text
Observed: <what the current version does, with evidence id>
Required: <what the current goal or acceptance criterion says>
Status: CONFLICT — do not mark the node VERIFIED
Next: <fix, requirement decision, or evaluation task>
```

This prevents a stable but wrong behavior from becoming the baseline merely because it is easy to observe.
## Gate credibility

A gate is evidence only when it can fail for the right reason. Before relying on a new gate, prove it: introduce the failure it is meant to catch, confirm the gate turns red, then restore the code. Record the demonstration alongside the evidence id.

A gate that has never been observed failing — or that executes without asserting anything, such as coverage-only, smoke-only, or exit-code-only checks — supports `? UNKNOWN`, never `✅ VERIFIED`. Coverage measured over a suite whose validity is unproven is not evidence of correctness.

## Independent review

The three checks are easier to keep separate when a second context performs them. For work that closes a milestone or changes a shared interface, hand another agent — or the same model with its focus shifted — the task and the change, and ask it to find problems rather than to confirm success. Reviewers and implementers attend to different things even on the same model.

Record what the review found and how each point was resolved, accepted as a known limitation, or turned into a new task.

