#!/usr/bin/env python3
"""cortex.py — the Cortex's lifecycle script over one ledger per project.

The Cortex is a **history of how each science project unfolds**, not a queue
of work to finish. Every project in `projects.yaml` that is doing anything has
one file, `projects/<key>.md`, holding three things and nothing else:

    ## Now    — two or three lines, rewritten: what is running and what the
                human meant to do next. The "pick up where I left off" line.
    ## Runs   — the jobs on the cluster right now, `open` or `running`. A run
                that has finished leaves this list and becomes a log entry.
    ## Log    — dated entries, newest first: a run set off, a result the human
                noted, a lesson they stated, a thought. Nothing here is ever
                "done"; it only gets older. The board shows the last five.

Nothing in a ledger is inferred from results. A run's submission, start and
end are cluster facts and this script records them; a `result` or `lesson`
entry is the human's own words, written on their ask.

PyYAML for `projects.yaml` and otherwise stdlib only, `main(argv)`, no
import-time side effects, `--root` on every verb (default: the repo this
script lives in), so every leg runs against a `tmp_path` copy of the fixture
in tests. The date is injectable (`--today`) for the same reason.

Usage:
    python3 scripts/cortex.py check                                 # OK or DRIFT (exit 1)
    python3 scripts/cortex.py new <project> --summary "<one line>" [--issue Repo#N]
    python3 scripts/cortex.py run <project> <jobid> "<what it is>" [--partition P]
    python3 scripts/cortex.py running <project> <jobid>
    python3 scripts/cortex.py done <project> <jobid> [--failed] [--wall H:MM] [--note "..."]
    python3 scripts/cortex.py log <project> "<text>" [--kind note|result|lesson]
    python3 scripts/cortex.py now <project> "<text>"
    python3 scripts/cortex.py issue <project> [-n 5]               # the issue-top block
    python3 scripts/cortex.py link <project> <Repo#N | URL | none>  # set `Issue:`
    python3 scripts/cortex.py retire <project> --why "<one line>"   # a project's row
    python3 scripts/cortex.py sync-runs <project> --digest <digest.json> [--dry-run]

Exit codes: 0 = done · 1 = drift or a refused edit · 2 = bad arguments.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

# --------------------------------------------------------------------------- #
# vocabulary (REFERENCE.md)
# --------------------------------------------------------------------------- #
LEDGER_DIR = "projects"
SECTIONS = ("Now", "Runs", "Log")
HEADER_KEYS = ("Project", "Issue")
#: what an entry is: a run set off or finished (recorded by this script), a
#: result the human read off, a lesson they want kept, or anything else.
KINDS = ("run", "result", "lesson", "note")
#: a run on the cluster is `open` (submitted, not seen running) or `running`;
#: there is no third state — a finished run is a log entry, not a run line.
RUN_STATES = ("open", "running")
#: how many words a project's one-line summary (the title tail) may hold.
SUMMARY_MAX_WORDS = 15
#: the board's window on the log.
LOG_WINDOW = 5

PROJECT_FIELDS = ("remote", "local_path", "ral_root", "mirror", "sync_cli",
                  "sync_verbs", "ledger", "assistant", "witness_file", "partition",
                  "status")
PROJECT_OPTIONAL_FIELDS = ("note", "campaign_file", "digest")
#: the optional campaign fields: paths relative to `local_path` (or absolute).
CAMPAIGN_FIELDS = ("campaign_file", "digest")
PARTITIONS = ("gpu", "ral", "both")
PROJECT_STATUSES = ("active", "dormant", "planned", "retired")

# --------------------------------------------------------------------------- #
# grammars
# --------------------------------------------------------------------------- #
PROJECT_KEY_RE = re.compile(r"^[a-z][a-z0-9_]*$")
PROJECT_KEY_LINE_RE = re.compile(r"^([a-z][a-z0-9_]*):\s*(#.*)?$")
LEDGER_FILE_RE = re.compile(r"^projects/([a-z][a-z0-9_]*)\.md$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WALL_RE = re.compile(r"^\d+:\d{2}$")
RUN_IDENT_RE = re.compile(r"^\d+(?:_\d+|_\[\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*\])?$")
PARTITION_RE = re.compile(r"^[a-z][a-z0-9_-]*$")
#: `Repo#N` (owner PyAutoLabs), an issue URL, or `none` — the same grammar the
#: Mind uses for a GitHub ref.
ISSUE_RE = re.compile(
    r"^(?:none|(?<![\w/])[A-Za-z0-9_.-]+#\d+|"
    r"https://github\.com/[\w.-]+/[\w.-]+/issues/\d+)$")
DEFAULT_ISSUE_OWNER = "PyAutoLabs"
RUN_LINE_RE = re.compile(
    r"^- (?P<ident>\d+(?:_\d+|_\[[\d,\-]+\])?) — (?P<state>open|running) — "
    r"(?P<partition>[a-z][a-z0-9_-]*) — (?P<date>\d{4}-\d{2}-\d{2}) — (?P<what>\S.*)$")
LOG_LINE_RE = re.compile(
    r"^- (?P<date>\d{4}-\d{2}-\d{2}) — (?P<kind>run|result|lesson|note) — (?P<text>\S.*)$")
CONT_RE = re.compile(r"^  (?P<text>\S.*)$")
HEADER_KEY_RE = re.compile(r"^([A-Z][A-Za-z0-9-]*):(?:[ \t]+(.*?))?[ \t]*$")
HEADER_LINES = 12

TEMPLATE = """# {key} — {summary}

Project: {key}
Issue: {issue}

## Now

{now}

## Runs

## Log

