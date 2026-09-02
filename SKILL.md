---
name: project-pilot
version: 0.1.0
description: >-
  A project executive-function and recovery workflow for Codex. Use it to plan,
  navigate, execute, reconcile, or rescue large and complex software projects
  while continuously preserving global orientation: final goal, current phase,
  current milestone, current task, current micro-step, progress, evidence,
  blockers, and return target. It is designed to reduce cognitive overload,
  prevent project drift, recover brownfield projects that have become chaotic,
  and keep every local action visibly connected to the whole project.
license: MIT
---

# Project Pilot

## Purpose

Project Pilot is a project control layer for Codex.

It does **not** merely generate plans or TODO lists. It continuously controls the gap between:

- the project's intended outcome,
- the best current plan,
- the repository's observed reality,
- and the user's present location in that plan.

Its primary interaction principle is:

> **One Thing in Context.** Execute one thing at a time, while always showing where that thing sits in the whole project and how it moves the whole project forward.

Use Project Pilot for both:

1. **BUILD MODE** — starting or continuing a project from a reasonably coherent state.
2. **RESCUE MODE** — joining an existing project that is confused, drifting, partially broken, undocumented, overgrown, or no longer aligned with its original plan.

The skill is especially useful for users who benefit from persistent orientation, low-friction re-entry after interruption, explicit progress, visible hierarchy, and constrained decision load. Do not make medical claims or assume a diagnosis; simply provide the interaction behavior defined here.

---

# Core invariants

These rules are mandatory unless the user explicitly overrides them.

## 1. Always preserve global orientation

Every substantive project-work response must make these visible near the top:

- **Final Goal** — what “done” means at project level.
- **Overall Progress** — evidence-based, not guessed.
- **You Are Here** — `Phase → Milestone → Task → Step`.
- **Why This Matters** — connection from the current step to the final goal.
- **Now** — the single active action or decision.
- **Done When** — observable completion criteria.

Do not force the user to ask “where are we?” repeatedly.

## 2. Never confuse “focus” with “hiding the map”

Keep the global map available while focusing execution locally.

Default display ratio:

- roughly 10–20% global orientation,
- roughly 80–90% current work.

Hide irrelevant details, not the destination or location.

## 3. Progress must be computed from evidence

Never invent a percentage because the project “feels” halfway done.

Progress should be derived from a maintained project tree and verified state.

Use statuses:

- `✅ VERIFIED` — evidence proves complete.
- `◐ PARTIAL` — meaningfully implemented but incomplete.
- `⚠ AT RISK` — present but unreliable, drifting, or blocked.
- `✕ BROKEN` — known not to work.
- `○ NOT STARTED` — intentionally not begun.
- `? UNKNOWN` — insufficient evidence.

If weights are unavailable, use equal weights within the same hierarchy level and state that this is the current weighting policy. Prefer explicit weighted milestones for large projects.

A parent percentage is computed from its children. `UNKNOWN` items must not silently count as complete.

## 4. Reality outranks stale plans

For an existing project, distinguish declared state from observed state.

Prefer this evidence order when conflicts occur:

1. executable behavior and production/runtime evidence,
2. tests, CI, typecheck, lint, schema/migrations,
3. current code and current configuration,
4. recent accepted commits / merged work,
5. accepted ADRs/specifications,
6. maintained documentation,
7. old roadmap/TODO comments,
8. assumptions and recollection.

Never “fix” contradictions by silently choosing one. Surface material contradictions.

## 5. Do not modify a chaotic project before understanding it

When entering RESCUE MODE, start read-only unless a destructive production incident requires immediate containment and the user has asked for it.

The first job is **Project Archaeology**:

`observe → verify → reconstruct → diagnose → rebaseline → stabilize → continue`

## 6. One active execution target

At any moment, maintain exactly one `CURRENT` task/step for the user-facing main line.

Background agents may perform independent bounded work, but the user's main location must remain singular and stable.

## 7. Preserve a return target during detours

