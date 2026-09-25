# Knowledge maintenance

Use this reference at checkpoints, after a major correction, or when the agent starts ignoring a known constraint. Durable knowledge should make the next session more reliable, not merely longer.

## Classify before storing

- **Fact**: observed project or domain state. Keep source, scope, and date.
- **Assumption**: belief that still needs evidence. Keep the test and expiry or recheck trigger.
- **Decision**: chosen trade-off. Keep rationale, alternatives considered when useful, and the condition that would reopen it.
- **Temporary state**: current location, blocker, or experiment result. Keep it in state or a checkpoint, not in permanent rules.

## Groom before adding

1. Search the project’s existing state, decisions, docs, and instructions for the same topic.
2. Merge duplicates into the clearest entry tied to evidence or a decision.
3. Resolve contradictions by scope or by recording which entry supersedes the other.
4. Remove rules for deleted components, expired constraints, and markers whose referenced file or rationale no longer exists.
5. Keep domain scopes separate when two statements are both valid in different areas.

Promote a lesson when it recurs or protects a material decision; a single local incident stays local.

## Checkpoint contents

```markdown
## Checkpoint: <date or stable id>
Goal: <final goal>
Mode: BUILD | RECONCILE | RESCUE
Location: <Phase → Milestone → Task → Step>
Work type: DELIVERY | EXPLORATION | RECOVERY
Trusted evidence: <ids and short results>
Assumptions tested: <confirmed / disproved / still open>
Decisions: <new or changed decisions>
Blockers: <only active blockers>
Return to: <detour target or none>
Next action: <one bounded action>
```

## Stop condition

Stop grooming when the active task can be resumed without rereading unrelated history, each important constraint has one authoritative home, and open uncertainty is represented as a task or evidence gap. Perfectly tidy memory is not a project goal.