- {today} — note — ledger opened
"""


class CortexError(Exception):
    """A refused edit or an unusable input — printed, exit 1, nothing written."""


def _dash(line: str) -> str:
    """`--` is accepted for the em dash (phone keyboards); read both as one."""
    return line.replace(" -- ", " — ")


# --------------------------------------------------------------------------- #
# the light header
# --------------------------------------------------------------------------- #
def header_span(lines: "list[str]") -> "tuple[int, int]":
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
    lines = text.split("\n")
    title = lines[0][2:].strip() if lines and lines[0].startswith("# ") else None
    fields: "dict[str, str]" = {}
    start, end = header_span(lines)
    for line in lines[start:end]:
        m = HEADER_KEY_RE.match(line)
        if m and m.group(1) not in fields:
            fields[m.group(1)] = (m.group(2) or "").strip()
    return title, fields


def sections(text: str) -> "dict[str, tuple[int, int]]":
    """{name: (first body line index, end index exclusive)} for `## name`."""
    lines = text.split("\n")
    heads = [(i, ln[3:].strip()) for i, ln in enumerate(lines) if ln.startswith("## ")]
    out = {}
    for n, (i, name) in enumerate(heads):
        stop = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
        out.setdefault(name, (i + 1, stop))
    return out


def _section_lines(text: str, name: str) -> "list[str]":
    span = sections(text).get(name)
    if span is None:
        return []
    return text.split("\n")[span[0]:span[1]]


def _replace_section(text: str, name: str, body: "list[str]") -> str:
    """Return `text` with the body of `## name` replaced by `body` (one blank
    line either side; every other byte preserved)."""
    lines = text.split("\n")
    span = sections(text).get(name)
    if span is None:
        raise CortexError(f"no `## {name}` section")
    start, stop = span
    new = [""] + body + [""]
    return "\n".join(lines[:start] + new + lines[stop:])


# --------------------------------------------------------------------------- #
# projects.yaml
# --------------------------------------------------------------------------- #
def _duplicate_key_problems(text: str) -> "list[str]":
    """`yaml.safe_load` silently keeps the last of a repeated mapping key, so a
    project row pasted twice would vanish from view: scan the raw column-0
    keys first and name every repeat with its line numbers."""
    seen: "dict[str, list[int]]" = {}
    for n, line in enumerate(text.split("\n"), 1):
        m = PROJECT_KEY_LINE_RE.match(line)
        if m:
            seen.setdefault(m.group(1), []).append(n)
    return [f"projects.yaml: duplicate project key {key!r} "
            f"(lines {', '.join(map(str, lines))})"
            for key, lines in seen.items() if len(lines) > 1]


def parse_projects(text: str) -> "tuple[dict[str, dict], list[str]]":
    problems: "list[str]" = _duplicate_key_problems(text)
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
    assistant = row.get("assistant")
    if assistant and assistant != "none" and not re.match(r"^[A-Za-z0-9_.-]+$", assistant):
        problems.append(f"projects.yaml: {key}.assistant must be 'none' or a bare "
                        f"workspace-relative directory name (got {assistant!r})")
    for f in CAMPAIGN_FIELDS:
        value = row.get(f)
        if not value:
            continue
        if ".." in Path(value).parts:
            problems.append(f"projects.yaml: {key}.{f} must not climb out with `..`")
        if f == "campaign_file" and not value.endswith((".yaml", ".yml")):
            problems.append(f"projects.yaml: {key}.campaign_file must be a .yaml file")
        if f == "digest" and Path(value).name != "digest.json":
            problems.append(f"projects.yaml: {key}.digest must name a digest.json")


def load_projects(root: Path) -> "tuple[dict[str, dict], list[str]]":
    path = root / "projects.yaml"
    if not path.is_file():
        return {}, ["projects.yaml: missing"]
    return parse_projects(path.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
# the ledger file
# --------------------------------------------------------------------------- #
class Run:
    __slots__ = ("ident", "state", "partition", "date", "what", "cont", "lineno")

    def __init__(self, m: "re.Match", lineno: int):
        self.ident = m.group("ident")
        self.state = m.group("state")
        self.partition = m.group("partition")
        self.date = m.group("date")
        self.what = m.group("what").strip()
        self.cont: "list[str]" = []
        self.lineno = lineno

    def line(self) -> str:
        return f"- {self.ident} — {self.state} — {self.partition} — {self.date} — {self.what}"

    def text(self) -> str:
        return " ".join([self.what] + self.cont)


class Entry:
    __slots__ = ("date", "kind", "text_head", "cont", "lineno")

    def __init__(self, m: "re.Match", lineno: int):
        self.date = m.group("date")
        self.kind = m.group("kind")
        self.text_head = m.group("text").strip()
        self.cont: "list[str]" = []
        self.lineno = lineno

    def text(self) -> str:
        return " ".join([self.text_head] + self.cont)

    def lines(self) -> "list[str]":
        return [f"- {self.date} — {self.kind} — {self.text_head}"] + [f"  {c}" for c in self.cont]


class Ledger:
    __slots__ = ("key", "path", "rel", "title", "summary", "header", "now",
                 "runs", "log", "problems")

    def __init__(self, key: str, path: Path, rel: str):
        self.key = key
        self.path = path
        self.rel = rel
        self.title: "str | None" = None
        self.summary = ""
        self.header: "dict[str, str]" = {}
        self.now = ""
        self.runs: "list[Run]" = []
        self.log: "list[Entry]" = []
        self.problems: "list[str]" = []

    @property
    def issue(self) -> str:
        return self.header.get("Issue", "none") or "none"

    def live(self) -> "list[Run]":
        return list(self.runs)

    def recent(self, n: int = LOG_WINDOW) -> "list[Entry]":
        return self.log[:n]

    def updated(self) -> str:
        """The newest date on the file: the head log entry, else nothing."""
        return self.log[0].date if self.log else ""


def _parse_items(lines: "list[str]", offset: int, line_re, factory, problems: "list[str]",
                 what: str) -> list:
    out = []
    for i, raw in enumerate(lines):
        if not raw.strip():
            continue
        line = _dash(raw)
        m = line_re.match(line)
        if m:
            out.append(factory(m, offset + i + 1))
            continue
        m = CONT_RE.match(raw)
        if m:
            if not out:
                problems.append(f"line {offset + i + 1}: continuation line without a {what} line")
            else:
                out[-1].cont.append(m.group("text").strip())
            continue
        problems.append(f"line {offset + i + 1}: {what} line does not parse: {raw.strip()}")
    return out


def parse_ledger(text: str, key: str, path: Path, rel: str) -> Ledger:
    led = Ledger(key, path, rel)
    lines = text.split("\n")
    led.title, led.header = parse_header(text)
    secs = sections(text)
    names = [ln[3:].strip() for ln in lines if ln.startswith("## ")]
    if names != list(SECTIONS):
        led.problems.append(f"sections must be exactly ## {' · ## '.join(SECTIONS)} in that "
                            f"order (found: {', '.join(names) or 'none'})")
    if "Now" in secs:
        a, b = secs["Now"]
        led.now = "\n".join(lines[a:b]).strip()
    if "Runs" in secs:
        a, b = secs["Runs"]
        led.runs = _parse_items(lines[a:b], a, RUN_LINE_RE, Run, led.problems, "run")
    if "Log" in secs:
        a, b = secs["Log"]
        led.log = _parse_items(lines[a:b], a, LOG_LINE_RE, Entry, led.problems, "log")
    # title: `# <key> — <summary>`
    if led.title is None:
        led.problems.append("first line must be `# <key> — <summary>`")
    else:
        m = re.match(r"^([a-z][a-z0-9_]*) — (\S.*)$", _dash(led.title))
        if not m or m.group(1) != key:
            led.problems.append(f"title must be `# {key} — <summary>`, not `# {led.title}`")
        else:
            led.summary = m.group(2).strip()
            if len(led.summary.split()) > SUMMARY_MAX_WORDS:
                led.problems.append(f"summary is over {SUMMARY_MAX_WORDS} words: {led.summary}")
    return led


def _md_files(d: Path):
    return sorted(p for p in d.glob("*.md") if p.name not in ("AGENTS.md", "TEMPLATE.md"))


def load_ledgers(root: Path) -> "tuple[list[Ledger], list[str]]":
    d = root / LEDGER_DIR
    out: "list[Ledger]" = []
    problems: "list[str]" = []
    if not d.is_dir():
        return out, problems
    for p in _md_files(d):
        rel = p.relative_to(root).as_posix()
        m = LEDGER_FILE_RE.match(rel)
        if not m:
            problems.append(f"{rel}: file name must be projects/<key>.md with a bare key")
            continue
        out.append(parse_ledger(p.read_text(encoding="utf-8"), m.group(1), p, rel))
    return out, problems


def ledger_problems(root: Path, ledgers: "list[Ledger]", projects: "dict[str, dict]") -> "list[str]":
    problems: "list[str]" = []
    seen: "set[str]" = set()
    for led in ledgers:
        seen.add(led.key)
        rel = led.rel
        problems += [f"{rel}: {p}" for p in led.problems]
        if led.key not in projects:
            problems.append(f"{rel}: {led.key} is not a projects.yaml key")
        row = projects.get(led.key, {})
        for k in HEADER_KEYS:
            if k not in led.header:
                problems.append(f"{rel}: header is missing `{k}:`")
        extra = [k for k in led.header if k not in HEADER_KEYS]
        if extra:
            problems.append(f"{rel}: unknown header key(s) {', '.join(extra)} — the header "
                            f"holds only {', '.join(HEADER_KEYS)}")
        if led.header.get("Project") not in (None, led.key):
            problems.append(f"{rel}: `Project:` must be {led.key}")
        issue = led.header.get("Issue")
        if issue is not None and not ISSUE_RE.match(issue):
            problems.append(f"{rel}: `Issue:` must be Repo#N, an issue URL or none, not {issue!r}")
        if row.get("status") == "active" and not led.now:
            problems.append(f"{rel}: `## Now` is empty on an active project")
        idents: "set[str]" = set()
        for r in led.runs:
            if r.ident in idents:
                problems.append(f"{rel}: run {r.ident} listed twice")
            idents.add(r.ident)
            if not RUN_IDENT_RE.match(r.ident):
                problems.append(f"{rel}: run ident does not parse: {r.ident}")
            problems += _date_problems(rel, r.date, f"run {r.ident}")
            if row.get("partition") not in (None, "both", r.partition):
                problems.append(f"{rel}: run {r.ident} is on `{r.partition}` but the project "
                                f"runs on `{row['partition']}`")
        prev = None
        for e in led.log:
            problems += _date_problems(rel, e.date, f"log line {e.lineno}")
            if prev is not None and e.date > prev:
                problems.append(f"{rel}: log is not newest-first at line {e.lineno} "
                                f"({e.date} after {prev})")
            prev = e.date
        if row.get("status") == "retired" and led.runs:
            problems.append(f"{rel}: a retired project still lists runs")
    for key, row in projects.items():
        if row.get("status") == "active" and key not in seen:
            problems.append(f"projects.yaml: {key} is active but has no projects/{key}.md")
    return problems


def _date_problems(rel: str, value: str, what: str) -> "list[str]":
    if not DATE_RE.match(value):
        return [f"{rel}: {what} date is not YYYY-MM-DD: {value}"]
    try:
        date.fromisoformat(value)
    except ValueError:
        return [f"{rel}: {what} date is not a real date: {value}"]
    return []


def check_problems(root: Path) -> "list[str]":
    projects, problems = load_projects(root)
    ledgers, more = load_ledgers(root)
    problems += more
    problems += ledger_problems(root, ledgers, projects)
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
# the verbs that write a ledger
# --------------------------------------------------------------------------- #
def _today(args) -> date:
    if getattr(args, "today", None):
        try:
            return date.fromisoformat(args.today)
        except ValueError:
            raise CortexError(f"--today must be YYYY-MM-DD, not {args.today}")
    return date.today()


def _ledger_at(root: Path, key: str) -> Ledger:
    if not PROJECT_KEY_RE.match(key or ""):
        raise CortexError(f"{key!r} is not a project key")
    path = root / LEDGER_DIR / f"{key}.md"
    if not path.is_file():
        raise CortexError(f"no ledger for {key} — `new {key} --summary ...` opens one")
    led = parse_ledger(path.read_text(encoding="utf-8"), key, path,
                       path.relative_to(root).as_posix())
    if led.problems:
        raise CortexError(f"{led.rel} does not parse clean — run `check` first: "
                          + "; ".join(led.problems))
    return led


def _write(led: Ledger, text: str) -> None:
    led.path.write_text(text, encoding="utf-8")
    after = parse_ledger(text, led.key, led.path, led.rel)
    if after.problems:
        raise CortexError(f"the edit would not read back: " + "; ".join(after.problems))


def _one_line(text: str, what: str) -> str:
    text = _dash((text or "").strip())
    if not text:
        raise CortexError(f"{what} must say something")
    if "\n" in text:
        raise CortexError(f"{what} is one line (continuation lines are for the file)")
    return text


def _prepend_entry(text: str, entry_line: str) -> str:
    body = _section_lines(text, "Log")
    body = [ln for ln in body if ln.strip() or True]
    stripped = [ln for ln in body]
    # drop leading/trailing blanks, then put the new entry first
    while stripped and not stripped[0].strip():
        stripped.pop(0)
    while stripped and not stripped[-1].strip():
        stripped.pop()
    return _replace_section(text, "Log", [entry_line] + stripped)


def add_entry(root: Path, key: str, kind: str, text: str, today: date) -> str:
    if kind not in KINDS:
        raise CortexError(f"--kind must be one of {', '.join(KINDS)}")
    text = _one_line(text, "the entry")
    led = _ledger_at(root, key)
    raw = led.path.read_text(encoding="utf-8")
    if led.log and today.isoformat() < led.log[0].date:
        raise CortexError(f"the log's head is {led.log[0].date}; an entry dated "
                          f"{today.isoformat()} would break newest-first")
    _write(led, _prepend_entry(raw, f"- {today.isoformat()} — {kind} — {text}"))
    return f"{led.rel}: {kind} — {text}"


def set_now(root: Path, key: str, text: str) -> str:
    text = _dash((text or "").strip())
    if not text:
        raise CortexError("`now` must say something")
    led = _ledger_at(root, key)
    raw = led.path.read_text(encoding="utf-8")
    _write(led, _replace_section(raw, "Now", text.split("\n")))
    return f"{led.rel}: now — {text.splitlines()[0]}"


def _partition_for(row: dict, given: "str | None") -> str:
    if given:
        if not PARTITION_RE.match(given):
            raise CortexError(f"--partition must be a bare word, not {given!r}")
        return given
    part = row.get("partition", "")
    if part in ("gpu", "ral"):
        return part
    raise CortexError("the project runs on both partitions — say which with --partition")


def _runs_body(runs: "list[Run]") -> "list[str]":
    out: "list[str]" = []
    for r in runs:
        out.append(r.line())
        out += [f"  {c}" for c in r.cont]
    return out


def add_run(root: Path, key: str, ident: str, what: str, today: date, *,
            partition: "str | None" = None, projects: "dict | None" = None) -> str:
    if not RUN_IDENT_RE.match(ident or ""):
        raise CortexError(f"{ident!r} is not a SLURM job id (`342301`, `342301_3`, "
                          "`342301_[0-9]`)")
    what = _one_line(what, "what the run is")
    led = _ledger_at(root, key)
    if any(r.ident == ident for r in led.runs):
        raise CortexError(f"{ident} is already listed under ## Runs")
    rows = projects if projects is not None else load_projects(root)[0]
    part = _partition_for(rows.get(key, {}), partition)
    raw = led.path.read_text(encoding="utf-8")
    line = f"- {ident} — open — {part} — {today.isoformat()} — {what}"
    text = _replace_section(raw, "Runs", _runs_body(led.runs) + [line])
    text = _prepend_entry(text, f"- {today.isoformat()} — run — {ident} submitted: {what}")
    _write(led, text)
    return f"{led.rel}: run {ident} open"


def _run_at(led: Ledger, ident: str) -> Run:
    for r in led.runs:
        if r.ident == ident:
            return r
    raise CortexError(f"{ident} is not under ## Runs of {led.rel} "
                      f"({', '.join(r.ident for r in led.runs) or 'no runs'})")


def set_running(root: Path, key: str, ident: str) -> str:
    led = _ledger_at(root, key)
    run = _run_at(led, ident)
    if run.state == "running":
        return f"{led.rel}: run {ident} already running"
    run.state = "running"
    raw = led.path.read_text(encoding="utf-8")
    _write(led, _replace_section(raw, "Runs", _runs_body(led.runs)))
    return f"{led.rel}: run {ident} running"


def finish_run(root: Path, key: str, ident: str, today: date, *, failed: bool = False,
               wall: "str | None" = None, note: str = "") -> str:
    if wall and not WALL_RE.match(wall):
        raise CortexError(f"--wall must be H:MM, not {wall!r}")
    led = _ledger_at(root, key)
    run = _run_at(led, ident)
    verb = "failed" if failed else "finished"
    bits = [f"{ident} {verb}"]
    if wall:
        bits.append(f"wall {wall}")
    text = " — ".join(bits) + f": {run.what}"
    if note:
        text += f" — {_one_line(note, '--note')}"
    remaining = [r for r in led.runs if r.ident != ident]
    raw = led.path.read_text(encoding="utf-8")
    out = _replace_section(raw, "Runs", _runs_body(remaining))
    out = _prepend_entry(out, f"- {today.isoformat()} — run — {text}")
    _write(led, out)
    return f"{led.rel}: run {ident} {verb}"


def new_ledger(root: Path, key: str, summary: str, today: date, *, issue: str = "none",
               now: str = "") -> str:
    projects, problems = load_projects(root)
    if problems:
        raise CortexError("projects.yaml does not parse clean — run `check` first: "
                          + "; ".join(problems))
    if key not in projects:
        raise CortexError(f"{key} is not a projects.yaml key — add its row first "
                          "(projects.yaml is code: a human's turn)")
    summary = _one_line(summary, "--summary")
    if len(summary.split()) > SUMMARY_MAX_WORDS:
        raise CortexError(f"--summary is over {SUMMARY_MAX_WORDS} words")
    issue = (issue or "none").strip()
    if not ISSUE_RE.match(issue):
        raise CortexError(f"--issue must be Repo#N, an issue URL or none, not {issue!r}")
    path = root / LEDGER_DIR / f"{key}.md"
    if path.exists():
        raise CortexError(f"{path.relative_to(root).as_posix()} already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    now = _dash((now or "").strip()) or "Just opened — nothing submitted yet."
    path.write_text(TEMPLATE.format(key=key, summary=summary, issue=issue, now=now,
                                    today=today.isoformat()), encoding="utf-8")
    return f"opened {path.relative_to(root).as_posix()}"


# --------------------------------------------------------------------------- #
# the issue-top block
# --------------------------------------------------------------------------- #
ISSUE_BEGIN = "<!-- cortex:ledger begin — regenerated from projects/{key}.md; edit there -->"
ISSUE_END = "<!-- cortex:ledger end -->"


def issue_url(ref: str) -> str:
    if ref.startswith("https://"):
        return ref
    repo, _, n = ref.partition("#")
    return f"https://github.com/{DEFAULT_ISSUE_OWNER}/{repo}/issues/{n}"


def issue_block(led: Ledger, row: dict, n: int = LOG_WINDOW, home: str = "") -> str:
    """The concise, human-readable ledger that sits at the top of a project's
    issue: Now, the runs on the cluster, the last `n` entries. Markdown, fenced
    by the two markers so a re-sync replaces exactly this block."""
    link = f"{home}/blob/main/{led.rel}" if home else led.rel
    out = [ISSUE_BEGIN.format(key=led.key),
           f"**{led.key}** — {led.summary}  ",
           f"_{row.get('status', '?')} · ledger: [{led.rel}]({link})"
           + (f" · updated {led.updated()}" if led.updated() else "") + "_",
           "", "**Now**", "", led.now or "_(nothing yet)_", "", "**Runs**", ""]
    if led.runs:
        out += [f"- `{r.ident}` — {r.state} — {r.partition} — {r.date} — {r.text()}"
                for r in led.runs]
    else:
        out.append("_nothing on the cluster_")
    out += ["", f"**Last {n}**", ""]
    out += [f"- {e.date} — *{e.kind}* — {e.text()}" for e in led.recent(n)] or ["_empty_"]
    out.append(ISSUE_END)
    return "\n".join(out) + "\n"


def link_issue(root: Path, key: str, ref: str) -> str:
    """Set the ledger's `Issue:` — the one header edit there is. `none` unlinks."""
    ref = (ref or "").strip()
    if not ISSUE_RE.match(ref):
        raise CortexError(f"the ref must be Repo#N, an issue URL or none, not {ref!r}")
    led = _ledger_at(root, key)
    raw = led.path.read_text(encoding="utf-8")
    lines = raw.split("\n")
    start, end = header_span(lines)
    at = [i for i in range(start, end) if lines[i].startswith("Issue:")]
    if len(at) != 1:
        raise CortexError(f"{led.rel}: expected one `Issue:` header line, found {len(at)}")
    lines[at[0]] = f"Issue: {ref}"
    _write(led, "\n".join(lines))
    return f"{led.rel}: issue {ref}"


