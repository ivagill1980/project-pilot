# Health

Operational and project-control health, tracked separately from product completion.

```yaml
health:
  build: UNKNOWN
  tests: UNKNOWN
  ci: UNKNOWN
  docs_alignment: UNKNOWN
  architecture_alignment: UNKNOWN

risks:
  unresolved_blockers: []
  architecture_drift: []
  documentation_drift: []
  scope_drift: []
  half_built_features: []
  stale_or_contradictory_plans: []
  risky_uncommitted_changes: []
  unknown_critical_areas: []
```

## Reading it

- The five `health` entries use the shared status vocabulary.
- `risks` lists are free-form; each item records what was observed and what it blocks.
- A `BROKEN` or `AT_RISK` entry that stays unchanged across several sessions is itself a
  finding: either it is being tolerated or it is not really being tracked.
