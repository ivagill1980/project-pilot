# Canonical state schema

Load this reference when creating or updating control state. Keep field names and the status vocabulary stable across sessions so a fresh session can read what an earlier one wrote.

Maintain these concepts even if the repository uses different file names.

## STATE

```yaml
project:
  name: string
  final_goal: string
  success_criteria: [string]
  mode: BUILD | RECONCILE | RESCUE
  progress_policy: equal | weighted | milestone-weighted
  baseline_id: string
  baseline_date: YYYY-MM-DD
  overall_progress: number | unknown
  product_progress: number | unknown
  exploration_progress: number | unknown
  recovery_progress: number | unknown

location:
  phase: string
  milestone: string
  task: string
  step: string
  work_type: DELIVERY | EXPLORATION | RECOVERY
  return_to: string | null

current:
  purpose: string
  done_when: [string]
  blockers: [string]
  assumptions: [string]
  evidence_required: [string]
  next_action: string

health:
  build: VERIFIED | PARTIAL | AT_RISK | BROKEN | UNKNOWN
  tests: VERIFIED | PARTIAL | AT_RISK | BROKEN | UNKNOWN
  ci: VERIFIED | PARTIAL | AT_RISK | BROKEN | UNKNOWN
  docs_alignment: VERIFIED | PARTIAL | AT_RISK | BROKEN | UNKNOWN
  architecture_alignment: VERIFIED | PARTIAL | AT_RISK | BROKEN | UNKNOWN

recent:
  completed: [string]
  decisions: [string]
  discoveries: [string]
  evidence: [string]
```

## MAP

Model the work as:

```text
PROJECT
└── PHASE
    └── MILESTONE
        └── TASK
            └── STEP
```

Each node should support:

```yaml
id: stable-id
title: string
parent: id | null
status: VERIFIED | PARTIAL | AT_RISK | BROKEN | NOT_STARTED | UNKNOWN
work_type: DELIVERY | EXPLORATION | RECOVERY
weight: number
progress: number | unknown
depends_on: [id]
assumptions: [string]
evidence: [string]
evidence_scope: version, environment, and scenarios
recheck_when: [changes that invalidate evidence]
notes: string
```

`parent` is containment, and it builds the tree that progress rolls up; `depends_on` is
ordering. A node with no `parent` sits at the top level. Keep the hierarchy stable enough
that progress history remains meaningful.

## Rolling up progress

A container's progress is computed from its children, never estimated. `progress_policy`
in `STATE.md` decides which weights are honoured:

| Policy | Rule |
| --- | --- |
| `equal` | every child counts the same; declared `weight` is ignored |
| `weighted` | each child contributes its declared `weight`, defaulting to 1 |
| `milestone-weighted` | only children that are themselves containers carry weight, so weights belong on phases and milestones |

An `unknown` child is left out of the average rather than counted as zero, and a container
whose children are all unknown is itself unknown. A declared `progress` on a container that
disagrees with the computed rollup is a warning: the children are the source of truth.

## EVIDENCE

For material claims, use the evidence record from Core invariant 3. Store the full record in the project-native state, decision, or test documentation and summarize its identifier or result on the relevant node. Read [evidence-record.md](evidence-record.md) when designing a new evidence or acceptance workflow.

## HEALTH

Track operational/project-control health separately from product completion.

Suggested sections:

- build/test/CI health,
- unresolved blockers,
- architecture drift,
- documentation drift,
- scope drift,
- half-built features,
- stale or contradictory plans,
- risky uncommitted changes,
- unknown critical areas.

## RECOVERY

Use only while reconciling/rescuing or retain as a historical record.

Include:

- why recovery was triggered,
- observed evidence,
- major contradictions,
- drift findings,
- stabilization milestones,
- explicit `RETURN TO`,
- criteria for leaving recovery mode.

## PARKING_LOT

Capture distractions without losing them.

Each item should contain:

- idea/problem,
- source/context,
- urgency,
- whether it blocks current work,
- revisit trigger or target phase.

A parking-lot item enters active scope through an explicit decision.
## Machine-checked rules

`python scripts/project_state.py validate <dir>` decides the parts of this schema that can be decided mechanically, so the shape is enforced rather than requested:

- required fields and enums for `STATE`, `MAP`, `HEALTH`, and evidence records;
- `baseline_date` in `YYYY-MM-DD`, and progress values that are a number `0-100` or `unknown`;
- node ids unique and slug-like, `depends_on` targets that exist, and no dependency cycles;
- `parent` targets that exist, with no containment cycles;
- **a `VERIFIED` node with no evidence id is an error** (Core invariant 3);
- a container whose declared `progress` disagrees with its children is a warning;
- evidence records need `claim`, `source`, `result`, and a `recheck_when` trigger;
- a passing test record without `gate_proven: true` is a warning (gate credibility).

`progress <dir>` prints the rolled-up tree, and `--json` emits it for other tools. Separately, `drift <repo>` scans the repository itself — broken relative links in documentation, and TODO markers that name a path which no longer exists — and states which drift classes it cannot check. Exit `0` is clean, `1` means errors were found, and `--strict` turns warnings into errors. `init <dir>` scaffolding and `selftest` live in the same script. Python 3.8+, standard library only.