def cmd_link(args) -> int:
    print(link_issue(args.root, args.project, args.ref))
    return 0


def cmd_issue(args) -> int:
    led = _ledger_at(args.root, args.project)
    projects, _ = load_projects(args.root)
    print(issue_block(led, projects.get(args.project, {}), args.n), end="")
    return 0


# --------------------------------------------------------------------------- #
# retire
# --------------------------------------------------------------------------- #
def retire_project(root: Path, key: str, why: str, today: date) -> str:
    """Flip one `projects.yaml` row to `status: retired` and stamp the reason
    on its `note:`. With `birth`, the only verbs that write `projects.yaml`. It does not
    delete the row (it is the one record of where the data lives), it does not
    touch the ledger file (history is not rewritten by a change of status), and
    it refuses while the ledger still lists a run on the cluster."""
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
    path_led = root / LEDGER_DIR / f"{key}.md"
    if path_led.is_file():
        led = parse_ledger(path_led.read_text(encoding="utf-8"), key, path_led,
                           path_led.relative_to(root).as_posix())
        if led.runs:
            raise CortexError(f"{key} still lists runs on the cluster — `done` them "
                              f"first: {', '.join(r.ident for r in led.runs)}")

    path = root / "projects.yaml"
    original = path.read_text(encoding="utf-8")
    lines = original.split("\n")
    starts = [i for i, ln in enumerate(lines) if ln == f"{key}:"]
    if len(starts) != 1:
        raise CortexError(f"projects.yaml: expected one `{key}:` line, found {len(starts)}")
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
    if path_led.is_file():
        add_entry(root, key, "note", f"retired: {why}", today)
    return f"retired {key}"


