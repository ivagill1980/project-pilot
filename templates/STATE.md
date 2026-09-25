# State

The single source of truth for where the project is. Keep field names and the status
vocabulary stable across sessions; `references/state-schema.md` defines the canonical
shape and `scripts/project_state.py validate` checks it.

```yaml
project:
  name: <project name>
  final_goal: <what done means at project level>
  success_criteria: []
  mode: BUILD
  progress_policy: equal
  baseline_id: base-001
  baseline_date: 2026-01-01
  overall_progress: unknown
  product_progress: unknown
  exploration_progress: unknown
  recovery_progress: unknown

location:
  phase: Phase 1
  milestone: <milestone>
  task: <task>
  step: <step>
  work_type: DELIVERY
  return_to: null

current:
  purpose: <the one active purpose>
  done_when:
    - <observable acceptance gate>
  blockers: []
  assumptions: []
  evidence_required:
    - <what evidence this step must produce>
  next_action: <one bounded action>

recent:
  completed: []
  decisions: []
  discoveries: []
  evidence: []
```

## Notes

- `progress_policy` records how percentages are combined: `equal`, `weighted`, or
  `milestone-weighted`. State it once, when the baseline is created.
- `location.return_to` stays set while a detour is open, and returns to `null` when the
  detour closes.
- `unknown` is a valid value for any progress field. Use it instead of a guess.
