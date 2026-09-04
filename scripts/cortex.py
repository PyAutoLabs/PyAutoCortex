#!/usr/bin/env python3
"""cortex.py — the Cortex's lifecycle script: check · gates · rule · move · new · retire.

The run-and-ruling registry (project → phase → runs → rulings) is a tree of
markdown files with light headers, and this script is the one thing that
writes their state and the one thing that checks it. Every rule it enforces is
written down in REFERENCE.md; the transition table there is `move`'s and the
chain rules are `rule`'s. Nothing here is not in that file.

PyYAML for `projects.yaml` and otherwise stdlib only, `main(argv)`, no
import-time side effects, `--root` on every verb
(default: the repo this script lives in), so every leg runs against a
`tmp_path` copy of the fixture in tests. The date is injectable (`--today`)
for the same reason.

Usage:
    python3 scripts/cortex.py check                      # OK or DRIFT (exit 1)
    python3 scripts/cortex.py gates                       # gated phases and their refs
    python3 scripts/cortex.py rule <phase> <verb> --body <file> [...]
    python3 scripts/cortex.py move <phase> <state> [...]
    python3 scripts/cortex.py new <project> <slug> --phase <n> [...]
    python3 scripts/cortex.py retire <project> --why "<one line>"   # a project's row

Exit codes: 0 = done · 1 = drift or a refused edit · 2 = bad arguments.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

# --------------------------------------------------------------------------- #
# vocabulary (REFERENCE.md)
# --------------------------------------------------------------------------- #
PHASE_STATES = (
    "planned", "gated", "ready", "submitted", "running", "pulled",
    "awaiting-ruling", "accepted", "rerun", "dropped",
)
TERMINAL_STATES = {"dropped"}
NON_TERMINAL_STATES = set(PHASE_STATES) - TERMINAL_STATES
#: `submitted..accepted` (and `rerun`) — the states that need a `Witness:`.
WITNESS_STATES = {"submitted", "running", "pulled", "awaiting-ruling",
                  "accepted", "rerun"}
#: reachable only through `rule`, so they need a `Ruling:`.
RULED_STATES = {"accepted", "rerun", "dropped"}

RUN_STATES = ("submitted", "running", "done", "failed", "timeout", "void",
              "legacy", "legacy_wrong")
LIVE_RUN_STATES = {"submitted", "running"}
LEGACY_RUN_STATES = {"legacy", "legacy_wrong"}
RESET_RUN_STATES = {"failed", "timeout", "void"}

#: What `new` writes into `## Where to look` before a phase has an output
#: path. It is honest on a `planned` phase and a hole on any other, because
#: the section is now rendered as the "which folder do I open" answer on the
#: dashboard's `## By project` view and in `pyauto-brain cortex checkin`.
WHERE_PLACEHOLDER = "(the output path, once there is one)"
#: The one state that may still be carrying the placeholder.
WHERE_EXEMPT_STATES = {"planned"}

RULING_VERBS = ("accept", "rerun", "drop", "leave-to-finish")
#: the head verb ↔ phase state agreement `check` enforces.
VERB_STATES = {
    "accept": {"accepted"},
    "drop": {"dropped"},
    "rerun": {"rerun", "ready", "submitted", "running", "pulled", "awaiting-ruling"},
    "leave-to-finish": NON_TERMINAL_STATES,
}
#: `rule` writes the phase into this state (None = unchanged).
VERB_TARGET = {"accept": "accepted", "rerun": "rerun", "drop": "dropped",
               "leave-to-finish": None}

# Canonical header key order — `new` writes it and the edit helpers insert a
# missing key at its slot so a hand-edited file keeps reading the same.
PHASE_KEYS = (
    "Project", "Phase", "State", "Gates", "Reset", "Witness", "Budget",
    "Runs", "Ruling", "Review-minutes", "Epic", "Filed", "Migrated-from",
)
#: `Batch:` is optional-historical — the 2026-08/09 rulings cite the batch
#: record they were filed from; nothing writes new ones (the slot apparatus
#: was retired 2026-09-03).
RULING_KEYS = (
    "Project", "Phase", "Runs", "Ruling", "Supersedes", "Batch", "Reviewed-at",
    "Review-minutes-actual", "Follow-ups", "Migrated-from",
)
PHASE_SECTIONS = ("Question", "Witness", "Where to look", "Runs", "Ruling")
RULING_SECTIONS = ("Ruling", "Evidence")

PROJECT_FIELDS = ("remote", "local_path", "ral_root", "mirror", "sync_cli",
                  "sync_verbs", "ledger", "witness_file", "partition", "status")
#: the one optional field — free text about the row (why a remote is `none`,
#: what a verb does). A row may omit it; an empty `note:` is still drift, and
#: any field outside these two tuples is still an error.
PROJECT_OPTIONAL_FIELDS = ("note",)
PARTITIONS = ("gpu", "ral", "both")
PROJECT_STATUSES = ("active", "dormant", "planned", "retired")

# --------------------------------------------------------------------------- #
# grammars (REFERENCE.md)
# --------------------------------------------------------------------------- #
# Copied verbatim from PyAutoMind/scripts/lifecycle.py: the lookbehind is what
# rejects `owner/Repo#N` — another owner is spelled as a URL.
GATE_REF_RE = re.compile(
    r"https://github\.com/([\w.-]+)/([\w.-]+)/(?:issues|pull)/(\d+)"
    r"|(?<![\w/])([A-Za-z_][\w.]*)#(\d+)\b"
)
DEFAULT_GATE_OWNER = "PyAutoLabs"

RUN_LINE_RE = re.compile(
    r"^- (?P<stem>\d+)"
    r"(?:_(?P<task>\d+)|_\[(?P<tasks>\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*)\])?"
    r": (?P<state>submitted|running|done|failed|timeout|void|legacy|legacy_wrong)"
    r" — (?P<partition>[a-z][a-z0-9_-]*)"
    r" — submitted (?P<date>\d{4}-\d{2}-\d{2})"
    r" — wall (?P<wall>\d+:\d{2})"
    r"(?: — (?P<note>.+))?$"
)
RUN_CONT_RE = re.compile(
    r"^    (?P<key>pulled_to|after|resumes|where|ruled): (?P<value>\S.*)$"
)
RUN_IDENT_RE = re.compile(r"^\d+(?:_\d+|_\[\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*\])?$")
PARTITION_RE = re.compile(r"^[a-z][a-z0-9_-]*$")

RULING_ID_RE = re.compile(r"^R-(\d{4})(\d{2})(\d{2})-(\d{2})$")
RULING_FILE_RE = re.compile(r"^rulings/(\d{4})/(\d{2})/(R-\d{8}-\d{2})\.md$")
PHASE_FILE_RE = re.compile(r"^phases/([a-z][a-z0-9_]*)/([^/]+)\.md$")
PROJECT_KEY_RE = re.compile(r"^[a-z][a-z0-9_]*$")
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WALL_RE = re.compile(r"^\d+:\d{2}$")
INT_RE = re.compile(r"^\d+$")

#: a light-header line: `Key: value` or a bare `Key:` (empty, or a list follows).
HEADER_KEY_RE = re.compile(r"^([A-Z][A-Za-z0-9-]*):(?:[ \t]+(.*?))?[ \t]*$")
HEADER_LINES = 30


class CortexError(Exception):
    """A refused edit or an unusable input — printed, exit 1, nothing written."""


def _dash(line: str) -> str:
    """`--` is accepted for the em dash (phone keyboards); read both as one."""
    return line.replace(" -- ", " — ")


# --------------------------------------------------------------------------- #
# the light header
# --------------------------------------------------------------------------- #
def header_span(lines: "list[str]") -> "tuple[int, int]":
    """(start, end) line indexes of the header block, end exclusive.

    The block starts at the first `Key:` line after the title (within the
    first 30 lines) and ends at the next blank line; (1, 1) when there is
    none."""
    start = None
    for i in range(1, min(len(lines), HEADER_LINES)):
        if HEADER_KEY_RE.match(lines[i]):
            start = i
            break
    if start is None:
        return 1, 1
    end = start
    while end < min(len(lines), HEADER_LINES) and lines[end].strip():
        end += 1
    return start, end


def parse_header(text: str) -> "tuple[str | None, dict[str, str]]":
    """(title, fields) — first occurrence of a key wins; a bare `Key:` followed
    by `- item` lines is a list, joined with commas."""
    lines = text.split("\n")
    title = lines[0][2:].strip() if lines and lines[0].startswith("# ") else None
    fields: "dict[str, str]" = {}
    start, end = header_span(lines)
    last_key = None
    for line in lines[start:end]:
        m = HEADER_KEY_RE.match(line)
        if m:
            key, value = m.group(1), (m.group(2) or "").strip()
            if key not in fields:
                fields[key] = value
                last_key = key
            else:
                last_key = None
            continue
        if line.startswith("- ") and last_key is not None:
            item = line[2:].strip()
            fields[last_key] = f"{fields[last_key]}, {item}" if fields[last_key] else item
    return title, fields


def edit_header(text: str, updates: "dict[str, str | None]", order=PHASE_KEYS) -> str:
    """Return `text` with header keys set (value) or removed (None), in place.

    Every other byte is preserved: a present key has only its value replaced;
    a missing key is inserted at its canonical slot; the block, the body and
    the line endings are untouched."""
    lines = text.split("\n")
    start, end = header_span(lines)
    if start == end and any(v is not None for v in updates.values()):
        # No header block yet: open one after the title line.
        insert_at = 1
        if len(lines) > 1 and lines[1].strip():
            lines.insert(1, "")
        lines.insert(insert_at + 1, "")
        start = end = insert_at + 1
    for key, value in updates.items():
        idx = next((i for i in range(start, end) if HEADER_KEY_RE.match(lines[i])
                    and HEADER_KEY_RE.match(lines[i]).group(1) == key), None)
        if value is None:
            if idx is not None:
                del lines[idx]
                end -= 1
            continue
        line = f"{key}: {value}" if value else f"{key}:"
        if idx is not None:
            lines[idx] = line
            continue
        rank = {k: i for i, k in enumerate(order)}
        after = start - 1
        for i in range(start, end):
            m = HEADER_KEY_RE.match(lines[i])
            if m and rank.get(m.group(1), -1) < rank.get(key, len(order)):
                after = i
        lines.insert(after + 1, line)
        end += 1
    return "\n".join(lines)


def sections(text: str) -> "dict[str, tuple[int, int]]":
    """{name: (first body line index, end index exclusive)} for `## name`."""
    lines = text.split("\n")
    heads = [(i, ln[3:].strip()) for i, ln in enumerate(lines) if ln.startswith("## ")]
    out = {}
    for n, (i, name) in enumerate(heads):
        stop = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
        out.setdefault(name, (i + 1, stop))
    return out


def append_to_section(text: str, name: str, new_lines: "list[str]",
                      replace_placeholder: "str | None" = None) -> str:
    """Append lines at the end of `## name` (before the next heading),
    keeping one blank line between the content and the next heading."""
    lines = text.split("\n")
    span = sections(text).get(name)
    if span is None:
        raise CortexError(f"no `## {name}` section to write into")
    body_start, stop = span
    # last content line of the section
    last = stop - 1
    while last >= body_start and not lines[last].strip():
        last -= 1
    if replace_placeholder is not None and last >= body_start \
            and lines[last].strip() == replace_placeholder \
            and all(not ln.strip() for ln in lines[body_start:last]):
        lines[last:last + 1] = new_lines
        return "\n".join(lines)
    if last < body_start:
        # An empty section: replace whatever blank lines it held with
        # `blank, content, blank` so the next heading keeps its gap.
        lines[body_start:stop] = [""] + new_lines + [""]
        return "\n".join(lines)
    lines[last + 1:last + 1] = new_lines
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# projects.yaml — PyYAML plus the field validation
# --------------------------------------------------------------------------- #
def parse_projects(text: str) -> "tuple[dict[str, dict], list[str]]":
    """Parse projects.yaml into {key: {field: value}} and validate the fields.

    The document itself is PyYAML's job (`yaml.safe_load`); this validates the
    shape the Cortex depends on — a mapping of project key → field mapping,
    the required and optional field names, and each field's value. An empty or
    comment-only file parses to an empty map."""
    problems: "list[str]" = []
    try:
        doc = yaml.safe_load(text)
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        where = f"projects.yaml:{mark.line + 1}" if mark is not None else "projects.yaml"
        return {}, [f"{where}: not valid YAML: {getattr(e, 'problem', None) or e}"]
    if doc is None:
        return {}, []
    if not isinstance(doc, dict):
        return {}, ["projects.yaml: the document is not a mapping of project keys"]
    rows: "dict[str, dict]" = {}
    for key, row in doc.items():
        if not (isinstance(key, str) and PROJECT_KEY_RE.match(key)):
            problems.append(f"projects.yaml: project key {key!r} must match "
                            f"{PROJECT_KEY_RE.pattern}")
            continue
        if not isinstance(row, dict):
            problems.append(f"projects.yaml: {key} is not a mapping of fields")
            continue
        rows[key] = _project_row(key, row, problems)
    return rows, problems


def _project_row(key: str, row: dict, problems: "list[str]") -> dict:
    """One validated row: unknown/missing fields and bad values are problems."""
    out: "dict[str, object]" = {}
    for field, value in row.items():
        if field not in PROJECT_FIELDS + PROJECT_OPTIONAL_FIELDS:
            problems.append(f"projects.yaml: unknown field `{field}` on {key}")
            continue
        if field == "sync_verbs":
            if not isinstance(value, list):
                problems.append(f"projects.yaml: {key}.sync_verbs must be a list `[a, b]`")
                continue
            bad = [x for x in value if not (isinstance(x, str) and re.match(r"^[a-z][a-z0-9_-]*$", x))]
            if bad:
                problems.append(f"projects.yaml: {key}.sync_verbs holds a non-bare word: {bad}")
            out[field] = [x for x in value if isinstance(x, str)]
            continue
        if value is None:
            problems.append(f"projects.yaml: {key}.{field} has no value")
            out[field] = ""
            continue
        if not isinstance(value, str):
            problems.append(f"projects.yaml: {key}.{field} must be a string, not "
                            f"{type(value).__name__}")
            value = str(value)
        out[field] = value
    _finish_row(key, out, problems)
    return out


def _finish_row(key: str, row: dict, problems: "list[str]") -> None:
    missing = [f for f in PROJECT_FIELDS if f not in row]
    if missing:
        problems.append(f"projects.yaml: {key} is missing {', '.join(missing)}")
    for f, v in row.items():
        if isinstance(v, str) and not v.strip():
            problems.append(f"projects.yaml: {key}.{f} is empty")
    if row.get("partition") and row["partition"] not in PARTITIONS:
        problems.append(f"projects.yaml: {key}.partition must be gpu | ral | both, "
                        f"not {row['partition']}")
    if row.get("status") and row["status"] not in PROJECT_STATUSES:
        problems.append(f"projects.yaml: {key}.status must be "
                        f"active | dormant | planned | retired, not {row['status']}")
    remote = row.get("remote")
    if remote and remote != "none" and not re.match(r"^[\w.-]+/[\w.-]+$", remote):
        problems.append(f"projects.yaml: {key}.remote must be owner/repo or none")
    for f in ("local_path", "ral_root"):
        if row.get(f) and not row[f].startswith("/"):
            problems.append(f"projects.yaml: {key}.{f} must be an absolute path")
    if row.get("mirror") and row["mirror"] != "none" and not row["mirror"].startswith("/"):
        problems.append(f"projects.yaml: {key}.mirror must be an absolute path or none")


def load_projects(root: Path) -> "tuple[dict[str, dict], list[str]]":
    path = root / "projects.yaml"
    if not path.is_file():
        return {}, ["projects.yaml: missing"]
    return parse_projects(path.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
# run lines
# --------------------------------------------------------------------------- #
class Run:
    __slots__ = ("ident", "stem", "task", "tasks", "state", "partition", "date",
                 "wall", "note", "cont", "lineno")

    def __init__(self, m: "re.Match", lineno: int):
        self.stem = m.group("stem")
        self.task = m.group("task")
        self.tasks = m.group("tasks")
        self.ident = self.stem + (f"_{self.task}" if self.task else
                                  f"_[{self.tasks}]" if self.tasks else "")
        self.state = m.group("state")
        self.partition = m.group("partition")
        self.date = m.group("date")
        self.wall = m.group("wall")
        self.note = m.group("note") or ""
        self.cont: "dict[str, str]" = {}
        self.lineno = lineno

    def task_set(self) -> "set[int] | None":
        """The tasks this line covers; None = the whole job (a bare stem)."""
        if self.task:
            return {int(self.task)}
        if self.tasks is None:
            return None
        out: "set[int]" = set()
        for part in self.tasks.split(","):
            if "-" in part:
                a, b = (int(x) for x in part.split("-"))
                out.update(range(a, b + 1))
            else:
                out.add(int(part))
        return out

    def ascending(self) -> bool:
        if self.tasks is None:
            return True
        last = -1
        for part in self.tasks.split(","):
            a, b = (int(x) for x in part.split("-")) if "-" in part else (int(part),) * 2
            if a <= last or b < a:
                return False
            last = b
        return True


def parse_runs(text: str) -> "tuple[list[Run], list[str]]":
    """Run lines of `## Runs`; a missing section = no runs (reported by the
    section check, not here)."""
    lines = text.split("\n")
    span = sections(text).get("Runs")
    runs: "list[Run]" = []
    problems: "list[str]" = []
    if span is None:
        return runs, problems
    for i in range(*span):
        raw = lines[i]
        if not raw.strip():
            continue
        line = _dash(raw)
        m = RUN_LINE_RE.match(line)
        if m:
            run = Run(m, i + 1)
            if not run.ascending():
                problems.append(f"line {i + 1}: task set not ascending: {run.ident}")
            runs.append(run)
            continue
        m = RUN_CONT_RE.match(line)
        if m:
            if not runs:
                problems.append(f"line {i + 1}: continuation line without a run line")
            else:
                runs[-1].cont[m.group("key")] = m.group("value").strip()
            continue
        problems.append(f"line {i + 1}: run line does not parse: {raw.strip()}")
    return runs, problems


def _overlaps(a: "set[int] | None", b: "set[int] | None") -> bool:
    return a is None or b is None or bool(a & b)


def run_problems(runs: "list[Run]", header_runs: str, state: str,
                 ruling_ids: "set[str]") -> "list[str]":
    problems: "list[str]" = []
    idents = {r.ident for r in runs}
    for i, a in enumerate(runs):
        for b in runs[i + 1:]:
            if a.stem == b.stem and _overlaps(a.task_set(), b.task_set()):
                problems.append(f"run {a.ident} overlaps {b.ident} on stem {a.stem}")
    body_stems = {r.stem for r in runs}
    listed = [s.strip() for s in header_runs.split(",") if s.strip()]
    for s in listed:
        if not INT_RE.match(s):
            problems.append(f"Runs: '{s}' is not a job stem")
    if set(listed) != body_stems:
        problems.append(f"Runs: header {{{', '.join(sorted(listed))}}} != body stems "
                        f"{{{', '.join(sorted(body_stems))}}}")
    if state == "pulled" and not any(r.state in ("done", "legacy") and "pulled_to" in r.cont
                                     for r in runs):
        problems.append("State: pulled needs at least one done | legacy run with pulled_to:")
    for r in runs:
        if r.state in LEGACY_RUN_STATES and "where" not in r.cont:
            problems.append(f"run {r.ident} is {r.state} without where:")
        for key in ("after", "resumes"):
            target = r.cont.get(key)
            if target is not None and (target not in idents or target == r.ident):
                problems.append(f"run {r.ident} {key}: {target} names no other run of this phase")
        ruled = r.cont.get("ruled")
        if ruled is not None and ruled not in ruling_ids:
            problems.append(f"run {r.ident} ruled: {ruled} does not resolve to a ruling file")
    return problems


def gate_refs(value: str) -> "tuple[list[str], list[str]]":
    """(refs, bad) from a comma-separated `Gates:` / `Follow-ups:` value."""
    refs, bad = [], []
    for token in (t.strip() for t in value.split(",")):
        if not token:
            continue
        if GATE_REF_RE.fullmatch(token):
            refs.append(token)
        else:
            bad.append(token)
    return refs, bad


def gate_url(ref: str) -> str:
    """Canonical issues URL for either GATE_REF_RE form (a PR *is* an issue)."""
    m = GATE_REF_RE.fullmatch(ref)
    owner, repo, num, short_repo, short_num = m.groups()
    if owner:
        return f"https://github.com/{owner}/{repo}/issues/{num}"
    return f"https://github.com/{DEFAULT_GATE_OWNER}/{short_repo}/issues/{short_num}"


# --------------------------------------------------------------------------- #
# the tree
# --------------------------------------------------------------------------- #
class Phase:
    def __init__(self, root: Path, path: Path):
        self.path = path
        self.rel = path.relative_to(root).as_posix()
        self.text = path.read_text(encoding="utf-8")
        self.title, self.fields = parse_header(self.text)
        self.project_dir = path.parent.name
        self.slug = path.stem
        self.runs, self.run_parse_problems = parse_runs(self.text)

    def get(self, key: str) -> str:
        return self.fields.get(key, "")

    @property
    def state(self) -> str:
        return self.get("State")


class Ruling:
    def __init__(self, root: Path, path: Path):
        self.path = path
        self.rel = path.relative_to(root).as_posix()
        self.text = path.read_text(encoding="utf-8")
        self.title, self.fields = parse_header(self.text)
        self.id = path.stem

    def get(self, key: str) -> str:
        return self.fields.get(key, "")


def _md_files(d: Path):
    return sorted(p for p in d.rglob("*.md")) if d.is_dir() else []


def load_phases(root: Path) -> "tuple[list[Phase], list[str]]":
    phases, problems = [], []
    for p in _md_files(root / "phases"):
        rel = p.relative_to(root).as_posix()
        if not PHASE_FILE_RE.match(rel):
            problems.append(f"{rel}: not a phase path (phases/<project>/<slug>.md)")
            continue
        phases.append(Phase(root, p))
    return phases, problems


def load_rulings(root: Path) -> "tuple[list[Ruling], list[str]]":
    rulings, problems = [], []
    for p in _md_files(root / "rulings"):
        rel = p.relative_to(root).as_posix()
        if rel == "rulings/AGENTS.md":
            continue
        m = RULING_FILE_RE.match(rel)
        if not m:
            problems.append(f"{rel}: not a ruling path (rulings/<YYYY>/<MM>/R-<YYYYMMDD>-<nn>.md)")
            continue
        yyyy, mm, rid = m.groups()
        r = Ruling(root, p)
        if rid[2:6] != yyyy or rid[6:8] != mm:
            problems.append(f"{rel}: filed under {yyyy}/{mm} but the id is dated {rid[2:6]}-{rid[6:8]}")
        rulings.append(r)
    return rulings, problems


def ruling_files(root: Path) -> "dict[str, Path]":
    """{id: path} of every ruling on disk (no validation)."""
    out = {}
    for p in _md_files(root / "rulings"):
        if RULING_ID_RE.match(p.stem):
            out.setdefault(p.stem, p)
    return out


def batch_records(root: Path) -> "list[Path]":
    d = root / "batches"
    return sorted(p for p in d.glob("*.md") if p.name != "AGENTS.md") if d.is_dir() else []


def batch_reviews(root: Path) -> "list[Path]":
    d = root / "batches" / "reviews"
    return sorted(p for p in d.glob("*.md") if p.name != "AGENTS.md") if d.is_dir() else []


# --------------------------------------------------------------------------- #
# check
# --------------------------------------------------------------------------- #
def phase_problems(root: Path, phases: "list[Phase]", projects: "dict[str, dict]",
                   rulings: "dict[str, Ruling]", successors: "dict[str, list[str]]") -> "list[str]":
    problems: "list[str]" = []
    numbers: "dict[tuple[str, str], str]" = {}
    for ph in phases:
        f = ph.fields
        p = [f"{ph.rel}: {msg}" for msg in ph.run_parse_problems]
        if ph.title is None:
            p.append(f"{ph.rel}: line 1 is not `# <title>`")
        for key in ("Project", "Phase", "State"):
            if not f.get(key):
                p.append(f"{ph.rel}: missing header key {key}:")
        for key in f:
            if key not in PHASE_KEYS:
                p.append(f"{ph.rel}: unknown header key {key}:")
        for name in PHASE_SECTIONS:
            if name not in sections(ph.text):
                p.append(f"{ph.rel}: missing section ## {name}")
        project = f.get("Project", "")
        if project and project != ph.project_dir:
            p.append(f"{ph.rel}: Project: {project} is not the directory name {ph.project_dir}")
        if project and project not in projects:
            p.append(f"{ph.rel}: Project: {project} is not a projects.yaml key")
        number = f.get("Phase", "")
        if number and not INT_RE.match(number):
            p.append(f"{ph.rel}: Phase: '{number}' is not an integer")
        elif number:
            prior = numbers.setdefault((ph.project_dir, number), ph.rel)
            if prior != ph.rel:
                p.append(f"{ph.rel}: duplicate Phase: {number} (also {prior})")
        state = f.get("State", "")
        if state and state not in PHASE_STATES:
            p.append(f"{ph.rel}: State: '{state}' is not a phase state")
        refs, bad = gate_refs(f.get("Gates", ""))
        for token in bad:
            p.append(f"{ph.rel}: Gates: unrecognised ref '{token}' — Repo#N or an "
                     f"issue/PR URL; no owner/Repo#N form")
        if f.get("Filed") and not DATE_RE.match(f["Filed"]):
            p.append(f"{ph.rel}: Filed: '{f['Filed']}' is not YYYY-MM-DD")
        if f.get("Budget") and not WALL_RE.match(f["Budget"]):
            p.append(f"{ph.rel}: Budget: '{f['Budget']}' is not H+:MM")
        if f.get("Review-minutes") and not INT_RE.match(f["Review-minutes"]):
            p.append(f"{ph.rel}: Review-minutes: '{f['Review-minutes']}' is not an integer")
        # the offline invariants on top of the table
        if state == "gated" and not refs:
            p.append(f"{ph.rel}: State: gated with an empty Gates:")
        if state in WITNESS_STATES and not f.get("Witness"):
            p.append(f"{ph.rel}: State: {state} needs a Witness:")
        ruling_id = f.get("Ruling", "")
        if state in RULED_STATES and not ruling_id:
            p.append(f"{ph.rel}: State: {state} needs a Ruling: (reachable only through rule)")
        head = None
        if ruling_id:
            if not RULING_ID_RE.match(ruling_id):
                p.append(f"{ph.rel}: Ruling: '{ruling_id}' is not a ruling id")
            elif ruling_id not in rulings:
                p.append(f"{ph.rel}: Ruling: {ruling_id} does not resolve to a ruling file")
            else:
                head = rulings[ruling_id]
                if successors.get(ruling_id):
                    p.append(f"{ph.rel}: Ruling: {ruling_id} is not a chain head "
                             f"(superseded by {', '.join(successors[ruling_id])})")
                if head.get("Phase") != ph.rel:
                    p.append(f"{ph.rel}: Ruling: {ruling_id} names {head.get('Phase') or '(nothing)'}, not this phase")
                verb = head.get("Ruling")
                if state and verb in VERB_STATES and state not in VERB_STATES[verb]:
                    p.append(f"{ph.rel}: Ruling: {ruling_id} verb '{verb}' does not fit State: {state}")
        # `## Where to look` is rendered, not just parsed: the by-project view
        # prints these bullets verbatim as the folders to open, and `collect`
        # resolves them to the artefacts it scores. A phase that has left
        # `planned` with only the template placeholder names nowhere.
        if state and state not in WHERE_EXEMPT_STATES:
            if not [b for b in _where_to_look(ph) if WHERE_PLACEHOLDER not in b]:
                p.append(f"{ph.rel}: ## Where to look names nowhere — a phase "
                         f"past planned needs at least one bullet that is not "
                         f"'{WHERE_PLACEHOLDER}'")
        if state == "pulled" and any(r.state in LIVE_RUN_STATES for r in ph.runs):
            if head is None or head.get("Ruling") != "leave-to-finish":
                p.append(f"{ph.rel}: State: pulled with a live run needs a leave-to-finish ruling head (--partial)")
        p.extend(f"{ph.rel}: {msg}" for msg in
                 run_problems(ph.runs, f.get("Runs", ""), state, set(rulings)))
        problems.extend(p)
    return problems


def ruling_problems(root: Path, rulings: "list[Ruling]", phases_by_rel: "dict[str, Phase]",
                    by_id: "dict[str, Ruling]", successors: "dict[str, list[str]]") -> "list[str]":
    problems: "list[str]" = []
    seen: "dict[str, str]" = {}
    for r in rulings:
        p: "list[str]" = []
        prior = seen.setdefault(r.id, r.rel)
        if prior != r.rel:
            p.append(f"{r.rel}: duplicate ruling id {r.id} (also {prior})")
        if r.title is None or not (r.title == r.id or r.title.startswith(f"{r.id} — ")):
            p.append(f"{r.rel}: title must be `# {r.id}` or `# {r.id} — <summary>`")
        for key in ("Project", "Phase", "Ruling"):
            if not r.get(key):
                p.append(f"{r.rel}: missing header key {key}:")
        for key in r.fields:
            if key not in RULING_KEYS:
                p.append(f"{r.rel}: unknown header key {key}:")
        for name in RULING_SECTIONS:
            if name not in sections(r.text):
                p.append(f"{r.rel}: missing section ## {name}")
        verb = r.get("Ruling")
        if verb and verb not in RULING_VERBS:
            p.append(f"{r.rel}: Ruling: '{verb}' is not a ruling verb")
        phase_rel = r.get("Phase")
        ph = phases_by_rel.get(phase_rel)
        if phase_rel and ph is None:
            p.append(f"{r.rel}: Phase: {phase_rel} does not resolve to a phase file")
        if ph is not None and r.get("Project") and ph.get("Project") != r.get("Project"):
            p.append(f"{r.rel}: Phase: {phase_rel} is not a phase of Project: {r.get('Project')}")
        if ph is not None:
            stems = {s.strip() for s in r.get("Runs").split(",") if s.strip()}
            phase_stems = {x.stem for x in ph.runs}
            if not stems <= phase_stems:
                p.append(f"{r.rel}: Runs: {{{', '.join(sorted(stems - phase_stems))}}} not in the phase's runs")
        sup = r.get("Supersedes")
        if sup:
            if sup == r.id:
                p.append(f"{r.rel}: Supersedes: itself")
            elif sup not in by_id:
                p.append(f"{r.rel}: Supersedes: {sup} does not resolve to a ruling file")
            else:
                old = by_id[sup]
                if not sup < r.id:
                    p.append(f"{r.rel}: Supersedes: {sup} is not earlier than {r.id}")
                if (old.get("Project"), old.get("Phase")) != (r.get("Project"), r.get("Phase")):
                    p.append(f"{r.rel}: Supersedes: {sup} names a different project/phase")
        if len(successors.get(r.id, [])) > 1:
            p.append(f"{r.rel}: has {len(successors[r.id])} successors "
                     f"({', '.join(successors[r.id])}) — a chain, not a tree")
        batch = r.get("Batch")
        if batch and not (root / "batches" / f"{batch}.md").is_file():
            p.append(f"{r.rel}: Batch: {batch} names no batches/{batch}.md")
        for key in ("Reviewed-at",):
            pass
        if r.get("Review-minutes-actual") and not INT_RE.match(r.get("Review-minutes-actual")):
            p.append(f"{r.rel}: Review-minutes-actual: not an integer")
        _, bad = gate_refs(r.get("Follow-ups"))
        for token in bad:
            p.append(f"{r.rel}: Follow-ups: unrecognised ref '{token}'")
        problems.extend(p)
    return problems


def check_problems(root: Path) -> "list[str]":
    """Every `check` rule, over the tree at `root`. Hermetic."""
    projects, problems = load_projects(root)
    phases, stray = load_phases(root)
    problems.extend(stray)
    rulings, stray = load_rulings(root)
    problems.extend(stray)
    by_id: "dict[str, Ruling]" = {}
    for r in rulings:
        by_id.setdefault(r.id, r)
    successors: "dict[str, list[str]]" = {}
    for r in rulings:
        if r.get("Supersedes"):
            successors.setdefault(r.get("Supersedes"), []).append(r.id)
    phases_by_rel = {ph.rel: ph for ph in phases}
    problems.extend(phase_problems(root, phases, projects, by_id, successors))
    problems.extend(ruling_problems(root, rulings, phases_by_rel, by_id, successors))
    return problems


def cmd_check(args) -> int:
    problems = check_problems(args.root)
    if problems:
        print("cortex check: DRIFT")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("cortex check: OK")
    return 0


# --------------------------------------------------------------------------- #
# gates
# --------------------------------------------------------------------------- #
def gates_report(root: Path) -> "tuple[list[str], int]":
    """(report lines, exit code) — every `gated` phase, its refs and their URLs.

    Read-only and offline: nothing asks GitHub whether a ref has cleared. Gate
    grading was retired 2026-09-03 — 2 gated refs and 0 flips in its whole
    life, while schema decision 54 routes sequencing through prose
    `Ready when:` lines. A gated phase is moved on by a human reading this
    listing and typing `move <phase> ready`."""
    phases, _ = load_phases(root)
    wanted = [ph for ph in phases
              if ph.state == "gated" and gate_refs(ph.get("Gates"))[0]]
    if not wanted:
        return ["gates: no gated phase"], 0
    lines = [f"gates: {len(wanted)} phase(s)"]
    for ph in wanted:
        refs = gate_refs(ph.get("Gates"))[0]
        lines.append(f"  {ph.rel}: {ph.state} — {', '.join(refs)}")
        for ref in refs:
            lines.append(f"    {ref} → {gate_url(ref)}")
    return lines, 0


def cmd_gates(args) -> int:
    lines, rc = gates_report(args.root)
    print("\n".join(lines))
    return rc


# --------------------------------------------------------------------------- #
# shared helpers for the writing verbs
# --------------------------------------------------------------------------- #
def _today(args) -> date:
    if getattr(args, "today", None):
        try:
            return date.fromisoformat(args.today)
        except ValueError:
            raise CortexError(f"--today must be YYYY-MM-DD, not {args.today}")
    return date.today()


def _phase_at(root: Path, ref: str) -> Phase:
    """The phase file `ref` names — repo-relative, or a path under root."""
    p = Path(ref)
    path = p if p.is_absolute() else root / p
    if not path.is_file():
        raise CortexError(f"no phase file at {ref}")
    try:
        path = path.resolve()
        path.relative_to(root.resolve())
    except ValueError:
        raise CortexError(f"{ref} is outside {root}")
    rel_path = root.resolve() / path.relative_to(root.resolve())
    if not PHASE_FILE_RE.match(path.relative_to(root.resolve()).as_posix()):
        raise CortexError(f"{ref} is not phases/<project>/<slug>.md")
    return Phase(root.resolve(), rel_path)


def _partition_for(root: Path, project: str, given: "str | None") -> str:
    if given:
        if not PARTITION_RE.match(given):
            raise CortexError(f"--partition '{given}' is not a bare partition name")
        return given
    projects, problems = load_projects(root)
    row = projects.get(project)
    if row is None:
        raise CortexError(f"project {project} is not a projects.yaml key")
    part = row.get("partition")
    if part in ("gpu", "ral"):
        return part
    raise CortexError(f"project {project} may use either partition (`both`) — pass --partition")


def _run_line(ident: str, state: str, partition: str, day: date, wall: str = "0:00",
              note: str = "") -> str:
    line = f"- {ident}: {state} — {partition} — submitted {day.isoformat()} — wall {wall}"
    return f"{line} — {note}" if note else line


def _append_run(ph: Phase, ident: str, state: str, partition: str, day: date, *,
                note: str = "", cont: "dict[str, str] | None" = None) -> str:
    """Phase text with one run line (and its continuations) appended to
    `## Runs` and the `Runs:` header re-derived from the body."""
    if not RUN_IDENT_RE.match(ident):
        raise CortexError(f"--run '{ident}' is not <stem>[_<task>|_[<set>]]")
    probe = Run(RUN_LINE_RE.match(_run_line(ident, state, partition, day)), 0)
    for r in ph.runs:
        if r.stem == probe.stem and _overlaps(r.task_set(), probe.task_set()):
            raise CortexError(f"run {ident} overlaps {r.ident} already on this phase")
    idents = {r.ident for r in ph.runs}
    for key, value in (cont or {}).items():
        if key in ("after", "resumes") and value not in idents:
            raise CortexError(f"{key}: {value} names no run of this phase")
    new_lines = [_run_line(ident, state, partition, day, note=note)]
    new_lines += [f"    {k}: {v}" for k, v in (cont or {}).items()]
    text = append_to_section(ph.text, "Runs", new_lines)
    stems = []
    for r in ph.runs + [probe]:
        if r.stem not in stems:
            stems.append(r.stem)
    return edit_header(text, {"Runs": ", ".join(stems)})


def _add_pulled_to(ph: Phase, text: str, pulled_to: "str | None", states: "set[str]") -> str:
    """Give every run in `states` a `pulled_to:` it lacks — `pulled_to` if
    given, else the run's own `where:` (a legacy run's quarantine path is
    where its results already are). Refuse when no run would carry one, so
    `move pulled` never writes a state `check` rejects."""
    targets = [r for r in ph.runs if r.state in states]
    if not targets:
        raise CortexError(f"no {' | '.join(sorted(states))} run to pull — nothing to review "
                          "(rule drop, or fix the run lines)")
    lacking = [r for r in targets if "pulled_to" not in r.cont]
    if not lacking or (not pulled_to and all("where" not in r.cont for r in lacking)):
        if any("pulled_to" in r.cont for r in targets):
            return text
        raise CortexError("no run carries pulled_to: — pass --pulled-to <laptop path>")
    lines = text.split("\n")
    for r in sorted(lacking, key=lambda x: x.lineno, reverse=True):
        path = pulled_to or r.cont.get("where")
        if not path:
            continue
        i = r.lineno  # 1-based run line → index of the line after it
        while i < len(lines) and RUN_CONT_RE.match(_dash(lines[i])):
            i += 1
        lines.insert(i, f"    pulled_to: {path}")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# move
# --------------------------------------------------------------------------- #
def move_phase(root: Path, ref: str, to: str, *, run: "str | None" = None,
               reason: "str | None" = None,
               partial: bool = False, partition: "str | None" = None,
               after: "str | None" = None, resumes: "str | None" = None,
               note: str = "", pulled_to: "str | None" = None,
               today: "date | None" = None) -> str:
    """Apply one edge of the transition table; return a one-line summary."""
    today = today or date.today()
    ph = _phase_at(root, ref)
    cur = ph.state
    if cur not in PHASE_STATES:
        raise CortexError(f"{ph.rel} has State: '{cur}', which is not a phase state")
    if to not in PHASE_STATES:
        raise CortexError(f"'{to}' is not a phase state ({' | '.join(PHASE_STATES)})")
    if cur == "dropped":
        raise CortexError(f"{ph.rel} is dropped — terminal; revival is a new phase number")
    if to == "dropped":
        raise CortexError("dropped is a ruling edge: `cortex.py rule <phase> drop`")
    if to in ("accepted", "rerun"):
        raise CortexError(f"{to} is a ruling edge: `cortex.py rule <phase> {VERB_FOR_STATE[to]}`"
                          + (" --supersedes <Ruling:>" if cur == "accepted" else ""))
    refs, bad = gate_refs(ph.get("Gates"))
    if bad:
        raise CortexError(f"{ph.rel}: Gates: unrecognised ref '{bad[0]}' — fix it first")
    updates: "dict[str, str | None]" = {}
    text = ph.text
    cont = {}
    if after:
        cont["after"] = after
    if resumes:
        cont["resumes"] = resumes

    if cur == to:
        if cur in ("submitted", "running") and run:
            part = _partition_for(root, ph.project_dir, partition)
            text = _append_run(ph, run, "submitted", part, today, note=note, cont=cont)
            ph.path.write_text(text, encoding="utf-8")
            return f"{ph.rel}: {cur} — appended run {run}"
        raise CortexError(f"{ph.rel} is already {cur}"
                          + ("" if cur in ("submitted", "running") else
                             "; --run is for submitted | running phases"))
    edge = (cur, to)
    if run and edge not in (("ready", "submitted"), ("submitted", "running")):
        raise CortexError("--run applies to ready → submitted and to a submitted | running phase")
    if edge == ("planned", "gated"):
        if not refs:
            raise CortexError(f"{ph.rel}: Gates: is empty — planned → ready")
    elif edge == ("planned", "ready"):
        if refs:
            raise CortexError(f"{ph.rel}: Gates: is non-empty — planned → gated")
    elif edge == ("gated", "ready"):
        pass  # the human read `gates` and judged the refs cleared
    elif edge == ("ready", "gated"):
        raise CortexError("ready → gated is a hand edit of the header — re-gating a "
                          "ready phase is a judgement, not an edge")
    elif edge == ("ready", "submitted"):
        if not ph.get("Witness"):
            raise CortexError(f"{ph.rel}: Witness: is empty — register the witness before submitting")
        if not run:
            raise CortexError("ready → submitted needs --run <id>")
        part = _partition_for(root, ph.project_dir, partition)
        text = _append_run(ph, run, "submitted", part, today, note=note, cont=cont)
    elif edge == ("ready", "pulled"):
        if not ph.runs or not all(r.state in LEGACY_RUN_STATES for r in ph.runs):
            raise CortexError("ready → pulled is for a legacy-born phase: every run line "
                              "legacy | legacy_wrong")
        if not ph.get("Witness"):
            raise CortexError(f"{ph.rel}: Witness: is empty — still mandatory for a legacy-born phase")
        text = _add_pulled_to(ph, text, pulled_to, {"legacy"})
    elif edge == ("submitted", "running"):
        if run:
            part = _partition_for(root, ph.project_dir, partition)
            text = _append_run(ph, run, "submitted", part, today, note=note, cont=cont)
    elif edge in (("submitted", "ready"), ("running", "ready")):
        if any(r.state in LIVE_RUN_STATES for r in ph.runs):
            raise CortexError(f"{ph.rel}: a run is still submitted | running")
        if not any(r.state in RESET_RUN_STATES for r in ph.runs):
            raise CortexError(f"{ph.rel}: no failed | timeout | void run to reset from")
        if not reason:
            raise CortexError(f"{cur} → ready needs --reason")
        updates["Reset"] = reason
    elif edge == ("running", "pulled"):
        if any(r.state in LIVE_RUN_STATES for r in ph.runs) and not partial:
            raise CortexError(f"{ph.rel}: a run is still submitted | running — "
                              "--partial for a partial array (then rule leave-to-finish)")
        text = _add_pulled_to(ph, text, pulled_to, {"done"})
    elif edge in (("pulled", "awaiting-ruling"), ("rerun", "ready")):
        pass
    else:
        raise CortexError(f"no edge {cur} → {to} in the transition table")
    updates["State"] = to
    ph.path.write_text(edit_header(text, updates), encoding="utf-8")
    return f"{ph.rel}: {cur} → {to}"


VERB_FOR_STATE = {"accepted": "accept", "rerun": "rerun", "dropped": "drop"}


def cmd_move(args) -> int:
    print(move_phase(args.root, args.phase, args.state, run=args.run, reason=args.reason,
                     partial=args.partial, partition=args.partition,
                     after=args.after, resumes=args.resumes, note=args.note or "",
                     pulled_to=args.pulled_to, today=_today(args)))
    return 0


# --------------------------------------------------------------------------- #
# retire
# --------------------------------------------------------------------------- #
def retire_project(root: Path, key: str, why: str, today: date) -> str:
    """Flip one `projects.yaml` row to `status: retired` and stamp the reason
    on its `note:`. The only verb that writes `projects.yaml`.

    Three things it deliberately does not do. It does not **delete the row**:
    that row is the only record of where the project's data lives, and a
    retired project still has to be findable. It does not touch a **phase** or
    a **ruling**: `rulings/` is append-only and history is not rewritten by a
    change of status. And it does not retire over **live work** — every state
    outside `RULED_STATES` and `planned` is an unfinished question, so the
    refusal names each one and the human rules or drops it first. `planned`
    stays: an unasked question costs nothing to leave behind.

    The edit is two lines. Everything else in the file — comments, blank
    lines, the order of the rows, the other rows' bytes — is preserved, and
    the result is re-parsed before it is kept: a `projects.yaml` this verb
    could not read back is restored to the bytes it had.
    """
    why = (why or "").strip()
    if not why:
        raise CortexError("--why must say why, in one line")
    if '"' in why or "\n" in why:
        raise CortexError("--why cannot hold a double quote or a newline "
                          "(projects.yaml quotes with no escapes)")
    projects, problems = load_projects(root)
    if problems:
        raise CortexError("projects.yaml does not parse clean — run `check` "
                          "and fix it before retiring: " + "; ".join(problems))
    if key not in projects:
        raise CortexError(f"{key} is not a projects.yaml key")
    if projects[key].get("status") == "retired":
        raise CortexError(f"{key} is already retired")
    phases, _ = load_phases(root)
    live = [f"{ph.rel} — {ph.state}" for ph in phases
            if ph.project_dir == key
            and ph.state not in RULED_STATES | {"planned"}]
    if live:
        raise CortexError(f"{key} still has live work — rule or drop it "
                          f"first: {', '.join(live)}")

    path = root / "projects.yaml"
    original = path.read_text(encoding="utf-8")
    lines = original.split("\n")
    starts = [i for i, ln in enumerate(lines) if ln == f"{key}:"]
    if len(starts) != 1:
        raise CortexError(f"projects.yaml: expected one `{key}:` line, "
                          f"found {len(starts)}")
    start = starts[0]
    stop = start + 1
    while stop < len(lines) and lines[stop].startswith("  "):
        stop += 1
    block = lines[start:stop]
    at_status = [i for i, ln in enumerate(block) if re.match(r"^  status: .*$", ln)]
    at_note = [i for i, ln in enumerate(block) if re.match(r"^  note:(?: .*)?$", ln)]
    if len(at_status) != 1 or len(at_note) > 1:
        raise CortexError(f"projects.yaml: {key} is not one `  status:` line "
                          f"and at most one `  note:` line")
    block[at_status[0]] = "  status: retired"
    note = f'  note: "retired {today.isoformat()}: {why}"'
    if at_note:
        block[at_note[0]] = note
    else:
        block.append(note)
    lines[start:stop] = block
    path.write_text("\n".join(lines), encoding="utf-8")

    rows, problems = load_projects(root)
    if problems or rows.get(key, {}).get("status") != "retired":
        path.write_text(original, encoding="utf-8")
        raise CortexError("the edit would not read back — projects.yaml is "
                          "unchanged: " + ("; ".join(problems) or
                                           f"{key} did not come back retired"))
    return f"retired {key}"


def cmd_retire(args) -> int:
    print(retire_project(args.root, args.project, args.why, _today(args)))
    return 0


# --------------------------------------------------------------------------- #
# rule
# --------------------------------------------------------------------------- #
def next_ruling_id(root: Path, day: date, taken: "set[str] | None" = None) -> str:
    stamp = day.strftime("%Y%m%d")
    existing = set(ruling_files(root)) | (taken or set())
    for n in range(1, 100):
        rid = f"R-{stamp}-{n:02d}"
        if rid not in existing:
            return rid
    raise CortexError(f"99 rulings already filed on {day.isoformat()}")


def _ruling_target(ph: Phase, verb: str, supersedes: "str | None", by_id: "dict[str, Ruling]",
                   successors: "dict[str, list[str]]") -> "str | None":
    """The phase state `verb` writes, or raise if the table forbids it."""
    state = ph.state
    if verb not in RULING_VERBS:
        raise CortexError(f"'{verb}' is not a ruling verb ({' | '.join(RULING_VERBS)})")
    if state == "dropped":
        raise CortexError(f"{ph.rel} is dropped — terminal")
    if supersedes:
        if supersedes not in by_id:
            raise CortexError(f"--supersedes {supersedes} does not resolve to a ruling file")
        old = by_id[supersedes]
        if old.get("Phase") != ph.rel:
            raise CortexError(f"--supersedes {supersedes} rules on {old.get('Phase')}, not {ph.rel}")
        if successors.get(supersedes):
            raise CortexError(f"{supersedes} already has a successor "
                              f"({successors[supersedes][0]}) — supersede the head")
    if state == "accepted":
        if verb not in ("rerun", "drop"):
            raise CortexError(f"accepted takes only rerun | drop, with --supersedes {ph.get('Ruling')}")
        if supersedes != ph.get("Ruling"):
            raise CortexError(f"accepted → {VERB_TARGET[verb]} needs --supersedes {ph.get('Ruling')} "
                              "(the REWIND case)")
        return VERB_TARGET[verb]
    if verb == "leave-to-finish":
        if state not in ("running", "pulled", "awaiting-ruling"):
            raise CortexError(f"leave-to-finish applies to running | pulled | awaiting-ruling, "
                              f"not {state}")
        return None
    if state == "awaiting-ruling":
        return VERB_TARGET[verb]
    if verb == "drop":
        return "dropped"
    raise CortexError(f"'{verb}' is not allowed from State: {state} "
                      f"(the table: awaiting-ruling → {VERB_TARGET[verb]})")


def rule_phase(root: Path, ref: str, verb: str, body: str, *, supersedes: "str | None" = None,
               batch: "str | None" = None, minutes: "int | None" = None,
               follow_ups: "tuple[str, ...]" = (),
               today: "date | None" = None, now: "datetime | None" = None) -> "list[str]":
    """File the ruling for one phase and update its `Ruling:` and `State:`;
    return the ruling paths written (a list of one).
    Everything is validated before anything is written."""
    today = today or date.today()
    now = now or datetime.now(timezone.utc)
    root = root.resolve()
    rulings, _ = load_rulings(root)
    by_id = {r.id: r for r in rulings}
    successors: "dict[str, list[str]]" = {}
    for r in rulings:
        if r.get("Supersedes"):
            successors.setdefault(r.get("Supersedes"), []).append(r.id)
    if batch and not (root / "batches" / f"{batch}.md").is_file():
        raise CortexError(f"--batch {batch} names no batches/{batch}.md")
    _, bad = gate_refs(", ".join(follow_ups))
    if bad:
        raise CortexError(f"--follow-up '{bad[0]}' is not Repo#N or an issue/PR URL "
                          "(create the issue first)")
    body = body.strip("\n")
    if not body.strip():
        raise CortexError("--body is empty — the human's words, verbatim")

    ph = _phase_at(root, ref)
    plan = [(ph, supersedes, _ruling_target(ph, verb, supersedes, by_id, successors))]

    taken: "set[str]" = set()
    written = []
    for ph, sup, new_state in plan:
        rid = next_ruling_id(root, today, taken)
        taken.add(rid)
        if sup and not sup < rid:
            raise CortexError(f"{sup} is not earlier than the new id {rid} (--today?)")
        path = root / "rulings" / rid[2:6] / rid[6:8] / f"{rid}.md"
        if path.exists():
            raise CortexError(f"refusing to touch an existing ruling: {path.relative_to(root)}")
        plan_item = (ph, sup, new_state, rid, path)
        written.append(plan_item)

    stamp = f"{today.isoformat()}T{now.strftime('%H:%M')}Z"
    out = []
    for ph, sup, new_state, rid, path in written:
        header = [f"Project: {ph.get('Project')}", f"Phase: {ph.rel}",
                  f"Runs: {ph.get('Runs')}" if ph.get("Runs") else "Runs:",
                  f"Ruling: {verb}"]
        if sup:
            header.append(f"Supersedes: {sup}")
        if batch:
            header.append(f"Batch: {batch}")
        header.append(f"Reviewed-at: {stamp}")
        if minutes is not None:
            header.append(f"Review-minutes-actual: {minutes}")
        if follow_ups:
            header.append(f"Follow-ups: {', '.join(follow_ups)}")
        evidence = _where_to_look(ph) or ["- (none given)"]
        text = "\n".join([f"# {rid} — {verb} {ph.get('Project')} phase {ph.get('Phase')}", ""]
                         + header + ["", "## Ruling", "", body, "", "## Evidence", ""]
                         + evidence) + "\n"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        updates: "dict[str, str | None]" = {"Ruling": rid}
        if new_state:
            updates["State"] = new_state
        line = f"{rid} — {verb}" + (f" (supersedes {sup})" if sup else "")
        ptext = append_to_section(ph.text, "Ruling", [line], replace_placeholder="(none)")
        ph.path.write_text(edit_header(ptext, updates), encoding="utf-8")
        out.append(path.relative_to(root).as_posix())
    return out


def _where_to_look(ph: Phase) -> "list[str]":
    span = sections(ph.text).get("Where to look")
    if span is None:
        return []
    lines = ph.text.split("\n")[span[0]:span[1]]
    return [ln for ln in lines if ln.startswith("- ") and ln.strip() != "-"]


def cmd_rule(args) -> int:
    body_path = Path(args.body)
    if not body_path.is_file():
        raise CortexError(f"--body {args.body} is not a file")
    paths = rule_phase(args.root, args.phase, args.verb, body_path.read_text(encoding="utf-8"),
                       supersedes=args.supersedes, batch=args.batch, minutes=args.minutes,
                       follow_ups=tuple(args.follow_up or ()), today=_today(args))
    for p in paths:
        print(f"wrote {p}")
    return 0


# --------------------------------------------------------------------------- #
# new
# --------------------------------------------------------------------------- #
def new_phase(root: Path, project: str, slug: str, number: int, *, gates: str = "",
              epic: str = "", legacy_runs: "tuple[str, ...]" = (),
              legacy_wrong: "tuple[str, ...]" = (), where: "str | None" = None,
              partition: "str | None" = None, witness: str = "", budget: str = "",
              minutes: "int | None" = None, title: "str | None" = None,
              today: "date | None" = None) -> str:
    """Write phases/<project>/<slug>.md from the template; return its rel path."""
    today = today or date.today()
    projects, problems = load_projects(root)
    if project not in projects:
        raise CortexError(f"project {project} is not a projects.yaml key"
                          + (f" ({problems[0]})" if problems else ""))
    if not SLUG_RE.match(slug):
        raise CortexError(f"slug '{slug}' must match {SLUG_RE.pattern}")
    if number < 1:
        raise CortexError("--phase must be a positive integer")
    path = root / "phases" / project / f"{slug}.md"
    if path.exists():
        raise CortexError(f"{path.relative_to(root).as_posix()} already exists")
    for existing in sorted((root / "phases" / project).glob("*.md")) if (root / "phases" / project).is_dir() else []:
        _, fields = parse_header(existing.read_text(encoding="utf-8"))
        if fields.get("Phase") == str(number):
            raise CortexError(f"phase {number} already exists: {existing.relative_to(root).as_posix()}")
    _, bad = gate_refs(gates)
    if bad:
        raise CortexError(f"--gates '{bad[0]}' is not Repo#N or an issue/PR URL (no owner/Repo#N form)")
    legacy = [(r, "legacy") for r in legacy_runs] + [(r, "legacy_wrong") for r in legacy_wrong]
    if legacy:
        if gates.strip():
            raise CortexError("a legacy-born phase cannot be gated — its runs already happened")
        if not where:
            raise CortexError("--legacy-run needs --where <quarantine path> (check requires where:)")
        for ident, _ in legacy:
            if not RUN_IDENT_RE.match(ident):
                raise CortexError(f"legacy run '{ident}' is not <stem>[_<task>|_[<set>]]")
        part = _partition_for(root, project, partition)
    if budget and not WALL_RE.match(budget):
        raise CortexError(f"--budget '{budget}' is not H+:MM")
    state = "ready" if legacy else "planned"
    stems = []
    for ident, _ in legacy:
        stem = ident.split("_")[0]
        if stem not in stems:
            stems.append(stem)
    words = slug.replace("_", " ").replace("-", " ")
    title = title or words
    header = [
        f"Project: {project}", f"Phase: {number}", f"State: {state}",
        f"Gates: {gates.strip()}" if gates.strip() else "Gates:",
        f"Witness: {witness}" if witness else "Witness:",
        f"Budget: {budget}" if budget else "Budget:",
        f"Runs: {', '.join(stems)}" if stems else "Runs:",
        "Ruling:",
        f"Review-minutes: {minutes}" if minutes is not None else "Review-minutes:",
        f"Epic: {epic}" if epic else "Epic:", f"Filed: {today.isoformat()}",
    ]
    run_lines = []
    for ident, rstate in legacy:
        run_lines.append(_run_line(ident, rstate, part, today, note="pre-Cortex run, migrated"))
        run_lines.append(f"    where: {where}")
    body = [
        f"# {project.capitalize()} — phase {number}: {title}", "",
        *header, "",
        "## Question", "", "(the question this phase answers)", "",
        "## Witness", "", witness or "(not yet registered — a planned phase may leave this empty)", "",
        # A legacy-born phase already knows where to look — `--where` is the
        # quarantine path its runs landed in, and it is required for one — so
        # the section names it rather than the placeholder `check` refuses on
        # anything past `planned`.
        "## Where to look", "",
        f"- `{where}`" if where else f"- {WHERE_PLACEHOLDER}", "",
        "## Runs", "",
    ]
    if run_lines:
        body += run_lines + [""]
    body += ["## Ruling", "", "(none)", ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(body), encoding="utf-8")
    return path.relative_to(root).as_posix()


def cmd_new(args) -> int:
    rel = new_phase(args.root, args.project, args.slug, args.phase, gates=args.gates or "",
                    epic=args.epic or "", legacy_runs=tuple(args.legacy_run or ()),
                    legacy_wrong=tuple(args.legacy_wrong or ()), where=args.where,
                    partition=args.partition, witness=args.witness or "",
                    budget=args.budget or "", minutes=args.minutes, title=args.title,
                    today=_today(args))
    print(f"wrote {rel}")
    return 0


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def _common(p: argparse.ArgumentParser, dated: bool = False) -> None:
    p.add_argument("--root", type=Path, default=ROOT,
                   help="the Cortex tree to operate on (default: this checkout)")
    if dated:
        p.add_argument("--today", help="the date to write (YYYY-MM-DD; default: today)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cortex.py", description=__doc__.split("\n\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    c = sub.add_parser("check", help="every rule in REFERENCE.md; exit 1 on drift")
    _common(c)
    c.set_defaults(func=cmd_check)

    g = sub.add_parser("gates", help="list every gated phase, its refs and their URLs")
    _common(g)
    g.set_defaults(func=cmd_gates)

    r = sub.add_parser("rule", help="file a ruling and move the phase per the table")
    _common(r, dated=True)
    r.add_argument("phase", help="phases/<project>/<slug>.md")
    r.add_argument("verb", choices=RULING_VERBS)
    r.add_argument("--body", required=True, help="file holding the human's words, verbatim")
    r.add_argument("--supersedes", help="the ruling id this one replaces (the chain head)")
    r.add_argument("--batch", help="the <YYYY-MM-DD>-<slot> the ruling was filed from")
    r.add_argument("--minutes", type=int, help="Review-minutes-actual")
    r.add_argument("--follow-up", action="append", metavar="REF",
                   help="Repo#N or an issue/PR URL; repeatable; the issue exists already")
    r.set_defaults(func=cmd_rule)

    m = sub.add_parser("move", help="one edge of the transition table")
    _common(m, dated=True)
    m.add_argument("phase", help="phases/<project>/<slug>.md")
    m.add_argument("state", help="the state to move to")
    m.add_argument("--run", metavar="ID", help="SLURM job id (<stem>[_<task>|_[<set>]]) to append")
    m.add_argument("--reason", help="why a submitted | running phase goes back to ready (Reset:)")
    m.add_argument("--partial", action="store_true",
                   help="running → pulled with a run still live (needs a leave-to-finish ruling)")
    m.add_argument("--partition", help="the run line's partition (default: the project's row)")
    m.add_argument("--after", metavar="RUN", help="afterok dependency of the appended run")
    m.add_argument("--resumes", metavar="RUN", help="the run the appended run resumes from")
    m.add_argument("--note", help="free text after the appended run line's fourth dash")
    m.add_argument("--pulled-to", metavar="PATH",
                   help="→ pulled: the laptop path written as pulled_to: on each done | legacy "
                        "run lacking one (default for a legacy run: its where:)")
    m.set_defaults(func=cmd_move)

    n = sub.add_parser("new", help="write phases/<project>/<slug>.md from the template")
    _common(n, dated=True)
    n.add_argument("project")
    n.add_argument("slug")
    n.add_argument("--phase", type=int, required=True, help="the phase number (unique per project)")
    n.add_argument("--gates", help="comma-separated Repo#N or issue/PR URLs")
    n.add_argument("--epic", help="the epic slug shared with the Mind")
    n.add_argument("--legacy-run", action="append", metavar="ID", help="a pre-Cortex run, reusable")
    n.add_argument("--legacy-wrong", action="append", metavar="ID", help="a pre-Cortex run, not reusable")
    n.add_argument("--where", help="quarantine path written to each legacy run's where:")
    n.add_argument("--partition", help="the legacy runs' partition (default: the project's row)")
    n.add_argument("--witness", help="the pre-registered checkable claim")
    n.add_argument("--budget", help="wall budget per run, H+:MM")
    n.add_argument("--minutes", type=int, help="Review-minutes seed")
    n.add_argument("--title", help="the title after `phase <n>:` (default: the slug's words)")
    n.set_defaults(func=cmd_new)

    t = sub.add_parser("retire", help="flip a project's row to status: retired")
    _common(t, dated=True)
    t.add_argument("project", help="the projects.yaml key")
    t.add_argument("--why", required=True,
                   help="one line: why the project is being retired")
    t.set_defaults(func=cmd_retire)
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.root.is_dir():
        print(f"cortex {args.command}: --root {args.root} is not a directory", file=sys.stderr)
        return 2
    try:
        return args.func(args)
    except CortexError as e:
        print(f"cortex {args.command}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