def _yaml_scalar(field: str, value: str) -> str:
    """A `projects.yaml` scalar: bare, or `"..."` (no escapes) when it holds
    `#`, `:` or edge spaces. A double quote, a backslash (YAML would read it
    as an escape inside quotes) or a newline cannot be written."""
    value = str(value)
    if '"' in value or "\\" in value or "\n" in value:
        raise CortexError(f"{field} cannot hold a double quote, a backslash or a "
                          "newline (projects.yaml quotes with no escapes)")
    if not value.strip():
        raise CortexError(f"{field} is empty")
    if "#" in value or ":" in value or value != value.strip():
        return f'"{value}"'
    return value


def birth_project(root: Path, key: str, row: dict, summary: str, today: date, *,
                  issue: str = "none", now: str = "") -> str:
    """Append one `projects.yaml` row and open its ledger — a project birth.

    The second verb that writes `projects.yaml` (with `retire`), and the only
    one that adds a row. It refuses a key or a `local_path` already in the
    map, writes the row in `PROJECT_FIELDS` order at the end of the file,
    reads the file back and restores it on any problem, then opens the ledger
    with `new_ledger`. The diff is add-only — a row plus its ledger — which
    `ledger_merge.py` classifies as a birth, so it lands by itself."""
    if not PROJECT_KEY_RE.match(key or ""):
        raise CortexError(f"{key!r} is not a project key (^[a-z][a-z0-9_]*$)")
    projects, problems = load_projects(root)
    if problems:
        raise CortexError("projects.yaml does not parse clean — run `check` "
                          "and fix it before a birth: " + "; ".join(problems))
    if key in projects:
        raise CortexError(f"{key} is already a projects.yaml key")
    unknown = set(row) - set(PROJECT_FIELDS + PROJECT_OPTIONAL_FIELDS)
    missing = [f for f in PROJECT_FIELDS if not row.get(f)]
    if unknown or missing:
        raise CortexError("a birth row needs every field and no others — "
                          + "; ".join([f"missing {', '.join(missing)}"] * bool(missing)
                                      + [f"unknown {', '.join(sorted(unknown))}"] * bool(unknown)))
    local = row["local_path"].rstrip("/")
    for other, r in projects.items():
        if (r.get("local_path") or "").rstrip("/") == local:
            raise CortexError(f"{local} is already the local_path of {other}")
    if (root / LEDGER_DIR / f"{key}.md").exists():
        raise CortexError(f"{LEDGER_DIR}/{key}.md already exists")

    lines = [f"{key}:"]
    for field in PROJECT_FIELDS + PROJECT_OPTIONAL_FIELDS:
        if field not in row:
            continue
        value = row[field]
        if field == "sync_verbs":
            verbs = list(value)
            if not verbs or not all(re.match(r"^[a-z][a-z0-9-]*$", v) for v in verbs):
                raise CortexError(f"sync_verbs must be bare words, not {verbs!r}")
            lines.append(f"  sync_verbs: [{', '.join(verbs)}]")
        else:
            lines.append(f"  {field}: {_yaml_scalar(field, value)}")

    path = root / "projects.yaml"
    original = path.read_text(encoding="utf-8")
    path.write_text(original.rstrip("\n") + "\n\n" + "\n".join(lines) + "\n",
                    encoding="utf-8")
    rows, problems = load_projects(root)
    back = rows.get(key, {})
    differs = [f for f in row if (back.get(f) != list(row[f]) if f == "sync_verbs"
                                  else back.get(f) != str(row[f]))]
    if problems or not back or differs:
        path.write_text(original, encoding="utf-8")
        if problems:
            why = "; ".join(problems)
        elif not back:
            why = f"{key} is missing"
        else:
            why = f"{key} came back with {', '.join(differs)} changed"
        raise CortexError("the row would not read back as written — projects.yaml "
                          f"is unchanged: {why}")
    try:
        new_ledger(root, key, summary, today, issue=issue, now=now)
    except CortexError:
        path.write_text(original, encoding="utf-8")
        raise
    return f"born {key}: projects.yaml row + {LEDGER_DIR}/{key}.md"


