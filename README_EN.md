# Project Pilot

> A **project control layer** for AI coding agents — keeps large, long-running,
> or already-chaotic projects **globally visible while locally focused**.

![Version](https://img.shields.io/badge/version-0.8.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Format](https://img.shields.io/badge/format-Agent%20Skills%20%2F%20SKILL.md-orange)
![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen)
![Stack](https://img.shields.io/badge/deps-none-lightgrey)

[简体中文](./README.md) · [Visual Guide](./project-pilot-guide.html) · [Changelog](./CHANGELOG.md) · [Contributing](./CONTRIBUTING.md)

---

## Table of Contents

- [The Problem](#the-problem)
- [Core Model](#core-model)
- [Adaptive Progress](#adaptive-progress)
- [The Navigation HUD](#the-navigation-hud)
- [Three Modes](#three-modes)
- [Install](#install)
- [Command Cheatsheet](#command-cheatsheet)
- [What It Leaves In Your Project](#what-it-leaves-in-your-project)
- [Status Vocabulary](#status-vocabulary)
- [Evidence and Knowledge Maintenance](#evidence-and-knowledge-maintenance)
- [How It Compares](#how-it-compares)
- [Repository Layout](#repository-layout)
- [When to Use / Not to Use](#when-to-use--not-to-use)
- [Roadmap](#roadmap)
- [Credits](#credits)
- [License](#license)

---

## The Problem

Agents rarely fail at long-running projects because they write bad code.
They fail because they **lose their coordinates**.

| Symptom | Root cause |
| --- | --- |
| Lots of locally correct work that doesn't move the goal | Execution disconnected from the global objective |
| "Where was I?" after a few days away | No recoverable durable state |
| An old project gets messier the more you touch it | Declared state ≠ observed state |
| UI, API and schema all exist, the feature doesn't work | False completion |
| A small detour you never come back from | No return target |
| "Feels about half done" with no basis | Progress not derived from evidence |

Project Pilot doesn't touch your stack and doesn't generate code.
It adds **project-control discipline** on top of the agent.

> **One Thing in Context**
> Execute one thing at a time, while always showing where that thing sits in
> the whole project and how it moves the whole project forward.

---

## Core Model

Work is modelled as four stable levels; progress rolls up from leaves to root.

```text
PROJECT
└── PHASE
    └── MILESTONE
        └── TASK
            └── STEP   ← the single active execution point
```

Design points:

- **Global map always visible, detail just in time** — only the active or next
  milestone is deeply planned. No unmaintainable 500-step plan.
- **Exactly one active execution point** — background agents may run in parallel,
  but the user-facing main-line coordinate stays singular and stable.
- **Progress is computed from evidence** — never from vibes.

### Adaptive Progress

Every active node is marked as one of:

- `DELIVERY`: moves the product toward an accepted outcome;
- `EXPLORATION`: reduces a decision-blocking uncertainty with an experiment, prototype, or benchmark;
- `RECOVERY`: restores a trustworthy baseline, validation signal, or project-control surface.

Choose the next move from uncertainty, feedback cost, reversibility, and coupling. Use a small delivery slice when the goal is clear and feedback is cheap; explore first when a cheap experiment can distinguish routes; establish boundaries and recovery paths before high-coupling or safety-relevant changes. A result that rejects a route is useful exploration, not product completion.

---

## The Navigation HUD

Every substantive project turn opens with a fixed-shape header:

```text
🎯 PROJECT
Ship an MVP users can sign up for, analyze filings with, and be billed for
Overall: 38%

📍 YOU ARE HERE
Discovery → Product Definition → Target User → Step 1/3

🧪 WORK TYPE
EXPLORATION

🧭 WHY THIS MATTERS
The target user determines the data pipeline, report depth and product
boundaries. Deciding it now prevents premature architectural sprawl.

🔨 NOW
Pick the first target user segment.

✅ DONE WHEN
- Target user written into the project baseline
- First core user journey can be derived from it
```

While on a detour, the return target is also shown:

```text
↩ RETURN TO
MVP → Dashboard → Chart Rendering → Step 4
```

Default ratio: **10–20% global orientation, 80–90% current work.**
Hide irrelevant details — never the destination or your location.

---

## Three Modes

| Mode | When | What it does |
| --- | --- | --- |
| **BUILD** | New project, or a coherent one | `Orient → Map → Select → Align → Act → Verify → Record → Navigate` loop |
| **RECONCILE** | Suspected drift, not yet chaos | Freeze unverified claims, compare expected vs observed, classify drift as NORMAL / RECONCILE / RESCUE |
| **RESCUE** | Brownfield takeover, severe drift, repeated failed fixes, stale plans | Project archaeology: `observe → verify → reconstruct → diagnose → rebaseline → stabilize → continue` |

### Two hard rules in Rescue

1. **Observe before changing.** Read-only during archaeology unless a production
   incident needs immediate containment *and* the user asked for it.
2. **Rebaseline from verified reality.** Old plans are
   preserved as history (`plans/abandoned/`); the new baseline starts from
   today's verified reality.

Stabilization runs in fixed priority order:

```text
1. Stop data / security / production damage
2. Restore a trustworthy build / test / CI signal
3. Close dangerous half-built features
4. Resolve blockers on the product critical path
5. Repair the project map and durable knowledge
6. Return to product delivery
```

### Drift detector

Rescue checks each class explicitly: plan drift, documentation drift,
architecture drift, scope drift, TODO drift, **false completion**,
validation drift, decision drift.

---

## Install

Standard [Agent Skills](https://github.com/anthropics/skills) format.
`SKILL.md` is the only required file; `references/` and `examples/` hold optional, progressive-disclosure guidance — mode workflows, state schema, decision selection, evidence records, and knowledge maintenance. **No dependencies, no build step, no network calls.**

### Codex CLI

```bash
# User level: available in every project
git clone https://github.com/ivagill1980/project-pilot.git ~/.codex/skills/project-pilot

# Project level: committed to the repo, shared with the team
mkdir -p .codex/skills
cp -r project-pilot .codex/skills/
```

### Other agents

`SKILL.md` is a cross-agent format — drop it in the matching directory, no edits needed:

| Agent | User level | Project level |
| --- | --- | --- |
| Codex CLI | `~/.codex/skills/` | `.codex/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| WorkBuddy | `~/.workbuddy/skills/` | `.workbuddy/skills/` |

> The directory name is the skill name, and it must contain `SKILL.md` directly.
> **Restart or open a new session** afterwards so the agent rescans.

### Verify

```bash
ls ~/.codex/skills/project-pilot/SKILL.md
```

Then just talk to your agent — no commands to memorise:

- "Take over and make sense of this project."
- "Where am I?"
- "Continue."

---

## Command Cheatsheet

Natural-language equivalents work everywhere.

| Command | Effect |
| --- | --- |
| `continue` / `继续` | Accept the recommended path, advance to the next safe action |
| `where am I?` / `我乱了` | **Spatial recovery**: rebuild goal, progress, route, coordinate, return target, recent wins, next action |
| `zoom out` / `看全局` | Phase/milestone map, risks, critical path |
| `zoom in` / `看当前` | Current task and step, files, blockers, acceptance gates |
| `why` / `为什么` | Why this action exists and what it unlocks |
| `explain simpler` / `我不懂` | Same plan, simpler words |
| `alternative` / `换一个` | Up to three materially different routes with trade-offs |
| `park it` / `先放着` | Move to the parking lot, return attention to the main line |
| `rescue` / `接管项目` / `梳理项目` | Enter RESCUE mode and begin archaeology |
| `reconcile` / `校准` | Compare expected vs reality without rebuilding the roadmap |
| `rebaseline` / `重新基线` | Build a new baseline from current reality |
| `checkpoint` / `暂停` | Write a durable checkpoint for cheap re-entry |
| `wrap up` / `今天收尾` | Learning Loop: summarize, capture, update state, checkpoint, name the next re-entry step |

Decision-load rule: when a decision is needed, offer **one recommended default
plus at most two alternatives**, state the reason and the impact on the map,
and let `continue` accept it.

---

## What It Leaves In Your Project

If no equivalent convention exists yet, the skill maintains durable control
files under `.project-pilot/`:

```text
.project-pilot/
├── STATE.md          # goal, current coordinate, next action, health
├── MAP.md            # Phase → Milestone → Task → Step tree with statuses
├── HEALTH.md         # project-control health, tracked separately from product completion
├── RECOVERY.md       # rescue evidence, contradictions, stabilization milestones
├── PARKING_LOT.md    # parked ideas that must not silently enter scope
├── DECISIONS.md      # decision log
├── SESSION_LOG.md    # session log
├── plans/
│   ├── active/
│   ├── completed/
│   └── abandoned/    # superseded plans kept as history
└── snapshots/
```

If the repo already uses `AGENTS.md` or `docs/`, existing structures are reused
instead of creating competing ones.

State schema (YAML, abridged):

```yaml
project:  { name, final_goal, success_criteria, mode, progress_policy, baseline_id, baseline_date, overall_progress, product_progress, exploration_progress, recovery_progress }
location: { phase, milestone, task, step, work_type, return_to }
current:  { purpose, done_when, blockers, assumptions, evidence_required, next_action }
health:   { build, tests, ci, docs_alignment, architecture_alignment }
recent:   { completed, decisions, discoveries, evidence }
```

> Commit `.project-pilot/` if you want project state versioned; ignore it otherwise.
> This repo's `.gitignore` ignores `.project-pilot/` by default.

---

## Status Vocabulary

Progress must be derived from evidence, never estimated by feel.

| Mark | Status | Meaning |
| --- | --- | --- |
| ✅ | `VERIFIED` | Evidence proves it's complete |
| ◐ | `PARTIAL` | Meaningfully implemented but incomplete |
| ⚠ | `AT RISK` | Present but unreliable, drifting, or blocked |
| ✕ | `BROKEN` | Known not to work |
| ○ | `NOT STARTED` | Intentionally not begun |
| ? | `UNKNOWN` | Insufficient evidence |

Rules:

- A parent percentage is computed from its children; `UNKNOWN` never silently counts as done.
- Without weights, use equal weights within the same level and state that policy.
- **Unknown is a valid answer** — create an investigation step when it blocks planning.
- Record the source, version / environment / scenario scope, limitations, and recheck trigger for each material completion claim.
- Runtime evidence describes current behavior; it does not alone decide whether that behavior satisfies the goal. Check implementation, requirement, and evaluation separately.

Evidence priority when sources conflict (top wins):

```text
runtime / production behavior (for current behavior) > tests / CI / typecheck / lint > current code and config
  > recent accepted commits > accepted ADRs / specs > maintained docs
  > old roadmap / TODO comments > assumptions and recollection
```

This order answers “what does the system do now?” The user's current goal and the latest credible requirements or acceptance criteria still decide “what should it do?” A reproducibly wrong behavior is not a correct baseline just because it is easy to observe.

## Evidence and Knowledge Maintenance

Read the supporting reference only when the current task needs it:

- [build-mode.md](./references/build-mode.md) — the `B0`-`B7` loop, planning rules, decision load, and verification detail;
- [reconcile-mode.md](./references/reconcile-mode.md) — `R0`-`R5`;
- [rescue-mode.md](./references/rescue-mode.md) — `S1`-`S9` archaeology, the drift detector, and drift triggers;
- [diagnosis.md](./references/diagnosis.md) — observable symptom to cause to response, separating inherent limits from usage errors;
- [team.md](./references/team.md) — more than one person, and handoffs: control state written for a reader who was not there;
- [state-schema.md](./references/state-schema.md) — canonical `STATE` / `MAP` / `EVIDENCE` / `HEALTH` / `RECOVERY` / `PARKING_LOT` fields;
- [multi-agent.md](./references/multi-agent.md) — background and parallel agent orchestration;
- [decision-policy.md](./references/decision-policy.md) — choose delivery, exploration, or recovery work;
- [evidence-record.md](./references/evidence-record.md) — claims, acceptance examples, gate credibility, independent review, and conflicts;
- [knowledge-maintenance.md](./references/knowledge-maintenance.md) — classify and groom durable project knowledge;
- [output-patterns.md](./references/output-patterns.md) — the four response shapes;
- [pattern-router.md](./references/pattern-router.md) — internal strategy labels (optional, carries attribution).

`examples/` holds complete worked dialogues.

---

## Control state: templates and validation

The field definitions live in `references/state-schema.md`; the shape is enforced by a
script rather than by good intentions:

```bash
python scripts/project_state.py init .project-pilot      # create the seven state files from templates/
python scripts/project_state.py validate .project-pilot  # check fields, enums, ids, dependencies, evidence
python scripts/project_state.py progress .project-pilot  # roll progress up the parent links
python scripts/project_state.py drift .                  # scan the repo: broken doc links and stale TODOs
python scripts/project_state.py selftest                 # check the tool itself against known-good and known-bad fixtures
```

The validator turns the mechanically decidable part into a mechanism: required fields and
enums, date and progress ranges, unique slug-like node ids, `depends_on` and `parent`
targets that exist with no cycles, and evidence records that carry a `recheck_when` trigger.
The headline rule is that **a `VERIFIED` node with no evidence id is an error** — a progress
claim can no longer be made by feel.

`progress` implements what invariant 3 promises: it walks the `parent` links in `MAP.md`,
averages each container from its children under the weighting policy, leaves `unknown`
children out of the average instead of counting them as zero, and warns when a container's
own declared progress disagrees with the rollup — the children are the source of truth.
`--json` emits the same numbers for other tools. Exit `0` is clean and `1` means errors; `--strict` counts warnings
as errors. Standard library only, Python 3.8+.

---

## How It Compares

| | TODO lists | One-shot planning prompt | **Project Pilot** |
| --- | --- | --- | --- |
| Output | A task list | One document | Continuously maintained control state |
| Global orientation | None | Present at generation, then gone | **Shown at the top of every turn** |
| Progress source | Manual checkboxes | Estimation | **Derived from evidence** |
| Recovery after interruption | Memory | Re-read the doc | **`where am I?` rebuilds the coordinate** |
| Brownfield takeover | N/A | Tends to copy stale docs | **Read-only archaeology + rebaseline** |
| Scope control | None | None | **Parking Lot + Return Target** |

---

## Repository Layout

```text
project-pilot/
├── SKILL.md                  # the skill itself — the only required file
├── project-pilot-guide.html  # visual guide (Chinese), single file, no deps — just open it
├── README.md                 # 简体中文 README
├── README_EN.md              # this file
├── CHANGELOG.md              # Keep a Changelog
├── CONTRIBUTING.md           # contribution guide
├── CREDITS.md                # third-party pattern attribution and upstream licensing status
├── references/                # progressive-disclosure mode, state, evidence, and knowledge guidance
│   ├── build-mode.md
│   ├── reconcile-mode.md
│   ├── rescue-mode.md
│   ├── diagnosis.md
│   ├── team.md
│   ├── state-schema.md
│   ├── multi-agent.md
│   ├── decision-policy.md
│   ├── evidence-record.md
│   ├── knowledge-maintenance.md
│   ├── output-patterns.md
│   └── pattern-router.md      # optional; carries third-party attribution
├── examples/                  # complete worked dialogues
│   ├── greenfield-saas-mvp.md
│   └── brownfield-rescue-ecommerce.md
├── templates/                 # starting templates for the seven .project-pilot/ files
├── scripts/                   # state tool: init / validate / selftest (stdlib only)
├── LICENSE                   # MIT
└── .gitignore
```

Open `project-pilot-guide.html` in a browser for the fastest intuition:
core model, HUD, three modes, commands, state files, and worked dialogues.

---

## When to Use / Not to Use

**Use it for**

- Multi-phase, long-running, large projects
- Taking over a brownfield repo from someone else — or from yourself, six months ago
- Work that gets interrupted often and needs cheap re-entry
- Situations that need *credible* progress rather than "feels about done"
- Outer-loop orchestration when several background agents run in parallel

**Don't bother for**

- One-off scripts and single-file tweaks
- Pure Q&A or research
- Tasks already small enough to hold in your head — the HUD would be pure noise

---

## Roadmap

Completed in v0.2:

- [x] Select delivery, exploration, or recovery work from uncertainty, feedback cost, reversibility, and coupling
- [x] Add traceable, replayable evidence records for material completion claims
- [x] Separate product, exploration, and recovery progress, and surface requirement conflicts
- [x] Add progressive-disclosure references for decisions, evidence, and knowledge maintenance

Completed in v0.3:

- [x] Split the always-loaded core from on-demand references: mode workflows, state schema, output shapes, and examples moved out of `SKILL.md`
- [x] Strengthen verification: gate credibility (a new gate must be shown to fail), independent review, and a phase goal check
- [x] Add invariant 14: authored state stays separate from generated artifacts, lives in version control, and survives regeneration

Completed in v0.4:

- [x] Add `references/diagnosis.md`: attribute a symptom to an inherent limit or a usage error before choosing the response
- [x] Two header weights: the full header at transitions, a three-line compact header during consecutive micro-steps
- [x] Disposal threshold and explicit revert: commit before the change, and restart after two or three non-improving iterations
- [x] Review handoff: split a large delivery into independently reviewable units
- [x] Core rules rephrased as targets rather than prohibitions (invariant 2, 5, and 11 titles updated)

Completed in v0.5:

- [x] `templates/` with starting templates for all seven state files, scaffolded by one `init` command
- [x] `scripts/project_state.py validate`: fields, enums, dates, progress, node ids, dependency cycles, and evidence links
- [x] A `VERIFIED` node without evidence is an error; a passing test with no proven gate is a warning
- [x] `selftest`: nine known-good and known-bad fixtures check the validator itself

Completed in v0.6:

- [x] `references/team.md`: multi-person work and handoffs, with control state written for a reader who was not there
- [x] The Learning Loop gained its read-back half, so the session log stops being write-only
- [x] A sub-agent return contract: bounded result plus evidence pointers, not the raw trail
- [x] Two ways out of a stuck step: a playground for assumptions, or variants behind one gate
- [x] History mining in RESCUE (hotspots and change coupling), with metrics nominating rather than deciding

Completed in v0.7:

- [x] `parent` on map nodes: containment, kept distinct from `depends_on` ordering
- [x] `scripts/project_state.py progress` rolls progress up the tree under `equal`, `weighted`, or `milestone-weighted`
- [x] `unknown` children stay out of the average, and a container that disagrees with its children is flagged
- [x] Validator gains `parent` existence and containment-cycle checks; selftest grows to 18 cases, six of them rollup arithmetic

Completed in v0.8:

- [x] `drift` subcommand: scans for documentation links that no longer resolve (markdown links plus HTML href/src) and for stale TODOs
- [x] Tuned for precision over recall: a marker must be an annotation rather than prose, dotted identifiers are not paths, and quoted data is not a comment
- [x] `references/rescue-mode.md` gains a coverage table: which of the ten drift classes a machine decides and which need a reader
- [x] selftest grows to 33 cases, fifteen of them scanner cases including five counter-examples

Next directions (PRs welcome, see [CONTRIBUTING.md](./CONTRIBUTING.md)):

- [ ] Copy-paste templates for every `.project-pilot/` state file
- [ ] Optional init / validation scripts to offload deterministic work from the agent
- [ ] Finer progress weighting (critical-path weighting)
- [ ] Fuller Chinese/English command alias coverage
- [ ] More real-world rescue case studies

---

## Design Intent

Project Pilot succeeds when:

> The user can stop for a day, a week, or a month and return without losing the
> project narrative; when local work never becomes disconnected from the final
> goal; and when a chaotic repository can be re-entered from its verified reality.

It should make a large project feel **navigable** — without making it look
deceptively small.

---

## Credits

The **Pattern Router** (`references/pattern-router.md`) and **Diagnosis** (`references/diagnosis.md`) references — both loaded from `SKILL.md` on demand — use strategy labels from
[**Augmented Coding Patterns**](https://github.com/lexler/augmented-coding-patterns)
by [@lexler](https://github.com/lexler) — an evolving collection of patterns and
anti-patterns for developing software with LLMs.
Read it online at <https://lexler.github.io/augmented-coding-patterns/>.

This project **only references pattern names** as internal strategy labels for the
agent. No pattern text, examples, or documentation from the upstream project is
copied, translated, or reproduced here. The full list — each label, its trigger
situation, and a link back upstream — lives in [CREDITS.md](./CREDITS.md).

> 📌 **Scope of use.** This skill is positioned as a personal, local tool and is not
> redistributed. For the record: as of 2026-09-02 the upstream repository declares no
> license (GitHub API reports `license: null`; no `LICENSE` file at the repository
> root), which under the GitHub Terms of Service defaults to **all rights reserved**.
> Attribution and the full explanation live in [CREDITS.md](./CREDITS.md).

Apart from the pattern names referenced by `references/pattern-router.md` and
`references/diagnosis.md`, everything else here (the 14 core invariants, the three
modes, the `.project-pilot/` conventions, the command set, the HUD format) and the
whole of `project-pilot-guide.html` are original work of this project.

---

## License

[MIT](./LICENSE) © 2026 Project Pilot contributors

Attribution and upstream licensing status for third-party pattern names: [CREDITS.md](./CREDITS.md).