Whenever work leaves the main line because of a blocker, yak shave, investigation, or recovery task, record:

`RETURN TO: Phase → Milestone → Task → Step`

Keep displaying it until the detour is closed or the baseline is intentionally changed.

## 8. Small steps must have proof

A micro-step must have:

- one clear purpose,
- one bounded action,
- one observable result,
- one completion gate.

Prefer:

`change → run/test/inspect → record → next`

over:

`change many things → hope → test at the end`.

## 9. Offload deterministic work

Use AI for exploration, interpretation, planning, synthesis, and judgment.

Use scripts/tests/tools for deterministic repetition, counting, validation, parsing, formatting, inventory, and gates whenever practical.

If the same deterministic action is repeated, automate it.

## 10. Unknown is valid

Do not hallucinate project state to make the map look complete.

Use `? UNKNOWN` and create an investigation step if the unknown materially affects planning.

## 11. Rebaseline instead of pretending old plans remain valid

When reality has diverged significantly, do not force the project back onto a stale roadmap.

Create a new baseline from today’s verified reality to the final goal.

Preserve old plans as historical context; do not overwrite history silently.

## 12. The user must be able to re-enter instantly

After an interruption, a fresh session, or the command “我乱了 / where am I?”, reconstruct the working coordinate from durable state and respond with:

- final goal,
- overall progress,
- route overview,
- current hierarchy,
- recent completed nodes,
- active blocker/detour if any,
- exact next action.

---

# Recommended durable project control files

Do not require these exact paths when a repository already has equivalent conventions. Reuse existing structures where possible.

If no equivalent exists, prefer:

```text
.project-pilot/
├── STATE.md
├── MAP.md
├── HEALTH.md
├── RECOVERY.md
├── PARKING_LOT.md
├── DECISIONS.md
├── SESSION_LOG.md
├── plans/
│   ├── active/
│   ├── completed/
│   └── abandoned/
└── snapshots/
```

Use project-native documentation for durable architecture/product knowledge when it already exists, e.g.:

```text
AGENTS.md
README.md
docs/
├── architecture/
├── product/
├── decisions/
├── reference/
└── plans/
```

Do not turn `AGENTS.md` into a dumping ground. Treat it as stable operating guidance and a map to deeper documentation.

---

# Canonical state schema

Maintain these concepts even if the repository uses different file names.

## STATE

```yaml
project:
  name: string
  final_goal: string
  success_criteria: [string]
  mode: BUILD | RECONCILE | RESCUE
  baseline_id: string
  baseline_date: YYYY-MM-DD
  overall_progress: number | unknown

location:
  phase: string
  milestone: string
  task: string
  step: string
  return_to: string | null

current:
  purpose: string
  done_when: [string]
  blockers: [string]
  next_action: string

health:
  build: VERIFIED | PARTIAL | AT_RISK | BROKEN | UNKNOWN
  tests: VERIFIED | PARTIAL | AT_RISK | BROKEN | UNKNOWN
  ci: VERIFIED | PARTIAL | AT_RISK | BROKEN | UNKNOWN
  docs_alignment: VERIFIED | PARTIAL | AT_RISK | BROKEN | UNKNOWN
  architecture_alignment: VERIFIED | PARTIAL | AT_RISK | BROKEN | UNKNOWN

recent:
  completed: [string]
  decisions: [string]
  discoveries: [string]
```

## MAP

Model the work as:

```text
PROJECT
└── PHASE
    └── MILESTONE
        └── TASK
            └── STEP
```

Each node should support:

```yaml
id: stable-id
title: string
status: VERIFIED | PARTIAL | AT_RISK | BROKEN | NOT_STARTED | UNKNOWN
weight: number
progress: number | unknown
depends_on: [id]
evidence: [string]
notes: string
```

Keep the hierarchy stable enough that progress history remains meaningful.

## HEALTH

Track operational/project-control health separately from product completion.

Suggested sections:

- build/test/CI health,
- unresolved blockers,
- architecture drift,
- documentation drift,
- scope drift,
- half-built features,
- stale or contradictory plans,
- risky uncommitted changes,
- unknown critical areas.

## RECOVERY

Use only while reconciling/rescuing or retain as a historical record.

Include:

- why recovery was triggered,
- observed evidence,
- major contradictions,
- drift findings,
- stabilization milestones,
- explicit `RETURN TO`,
- criteria for leaving recovery mode.

## PARKING_LOT

Capture distractions without losing them.

Each item should contain:

- idea/problem,
- source/context,
- urgency,
- whether it blocks current work,
- revisit trigger or target phase.

Never silently turn parking-lot ideas into active scope.

---

# Interaction contract

## Default response header

For substantive project work, use a compact header in this shape:

```text
🎯 PROJECT
<final goal>
Overall: <progress or “reconstructing”>

📍 YOU ARE HERE
<Phase> → <Milestone> → <Task> → <Step>

🧭 WHY THIS MATTERS
<1–3 concise sentences connecting the step to milestone and final goal>

🔨 NOW
<single active action or decision>

✅ DONE WHEN
<observable acceptance gates>
```

If currently on a detour, also show:

```text
↩ RETURN TO
<original location>
```

If in RESCUE MODE, show both product progress and recovery progress where useful.

Do not make the header so verbose that it becomes noise. Keep it stable and scannable.

## Progress view

When useful, show nested progress:

```text
Project       ████████░░░░░░░░  48%
Phase         ███████████░░░░░  67%
Milestone     ██████████████░░  84%
Task          ███████████████░  92%
```

Never create false precision. Round appropriately and explain the weighting policy when first establishing it.

## Route view

For reorientation or phase changes, show:

```text
Discovery ✓
  ↓
Architecture ✓
  ↓
MVP ◉  ← YOU ARE HERE
  ↓
Integration
  ↓
Hardening
  ↓
Launch
```

## Recent momentum

When the project is long-running, include a short “recently completed” trail when it helps orientation:

```text
Recently:
✓ User schema
✓ Registration API
✓ Login happy path
→ Current: login error handling
```

Do not dump the full history every turn.

---

# Low-friction user commands

Treat natural-language equivalents the same way.

## `继续` / `continue`

Accept the current recommended path and proceed to the next safe action.

Do not ask the user to repeat information already known.

If a choice is necessary but one option is clearly preferred, present the recommendation and allow `继续` to accept it.

## `我乱了` / `where am I?`

Perform **Spatial Recovery**.

Reconstruct and display:

1. final goal,
2. overall project progress,
3. route overview,
4. exact current location,
5. active detour and return target,
6. last 3–7 meaningful completed nodes,
7. exact next action.

Keep the explanation concise.

## `看全局` / `zoom out`

Show the whole project map at phase/milestone level, risks, critical path, and completion estimate basis.

Do not flood with individual micro-steps unless requested.

## `看当前` / `zoom in`

Show current task and step, relevant files/components, blockers, acceptance gates, and immediate sequence.

## `为什么` / `why`

Explain only why the current action exists, which dependency it resolves, and what it unlocks.

## `我不懂` / `explain simpler`

Explain the current step in simpler language without changing the plan unless misunderstanding reveals a planning flaw.

## `换一个` / `alternative`

Offer a materially different route. Prefer at most three options. State recommendation, trade-off, and effect on the project map.

## `先放着` / `park it`

Record the item in the parking lot and return attention to the current main line unless it is a true blocker.

Confirm the return target.

## `接管项目` / `rescue` / `梳理项目`

Enter RESCUE MODE and begin Project Archaeology.

## `校准` / `reconcile`

Compare expected state with current reality without automatically rebuilding the entire roadmap.

## `重新基线` / `rebaseline`

Create a new evidence-based route from current reality to the unchanged or newly confirmed final goal.

## `暂停` / `checkpoint`

Record a durable checkpoint that allows a fresh session to resume with minimal reconstruction.

## `今天收尾` / `wrap up`

Run the Learning Loop:

- summarize meaningful completed work,
- capture discoveries,
- propose durable knowledge updates,
- update state/map/health,
- write checkpoint,
- identify the clean next re-entry step.

---

# BUILD MODE workflow

Use when the project is new or sufficiently coherent.

## B0 — Orient

Establish or recover:

- final goal,
- success criteria,
- constraints,
- current repository reality,
- current route.

If the project already contains meaningful code, do not assume it is a greenfield project. Perform a lightweight archaeology scan first.

## B1 — Map

Construct the minimum useful hierarchy:

`Project → Phases → Milestones`

Do not pre-plan every micro-step for the entire project. Plan detailed tasks just in time near the active milestone.

Show the full high-level route to preserve orientation.

## B2 — Select

Choose one current task and one micro-step.

Selection order:

1. blockers on critical path,
2. verification/stability work required for reliable progress,
3. smallest valuable vertical slice,
4. dependencies before dependents,
5. optional polish last.

## B3 — Align

Before risky or ambiguous changes, briefly check alignment:

- restate the intended result,
- identify affected area,
- surface uncertainty,
- ask only when ambiguity cannot be resolved safely from repository evidence.

Do not over-question obvious work.

## B4 — Act

Make the smallest coherent change.

Prefer reversible changes and clear diffs.

## B5 — Verify

Use deterministic gates:

- tests,
- build,
- typecheck,
- lint,
- static checks,
- runtime behavior,
- screenshots or E2E when appropriate.

A step is not `VERIFIED` without appropriate evidence.

## B6 — Record

Update:

- node status,
- evidence,
- progress,
- decisions,
- new risks/unknowns,
- parking-lot items.

## B7 — Navigate

Show how the completion changed:

- task progress,
- milestone progress,
- phase progress,
- project progress when meaningfully affected.

Then select the next step.

Repeat B2–B7.

---

# RECONCILE MODE workflow

Use when the project may be drifting but does not obviously require full rescue.

## R0 — Freeze assumptions, not development

Do not necessarily stop all work. Stop making unverified claims about project state.

## R1 — Compare expected vs observed

Check current plan against:

- repository state,
- tests/build/CI,
- recent commits,
- active work,
- material docs/specs.

## R2 — Detect drift

Look for:

- plan drift,
- documentation drift,
- architecture drift,
- scope drift,
- stale TODO drift,
- false completion,
- repeated failed fixes,
- unbounded detours,
- inconsistent acceptance criteria.

## R3 — Classify severity

### NORMAL

Minor mismatch. Update state and continue.

### RECONCILE

Meaningful mismatch, but current baseline is still useful. Correct map/status and continue.

### RESCUE

Baseline is unreliable, critical health is broken, or the agent cannot explain the project’s current location confidently. Enter RESCUE MODE.

## R4 — Report compactly

Default report:

- what still matches,
- top 3 drifts,
- effect on progress,
- whether rebaseline is recommended,
- current return target.

---

# RESCUE MODE workflow

Use for brownfield recovery, severe drift, project chaos, repeated failed work, stale plans, or explicit user request.

## Rescue rule: observe before changing

Unless the user explicitly asks for an emergency fix, begin read-only.

State that code will not be changed during archaeology.

## S1 — Project Archaeology

Collect the smallest sufficient evidence set.

### Repository structure

Inspect:

- top-level structure,
- entry points,
- package/build manifests,
- major modules,
- generated vs authored code,
- migrations/schema,
- test layout,
- CI configuration,
- deploy configuration,
- existing `AGENTS.md` and project instructions.

### Documentation

Inspect:

- README,
- roadmap,
- specs,
- ADRs/decision logs,
- architecture docs,
- TODO/plan docs,
- current task trackers if accessible.

### Git reality

Inspect when available:

- branch,
- worktree cleanliness,
- recent commits,
- merge history,
- tags/releases,
- long-lived divergent branches only when relevant.

### Executable reality

Run appropriate non-destructive checks when feasible:

- build,
- tests,
- typecheck,
- lint,
- targeted smoke checks.

Do not spend huge time running an obviously expensive suite before understanding the repo. Start cheap and escalate.

## S2 — Reality Snapshot

Produce a concise verified snapshot:

```text
Commit / branch
Working tree
Build
Tests
CI if known
Major modules
Known broken areas
Unknown critical areas
```

Mark each as VERIFIED / PARTIAL / AT_RISK / BROKEN / UNKNOWN.

## S3 — Reconstruct intended outcome

Determine:

- original/final goal,
- latest credible success criteria,
- whether the goal itself changed.

If sources conflict, present the conflict and use the user’s current intent as the final authority for goal selection.

## S4 — Reconstruct map from evidence

Build a project map from:

`declared plan + observed repository + test/runtime evidence + recent history + current user intent`.

Distinguish:

- confirmed complete,
- partial,
- broken,
- not started,
- unknown.

## S5 — Drift Detector

Explicitly inspect these drift classes.

### Plan Drift

Planned sequence and actual work diverged.

### Documentation Drift

Docs describe a system that no longer exists.

### Architecture Drift

Boundaries/dependencies violate accepted architecture in ways that create material risk.

### Scope Drift

Unplanned work has expanded the definition of “done” or is displacing critical-path work.

### TODO Drift

TODO/FIXME/HACK items are stale, contradictory, or hiding active risk.

### False Completion

A feature appears present but lacks one or more critical layers such as wiring, migrations, tests, failure states, deployment, permissions, observability, or acceptance evidence.

### Validation Drift

Tests/CI no longer represent actual success, are ignored, or remain red while the project claims progress.

### Decision Drift

Implementation repeatedly revisits settled choices without an explicit new decision.

## S6 — Chaos Report

Default to a compact report, not a wall of issues.

Show:

- final goal,
- reconstructed overall progress,
- current real location,
- project health statement,
- three most important problems,
- key unknowns,
- recommendation: continue / reconcile / stabilization / rebaseline.

Provide deeper inventories only on request or when needed for safe execution.

## S7 — Rebaseline

When needed, create a new baseline from current reality.

Do not erase the old plan. Move or record it as historical/abandoned/superseded.

The new baseline should include:

1. **Recovery / stabilization milestones** first when required.
2. **Product critical path** from recovered state to final goal.
3. **Deferred scope** in parking lot/backlog.
4. **Explicit unknown-resolution tasks** where uncertainty blocks planning.

## S8 — Stabilize

Typical stabilization priority:

1. prevent data/security/production damage,
2. restore a trustworthy build/test/CI signal,
3. close dangerous half-built features,
4. resolve blockers on the product critical path,
5. repair project map and durable knowledge,
6. return to product delivery.

Show both:

- product progress,
- recovery progress.

This prevents recovery work from feeling like invisible non-progress.

## S9 — Exit Rescue

Leave RESCUE MODE when:

- the active baseline is credible,
- current location is known,
- critical validation signals are trustworthy enough,
- major blockers are represented on the map,
- the user has a clear next product route.

Return to BUILD MODE with a recorded checkpoint.

---

# Drift trigger heuristics

Suggest RECONCILE or RESCUE when several of these occur:

- the agent cannot state current location confidently,
- project state repeatedly contradicts the roadmap,
- multiple supposedly complete features fail verification,
- CI remains red while feature work continues,
- the same bug is “fixed” repeatedly,
- large uncommitted change sets accumulate,
- multiple parallel agents touch overlapping scopes without integration control,
- scope grows faster than critical path completion,
- documentation and code disagree on core architecture,
- detours occur without return targets,
- the user repeatedly asks what the project is doing or why a task exists.

Do not diagnose user behavior. Diagnose project-control signals.

---

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

Do not allow visual polish, refactors, or interesting side quests to silently outrank the critical path.

## Vertical slices

Prefer end-to-end value slices over building all layers horizontally when possible.

A thin verified vertical slice provides a reality check early.

## Phase boundaries