# --------------------------------------------------------------------------- #
# sync-runs: run status from a campaign digest (schema decision 64)
# --------------------------------------------------------------------------- #
DIGEST_SCHEMA = 1
#: a task's state in `tasks.jsonl` (PyAutoFit `autofit.campaign`) that ends it.
TERMINAL_TASK_STATES = ("completed", "failed", "timeout", "oom", "node_fail",
                        "cancelled", "preempted")
#: states that say a task has begun on the cluster (or already ended).
STARTED_TASK_STATES = ("running", "timeout_pending") + TERMINAL_TASK_STATES


def _task_set(ident: str) -> "tuple[str, set[int] | None]":
    """The job id and the array indices a run ident names (None = every task)."""
    m = re.match(r"^(\d+)(?:_(\d+)|_\[([\d,\-]+)\])?$", ident)
    if not m:
        raise CortexError(f"run ident does not parse: {ident}")
    job, one, many = m.groups()
    if one is not None:
        return job, {int(one)}
    if many is None:
        return job, None
    out: "set[int]" = set()
    for part in many.split(","):
        lo, _, hi = part.partition("-")
        out.update(range(int(lo), int(hi or lo) + 1))
    return job, out


def read_digest(path: Path) -> "tuple[dict, list[dict]]":
    """`digest.json` and the `tasks.jsonl` beside it; a CortexError if either is
    missing or malformed. `path` may be the file or its folder."""
    path = Path(path)
    if path.is_dir():
        path = path / "digest.json"
    try:
        digest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise CortexError(f"{path}: not a readable digest ({e})")
    if not isinstance(digest, dict) or digest.get("schema") != DIGEST_SCHEMA:
        raise CortexError(f"{path}: not a schema-{DIGEST_SCHEMA} campaign digest")
    tasks_path = path.with_name("tasks.jsonl")
    tasks: "list[dict]" = []
    try:
        lines = tasks_path.read_text(encoding="utf-8").splitlines()
    except OSError as e:
        raise CortexError(f"{tasks_path}: missing beside the digest ({e})")
    for n, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError:
            raise CortexError(f"{tasks_path}:{n}: not JSON")
        if not isinstance(row, dict) or "state" not in row:
            raise CortexError(f"{tasks_path}:{n}: a task row needs a state")
        tasks.append(row)
    return digest, tasks


