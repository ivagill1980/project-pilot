#!/usr/bin/env python3
"""Project Pilot state tool.

Offloads the deterministic part of project control: scaffold the `.project-pilot/`
files from templates, and check that their content obeys the documented schema.

Standard library only. No dependencies, no network, no build step.

Usage:
  python scripts/project_state.py init <dir> [--force]
  python scripts/project_state.py validate <dir> [--strict]
  python scripts/project_state.py selftest

Exit codes: 0 clean, 1 errors found (or selftest failed), 2 usage error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
TEMPLATES = HERE.parent / "templates"

STATUS = ("VERIFIED", "PARTIAL", "AT_RISK", "BROKEN", "NOT_STARTED", "UNKNOWN")
MODE = ("BUILD", "RECONCILE", "RESCUE")
POLICY = ("equal", "weighted", "milestone-weighted")
WORK_TYPE = ("DELIVERY", "EXPLORATION", "RECOVERY")
SOURCE = ("test", "build", "runtime", "inspection", "user_acceptance", "external_system")
RESULT = ("pass", "partial", "fail", "inconclusive")

EVID_RE = re.compile(r"^EVID-\d{8}-\d{3,}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")

FENCE_RE = re.compile(r"^\s*```ya?ml\s*$", re.IGNORECASE)

STATE_FILES = (
    "STATE.md",
    "MAP.md",
    "HEALTH.md",
    "RECOVERY.md",
    "PARKING_LOT.md",
    "DECISIONS.md",
    "SESSION_LOG.md",
)


# --------------------------------------------------------------------------
# minimal YAML subset parser (maps, lists, inline lists, scalars)
# --------------------------------------------------------------------------

def _scalar(text: str):
    text = text.strip()
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [_unquote(part.strip()) for part in inner.split(",") if part.strip()]
    low = text.lower()
    if low in ("null", "~", "none"):
        return None
    if low == "true":
        return True
    if low == "false":
        return False
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if re.fullmatch(r"-?\d+\.\d+", text):
        return float(text)
    return _unquote(text)


def _unquote(text: str) -> str:
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1]
    return text


def _parse(text: str, first_line: int):
    """Return (data, lines) for one YAML block. lines maps a dotted path to a line number."""
    rows = []
    for offset, raw in enumerate(text.splitlines()):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        rows.append((len(raw) - len(raw.lstrip(" ")), raw.strip(), first_line + offset))

    data: dict = {}
    lines: dict = {}
    pos = 0

    def parse_block(indent: int, container: dict, path: str):
        nonlocal pos
        while pos < len(rows):
            ind, text_, lineno = rows[pos]
            if ind < indent:
                return
            if ind > indent or text_.startswith("- "):
                return
            key, _, val = text_.partition(":")
            key, val = key.strip(), val.strip()
            child = f"{path}.{key}" if path else key
            lines[child] = lineno
            if val == "":
                nxt = rows[pos + 1] if pos + 1 < len(rows) else None
                pos += 1
                if nxt and nxt[0] > ind and nxt[1].startswith("- "):
                    container[key] = parse_list(nxt[0], child)
                elif nxt and nxt[0] > ind:
                    container[key] = {}
                    parse_block(nxt[0], container[key], child)
                else:
                    container[key] = None
            else:
                container[key] = _scalar(val)
                pos += 1

    def parse_list(indent: int, path: str):
        nonlocal pos
        items = []
        while pos < len(rows):
            ind, text_, lineno = rows[pos]
            if ind != indent or not text_.startswith("- "):
                break
            body = text_[2:].strip()
            pos += 1
            if ":" in body and not body.startswith("["):
                item: dict = {}
                key, _, val = body.partition(":")
                key, val = key.strip(), val.strip()
                lines[f"{path}[{len(items)}].{key}"] = lineno
                if val == "":
                    nxt = rows[pos] if pos < len(rows) else None
                    if nxt and nxt[0] > indent and nxt[1].startswith("- "):
                        item[key] = parse_list(nxt[0], f"{path}[{len(items)}].{key}")
                    elif nxt and nxt[0] > indent:
                        item[key] = {}
                        parse_block(nxt[0], item[key], f"{path}[{len(items)}].{key}")
                    else:
                        item[key] = None
                else:
                    item[key] = _scalar(val)
                if pos < len(rows) and rows[pos][0] > indent:
                    parse_block(rows[pos][0], item, f"{path}[{len(items)}]")
                items.append(item)
            else:
                items.append(_scalar(body))
        return items

    parse_block(0, data, "")
    return data, lines


def yaml_blocks(text: str):
    blocks, current, start = [], None, 0
    for lineno, raw in enumerate(text.splitlines(), 1):
        if current is None and FENCE_RE.match(raw):
            current, start = [], lineno + 1
        elif current is not None and raw.strip().startswith("```"):
            blocks.append(("\n".join(current), start))
            current = None
        elif current is not None:
            current.append(raw)
    return blocks


def load(path: Path):
    text = path.read_text(encoding="utf-8")
    merged: dict = {}
    lines: dict = {}
    for block, start in yaml_blocks(text):
        data, block_lines = _parse(block, start)
        merged.update(data)
        lines.update(block_lines)
    return merged, lines


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------

class Report:
    def __init__(self):
        self.rows: list[tuple[str, str, int, str]] = []

    def error(self, filename, path, message, line=None):
        self.rows.append(("ERROR", filename, line or 0, f"{path}: {message}" if path else message))

    def warn(self, filename, path, message, line=None):
        self.rows.append(("WARN", filename, line or 0, f"{path}: {message}" if path else message))

    @property
    def errors(self):
        return [r for r in self.rows if r[0] == "ERROR"]

    @property
    def warnings(self):
        return [r for r in self.rows if r[0] == "WARN"]

    def render(self, strict=False):
        order = {"ERROR": 0, "WARN": 1}
        for severity, filename, line, message in sorted(self.rows, key=lambda r: (r[1], order[r[0]], r[2])):
            where = f"{filename}:{line}" if line else filename
            print(f"  {'E' if severity == 'ERROR' else 'W'} {where}  {message}")
        print()
        print(f"  errors: {len(self.errors)}   warnings: {len(self.warnings)}")
        if strict and self.warnings:
            print("  --strict: warnings count as errors")
        return 1 if self.errors or (strict and self.warnings) else 0


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------

def _get(data: dict, dotted: str, default=None):
    node = data
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node


def _require(rep: Report, name, data, lines, dotted, kind="text", enum=None):
    value = _get(data, dotted)
    if value is None or (isinstance(value, str) and not value.strip()):
        rep.error(name, dotted, "missing or empty", lines.get(dotted))
        return None
    if enum and value not in enum:
        rep.error(name, dotted, f"{value!r} is not one of {' | '.join(enum)}", lines.get(dotted))
        return None
    if kind == "date" and not (isinstance(value, str) and DATE_RE.match(value)):
        rep.error(name, dotted, f"{value!r} is not YYYY-MM-DD", lines.get(dotted))
    if kind == "progress" and value != "unknown":
        if not isinstance(value, (int, float)) or not 0 <= value <= 100:
            rep.error(name, dotted, f"{value!r} must be a number 0-100, or unknown", lines.get(dotted))
    return value


def check_state(rep: Report, name, data, lines):
    for key, kind, enum in (
        ("project.name", "text", None),
        ("project.final_goal", "text", None),
        ("project.mode", "text", MODE),
        ("project.progress_policy", "text", POLICY),
        ("project.baseline_date", "date", None),
        ("project.overall_progress", "progress", None),
        ("location.phase", "text", None),
        ("location.milestone", "text", None),
        ("location.task", "text", None),
        ("location.step", "text", None),
        ("current.next_action", "text", None),
    ):
        _require(rep, name, data, lines, key, kind, enum)

    work_type = _get(data, "location.work_type")
    if work_type is not None and work_type not in WORK_TYPE:
        rep.error(name, "location.work_type", f"{work_type!r} is not one of {' | '.join(WORK_TYPE)}",
                  lines.get("location.work_type"))

    done_when = _get(data, "current.done_when")
    if not done_when:
        rep.warn(name, "current.done_when", "no acceptance gate recorded; invariant 8 asks for an observable result",
                 lines.get("current.done_when"))

    return_to = _get(data, "location.return_to")
    if return_to not in (None, "") and not work_type:
        rep.warn(name, "location.return_to", "return target set without a work type", lines.get("location.return_to"))


POLICY_WEIGHT_MODES = ("equal", "weighted", "milestone-weighted")


def build_tree(nodes: dict):
    """Return (children, roots) derived from the `parent` links."""
    children = {node_id: [] for node_id in nodes}
    roots = []
    for node_id, node in nodes.items():
        parent = node.get("parent")
        if parent and parent in nodes and parent != node_id:
            children[parent].append(node_id)
        else:
            roots.append(node_id)
    return children, roots


def rollup(nodes: dict, policy: str = "equal"):
    """Compute container progress from children (Core invariant 3).

    Returns (progress, children, roots, overall):
      progress maps a node id to a number, or None when it is unknown.
      A leaf uses its declared progress; a container averages its children.
      Unknown children are excluded from the average rather than counted as zero.

    `policy` decides which weights are honoured:
      equal               - every child counts the same, declared weights ignored
      weighted            - each child contributes its declared weight (default 1)
      milestone-weighted  - only children that are themselves containers carry weight
    """
    children, roots = build_tree(nodes)

    def weight_of(node_id: str) -> float:
        if policy == "equal":
            return 1.0
        declared = nodes[node_id].get("weight")
        if not isinstance(declared, (int, float)) or declared <= 0:
            declared = 1.0
        if policy == "milestone-weighted" and not children.get(node_id):
            return 1.0
        return float(declared)

    progress: dict = {}
    visiting: set = set()

    def value(node_id: str):
        if node_id in progress:
            return progress[node_id]
        if node_id in visiting:            # a cycle is reported by the validator; stay safe here
            return None
        visiting.add(node_id)
        kids = children.get(node_id) or []
        if not kids:
            own = nodes[node_id].get("progress")
            result = float(own) if isinstance(own, (int, float)) else None
        else:
            total = 0.0
            weight_sum = 0.0
            for kid in kids:
                kid_value = value(kid)
                if kid_value is None:
                    continue
                weight = weight_of(kid)
                total += kid_value * weight
                weight_sum += weight
            result = (total / weight_sum) if weight_sum else None
        visiting.discard(node_id)
        progress[node_id] = result
        return result

    for node_id in nodes:
        value(node_id)

    total = 0.0
    weight_sum = 0.0
    for root in roots:
        root_value = progress.get(root)
        if root_value is None:
            continue
        weight = weight_of(root)
        total += root_value * weight
        weight_sum += weight
    overall = (total / weight_sum) if weight_sum else None
    return progress, children, roots, overall


def check_map(rep: Report, name, data, lines, records, policy="equal"):
    nodes = _get(data, "nodes")
    if not nodes:
        rep.error(name, "nodes", "no nodes defined", lines.get("nodes"))
        return
    if not isinstance(nodes, list):
        rep.error(name, "nodes", "expected a list of nodes", lines.get("nodes"))
        return

    by_id = {}
    for index, node in enumerate(nodes):
        prefix = f"nodes[{index}]"
        if not isinstance(node, dict):
            rep.error(name, prefix, "node is not a mapping", lines.get(prefix))
            continue
        node_id = node.get("id")
        where = lines.get(f"{prefix}.id", lines.get(prefix))
        if not node_id or not isinstance(node_id, str):
            rep.error(name, f"{prefix}.id", "missing node id", where)
            continue
        if not ID_RE.match(node_id):
            rep.error(name, f"{prefix}.id", f"{node_id!r} should be a stable slug", where)
        if node_id in by_id:
            rep.error(name, f"{prefix}.id", f"duplicate node id {node_id!r}", where)
        by_id[node_id] = node

        if not node.get("title"):
            rep.error(name, f"{prefix}.title", "missing title", lines.get(f"{prefix}.title", where))

        status = node.get("status")
        if status is None:
            rep.error(name, f"{prefix}.status", "missing status", lines.get(f"{prefix}.status", where))
        elif status not in STATUS:
            rep.error(name, f"{prefix}.status", f"{status!r} is not one of {' | '.join(STATUS)}",
                      lines.get(f"{prefix}.status", where))

        progress = node.get("progress")
        if progress is None:
            rep.warn(name, f"{prefix}.progress", "missing progress", where)
        elif progress != "unknown":
            if not isinstance(progress, (int, float)) or not 0 <= progress <= 100:
                rep.error(name, f"{prefix}.progress", f"{progress!r} must be a number 0-100, or unknown",
                          lines.get(f"{prefix}.progress", where))
            elif status == "VERIFIED" and progress != 100:
                rep.warn(name, f"{prefix}.progress", f"VERIFIED but progress is {progress}",
                         lines.get(f"{prefix}.progress", where))
            elif status == "NOT_STARTED" and progress not in (0,):
                rep.warn(name, f"{prefix}.progress", f"NOT_STARTED but progress is {progress}",
                         lines.get(f"{prefix}.progress", where))

        evidence = node.get("evidence") or []
        if not isinstance(evidence, list):
            evidence = [evidence]
        evidence = [e for e in evidence if e]
        if status == "VERIFIED" and not evidence:
            rep.error(name, f"{prefix}.evidence",
                      f"node {node_id!r} is VERIFIED without an evidence id; invariant 3 requires evidence "
                      "for every material completion claim", lines.get(f"{prefix}.evidence", where))
        if status == "BROKEN" and progress == 100:
            rep.warn(name, f"{prefix}.progress", "BROKEN but progress is 100", lines.get(f"{prefix}.progress", where))
        for item in evidence:
            if isinstance(item, str) and EVID_RE.match(item) and records is not None and item not in records:
                rep.warn(name, f"{prefix}.evidence", f"{item} is not declared as an evidence record",
                         lines.get(f"{prefix}.evidence", where))

    for index, node in enumerate(nodes):
        if not isinstance(node, dict) or not node.get("id"):
            continue
        prefix = f"nodes[{index}]"
        for dep in node.get("depends_on") or []:
            if dep not in by_id:
                rep.error(name, f"{prefix}.depends_on", f"unknown dependency {dep!r}",
                          lines.get(f"{prefix}.depends_on", lines.get(prefix)))

    # dependency cycles
    colour: dict = {}

    def visit(node_id, trail):
        colour[node_id] = "grey"
        for dep in by_id[node_id].get("depends_on") or []:
            if dep not in by_id:
                continue
            if colour.get(dep) == "grey":
                rep.error(name, f"nodes[{node_id}]", f"dependency cycle: {' -> '.join(trail + [node_id, dep])}",
                          lines.get(f"nodes[{node_id}].depends_on"))
            elif colour.get(dep) is None:
                visit(dep, trail + [node_id])
        colour[node_id] = "black"

    for node_id in by_id:
        if colour.get(node_id) is None:
            visit(node_id, [])

    # containment: parent links must resolve
    for index, node in enumerate(nodes):
        if not isinstance(node, dict) or not node.get("id"):
            continue
        prefix = f"nodes[{index}]"
        parent = node.get("parent")
        if parent in (None, ""):
            continue
        if parent == node["id"]:
            rep.error(name, f"{prefix}.parent", "a node cannot be its own parent",
                      lines.get(f"{prefix}.parent", lines.get(prefix)))
        elif parent not in by_id:
            rep.error(name, f"{prefix}.parent", f"unknown parent {parent!r}",
                      lines.get(f"{prefix}.parent", lines.get(prefix)))

    # containment: parent links must not form a cycle
    seen_cycles = set()
    for start in by_id:
        chain = []
        cursor = start
        while cursor in by_id and cursor not in chain:
            chain.append(cursor)
            cursor = by_id[cursor].get("parent") or None
        if cursor in by_id and cursor in chain:
            cycle = chain[chain.index(cursor):]
            key = frozenset(cycle)
            if key not in seen_cycles:
                seen_cycles.add(key)
                rep.error(name, f"nodes[{cursor}]", f"parent cycle: {' -> '.join(cycle + [cursor])}",
                          lines.get(f"nodes[{cursor}].parent"))

    # invariant 3: a container's progress is computed from its children,
    # under the weighting policy the project actually declared
    rolled, _children, _roots, _overall = rollup(by_id, policy)
    for node_id, node in by_id.items():
        declared = node.get("progress")
        computed = rolled.get(node_id)
        if computed is None or not isinstance(declared, (int, float)):
            continue
        if abs(float(declared) - computed) > 1:
            rep.warn(name, f"nodes[{node_id}].progress",
                     f"declares {declared} but its children roll up to {round(computed, 1)}; "
                     "invariant 3 computes a parent from its children",
                     lines.get(f"nodes[{node_id}].progress"))


def check_health(rep: Report, name, data, lines):
    health = _get(data, "health")
    if not isinstance(health, dict) or not health:
        rep.warn(name, "health", "no health entries recorded", lines.get("health"))
        return
    for key, value in health.items():
        if value not in STATUS:
            rep.error(name, f"health.{key}", f"{value!r} is not one of {' | '.join(STATUS)}", lines.get(f"health.{key}"))


def check_evidence(rep: Report, name, data, lines):
    records = _get(data, "evidence") or _get(data, "records")
    if not records:
        return None
    if not isinstance(records, list):
        rep.error(name, "evidence", "expected a list of records", lines.get("evidence"))
        return None
    ids = set()
    for index, record in enumerate(records):
        prefix = f"evidence[{index}]"
        if not isinstance(record, dict):
            rep.error(name, prefix, "record is not a mapping", lines.get(prefix))
            continue
        rid = record.get("id")
        where = lines.get(f"{prefix}.id", lines.get(prefix))
        if not rid:
            rep.error(name, f"{prefix}.id", "missing evidence id", where)
        else:
            ids.add(rid)
            if not EVID_RE.match(str(rid)):
                rep.error(name, f"{prefix}.id", f"{rid!r} should look like EVID-YYYYMMDD-###", where)
        if not record.get("claim"):
            rep.error(name, f"{prefix}.claim", "missing claim", lines.get(f"{prefix}.claim", where))
        source = record.get("source")
        if source is not None and source not in SOURCE:
            rep.error(name, f"{prefix}.source", f"{source!r} is not one of {' | '.join(SOURCE)}",
                      lines.get(f"{prefix}.source", where))
        result = record.get("result")
        if result is not None and result not in RESULT:
            rep.error(name, f"{prefix}.result", f"{result!r} is not one of {' | '.join(RESULT)}",
                      lines.get(f"{prefix}.result", where))
        if not record.get("recheck_when"):
            rep.error(name, f"{prefix}.recheck_when", "missing recheck trigger; evidence without an expiry "
                      "silently goes stale", lines.get(f"{prefix}.recheck_when", where))
        if result == "pass" and source == "test" and record.get("gate_proven") is not True:
            rep.warn(name, f"{prefix}.gate_proven", "passing test evidence with no record that the gate was "
                     "shown to fail; see B5 gate credibility", lines.get(f"{prefix}.gate_proven", where))
    return ids


def check_recovery(rep: Report, name, data, lines):
    if not data:
        return
    for key in ("trigger", "return_to", "exit_criteria"):
        if not _get(data, key):
            rep.warn(name, key, "missing", lines.get(key))


def check_parking(rep: Report, name, data, lines):
    items = _get(data, "items")
    if items is None:
        return
    if not isinstance(items, list):
        rep.error(name, "items", "expected a list", lines.get("items"))
        return
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        prefix = f"items[{index}]"
        if not (item.get("idea") or item.get("problem")):
            rep.warn(name, f"{prefix}.idea", "missing idea or problem", lines.get(prefix))
        if item.get("blocks_current") is None:
            rep.warn(name, f"{prefix}.blocks_current", "missing blocks_current flag", lines.get(f"{prefix}.blocks_current"))
        if not item.get("revisit_when"):
            rep.warn(name, f"{prefix}.revisit_when", "no revisit trigger", lines.get(f"{prefix}.revisit_when"))


def validate(root: Path, strict=False):
    rep = Report()
    if not root.exists():
        print(f"  no control state at {root}")
        print()
        print("  errors: 1   warnings: 0")
        return 1

    loaded = {}
    for filename in STATE_FILES:
        path = root / filename
        if path.exists():
            loaded[filename] = load(path)

    if "STATE.md" not in loaded:
        rep.error("STATE.md", "", "missing; init a control state or point at the right directory")
    if "MAP.md" not in loaded:
        rep.error("MAP.md", "", "missing; the map is what progress is computed from")
    if "HEALTH.md" not in loaded:
        rep.warn("HEALTH.md", "", "missing; operational health will not be tracked")

    records = None
    for filename, (data, _lines) in loaded.items():
        found = check_evidence(rep, filename, data, _lines)
        if found:
            records = (records or set()) | found

    if "STATE.md" in loaded:
        data, lines = loaded["STATE.md"]
        check_state(rep, "STATE.md", data, lines)
        if _get(data, "project.mode") == "RESCUE" and "RECOVERY.md" not in loaded:
            rep.warn("STATE.md", "project.mode", "RESCUE without RECOVERY.md", lines.get("project.mode"))

    policy = "equal"
    if "STATE.md" in loaded:
        declared = _get(loaded["STATE.md"][0], "project.progress_policy")
        if declared in POLICY_WEIGHT_MODES:
            policy = declared

    if "MAP.md" in loaded:
        data, lines = loaded["MAP.md"]
        check_map(rep, "MAP.md", data, lines, records, policy)

    if "HEALTH.md" in loaded:
        data, lines = loaded["HEALTH.md"]
        check_health(rep, "HEALTH.md", data, lines)

    if "RECOVERY.md" in loaded:
        data, lines = loaded["RECOVERY.md"]
        check_recovery(rep, "RECOVERY.md", data, lines)

    if "PARKING_LOT.md" in loaded:
        data, lines = loaded["PARKING_LOT.md"]
        check_parking(rep, "PARKING_LOT.md", data, lines)

    return rep.render(strict=strict)


# --------------------------------------------------------------------------
# init / selftest
# --------------------------------------------------------------------------

def cmd_init(target: Path, force=False):
    if not TEMPLATES.is_dir():
        print(f"  templates not found at {TEMPLATES}", file=sys.stderr)
        return 2
    target.mkdir(parents=True, exist_ok=True)
    written, skipped = [], []
    for src in sorted(TEMPLATES.glob("*.md")):
        dst = target / src.name
        if dst.exists() and not force:
            skipped.append(src.name)
            continue
        shutil.copyfile(src, dst)
        written.append(src.name)
    for name in written:
        print(f"  created  {target / name}")
    for name in skipped:
        print(f"  kept     {target / name} (exists; use --force to overwrite)")
    if not written:
        print("  nothing to do")
    print()
    print(f"  {len(written)} created, {len(skipped)} kept")
    return 0


GOOD_STATE = """---
title: State
---