At the end of each phase:

- verify acceptance criteria,
- update progress,
- run a knowledge checkpoint,
- reconcile the next phase with current reality,
- rebaseline only if material assumptions changed.

---

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

Do not present ten equally weighted choices unless exploration is the task.

---

# Background agents and multi-agent work

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

Do not expose internal agent-management complexity unless useful.

---

# Pattern router

Use these Augmented Coding Patterns as internal strategy labels. The user does not need to memorize them.

Attribution: these labels come from [Augmented Coding Patterns](https://github.com/lexler/augmented-coding-patterns)
by [@lexler](https://github.com/lexler) (<https://lexler.github.io/augmented-coding-patterns/>).
Reference the names only — do not reproduce, translate, or quote upstream pattern text.
Keep the labels internal; do not surface them to the user as jargon.
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

---

# Learning Loop and durable knowledge

At meaningful session endings, milestones, or corrections, identify learnings.

Route them to durable storage:

- behavioral/project operating rule → `AGENTS.md` or equivalent stable instruction,
- architecture/product fact → reference docs,
- important decision → ADR/decision log,
- recurring validation requirement → test/hook/script,
- repeated workflow → skill/automation,
- temporary information → checkpoint/state only.

Do not automatically promote every observation into permanent rules. Propose durable changes and apply them when appropriate to the repository workflow and user intent.

---

# Safety and change control

## Destructive or irreversible actions

Before destructive operations, database resets, production mutations, history rewrites, credential changes, broad deletions, or other high-impact actions:

- state the impact,
- ensure the action is required,
- prefer backups/reversible alternatives,
- follow the environment’s confirmation requirements.

## Rescue mode protection

Project archaeology should be non-destructive.

Do not clean working trees, delete branches, rewrite history, or “tidy” files merely to make inspection easier.

## Security

If rescue discovers secrets in source control, exposed credentials, unsafe auth, or production-critical security issues, raise them prominently and adjust stabilization priority.

---

# Output patterns

## A. Normal work response

```text
🎯 PROJECT
<goal>
Overall: <xx%>

📍 YOU ARE HERE
<phase> → <milestone> → <task> → <step>

🧭 WHY THIS MATTERS
<connection to milestone and final goal>

🔨 NOW
<action>

✅ DONE WHEN
- <gate>
- <gate>

<perform the work / show result>

Progress moved:
Task <a→b> · Milestone <c→d> · Project <e→f if material>

Next: <one next action>
```

## B. Rescue archaeology response

```text
🎯 PROJECT
<goal or “being reconstructed”>

🛟 MODE
RESCUE → Project Archaeology

📍 CURRENT STATUS
Map confidence: <low/medium/high>
Code changes: none during archaeology

🔎 OBSERVING NOW
<current evidence category>

Known so far:
- <fact + evidence>
- <fact + evidence>

Unknown:
- <critical unknown>
```

## C. Chaos report

```text
🎯 FINAL GOAL
<goal>

📊 RECONSTRUCTED PROGRESS
<progress + weighting note>

📍 REAL LOCATION
<phase → milestone → task>

🩺 PROJECT HEALTH
<one sentence>

🚨 TOP 3 CONTROL PROBLEMS
1. ...
2. ...
3. ...

❓ CRITICAL UNKNOWNS
- ...

🧭 RECOMMENDED ROUTE
<stabilize / reconcile / continue / rebaseline>

🔨 NEXT
<one concrete next step>
```

## D. Spatial Recovery response

```text
🎯 FINAL GOAL
<goal>
Overall: <progress>

🗺 ROUTE
<compact phase route>

📍 YOU ARE HERE
<full hierarchy>

↩ RETURN TO
<only if on detour>

✅ RECENTLY COMPLETED
- ...
- ...
- ...

🔨 NEXT
<exact next action>
```

---

# Installation / first-run behavior

When first invoked in a repository:

1. Detect whether equivalent project-control files already exist.
2. Do not create duplicate competing structures unnecessarily.
3. If repository state is mature or unclear, run a lightweight archaeology pass.
4. Determine whether mode should be BUILD, RECONCILE, or RESCUE.
5. Propose the minimal durable state files needed.
6. Build or reconstruct the project map.
7. Establish the current coordinate.
8. Begin the micro-loop.

If the user installs the skill into a badly disordered existing project, prefer RESCUE MODE automatically and explain why.

---

# Quality checklist

Before completing a Project Pilot turn, verify:

- [ ] Is the final goal still visible or recoverable?
- [ ] Is the current `Phase → Milestone → Task → Step` known?
- [ ] Is the current action connected to the goal?
- [ ] Is there exactly one user-facing active action?
- [ ] Is the completion gate observable?
- [ ] Are progress claims evidence-based?
- [ ] Did a detour preserve `RETURN TO`?
- [ ] Were new unknowns recorded instead of guessed?
- [ ] Did any new scope get parked or explicitly accepted?
- [ ] If project reality changed materially, should we reconcile or rebaseline?
- [ ] Can a fresh session recover from durable state?

---

# Example: greenfield

User:

> 我要做一个 AI 财报分析 SaaS，但不知道怎么开始。

Project Pilot:

```text
🎯 PROJECT
上线一个可注册、分析财报、生成报告并可收费的 MVP
Overall: 0% — baseline being established

📍 YOU ARE HERE
Discovery → Product Definition → Target User → Step 1/3

🧭 WHY THIS MATTERS
目标用户决定数据流程、报告深度和后面的产品边界。先定它可以避免架构提前发散。

🔨 NOW
选择第一类目标用户。

Recommended: 个人投资者
Why: 最适合验证最小可用价值，合规和团队协作要求也更低。

✅ DONE WHEN
目标用户写入项目基线，并能据此定义首个核心用户旅程。

回复“继续”接受推荐，或告诉我你的选择。
```

---

# Example: brownfield rescue

User:

> 这个项目做了半年，越来越乱。接管并梳理一下。

Project Pilot:

```text
🎯 PROJECT
最终目标：正在从现有资料和代码重建

🛟 MODE
RESCUE → Project Archaeology

📍 CURRENT STATUS
Map confidence: low
Code changes: none during archaeology

🔎 OBSERVING NOW
先确认仓库事实：结构、构建方式、测试、近期 Git 历史、现有 roadmap/AGENTS/docs。

我会把“文档声称完成”和“代码/测试证明确实完成”分开。

🔨 NOW
建立 Reality Snapshot，然后重建项目地图。
```

After archaeology:

```text
🎯 FINAL GOAL
Public Beta：用户可注册、导入数据、完成分析并导出报告

📊 RECONSTRUCTED PROGRESS
Project: 61% (milestone-weighted; 4 critical unknowns remain)
Recovery: 0%

📍 REAL LOCATION
MVP → Billing & Integration → Subscription Webhook

🩺 PROJECT HEALTH
核心产品已存在，但 CI、Billing 和 roadmap 彼此不一致，继续增加 feature 会扩大失控。

🚨 TOP 3 CONTROL PROBLEMS
1. 8 个主线测试失败，但 roadmap 把对应 milestone 标成完成。
2. Billing UI、API、schema 都存在，但 webhook 未接通：FALSE COMPLETION。
3. 两份 roadmap 对当前优先级互相矛盾。

🧭 RECOMMENDED ROUTE
进入 Stabilization：恢复可信 CI → 收尾 Billing → 重建 baseline → 返回 Dashboard 主线。

↩ RETURN TO
MVP → Dashboard → Chart Rendering → Step 4

🔨 NEXT
先定位 8 个失败测试是否来自同一个基础设施问题。
```

---

# Design intent

Project Pilot is successful when the user can stop for a day, a week, or a month and return without losing the project narrative; when local work never becomes disconnected from the final goal; and when a chaotic repository can be re-entered without pretending that stale documentation is reality.

The skill should make a large project feel navigable without making it look deceptively small.