def _tasks_of(ident: str, tasks: "list[dict]") -> "list[dict]":
    job, wanted = _task_set(ident)
    out = []
    for t in tasks:
        if str(t.get("job_id")) != job:
            continue
        if wanted is not None:
            key = str(t.get("key", ""))
            suffix = key.rpartition("_")[2]
            if not suffix.isdigit() or int(suffix) not in wanted:
                continue
        out.append(t)
    return out


def _wall(tasks: "list[dict]") -> "str | None":
    """H:MM from the first task start to the last task end, when both are known."""
    try:
        starts = [datetime.fromisoformat(t["start"]) for t in tasks if t.get("start")]
        ends = [datetime.fromisoformat(t["end"]) for t in tasks if t.get("end")]
    except (TypeError, ValueError):
        return None
    if not starts or not ends:
        return None
    seconds = max(0, int((max(ends) - min(starts)).total_seconds()))
    return f"{seconds // 3600}:{seconds % 3600 // 60:02d}"


def _counts(tasks: "list[dict]") -> str:
    from collections import Counter
    c = Counter(str(t["state"]) for t in tasks)
    return ", ".join(f"{n} {s}" for s, n in sorted(c.items(), key=lambda x: (-x[1], x[0])))


def _digest_path(root: Path, key: str, given: "str | None") -> Path:
    if given:
        return Path(given)
    rows, _ = load_projects(root)
    row = rows.get(key, {})
    if not row.get("digest"):
        raise CortexError(f"give --digest, or set {key}.digest in projects.yaml")
    p = Path(row["digest"])
    return p if p.is_absolute() else Path(row.get("local_path", "")) / p


