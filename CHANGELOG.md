# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Repository hygiene and documentation accuracy: added `.gitattributes` so the working tree
  keeps LF on every platform and `git add` stops warning about renormalising on each commit;
  the guide footer now carries the full version (`v0.8.0`); and `SKILL.md` lists `selftest`
  alongside the other four commands and describes them as five rather than two.
- `project-pilot-guide.html` was four releases behind: it still described v0.2.0 and never
  mentioned anything added since. It now covers the cause-naming layer, the two HUD weights
  and falsifiable markers, the complete drift list, history mining, the state templates and
  the validator, the stuck-step escapes, and a file map explaining why the always-loaded
  core is split from the reference library.

### Planned

- Critical-path-based progress weighting
- Fuller Chinese/English command alias coverage
- More real-world rescue case studies

## [0.8.0] - 2026-09-14

### Added

- `project_state.py drift <repo>`: the mechanical half of the S5 drift detector. It walks
  markdown and HTML for relative links that no longer resolve, and inventories TODO, FIXME,
  HACK and XXX markers, flagging the ones that name a path which no longer exists. `--json`
  emits the findings for other tools.
- A coverage table in `references/rescue-mode.md` that says which of the ten drift classes a
  machine decides and which need a reader, plus the instruction to report a clean scan as a
  clean scan rather than as a clean project.
- `selftest` grows from 18 to 33 cases, fifteen of them scanner cases with five
  counter-examples.

### Changed

- The scanner is tuned for precision over recall, because a noisy drift report gets ignored:
  a marker counts only when it follows a comment introducer (`# TODO:`, `// FIXME`,
  `<!-- TODO`), so prose about TODOs and markdown headings are skipped; a token counts as a
  path only when it contains a separator or ends in a known source suffix, so `re.compile` is
  not read as a file; and single-line string literals are stripped first, so fixture data
  inside a test table is not read as a comment. Against the first draft on this repository the
  inventory fell from 23 markers with 5 stale warnings to 0 and 0 — every one of those was
  false.
- `drift` is honest about its boundary: it prints the classes it cannot check instead of
  implying full coverage.

## [0.7.0] - 2026-09-14

### Added

- `parent` on map nodes. Containment was missing from the schema, so invariant 3's rule that
  "a parent percentage is computed from its children" had no way to find the children: the
  map carried ordering (`depends_on`) but no hierarchy. `parent` is containment, `depends_on`
  stays ordering, and a node without a parent sits at the top level.
- `scripts/project_state.py progress <dir>`: walks the `parent` links, uses each leaf's own
  progress, and averages each container from its children. `--json` emits the same numbers
  for other tools.
- Weighting semantics, now explicit instead of implied by a policy name: `equal` ignores
  declared weights, `weighted` honours them (default 1), and `milestone-weighted` honours
  weights only on children that are themselves containers, so the weight belongs on phases
  and milestones.
- Validator checks for `parent`: the target must exist, a node cannot parent itself, and the
  containment links must not form a cycle.
- `selftest` grew from 12 to 18 cases, six of them arithmetic: weighted 3:1 over 100/0 gives
  75, the same map under `equal` gives 50, an unknown child is excluded rather than counted
  as zero, all-unknown children give unknown, `milestone-weighted` weights containers only,
  and a nested tree averages its containers.

### Changed

- A container whose declared `progress` disagrees with the rollup is now a warning under the
  project's actual `progress_policy`. The first implementation of this check hardcoded
  `equal`, so it silently used the wrong rule under `weighted`; the earlier fixtures hid it
  because their child weights happened to be equal. Caught by testing with distinct weights.
- `templates/MAP.md` shows the tree with `parent` links and documents the weighting rules;
  `references/state-schema.md` gains a "Rolling up progress" section; `SKILL.md` lists the
  third command.

## [0.6.0] - 2026-09-14

### Added

- `references/team.md`: working with more than one person. Control state is written for a
  reader who was not in the session, ownership is recorded, deliveries come back to a human
  reviewer, and a handoff names the coordinate, the evidence, and what is still unknown.
- A "Read the log back" half to the Learning Loop. The session log was previously written
  and never read, so repeat complaints were re-learned instead of promoted. Reading is a
  separate pass with its own cadence; promotion deletes the entries it replaces.
- A sub-agent return contract: a bounded result plus evidence pointers, never the raw
  search trail, and `? UNKNOWN` for whatever could not be established.
- Two ways out of a stuck step in BUILD mode: a playground for testing an assumption
  directly, and several variants behind one shared acceptance gate when the route itself is
  undecided.