```yaml
project:
  name: demo
  final_goal: ship the thing
  mode: BUILD
  progress_policy: equal
  baseline_date: 2026-09-14
  overall_progress: unknown
location:
  phase: Phase 1
  milestone: M1
  task: T1
  step: S1
  work_type: DELIVERY
  return_to: null
current:
  purpose: prove the tool works
  done_when: [validate exits 0]
  next_action: run the validator
```
"""

GOOD_MAP = """---
title: Map
---

```yaml
nodes:
  - id: m1
    title: Milestone one
    status: VERIFIED
    progress: 100
    evidence: [EVID-20260914-001]
    depends_on: []
  - id: m2
    title: Milestone two
    status: NOT_STARTED
    progress: 0
    depends_on: [m1]
evidence:
  - id: EVID-20260914-001
    claim: milestone one is done
    source: test
    result: pass
    gate_proven: true
    recheck_when: [interface changes]
```
"""

BAD_VERIFIED_NO_EVIDENCE = GOOD_MAP.replace("    evidence: [EVID-20260914-001]\n", "")
BAD_UNKNOWN_DEP = GOOD_MAP.replace("depends_on: [m1]", "depends_on: [nope]")
BAD_CYCLE = GOOD_MAP.replace("depends_on: []", "depends_on: [m2]")
BAD_ENUM = GOOD_STATE.replace("mode: BUILD", "mode: build")
BAD_DATE = GOOD_STATE.replace("baseline_date: 2026-09-14", "baseline_date: 14/09/2026")
BAD_PROGRESS = GOOD_STATE.replace("overall_progress: unknown", "overall_progress: 140")
BAD_RECHECK = GOOD_MAP.replace("    recheck_when: [interface changes]\n", "")

# containment fixtures
MAP_MISSING_PARENT = """```yaml
nodes:
  - id: a
    title: A
    status: NOT_STARTED
    progress: 0
    parent: nope
```
"""

MAP_PARENT_CYCLE = """```yaml
nodes:
  - id: a
    title: A
    status: NOT_STARTED
    progress: 0
    parent: b
  - id: b
    title: B
    status: NOT_STARTED
    progress: 0
    parent: a
```
"""

MAP_CONTAINER_MISMATCH = """```yaml
nodes:
  - id: root
    title: Root
    status: PARTIAL
    progress: 10
  - id: a
    title: A
    status: VERIFIED
    progress: 100
    parent: root
    evidence: [EVID-20260101-001]
evidence:
  - id: EVID-20260101-001
    claim: a is done
    source: test
    result: pass
    gate_proven: true
    recheck_when: [changes]
```
"""

DRIFT_CASES = (
    ("a resolving relative link is not reported",
     {"a.md": "see [b](b.md)\n", "b.md": "x\n"}, 0, 0, 0),
    ("a broken relative link is reported",
     {"a.md": "see [b](missing.md)\n"}, 1, 0, 0),
    ("an external link is ignored",
     {"a.md": "[x](https://example.com/nope)\n"}, 0, 0, 0),
    ("a link with a fragment still resolves",
     {"a.md": "[x](b.md#part)\n", "b.md": "x\n"}, 0, 0, 0),
    ("a directory link resolves",
     {"a.md": "[x](sub/)\n", "sub/c.md": "x\n"}, 0, 0, 0),
    ("an html href is checked",
     {"a.html": '<a href="gone.html">x</a>\n'}, 1, 0, 0),
    ("a TODO naming a missing path is stale",
     {"a.py": "# TODO: fix lib/gone.py\n"}, 0, 1, 1),
    ("a TODO naming an existing path is not stale",
     {"a.py": "# TODO: tidy lib/here.py\n", "lib/here.py": "x\n"}, 0, 0, 1),
    ("a TODO with no path is inventoried but not stale",
     {"a.py": "# FIXME: this is slow\n"}, 0, 0, 1),
    ("placeholders and anchors are ignored",
     {"a.md": "[x](#frag)\n[y]({template})\n[z](<https://e.com/a>)\n"}, 0, 0, 0),
    ("prose about TODOs is not an annotation",
     {"a.md": "### TODO Drift\nSee the TODO lists.\n"}, 0, 0, 0),
    ("an html comment is an annotation",
     {"a.html": "<!-- TODO: remove lib/gone.py -->\n"}, 0, 1, 1),
    ("a markdown html comment is an annotation",
     {"a.md": "<!-- TODO: drop docs/old.md -->\n"}, 0, 1, 1),
    ("a dotted identifier is not a path",
     {"a.py": "# TODO: replace re.compile usage\n"}, 0, 0, 1),
    ("quoted fixture data is not a comment",
     {"a.py": 'CASE = {"a.py": "# TODO: fix lib/gone.py\\n"}\n'}, 0, 0, 0),
    ("documented marker syntax in inline code is not an annotation",
     {"a.md": "Use `<!-- TODO: x` to mark docs/gone.md\n"}, 0, 0, 0),
    ("a continuation line of a block comment is an annotation",
     {"a.c": "/* start\n * TODO: remove lib/old.c\n */\n"}, 0, 1, 1),
)

ROLLUP_CASES = (
    ("weighted rollup: weights 3:1 over 100/0 gives 75", "weighted",
     [{"id": "root"}, {"id": "a", "parent": "root", "progress": 100, "weight": 3},
      {"id": "b", "parent": "root", "progress": 0, "weight": 1}], 75.0),
    ("equal policy ignores declared weights", "equal",
     [{"id": "root"}, {"id": "a", "parent": "root", "progress": 100, "weight": 3},
      {"id": "b", "parent": "root", "progress": 0, "weight": 1}], 50.0),
    ("unknown leaf is excluded, not counted as zero", "weighted",
     [{"id": "root"}, {"id": "a", "parent": "root", "progress": 100},
      {"id": "b", "parent": "root", "progress": "unknown"}], 100.0),
    ("a container whose children are all unknown is unknown", "weighted",
     [{"id": "root"}, {"id": "a", "parent": "root", "progress": "unknown"}], None),
    ("milestone-weighted weights containers only", "milestone-weighted",
     [{"id": "root"}, {"id": "m1", "parent": "root", "weight": 3},
      {"id": "m2", "parent": "root", "weight": 1},
      {"id": "t1", "parent": "m1", "progress": 100}, {"id": "t2", "parent": "m1", "progress": 0},
      {"id": "t3", "parent": "m2", "progress": 100}], 62.5),
    ("nested rollup averages the containers", "weighted",
     [{"id": "root"}, {"id": "m1", "parent": "root"}, {"id": "m2", "parent": "root"},
      {"id": "t1", "parent": "m1", "progress": 80}, {"id": "t2", "parent": "m1", "progress": 20},
      {"id": "t3", "parent": "m2", "progress": 100}], 75.0),
)


DRIFT_EXCLUDE_DIRS = {
    ".git", ".hg", ".svn", "node_modules", ".venv", "venv", "virtualenv", "env",
    "dist", "build", "out", "target", ".next", ".nuxt", ".cache", ".tox",
    "__pycache__", "site-packages", "vendor", ".gradle", ".idea", ".mypy_cache",
    ".pytest_cache", "coverage", ".terraform",
}
DOC_EXT = (".md", ".markdown", ".html", ".htm")
CODE_EXT = (
    ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java",
    ".rb", ".cs", ".c", ".h", ".cpp", ".hpp", ".sh", ".bash", ".ps1", ".md",
    ".html", ".htm", ".yml", ".yaml", ".toml", ".sql", ".php", ".swift", ".kt",
)
MD_LINK_RE = re.compile(r"\]\(\s*<?([^)\s>]+)>?")
HTML_LINK_RE = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""")
TODO_RE = re.compile(r"(?:#|//|/\*|<!--|--|;|\*)\s*(TODO|FIXME|HACK|XXX)\b")
DOC_TODO_RE = re.compile(r"<!--\s*(TODO|FIXME|HACK|XXX)\b")
PATH_TOKEN_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_./-]*\.[A-Za-z0-9]{1,6}")
STRING_LITERAL_RE = re.compile(r""""(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'""")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
# A dotted identifier such as `re.compile` is not a path; require a separator or a known suffix.
PATH_SUFFIXES = (
    ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".rb",
    ".cs", ".c", ".h", ".cpp", ".hpp", ".sh", ".bash", ".ps1", ".md", ".html", ".htm",
    ".json", ".yml", ".yaml", ".toml", ".sql", ".css", ".php", ".swift", ".kt",
)