def sync_runs(root: Path, key: str, digest_path: Path, today: date, *,
              dry_run: bool = False) -> "list[str]":
    """Bring `## Runs` in line with a campaign digest — cluster facts only.

    A run line is matched to the digest's tasks by its SLURM job id (the array
    job), narrowed to the array indices its ident names (`3002_[0-3]`). An `open`
    run with a task that has started becomes `running` (with a `run` entry); a run
    whose matched tasks have all ended goes through `done`, with the task counts
    as its note and `--failed` when none completed. Nothing else is written:
    never a `result` or `lesson`, never `## Now`. Returns the lines to print, the
    first `sync-runs: <project>: <n> changed`."""
    digest, tasks = read_digest(digest_path)
    led = _ledger_at(root, key)
    campaign = digest.get("campaign") or "?"
    source = f"digest {campaign} updated {digest.get('updated') or '?'}"
    changes: "list[str]" = []
    notes: "list[str]" = []
    seen_jobs: "set[str]" = set()
    for run in list(led.runs):
        matched = _tasks_of(run.ident, tasks)
        seen_jobs.add(_task_set(run.ident)[0])
        if not matched:
            notes.append(f"  {run.ident}: not in the digest — unchanged")
            continue
        states = [str(t["state"]) for t in matched]
        if all(s in TERMINAL_TASK_STATES for s in states):
            completed = states.count("completed")
            failed = completed == 0
            note = f"{_counts(matched)} ({source})"
            changes.append(f"  {run.ident}: done — {'failed' if failed else 'finished'}: "
                           f"{_counts(matched)}")
            if not dry_run:
                finish_run(root, key, run.ident, today, failed=failed,
                           wall=_wall(matched), note=note)
        elif run.state == "open" and any(s in STARTED_TASK_STATES for s in states):
            changes.append(f"  {run.ident}: open → running ({_counts(matched)})")
            if not dry_run:
                set_running(root, key, run.ident)
                current = _ledger_at(root, key)
                raw = current.path.read_text(encoding="utf-8")
                _write(current, _prepend_entry(
                    raw, f"- {today.isoformat()} — run — {run.ident} running: {run.what} "
                         f"— {_counts(matched)} ({source})"))
    unknown = sorted({str(t.get("job_id")) for t in tasks
                      if t.get("job_id") and str(t.get("job_id")) not in seen_jobs})
    if unknown:
        shown = ", ".join(unknown[:8]) + (f" … (+{len(unknown) - 8})" if len(unknown) > 8 else "")
        notes.append(f"  {len(unknown)} digest job(s) are not runs in {led.rel} "
                     f"and were ignored: {shown}")
    head = f"sync-runs: {key}: {len(changes)} changed" + (" (dry run)" if dry_run else "")
    return [head] + changes + notes


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def cmd_new(args) -> int:
    print(new_ledger(args.root, args.project, args.summary, _today(args),
                     issue=args.issue, now=args.now or ""))
    return 0


def cmd_run(args) -> int:
    print(add_run(args.root, args.project, args.jobid, args.what, _today(args),
                  partition=args.partition))
    return 0