- History mining in RESCUE `S1`: hotspots and change coupling, with the metrics nominating
  candidates and a human reading each one before it becomes a refactor target.

### Changed

- Header markers became falsifiable. `🧪` must match the selected work type, `♻️` marks a
  turn that re-read durable state, and a marker whose condition did not hold stays out — a
  header that always looks the same carries no signal.
- The phrasing pass is complete: the last instructional prohibition, in
  `references/pattern-router.md`, now states the target instead of the taboo.

## [0.5.0] - 2026-09-14

### Added

- `templates/`: starting templates for the seven `.project-pilot/` files. A fresh `init`
  validates clean under `--strict`, so scaffolding and checking compose.
- `scripts/project_state.py`, three subcommands, no dependencies:
  - `init <dir>` scaffolds the state files from the templates;
  - `validate <dir>` checks required fields and enums, date and progress ranges, unique
    slug-like node ids, `depends_on` targets that resolve, dependency cycles, evidence
    record completeness, and evidence ids referenced by nodes;
  - `selftest` runs nine known-good and known-bad fixtures against the validator.
- The validator encodes the evidence rule mechanically: a node marked `VERIFIED` with no
  evidence id is an error, and a passing test record without `gate_proven: true` is a
  warning. Invariant 3 and the B5 gate-credibility rule are now checkable, not just stated.
- `references/state-schema.md` gains a "Machine-checked rules" section naming what the tool
  decides, so the schema and the enforcement cannot drift apart.

### Fixed

- Repairs content that a scripting error dropped from 0.4.0: the `state-schema` row of the
  `SKILL.md` reference table (it had been merged into the `diagnosis` row), two checklist
  items (one of which overwrote the reconcile item), the `diagnosis` entries in both
  READMEs, the v0.4 roadmap block in both READMEs, and the `[0.3.0]` changelog link.

### Changed

- `SKILL.md` points at the templates and the validator where it defines the durable files.
- The Planned list drops the two items this release delivers.

## [0.4.0] - 2026-09-14

### Added

- `references/diagnosis.md`: a cause layer that separates inherent limits (design
  around them) from usage errors (correct them), with the observable symptom,
  the cause, and the response for each.
- A header-weight rule: the full header at transitions and interruptions, a
  three-line compact header during consecutive micro-steps of one task. Both
  carry every field invariant 1 requires.
- A disposal threshold in BUILD mode: commit before the agent changes code, and
  when the second or third iteration stops improving, revert and restart with a
  sharper constraint instead of refining a failing approach.
- A review-handoff section in BUILD mode: split a large delivery into small,
  independently reviewable units, with vertical slices requested explicitly.

### Changed

- Core invariants and interaction rules are phrased as targets to hit rather than
  prohibitions to avoid, so the wording states what to do at the moment it applies.
  Invariant 2, 5, and 11 titles changed accordingly; numbering is unchanged.
- Invariant 9 now asks for the automation to be committed, so a repeated
  deterministic step becomes a reusable project artifact.

### Changed (positioning)

- The licensing posture is now stated as personal, local use. The project no longer
  treats "replace upstream labels with own names to reach zero external dependency"
  as a direction: the upstream names are the shared vocabulary of this field, so they
  are referenced directly with full attribution.
- README, README_EN, CONTRIBUTING, and CREDITS drop the "confirm authorization or
  delete the section before redistributing" wording. The fact that upstream declares
  no license is kept as a factual note in CREDITS.md.

### Notes

- `references/pattern-router.md` and `references/diagnosis.md` are the only files
  that reference upstream pattern names; both are attributed in CREDITS.md.

## [0.3.0] - 2026-09-14

### Added

- Invariant 14: authored state outlives generated artifacts — control state stays in
  version control and outside any path a build, regeneration, or cleanup step deletes,
  and a checkpoint must be sufficient to reconstruct the coordinate from a fresh clone.
- Gate credibility, independent review, and goal check as explicit verification rules
  for `B5`, with their mechanisms recorded in `references/evidence-record.md`.
- A progressive-disclosure map in `SKILL.md` naming every reference file and the
  trigger that requires it.

### Changed

- `SKILL.md` now holds only the always-loaded core: purpose, invariants, durable-file
  convention, interaction contract, commands, learning loop, safety, and checklist.
  The mode workflows, state schema, output shapes, and examples moved into
  `references/` and `examples/` with their content and headings unchanged.
- The Pattern Router moved to `references/pattern-router.md`, so the optional,
  attribution-bearing section can now be removed by deleting a single file.
