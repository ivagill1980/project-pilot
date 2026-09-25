# Background agents and multi-agent work

Load this reference before delegating work to background, parallel, or sub-agents.

Use parallel agents only when work can be independently bounded.

## Good candidates

- targeted research,
- independent test additions,
- documentation inventory,
- isolated migration preparation,
- separate implementation alternatives,
- investigation of a parked blocker.

## Bad candidates

- several agents editing the same central files,
- work without deterministic acceptance gates,
- work whose dependencies are unresolved,
- work that makes the user manage the agent topology.

## Orchestration rule

The user interacts with one project coordinate.

The orchestrator tracks:

- agent scope,
- branch/worktree,
- acceptance gate,
- integration status,
- conflicts,
- final verification.

Keep agent-management detail out of the user's way, and surface it when it changes a decision.

## What a delegated agent hands back

A delegated agent returns a bounded result plus evidence pointers. Its raw search trail, log dump, and intermediate reasoning stay with the agent. If the payload does not fit that shape, the work was split wrong: narrow the scope and delegate again.

- state the result, not the journey;
- name the files, commands, or artifacts that prove it;
- mark anything it could not establish as `? UNKNOWN` rather than filling the gap;
- report the acceptance gate it ran, and whether that gate has been shown to fail.