def cmd_running(args) -> int:
    print(set_running(args.root, args.project, args.jobid))
    return 0


def cmd_done(args) -> int:
    print(finish_run(args.root, args.project, args.jobid, _today(args),
                     failed=args.failed, wall=args.wall, note=args.note or ""))
    return 0


def cmd_log(args) -> int:
    print(add_entry(args.root, args.project, args.kind, args.text, _today(args)))
    return 0


def cmd_now(args) -> int:
    print(set_now(args.root, args.project, args.text))
    return 0


def cmd_birth(args) -> int:
    row = {
        "remote": args.remote, "local_path": args.local_path, "ral_root": args.ral_root,
        "mirror": args.mirror, "sync_cli": args.sync_cli,
        "sync_verbs": [v.strip() for v in args.sync_verbs.split(",") if v.strip()],
        "ledger": args.ledger, "assistant": args.assistant,
        "witness_file": args.witness_file, "partition": args.partition,
        "status": args.status,
    }
    if args.note:
        row["note"] = args.note
    print(birth_project(args.root, args.project, row, args.summary, _today(args),
                        issue=args.issue, now=args.now or ""))
    return 0


def cmd_sync_runs(args) -> int:
    path = _digest_path(args.root, args.project, args.digest)
    for line in sync_runs(args.root, args.project, path, _today(args), dry_run=args.dry_run):
        print(line)
    return 0


def cmd_retire(args) -> int:
    print(retire_project(args.root, args.project, args.why, _today(args)))
    return 0


def _common(p: argparse.ArgumentParser, dated: bool = False) -> None:
    p.add_argument("--root", type=Path, default=ROOT,
                   help="the Cortex tree to operate on (default: this checkout)")
    if dated:
        p.add_argument("--today", help="the date to write (YYYY-MM-DD; default: today)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cortex", description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("check", help="every structural rule; OK or DRIFT")
    _common(p)
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("new", help="open a project's ledger")
    p.add_argument("project")
    p.add_argument("--summary", required=True, help=f"one line, at most {SUMMARY_MAX_WORDS} words")
    p.add_argument("--issue", default="none", help="Repo#N or an issue URL (default none)")
    p.add_argument("--now", help="the opening `## Now` text")
    _common(p, dated=True)
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("run", help="record a submission: the run goes under ## Runs as open")
    p.add_argument("project")
    p.add_argument("jobid")
    p.add_argument("what", help="what the run is, one line")
    p.add_argument("--partition", help="gpu | ral (needed when the project runs on both)")
    _common(p, dated=True)
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("running", help="a run has started on the cluster")
    p.add_argument("project")
    p.add_argument("jobid")
    _common(p)
    p.set_defaults(func=cmd_running)

    p = sub.add_parser("done", help="a run has finished: it leaves ## Runs and enters the log")
    p.add_argument("project")
    p.add_argument("jobid")
    p.add_argument("--failed", action="store_true")
    p.add_argument("--wall", help="H:MM")
    p.add_argument("--note", help="one line to carry into the entry")
    _common(p, dated=True)
    p.set_defaults(func=cmd_done)

    p = sub.add_parser("log", help="write a dated entry in the human's words")
    p.add_argument("project")
    p.add_argument("text")
    p.add_argument("--kind", default="note", choices=KINDS)
    _common(p, dated=True)
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("now", help="rewrite ## Now")
    p.add_argument("project")
    p.add_argument("text")
    _common(p)
    p.set_defaults(func=cmd_now)

    p = sub.add_parser("issue", help="print the block that sits at the top of the project's issue")
    p.add_argument("project")
    p.add_argument("-n", type=int, default=LOG_WINDOW)
    _common(p)
    p.set_defaults(func=cmd_issue)

    p = sub.add_parser("link", help="set the ledger's `Issue:` (Repo#N, an issue URL, or none)")
    p.add_argument("project")
    p.add_argument("ref")
    _common(p)
    p.set_defaults(func=cmd_link)

    p = sub.add_parser("birth", help="add a project's row and open its ledger (a birth; "
                                     "lands by itself)")
    p.add_argument("project")
    p.add_argument("--local-path", required=True)
    p.add_argument("--ral-root", required=True)
    p.add_argument("--remote", default="none")
    p.add_argument("--mirror", default="none")
    p.add_argument("--sync-cli", default="hpc/sync")
    p.add_argument("--sync-verbs", required=True, help="comma-separated")
    p.add_argument("--ledger", default="wiki/project/state.md")
    p.add_argument("--assistant", default="none")
    p.add_argument("--witness-file", default="results/**/*.json")
    p.add_argument("--partition", default="ral", choices=PARTITIONS)
    p.add_argument("--status", default="active", choices=PROJECT_STATUSES)
    p.add_argument("--note")
    p.add_argument("--summary", required=True, help=f"one line, at most {SUMMARY_MAX_WORDS} words")
    p.add_argument("--issue", default="none", help="Repo#N or an issue URL (default none)")
    p.add_argument("--now", help="the opening `## Now` text")
    _common(p, dated=True)
    p.set_defaults(func=cmd_birth)

    p = sub.add_parser("sync-runs", help="flip run lines from a campaign digest "
                                         "(open → running, done with counts)")
    p.add_argument("project")
    p.add_argument("--digest", help="digest.json (or its folder); default the row's `digest`")
    p.add_argument("--dry-run", action="store_true", help="print what would change; write nothing")
    _common(p, dated=True)
    p.set_defaults(func=cmd_sync_runs)

    p = sub.add_parser("retire", help="retire a project's row (with `birth`, the only verbs "
                                      "that write projects.yaml)")
    p.add_argument("project")
    p.add_argument("--why", required=True)
    _common(p, dated=True)
    p.set_defaults(func=cmd_retire)
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
