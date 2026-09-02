# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Copy-paste templates for the `.project-pilot/` state files
- Optional init / validation scripts to offload deterministic work from the agent
- Critical-path-based progress weighting
- Fuller Chinese/English command alias coverage
- More real-world rescue case studies

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

[Unreleased]: https://github.com/ivagill1980/project-pilot/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/ivagill1980/project-pilot/releases/tag/v0.1.0