def strip_string_literals(line: str) -> str:
    """Remove single-line string literals so quoted fixture data is not read as a comment."""
    return STRING_LITERAL_RE.sub(" ", line)


def looks_like_path(token: str) -> bool:
    return "/" in token or token.lower().endswith(PATH_SUFFIXES)


def iter_files(root: Path, exts):
    """Yield files under root with one of exts, pruning well-known build and vendor dirs."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in DRIFT_EXCLUDE_DIRS)
        for name in sorted(filenames):
            if name.lower().endswith(exts):
                yield Path(dirpath) / name


def _is_navigable(target: str) -> bool:
    low = target.lower()
    if low.startswith(("http://", "https://", "mailto:", "tel:", "data:", "javascript:", "#", "//")):
        return False
    return not any(ch in target for ch in "<>{}$")


def _resolve(root: Path, base: Path, target: str):
    """Resolve a link target, returning None when it is a pure fragment."""
    clean = unquote(target.split("#")[0].split("?")[0]).strip()
    if not clean:
        return None
    candidate = (root / clean.lstrip("/")) if clean.startswith("/") else (base / clean)
    return candidate


def _exists_with_fallback(path: Path) -> bool:
    if path.exists():
        return True
    for extra in (path.with_suffix(".md"), path / "index.md", path / "README.md"):
        if extra.exists():
            return True
    return False


def collect_drift(root: Path):
    """Return (broken_links, todos). Both are lists of tuples carrying file, line and detail."""
    broken, todos = [], []
    for path in iter_files(root, DOC_EXT):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = path.relative_to(root).as_posix()
        pattern = HTML_LINK_RE if path.suffix.lower() in (".html", ".htm") else MD_LINK_RE
        for lineno, line in enumerate(text.splitlines(), 1):
            for match in pattern.finditer(line):
                target = match.group(1).strip()
                if not _is_navigable(target):
                    continue
                resolved = _resolve(root, path.parent, target)
                if resolved is None:
                    continue
                if not _exists_with_fallback(resolved):
                    broken.append((rel, lineno, target))

    for path in iter_files(root, CODE_EXT):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = path.relative_to(root).as_posix()
        is_doc = path.suffix.lower() in (".md", ".markdown")
        marker_re = DOC_TODO_RE if is_doc else TODO_RE
        for lineno, line in enumerate(text.splitlines(), 1):
            bare = strip_string_literals(line)
            if is_doc:
                bare = INLINE_CODE_RE.sub(" ", bare)
            match = marker_re.search(bare)
            if not match:
                continue
            tokens = [t for t in PATH_TOKEN_RE.findall(bare) if looks_like_path(t)]
            missing = [t for t in tokens
                       if not (root / t).exists() and not (path.parent / t).exists()]
            stale = missing if tokens and len(missing) == len(tokens) else []
            todos.append((rel, lineno, match.group(1), line.strip(), stale))
    return broken, todos


def cmd_drift(root: Path, strict=False, as_json=False):
    """Report repository drift: documentation links that no longer resolve, and stale TODOs."""
    if not root.is_dir():
        print(f"  not a directory: {root}")
        return 2
    broken, todos = collect_drift(root)
    stale = [t for t in todos if t[4]]

    if as_json:
        print(json.dumps({
            "root": str(root),
            "broken_links": [{"file": f, "line": n, "target": t} for f, n, t in broken],
            "todos": [{"file": f, "line": n, "marker": m, "text": s, "missing_paths": list(p)}
                      for f, n, m, s, p in todos],
            "counts": {"broken_links": len(broken), "todos": len(todos), "stale_todos": len(stale)},
        }, ensure_ascii=False, indent=2))
        return 1 if broken else 0

    rep = Report()
    for rel, lineno, target in broken:
        rep.error(rel, "", f"link does not resolve: {target}", lineno)
    for rel, lineno, marker, text, missing in stale:
        rep.warn(rel, "", f"{marker} names a path that does not exist: {', '.join(missing)}", lineno)

    print(f"  scanned: {root}")
    print(f"  broken links: {len(broken)}   TODO/FIXME/HACK: {len(todos)}   stale TODOs: {len(stale)}")
    print()
    shown = 0
    for rel, lineno, marker, text, missing in todos:
        if shown >= 20:
            print(f"    ... and {len(todos) - shown} more TODO items")
            break
        flag = " STALE" if missing else ""
        snippet = text if len(text) <= 96 else text[:93] + "..."
        print(f"    {rel}:{lineno}  [{marker}]{flag}  {snippet}")
        shown += 1
    if todos:
        print()
    print("  Human-checked classes: plan, architecture, scope, validation, decision, assumption,")
    print("  evaluation, and false completion beyond the evidence rule. See references/rescue-mode.md.")
    print()
    return rep.render(strict=strict)


def cmd_progress(root: Path, as_json=False):
    """Roll progress up the containment tree instead of asking a model to estimate it."""
    map_path = root / "MAP.md"
    if not map_path.exists():
        print(f"  no MAP.md at {map_path}")
        return 1
    map_data, _map_lines = load(map_path)
    node_list = _get(map_data, "nodes") or []
    if not isinstance(node_list, list):
        print("  nodes is not a list")
        return 1
    by_id = {n["id"]: n for n in node_list if isinstance(n, dict) and n.get("id")}
    if not by_id:
        print("  no nodes in MAP.md")
        return 1

    policy = "equal"
    state_path = root / "STATE.md"
    source = "default"
    if state_path.exists():
        state_data, _state_lines = load(state_path)
        declared = _get(state_data, "project.progress_policy")
        if declared in POLICY_WEIGHT_MODES:
            policy = declared
            source = "STATE.md"

    rolled, children, roots, overall = rollup(by_id, policy)
    leaves = [n for n in by_id if not children.get(n)]
    unknowns = sorted(n for n, v in rolled.items() if v is None)
    mismatches = []
    for node_id, node in by_id.items():
        declared = node.get("progress")
        computed = rolled.get(node_id)
        if computed is None or not isinstance(declared, (int, float)):
            continue
        if abs(float(declared) - computed) > 1:
            mismatches.append((node_id, declared, round(computed, 1)))

    if as_json:
        print(json.dumps({
            "policy": policy,
            "policy_source": source,
            "overall": None if overall is None else round(overall, 2),
            "nodes": {n: (None if v is None else round(v, 2)) for n, v in rolled.items()},
            "unknown": unknowns,
            "containers": len(by_id) - len(leaves),
            "leaves": len(leaves),
            "mismatches": [{"id": n, "declared": d, "computed": c} for n, d, c in mismatches],
        }, ensure_ascii=False, indent=2))
        return 0

    def show(value):
        return "unknown" if value is None else f"{round(value)}%"

    print(f"  overall: {show(overall)}   (progress_policy: {policy}, from {source})")
    print()
    rows = []

    def walk(node_id, depth):
        node = by_id[node_id]
        mark = "" if children.get(node_id) else ""
        rows.append(f"{'  ' * depth}{node_id}{mark}  {show(rolled.get(node_id))}  [{node.get('status', '?')}]")
        for kid in sorted(children.get(node_id) or []):
            walk(kid, depth + 1)

    for root_id in sorted(roots):
        walk(root_id, 0)
    for row in rows:
        print("  " + row)
    print()
    print(f"  nodes: {len(by_id)} ({len(by_id) - len(leaves)} containers, {len(leaves)} leaves)"
          f"   unknown: {len(unknowns)}")
    if unknowns:
        print(f"  excluded from the average: {', '.join(unknowns)}")
    if mismatches:
        print(f"  declared progress disagrees with the rollup ({len(mismatches)}):")
        for node_id, declared, computed in mismatches:
            print(f"    {node_id}: declares {declared}, children roll up to {computed}")
    return 0


def cmd_selftest(tmp_dir=None):
    cases = [
        ("clean state validates", {"STATE.md": GOOD_STATE, "MAP.md": GOOD_MAP, "HEALTH.md": "```yaml\nhealth:\n  build: VERIFIED\n```\n"}, 0, []),
        ("VERIFIED without evidence fails", {"STATE.md": GOOD_STATE, "MAP.md": BAD_VERIFIED_NO_EVIDENCE}, 1, ["VERIFIED without an evidence id"]),
        ("unknown dependency fails", {"STATE.md": GOOD_STATE, "MAP.md": BAD_UNKNOWN_DEP}, 1, ["unknown dependency"]),
        ("dependency cycle fails", {"STATE.md": GOOD_STATE, "MAP.md": BAD_CYCLE}, 1, ["dependency cycle"]),
        ("bad mode enum fails", {"STATE.md": BAD_ENUM, "MAP.md": GOOD_MAP}, 1, ["not one of BUILD"]),
        ("bad date fails", {"STATE.md": BAD_DATE, "MAP.md": GOOD_MAP}, 1, ["not YYYY-MM-DD"]),
        ("progress out of range fails", {"STATE.md": BAD_PROGRESS, "MAP.md": GOOD_MAP}, 1, ["0-100"]),
        ("missing recheck_when fails", {"STATE.md": GOOD_STATE, "MAP.md": BAD_RECHECK}, 1, ["recheck"]),
        ("missing STATE.md fails", {"MAP.md": GOOD_MAP}, 1, ["missing"]),
        ("unknown parent fails", {"STATE.md": GOOD_STATE, "MAP.md": MAP_MISSING_PARENT}, 1, ["unknown parent"]),
        ("parent cycle fails", {"STATE.md": GOOD_STATE, "MAP.md": MAP_PARENT_CYCLE}, 1, ["parent cycle"]),
        ("container progress that disagrees with its children warns",
         {"STATE.md": GOOD_STATE, "MAP.md": MAP_CONTAINER_MISMATCH}, 0, ["roll up to 100"]),
    ]
    failures = 0
    if tmp_dir:
        base = Path(tmp_dir) / "project-state-selftest"
        if base.exists():
            shutil.rmtree(base, ignore_errors=True)
        base.mkdir(parents=True, exist_ok=True)
    else:
        base = Path(tempfile.mkdtemp(prefix="pp-selftest-"))
    try:
        for index, (label, files, expected_code, expected_messages) in enumerate(cases):
            target = base / f"case{index}"
            target.mkdir()
            for name, body in files.items():
                (target / name).write_text(body, encoding="utf-8")
            import contextlib
            import io
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                code = validate(target)
            output = buffer.getvalue()
            problems = []
            if code != expected_code:
                problems.append(f"exit {code}, expected {expected_code}")
            for needle in expected_messages:
                if needle not in output:
                    problems.append(f"missing message {needle!r}")
            if problems:
                failures += 1
                print(f"  FAIL  {label}: {'; '.join(problems)}")
            else:
                print(f"  ok    {label}")
        for label, policy, nodes, expected in ROLLUP_CASES:
            by_id = {n["id"]: n for n in nodes}
            _progress, _children, _roots, overall = rollup(by_id, policy)
            matches = (overall is None and expected is None) or (
                overall is not None and expected is not None and abs(overall - expected) < 0.01)
            if matches:
                print(f"  ok    {label}")
            else:
                failures += 1
                print(f"  FAIL  {label}: got {overall}, expected {expected}")
        for drift_index, case in enumerate(DRIFT_CASES):
            label, files, expected_broken, expected_stale, expected_todos = case
            target = base / f"drift{drift_index}"
            target.mkdir()
            for name, body in files.items():
                item = target / name
                item.parent.mkdir(parents=True, exist_ok=True)
                item.write_text(body, encoding="utf-8")
            broken, todos = collect_drift(target)
            stale = [t for t in todos if t[4]]
            counts = (len(broken), len(stale), len(todos))
            wanted = (expected_broken, expected_stale, expected_todos)
            if counts == wanted:
                print(f"  ok    {label}")
            else:
                failures += 1
                print(f"  FAIL  {label}: broken/stale/todos={counts}, want {wanted}")
    finally:
        shutil.rmtree(base, ignore_errors=True)
    total = len(cases) + len(ROLLUP_CASES) + len(DRIFT_CASES)
    print()
    print(f"  {total - failures}/{total} passed")
    return 1 if failures else 0


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    parser = argparse.ArgumentParser(description="Project Pilot state tool")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="create .project-pilot files from templates")
    p_init.add_argument("dir")
    p_init.add_argument("--force", action="store_true", help="overwrite existing files")

    p_val = sub.add_parser("validate", help="check control state against the schema")
    p_val.add_argument("dir")
    p_val.add_argument("--strict", action="store_true", help="treat warnings as errors")

    p_self = sub.add_parser("selftest", help="run the built-in checks against fixtures")
    p_self.add_argument("--tmp", help="directory for fixtures (default: a system temp directory)")

    p_prog = sub.add_parser("progress", help="roll progress up the containment tree")
    p_prog.add_argument("dir")
    p_prog.add_argument("--json", action="store_true", help="emit machine-readable output")

    p_drift = sub.add_parser("drift", help="report broken documentation links and stale TODOs")
    p_drift.add_argument("dir", nargs="?", default=".", help="repository root (default: current directory)")
    p_drift.add_argument("--strict", action="store_true", help="treat warnings as errors")
    p_drift.add_argument("--json", action="store_true", help="emit machine-readable output")

    args = parser.parse_args(argv)
    if args.command == "init":
        return cmd_init(Path(args.dir), args.force)
    if args.command == "validate":
        return validate(Path(args.dir), args.strict)
    if args.command == "progress":
        return cmd_progress(Path(args.dir), args.json)
    if args.command == "drift":
        return cmd_drift(Path(args.dir), args.strict, args.json)
    return cmd_selftest(args.tmp)


if __name__ == "__main__":
    sys.exit(main())
