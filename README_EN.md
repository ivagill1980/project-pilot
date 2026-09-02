# Project Pilot

> A **project control layer** for AI coding agents — keeps large, long-running,
> or already-chaotic projects **globally visible while locally focused**.

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Format](https://img.shields.io/badge/format-Agent%20Skills%20%2F%20SKILL.md-orange)
![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen)
![Stack](https://img.shields.io/badge/deps-none-lightgrey)

[简体中文](./README.md) · [Visual Guide](./project-pilot-guide.html) · [Changelog](./CHANGELOG.md) · [Contributing](./CONTRIBUTING.md)

---

## Table of Contents

- [The Problem](#the-problem)
- [Core Model](#core-model)
- [The Navigation HUD](#the-navigation-hud)
- [Three Modes](#three-modes)
- [Install](#install)
- [Command Cheatsheet](#command-cheatsheet)
- [What It Leaves In Your Project](#what-it-leaves-in-your-project)
- [Status Vocabulary](#status-vocabulary)
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

---

## The Navigation HUD

Every substantive project turn opens with a fixed-shape header:

```text
🎯 PROJECT
Ship an MVP users can sign up for, analyze filings with, and be billed for
Overall: 38%

📍 YOU ARE HERE
Discovery → Product Definition → Target User → Step 1/3

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
2. **Rebaseline instead of pretending an old plan is still valid.** Old plans are
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
One `SKILL.md`. **No dependencies, no build step, no network calls.**

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
project:  { name, final_goal, success_criteria, mode, baseline_id, baseline_date, overall_progress }
location: { phase, milestone, task, step, return_to }
current:  { purpose, done_when, blockers, next_action }
health:   { build, tests, ci, docs_alignment, architecture_alignment }
recent:   { completed, decisions, discoveries }
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

Evidence priority when sources conflict (top wins):

```text
runtime / production behavior > tests / CI / typecheck / lint > current code and config
  > recent accepted commits > accepted ADRs / specs > maintained docs
  > old roadmap / TODO comments > assumptions and recollection
```

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

Toward v0.2 (PRs welcome, see [CONTRIBUTING.md](./CONTRIBUTING.md)):

- [ ] Confirm licensing status with upstream `augmented-coding-patterns`, or replace the external pattern labels with self-owned strategy names
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
> goal; and when a chaotic repository can be re-entered without pretending that
> stale documentation is reality.

It should make a large project feel **navigable** — without making it look
deceptively small.

---

## Credits

The **Pattern Router** section of `SKILL.md` uses strategy labels from
[**Augmented Coding Patterns**](https://github.com/lexler/augmented-coding-patterns)
by [@lexler](https://github.com/lexler) — an evolving collection of patterns and
anti-patterns for developing software with LLMs.
Read it online at <https://lexler.github.io/augmented-coding-patterns/>.

This project **only references pattern names** as internal strategy labels for the
agent. No pattern text, examples, or documentation from the upstream project is
copied, translated, or reproduced here. The full list — each label, its trigger
situation, and a link back upstream — lives in [CREDITS.md](./CREDITS.md).

> ⚠️ **Upstream licensing status.** As of 2026-09-02 the upstream repository declares
> no license (GitHub API reports `license: null`; there is no `LICENSE` file at the
> repository root). Under the GitHub Terms of Service, a public repository without a
> license defaults to **all rights reserved**.
>
> If you plan to redistribute or commercialize this skill, either confirm the
> licensing status upstream or remove the Pattern Router section from `SKILL.md`.
> That section is an optional enhancement: the 12 core invariants and the three
> mode workflows work unchanged without it. See [CREDITS.md](./CREDITS.md).

Everything else in `SKILL.md` (the 12 core invariants, the three modes, the
`.project-pilot/` conventions, the command set, the HUD format) and the whole of
`project-pilot-guide.html` are original work of this project.

---

## License

[MIT](./LICENSE) © 2026 Project Pilot contributors

Attribution and upstream licensing status for third-party pattern names: [CREDITS.md](./CREDITS.md).
