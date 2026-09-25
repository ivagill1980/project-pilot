# Decisions

One entry per settled trade-off. Keep the reason and the reopening condition, so a later
session can tell a deliberate choice from an accident.

## DEC-001 — <short title>

- **Date**: 2026-01-01
- **Status**: accepted
- **Context**: <the situation that forced a choice>
- **Decision**: <what was chosen>
- **Alternatives**: <what else was considered>
- **Rationale**: <why this one>
- **Consequences**: <what this makes easy, what it makes hard>
- **Reopen when**: <the condition that would make this worth revisiting>

## Guard markers

Counter-intuitive code can carry a short marker that points back here:

```text
// DEC-001: <one-line reason this stays as it is>
```

Reserve markers for code that looks wrong but is deliberate. A marker on everything is a
marker on nothing.
