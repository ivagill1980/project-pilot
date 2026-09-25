# RECONCILE MODE workflow

Load this reference when the project may be drifting but does not obviously require a full rescue.

Use when the project may be drifting but does not obviously require full rescue.

## R0 — Freeze assumptions, not development

Keep development moving; freeze the claims, not the work. Unverified statements about project state wait for evidence.

## R1 — Compare expected vs observed

Check current plan against:

- repository state,
- tests/build/CI,
- recent commits,
- active work,
- material docs/specs.

## R2 — Detect drift

Look for:

- plan drift,
- documentation drift,
- architecture drift,
- scope drift,
- stale TODO drift,
- false completion,
- repeated failed fixes,
- unbounded detours,
- inconsistent acceptance criteria,
- stale, narrow, or self-referential evidence,
- invalidated assumptions that still drive the plan.

## R3 — Classify severity

### NORMAL

Minor mismatch. Update state and continue.

### RECONCILE

Meaningful mismatch, but current baseline is still useful. Correct map/status and continue.

### RESCUE

Baseline is unreliable, critical health is broken, or the agent cannot explain the project’s current location confidently. Enter RESCUE MODE.

## R4 — Report compactly

Default report:

- what still matches,
- top 3 drifts,
- effect on progress,
- whether rebaseline is recommended,
- current return target.

## R5 — Re-evaluate evidence

For each material completion claim, check that the evidence still covers the current version, environment, and relevant scenarios. Check its limitations and `recheck_when` triggers after interface, dependency, configuration, or requirement changes.

Keep these questions separate:

1. Does the implementation produce the observed result?
2. Does the observed result satisfy the requirement?
3. Could the evaluation miss an important failure or be optimized without delivering the goal?

If the answer to the second or third question is unclear, keep the node `UNKNOWN` or `AT RISK`, create an evaluation task, and surface the conflict. A passing test generated from the same mistaken assumption as the implementation is not independent evidence.
