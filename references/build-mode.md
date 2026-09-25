# BUILD MODE workflow

Load this reference when the project is new or coherent enough to continue, or when the agent is working in BUILD mode. It holds the `B0`-`B7` loop, the planning rules for very large projects, and the decision-load rules.

Use when the project is new or sufficiently coherent.

## B0 — Orient

Establish or recover:

- final goal,
- success criteria,
- constraints,
- current repository reality,
- current route.

Classify the next unit of work as `DELIVERY`, `EXPLORATION`, or `RECOVERY`. Note the assumptions that could change the choice of route. Estimate only the properties that affect the next move: uncertainty, feedback cost, reversibility, and coupling.

If the project already contains meaningful code, perform a lightweight archaeology scan first and let the repository decide what it is.

## B1 — Map

Construct the minimum useful hierarchy:

`Project → Phases → Milestones`

Plan detailed tasks just in time near the active milestone; the rest of the project stays at phase and milestone level.

Show the full high-level route to preserve orientation.

Keep assumptions and evidence attached to the affected node. Tag exploration and recovery nodes as such, and keep their results out of product completion.

## B2 — Select

Choose one current task and one micro-step.

Selection order:

1. blockers on critical path,
2. a cheap experiment that can resolve a decision-blocking assumption,
3. verification/stability work required for reliable progress,
4. smallest valuable vertical slice,
5. dependencies before dependents,
6. optional polish last.

Use the decision policy in [decision-policy.md](decision-policy.md) when more than one route is plausible. Select an experiment before implementation when it can cheaply distinguish competing approaches.

## B3 — Align

Before risky or ambiguous changes, briefly check alignment:

- restate the intended result,
- identify affected area,
- state the work type and the assumptions being tested,
- define the success signal and the evidence scope,
- ask only when ambiguity cannot be resolved safely from repository evidence.

Obvious work needs no interview.

## B4 — Act

Make the smallest coherent change.

Prefer reversible changes and clear diffs.

For `EXPLORATION`, make the smallest experiment that changes a decision: prototype, benchmark, fixture, simulation, or observation path. Keep an experiment disposable until the route is confirmed; product polish follows confirmation.

### Disposal threshold

Commit before the agent changes code, so the previous state stays one command away. When the second or third iteration on the same approach stops improving, stop refining it: revert to that commit, keep the lesson, and restart with a sharper constraint.

Ask for the revert explicitly — `Please run git reset --hard and try again` — because otherwise the agent tends to rebuild the previous attempt from memory instead of restoring the file.

### Two ways out of a stuck step

- **Playground** — when the agent is stuck, or is working against an unfamiliar library, stop top-down debugging. Have it test the assumption directly in a scratch folder that version control ignores, until the real constraint is identified. Then implement against what was learned.
- **Variants behind one gate** — when the route itself is undecided rather than the implementation, build several small variants instead of one. Give every variant the same acceptance gate, compare the results, and choose explicitly. Record which one won and why; the discarded variants count as exploration progress, not as delivery.

## B5 — Verify

Use deterministic gates:

- tests,
- build,
- typecheck,
- lint,
- static checks,
- runtime behavior,
- screenshots or E2E when appropriate.

A step is not `VERIFIED` without appropriate evidence. Record the claim, source, scope, observed time, limitations, and recheck trigger. If the success signal itself is weak, mark the node `UNKNOWN` or `AT RISK` and improve the evaluation before declaring completion.

## B5 detail — credible gates, independent review, goal check

The gate list above says what to run. These three rules say when its result is trustworthy. Keep the record shape from [evidence-record.md](evidence-record.md).

### Prove the gate can fail

Before relying on a gate for the first time, break the thing it is meant to protect and confirm the gate turns red. A gate that has never been observed failing — or that executes without asserting anything, such as coverage-only, smoke-only, or exit-code-only checks — supports `? UNKNOWN`, never `✅ VERIFIED`. Record the demonstration as evidence.

### Independent review pass

For work that closes a milestone or changes a shared interface, hand the task and the change to a separate context — a different agent, or the same model with its focus shifted — and ask it to find problems rather than confirm success. An implementer and a reviewer attend to different things even on the same model. Resolve or explicitly record each finding before asking a human to review, so the human starts from better ground.

### Goal check

At a phase or milestone boundary, compare the delivered result against the final goal and that phase's acceptance criteria in a separate pass, and list the gaps explicitly. When gaps exist, adjust the plan and re-enter the implementation loop. Hold the phase open until the gaps close.

## B6 — Record

Update:

- node status,
- evidence,
- tested and invalidated assumptions,
- progress,
- decisions,
- new risks/unknowns,
- parking-lot items.

Report product, exploration, and recovery progress separately when more than one work type occurred.

## B7 — Navigate

Show how the completion changed:

- task progress,
- milestone progress,
- phase progress,
- project progress when meaningfully affected.

If evidence changes an assumption or invalidates the current route, update the affected subtree or rebaseline instead of continuing on the old plan. A disproved exploration result is a recorded learning, not a delivery regression.

Then select the next step.

Repeat B2–B7.

## Handing work to a human

Agents deliver more at once than a human can review, and a delivery that cannot be reviewed gets rubber-stamped or stalls. Before handing over a large change, add a splitting pass: reorganize the branch into a stack of small, coherent, independently reviewable units — preparatory refactorings first, then behavior changes, then cleanups.

- Each unit states its purpose in one sentence.
- Each unit stays within a couple of hundred lines, unless it is the same mechanical change repeated many times.
- Instruct vertical slices explicitly. The default split is by structural element, which produces units that cannot be reviewed on their own.
- The splitting pass doubles as a pruning pass: delete what turned out unnecessary while reorganizing.

# Planning rules for very large projects

## High-level map first, detail just in time

Keep phases and milestones visible globally.

Only deeply task-plan the active or next-near milestone.

This avoids both extremes:

- no map,
- an unmaintainable 500-step plan.

## Critical path

Identify dependencies that actually block the final goal.

Mark optional work as optional.

Keep the critical path ahead of visual polish, refactors, and side quests; anything that outranks it moves onto the critical path explicitly.

## Vertical slices

Prefer end-to-end value slices over building all layers horizontally when possible.

A thin verified vertical slice provides a reality check early.

## Reversibility and feedback

Treat decision reversibility and feedback cost as planning attributes. Delay high-cost, hard-to-reverse commitments until the relevant uncertainty is reduced; accelerate cheap, reversible experiments. As coupling or safety cost rises, move interface definition, simulation, rollback, and independent review earlier in the route. Match the loop to the domain: where the experiment itself is expensive — physical, regulated, or safety-relevant work — use simulation, staged trials, and independent review in place of a short iteration loop.

## Phase boundaries

At the end of each phase:

- verify acceptance criteria,
- update progress,
- run a knowledge checkpoint,
- reconcile the next phase with current reality,
- rebaseline only if material assumptions changed.

# Decision-load rules

Reduce unnecessary choices without taking control away from the user.

When a decision is needed:

1. offer a recommended default,
2. explain the most relevant reason briefly,
3. provide at most two meaningful alternatives unless breadth is specifically requested,
4. allow `继续` to accept the recommendation.

Example:

```text
Decision: primary relational database
Recommended: PostgreSQL
Why: current requirements do not justify a specialized store and PostgreSQL keeps migration options open.
Impact on map: unlocks Phase 2 → Data Foundation.

Reply “继续” to accept, or name another choice.
```

Present one recommended option plus up to two alternatives; when exploration is the task, present the option space instead.
