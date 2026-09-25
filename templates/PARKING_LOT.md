# Parking lot

Distractions captured without losing them. A parking-lot item enters active scope through
an explicit decision — never by drifting back into the current task.

```yaml
items:
  - idea: <the idea or problem>
    source: <where it came from>
    urgency: low
    blocks_current: false
    revisit_when: <trigger or target phase>
```

## Fields

- `idea` — the thing itself, in one line.
- `source` — the conversation, file, or observation it came from.
- `urgency` — `low`, `medium`, or `high`. Urgency alone does not promote an item.
- `blocks_current` — `true` only when the main line genuinely cannot proceed.
- `revisit_when` — the trigger or phase that makes this worth picking up.

When an item is promoted, record the decision in `DECISIONS.md` and remove it here.
