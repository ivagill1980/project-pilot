# Pattern router

Load this reference when choosing an internal strategy label for a situation. The user does not need to memorize these; keep the labels internal. This file is an optional enhancement and is the only place that carries third-party attribution, so it can be deleted as a unit.

Use these Augmented Coding Patterns as internal strategy labels. The user does not need to memorize them.

Attribution: these labels come from [Augmented Coding Patterns](https://github.com/lexler/augmented-coding-patterns)
by [@lexler](https://github.com/lexler) (<https://lexler.github.io/augmented-coding-patterns/>).
Reference the names only — do not reproduce, translate, or quote upstream pattern text.
Keep the labels internal: the user sees the behavior and its exit condition.
See `CREDITS.md` for the full list and upstream licensing status.
This section is an optional enhancement: if attribution or licensing is a concern,
omit it — the core invariants and the three mode workflows above stand on their own.

## When complexity is causing failure

Use:

- Chain of Small Steps
- Chunking
- Focused Agent
- Phased Delivery

## When context is decaying

Use:

- Context Management
- Ground Rules
- Reference Docs
- Knowledge Checkpoint
- Extract Knowledge
- Learning Loop
- Semantic Zoom
- Noise Cancellation

## When work is unreliable or non-deterministic

Use:

- Feedback Loop
- Constrained Tests
- Offload Deterministic
- Hooks
- Approved Scenarios / Approved Logs when suitable

## When the user and agent may be misaligned

Use:

- Check Alignment
- Active Partner
- ROSE Feedback when structured feedback is useful

## When solution space needs exploration

Use:

- Cast Wide
- Parallel Implementations
- Softest Prototype
- Take All Paths
- Refinement Loop

## When side quests threaten the main line

Use:

- Yak Shave Delegation
- Parking Lot behavior from this skill
- Background Agent when independently bounded

## When multi-agent throughput is useful

Use:

- Background Agent
- Orchestrator
- Phased Delivery
- Overnight Batch only with deterministic gates

## When cost/intelligence routing matters

Use:

- Smart Plan, Cheap Execution
- Advisor Strategy

## Translate a pattern into an action

Pattern names are prompts for a decision, not a second process to run. Apply the smallest matching behavior:

- For an untested direction, remove solution assumptions, make a soft prototype or a small comparison, and define what result will select the route.
- For non-deterministic or high-cost implementation, checkpoint the plan, use bounded parallel attempts only when their acceptance gate is clear, and keep the best result disposable until reviewed.
- For a weak success signal, create an executable acceptance example or constrained fixture before asking an agent to iterate.
- For a context or memory problem, extract the decision, rationale, and evidence to durable storage; groom duplicates and stale entries before adding more rules.
- For repeated failure, unvalidated leaps, or silent misalignment, stop the current loop, restate the model of the problem, validate the earliest assumption, and either change route or return to the last trusted checkpoint.

Lead with the behavior and its exit condition in the project map, and name a label only when the user asks about the pattern library.
