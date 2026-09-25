# Decision policy: choose the next move

Use this reference when a task could reasonably be approached as implementation, investigation, design, or recovery. It turns four project properties into a small choice without pretending that they are precise measurements.

## 1. Classify the work

Mark the active node as one of:

- `DELIVERY`: changes the product or project toward an accepted outcome.
- `EXPLORATION`: reduces uncertainty or compares routes before a commitment.
- `RECOVERY`: restores a trustworthy baseline, signal, or control surface.

An exploration can be valuable even when it rejects the proposed route. Count it as exploration progress.

## 2. Inspect the four properties

Use `low`, `medium`, or `high` only when the distinction changes the next action.

| Property | Low | High |
| --- | --- | --- |
| Uncertainty | Goal, constraints, and likely solution are understood | A key assumption or success condition is unverified |
| Feedback cost | A result is quick and cheap to observe | Feedback needs long runs, scarce hardware, users, or expensive review |
| Reversibility | The change is isolated and easy to undo | It locks an interface, data shape, migration, or safety-relevant behavior |
| Coupling | Few other components depend on the change | Many interfaces, shared resources, or emergent effects are involved |

## 3. Select the smallest useful move

| Situation | Preferred move | Minimum exit gate |
| --- | --- | --- |
| Low uncertainty, low feedback cost, high reversibility | Delivery slice | One observable behavior and its test or inspection evidence |
| High uncertainty, low feedback cost | Exploration | A result that selects, rejects, or narrows a route |
| High reversibility cost or coupling | Boundary and recovery preparation, then a small change | Interface/impact note, rollback or containment path, and targeted verification |
| No credible success signal | Build an acceptance example, fixture, benchmark, or observation path | Someone other than the implementation can inspect the expected result |
| Safety, regulated, or physical work | Simulation, staged trial, independent review, and explicit gate | The trial stays within approved limits and its evidence is recorded |

Decide what success means before running parallel implementations. If parallel exploration is worthwhile, create a checkpoint first, give every attempt the same gate, and choose or discard results explicitly.

## 4. Stop and re-route

Stop the current route when an early assumption is disproved, the success signal is revealed to be misleading, or repeated attempts are degrading the baseline. Record the finding, return to the last trusted checkpoint, and choose a new work type. Three or four failed iterations are a useful prompt to reassess, not a universal timeout.

## 5. Keep the map honest

Attach the selected work type, assumptions, evidence scope, and return target to the active node. Show product progress separately from exploration and recovery progress. When a result changes the route, update only the affected subtree unless the baseline itself is no longer credible.
