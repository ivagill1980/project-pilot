# Recovery

Used while reconciling or rescuing, and kept afterwards as a historical record.

```yaml
trigger: <why recovery was triggered>
mode: RESCUE
observed_evidence: []
contradictions: []
drift_findings: []
stabilization_milestones: []
return_to: <Phase → Milestone → Task → Step>
exit_criteria:
  - <observable condition for leaving recovery mode>
```

## Stabilization priority

1. Prevent data, security, or production damage.
2. Restore a trustworthy build, test, and CI signal.
3. Close dangerous half-built features.
4. Remove blockers from the product critical path.
5. Repair the map and the durable knowledge.
6. Return to product delivery.

Report recovery progress separately from product progress, so recovery work does not look
like invisible non-progress.
