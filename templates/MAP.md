# Map

The project tree that progress is computed from: `PROJECT → PHASE → MILESTONE → TASK → STEP`.
Keep node ids stable so progress history stays meaningful.

```yaml
nodes:
  - id: phase-1
    title: Phase 1 — <phase name>
    parent: null
    status: NOT_STARTED
    work_type: DELIVERY
    weight: 1
    progress: 0
    depends_on: []
    assumptions: []
    evidence: []
    notes: <why this phase exists>

  - id: milestone-1
    title: <milestone name>
    parent: phase-1
    status: NOT_STARTED
    work_type: DELIVERY
    weight: 1
    progress: 0
    depends_on: []
    assumptions: []
    evidence: []
    notes: <optional>

  - id: milestone-2
    title: <the milestone that waits for the first one>
    parent: phase-1
    status: NOT_STARTED
    work_type: DELIVERY
    weight: 1
    progress: 0
    depends_on: [milestone-1]
    assumptions: []
    evidence: []
    notes: <optional>
```

`parent` is containment; `depends_on` is ordering. Milestone 2 sits inside the same phase
but waits for milestone 1, so it carries both.

## Evidence records

Declare evidence here or in the project's own test and decision documents. Ids look like
`EVID-YYYYMMDD-###`. A node that is `VERIFIED` needs at least one evidence id, and a
record needs a recheck trigger — evidence without an expiry silently goes stale.

```yaml
evidence:
  - id: EVID-20260101-001
    claim: <what was observed>
    source: test
    result: pass
    gate_proven: true
    scope: <version, environment, scenarios covered>
    observed_at: 2026-01-01
    limitations: []
    recheck_when: [<change that invalidates this evidence>]
    related_nodes: [milestone-1]
```

## Status vocabulary

`VERIFIED` `PARTIAL` `AT_RISK` `BROKEN` `NOT_STARTED` `UNKNOWN`

A parent's progress is computed from its children. `UNKNOWN` never counts as complete,
and an experiment that disproves an assumption is a recorded learning, not a failed
delivery.

## Rolling it up

`python scripts/project_state.py progress .project-pilot` walks the `parent` links and
reports the total, so nobody has to estimate it. `project.progress_policy` in `STATE.md`
decides which weights are honoured:

- `equal` — every child counts the same; declared weights are ignored;
- `weighted` — each child contributes its declared `weight`, defaulting to 1;
- `milestone-weighted` — only children that are themselves containers carry weight, so put
  the weight on phases and milestones rather than on individual steps.

A declared `progress` on a container that disagrees with its children is reported as a
mismatch: the children are the source of truth.
