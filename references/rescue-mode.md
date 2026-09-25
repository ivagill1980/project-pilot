# RESCUE MODE workflow

Load this reference for brownfield recovery, severe drift, project chaos, repeated failed work, stale plans, or an explicit user request. It holds the read-only archaeology pass `S1`-`S9`, the drift detector, and the drift trigger heuristics.

Use for brownfield recovery, severe drift, project chaos, repeated failed work, stale plans, or explicit user request.

## Rescue rule: observe before changing

Unless the user explicitly asks for an emergency fix, begin read-only.

State that code will not be changed during archaeology.

## S1 — Project Archaeology

Collect the smallest sufficient evidence set.

### Repository structure

Inspect:

- top-level structure,
- entry points,
- package/build manifests,
- major modules,
- generated vs authored code,
- migrations/schema,
- test layout,
- CI configuration,
- deploy configuration,
- existing `AGENTS.md` and project instructions.

### Documentation

Inspect:

- README,
- roadmap,
- specs,
- ADRs/decision logs,
- architecture docs,
- TODO/plan docs,
- current task trackers if accessible.

### History

Once there are enough commits to be worth mining, look for:

- **hotspots** — files that change often and are complex. They concentrate risk and keep getting re-read into context.
- **change coupling** — files that repeatedly change together without a visible dependency, which usually means a boundary sits in the wrong place.

Derive both from version-control history, or with a tool when one is available. The metrics nominate candidates for a human to judge; the decision comes from reading the code. Hand the survivors to the plan as refactor targets rather than as facts about the code.

### Git reality

Inspect when available:

- branch,
- worktree cleanliness,
- recent commits,
- merge history,
- tags/releases,
- long-lived divergent branches only when relevant.

### Executable reality

Run appropriate non-destructive checks when feasible:

- build,
- tests,
- typecheck,
- lint,
- targeted smoke checks.

Start with cheap checks and escalate; an expensive suite can wait until the repository is understood.

## S2 — Reality Snapshot

Produce a concise verified snapshot:

```text
Commit / branch
Working tree
Build
Tests
CI if known
Major modules
Known broken areas
Unknown critical areas
```

Mark each as VERIFIED / PARTIAL / AT_RISK / BROKEN / UNKNOWN.

## S3 — Reconstruct intended outcome

Determine:

- original/final goal,
- latest credible success criteria,
- whether the goal itself changed.

If sources conflict, present the conflict and use the user’s current intent as the final authority for goal selection.

## S4 — Reconstruct map from evidence

Build a project map from:

`declared plan + observed repository + test/runtime evidence + recent history + current user intent`.

Distinguish:

- confirmed complete,
- partial,
- broken,
- not started,
- unknown.

## S5 — Drift Detector

Explicitly inspect these drift classes.

### Plan Drift

Planned sequence and actual work diverged.

### Documentation Drift

Docs describe a system that no longer exists.

### Architecture Drift

Boundaries/dependencies violate accepted architecture in ways that create material risk.

### Scope Drift

Unplanned work has expanded the definition of “done” or is displacing critical-path work.

### TODO Drift

TODO/FIXME/HACK items are stale, contradictory, or hiding active risk.

### False Completion

A feature appears present but lacks one or more critical layers such as wiring, migrations, tests, failure states, deployment, permissions, observability, or acceptance evidence.

### Validation Drift

Tests/CI no longer represent actual success, are ignored, or remain red while the project claims progress.

### Decision Drift

Implementation repeatedly revisits settled choices without an explicit new decision.

### Assumption Drift

The plan still depends on an assumption that evidence has disproved, or the assumption was never made explicit and cannot be checked.

### Evaluation Drift

The success signal no longer represents the requirement, covers too few scenarios, is derived from the implementation under test, or has passed while important failure modes remain unobserved.

### What a machine decides, and what it cannot

`python scripts/project_state.py drift <repo>` covers the mechanical part of this list:

| Drift class | Machine-checked | Needs a human |
| --- | --- | --- |
| Plan | — | yes |
| Documentation | relative links in markdown and HTML that no longer resolve | prose describing a system that no longer exists |
| Architecture | — | yes |
| Scope | — | yes |
| TODO | the inventory, and markers naming a path that no longer exists | whether a surviving marker hides active risk |
| False completion | `validate` flags `VERIFIED` without evidence; `progress` flags a declared percentage that contradicts the children | whether the missing layer matters |
| Validation | — | whether tests still represent success |
| Decision | — | yes |
| Assumption | — | yes |
| Evaluation | — | whether the signal still covers the requirement |

Report what the machine found, then say plainly which classes you inspected by reading and which ones you could not check. A clean scan is not a clean project.

## S6 — Chaos Report

Default to a compact report, not a wall of issues.

Show:

- final goal,
- reconstructed overall progress,
- current real location,
- project health statement,
- three most important problems,
- key unknowns,
- recommendation: continue / reconcile / stabilization / rebaseline.

Provide deeper inventories only on request or when needed for safe execution.

## S7 — Rebaseline

When needed, create a new baseline from current reality.

Keep the old plan as history: mark it superseded, abandoned, or historical.

The new baseline should include:

1. **Recovery / stabilization milestones** first when required.
2. **Product critical path** from recovered state to final goal.
3. **Deferred scope** in parking lot/backlog.
4. **Explicit unknown-resolution tasks** where uncertainty blocks planning.

## S8 — Stabilize

Typical stabilization priority:

1. prevent data/security/production damage,
2. restore a trustworthy build/test/CI signal,
3. close dangerous half-built features,
4. resolve blockers on the product critical path,
5. repair project map and durable knowledge,
6. return to product delivery.

Show both:

- product progress,
- recovery progress.

This prevents recovery work from feeling like invisible non-progress.

## S9 — Exit Rescue

Leave RESCUE MODE when:

- the active baseline is credible,
- current location is known,
- critical validation signals are trustworthy enough,
- major blockers are represented on the map,
- the user has a clear next product route.

Return to BUILD MODE with a recorded checkpoint.

---

# Drift trigger heuristics

Suggest RECONCILE or RESCUE when several of these occur:

- the agent cannot state current location confidently,
- project state repeatedly contradicts the roadmap,
- multiple supposedly complete features fail verification,
- CI remains red while feature work continues,
- the same bug is “fixed” repeatedly,
- large uncommitted change sets accumulate,
- multiple parallel agents touch overlapping scopes without integration control,
- scope grows faster than critical path completion,
- documentation and code disagree on core architecture,
- key assumptions remain implicit or have been disproved,
- evidence is older than the change that should invalidate it,
- tests pass but no one can state which requirement or scenarios they establish,
- detours occur without return targets,
- the user repeatedly asks what the project is doing or why a task exists.

Keep every diagnosis on the project's control signals.