- `CONTRIBUTING.md`'s "split before SKILL.md grows" rule is now satisfied by the
  skill itself rather than deferred.

### Removed

- Nothing. Every moved section is line-identical to its previous content.

## [0.2.0] - 2026-09-12

### Added

- A decision policy for choosing `DELIVERY`, `EXPLORATION`, or `RECOVERY`
  work from uncertainty, feedback cost, reversibility, and coupling.
- Evidence records that preserve claim, source, scope, limitations, and
  recheck triggers, with separate implementation, requirement, and evaluation checks.
- Progressive-disclosure references for decision selection, evidence workflows,
  and durable knowledge maintenance.

### Changed

- Project state and map schemas now track work type, assumptions, evidence scope,
  and separate product, exploration, and recovery progress.
- BUILD, RECONCILE, and RESCUE workflows now detect invalidated assumptions and
  stale or misleading evaluation signals, and can re-route without pretending an
  exploratory result was product delivery.
- README documentation now describes the adaptive execution model and reference files.

## [0.1.0] - 2026-09-02

Initial public release.

### Added

- `SKILL.md` — the skill itself. Defines 12 core invariants covering global
  orientation, evidence-based progress, detour return targets, unknown handling,
  rebaselining, and instant re-entry after interruption.
- Three operating modes:
  - **BUILD** — `Orient → Map → Select → Align → Act → Verify → Record → Navigate`
  - **RECONCILE** — expected vs observed comparison with NORMAL / RECONCILE / RESCUE severity
  - **RESCUE** — Project Archaeology, `S1`–`S9`, read-only by default
- Navigation HUD shown at the top of every substantive turn:
  final goal, overall progress, `Phase → Milestone → Task → Step`,
  why it matters, the single active action, and observable completion gates.
- Low-friction command set: `继续`, `我乱了`, `看全局`, `看当前`, `为什么`,
  `我不懂`, `换一个`, `先放着`, `接管项目`, `校准`, `重新基线`, `暂停`, `今天收尾`.
- Durable project-control file convention under `.project-pilot/`:
  `STATE.md`, `MAP.md`, `HEALTH.md`, `RECOVERY.md`, `PARKING_LOT.md`,
  `DECISIONS.md`, `SESSION_LOG.md`, `plans/{active,completed,abandoned}`, `snapshots/`.
- Status vocabulary with evidence-based rollup:
  `VERIFIED`, `PARTIAL`, `AT_RISK`, `BROKEN`, `NOT_STARTED`, `UNKNOWN`.
- Drift detector covering plan, documentation, architecture, scope, TODO,
  false completion, validation, and decision drift.
- Decision-load rules: one recommended default plus at most two alternatives.
- Background / multi-agent orchestration rules keeping a single user-facing coordinate.
- `project-pilot-guide.html` — single-file Chinese visual guide with zero dependencies.
- `README.md` (简体中文), `README_EN.md`, `LICENSE` (MIT), `CHANGELOG.md`,
  `CONTRIBUTING.md`, `CREDITS.md`, `.gitignore`.

### Attribution

- The Pattern Router section of `SKILL.md` uses strategy labels from
  [Augmented Coding Patterns](https://github.com/lexler/augmented-coding-patterns)
  by [@lexler](https://github.com/lexler). Pattern names are referenced only;
  no upstream text is copied, translated, or reproduced.
- `CREDITS.md` documents every referenced label, its trigger situation, a link back
  upstream, and the upstream licensing status.
- Note: as of 2026-09-02 the upstream repository declares no license
  (GitHub API `license: null`, no `LICENSE` file at root), which defaults to
  **all rights reserved**. Confirm licensing before any redistribution or commercial
  use, or remove the optional Pattern Router section.

[Unreleased]: https://github.com/ivagill1980/project-pilot/compare/v0.8.0...HEAD
[0.8.0]: https://github.com/ivagill1980/project-pilot/releases/tag/v0.8.0
[0.7.0]: https://github.com/ivagill1980/project-pilot/releases/tag/v0.7.0
[0.6.0]: https://github.com/ivagill1980/project-pilot/releases/tag/v0.6.0
[0.5.0]: https://github.com/ivagill1980/project-pilot/releases/tag/v0.5.0
[0.4.0]: https://github.com/ivagill1980/project-pilot/releases/tag/v0.4.0
[0.3.0]: https://github.com/ivagill1980/project-pilot/releases/tag/v0.3.0
[0.2.0]: https://github.com/ivagill1980/project-pilot/releases/tag/v0.2.0
[0.1.0]: https://github.com/ivagill1980/project-pilot/releases/tag/v0.1.0
