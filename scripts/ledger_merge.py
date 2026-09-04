#!/usr/bin/env python3
"""Classify a PyAutoCortex branch diff as *ledger* or *code*.

WHY THIS EXISTS. The Cortex's own work strands exactly as the Mind's does. A
branch-scoped session (the phone, claude.ai/code, any `claude/**` flow) pushes
a phase move, a ruling, a batch record to a feature branch and nothing moves
it: no workflow looks at a `claude/**` push. The branch sits there until a
human writes an explicit "merge this" prompt.

Almost all of what strands is *ledger*: a phase file under `phases/`, a ruling
under `rulings/`, a batch record or review under `batches/`, an epic entry.
It is the organism's own bookkeeping, it is template-shaped, its drift check
(`cortex.py check`) is already automated, and a human reviewing it adds
nothing. The minority that is *code* — `scripts/`, `tests/`, `.github/`,
`policy/`, `docs/`, `projects.yaml`, the prose pages — is exactly what review
is for.

So this script draws that line, and `ledger_merge.yml` merges only what falls
on the ledger side of it. The gate is a script, not workflow YAML, so it is
testable and so a session can predict the verdict before it pushes.

DEFAULT DENY. A path is ledger only by matching a rule below; an unrecognised
one — a new root file, a new top-level folder — is code. Getting that backwards
would auto-merge the next thing nobody thought about.

APPEND-ONLY. `rulings/` is the ledger of record and a ruling, once committed,
is never modified or deleted (rulings/AGENTS.md). When the diff comes from git
(`--base`), the classifier reads `git diff --name-status` and any entry under
`rulings/**` whose status is not `A` (added) — `M`, `D`, `R*`, or anything
else — is code, which leaves the branch for a human. Explicit-path and stdin
inputs carry no status and stay path-only, as in the Mind.

Usage:
    python3 scripts/ledger_merge.py classify --base origin/main   # diff HEAD vs base
    python3 scripts/ledger_merge.py classify path/one path/two    # explicit paths
    ... < paths-on-stdin

Exit codes: 0 = ledger-only (safe to auto-merge) · 1 = holds code (a human's
call) · 2 = the script could not run. The caller must distinguish 1 from 2:
"a human should look" and "the gate is broken" are not the same answer.
"""

from __future__ import annotations

import argparse
import fnmatch
import subprocess
import sys
from pathlib import Path

# Directories holding nothing but the run-and-ruling ledger: phase files,
# rulings of record, and the batch records and reviews kept as history. Their
# whole contents are ledger (subject to the EXCLUDED_NAMES guard below, and to
# the append-only leg for rulings/ and batches/ in classify_entries).
LEDGER_DIRS = ("phases/", "rulings/", "batches/")

# Root files that are ledger state. Deliberately NOT here: README.md,
# AGENTS.md, CLAUDE.md, REFERENCE.md — prose a human reads, changed rarely
# and on purpose — and projects.yaml, which is CODE: `sync_cli` and
# `local_path` are paths the batch conductor executes under, worse than the
# Mind's repos.yaml, which is already on the human side of its line.
#
# `dashboard.md` / `dashboard.html` join it as GENERATED ledger: the cortex
# conductor renders them from the registry, `dashboard_refresh.yml` self-heals
# them on main, and a branch that moves a phase re-renders them in the same
# push. If they were code, every ordinary ledger branch would stop for a human
# on two files nobody wrote by hand.
LEDGER_FILES = ("epics.md", "dashboard.md", "dashboard.html")

# Names that are ledger by location but must not ride along, for two different
# reasons.
#
# EXECUTABLE BY COLLECTION: a file pytest would *collect* runs in CI from
# anywhere in the tree, so it is code wherever it sits — a `test_*.py` dropped
# beside a batch record included.
#
# INSTRUCTIONAL BY CONTENT: `AGENTS.md` and `TEMPLATE.md` under a ledger dir
# (`rulings/AGENTS.md`, `batches/AGENTS.md`, `batches/reviews/AGENTS.md`) are
# not entries in the ledger — they are the doctrine that says what an entry may be, and the
# template every future entry is stamped from. They are read by agents as
# instructions, so a change to one is a change to behaviour: it needs a human,
# exactly as `scripts/` does. Auto-merging a rewrite of `rulings/AGENTS.md`
# would let a branch edit the rule that governs its own merge.
EXCLUDED_NAMES = ("conftest.py", "test_*.py", "*_test.py", "AGENTS.md", "TEMPLATE.md")


def is_ledger_path(path: str) -> bool:
    """True if `path` (repo-relative, POSIX separators) is ledger material."""
    # Normalise away "./" and any "..", so a traversal cannot smuggle a code
    # path in behind a ledger prefix.
    parts = [p for p in path.replace("\\", "/").split("/") if p not in ("", ".")]
    if not parts or ".." in parts:
        return False
    # A dot-directory or dot-file anywhere is never ledger: `.github/`,
    # `.claude/`, `.codex/`, `.gitignore` all carry behaviour.
    if any(p.startswith(".") for p in parts):
        return False
    name = parts[-1]
    if any(fnmatch.fnmatch(name, pattern) for pattern in EXCLUDED_NAMES):
        return False
    normalised = "/".join(parts)
    if len(parts) == 1:
        return normalised in LEDGER_FILES
    return any(normalised.startswith(d) for d in LEDGER_DIRS)


def classify(paths):
    """Split `paths` into (ledger, blocked), preserving order and dropping dupes."""
    ledger, blocked, seen = [], [], set()
    for path in paths:
        path = path.strip()
        if not path or path in seen:
            continue
        seen.add(path)
        (ledger if is_ledger_path(path) else blocked).append(path)
    return ledger, blocked


# The dirs where a change's KIND matters, not only its path: the ledger of
# record is append-only, so only an added file under one is ledger.
# `batches/` joined `rulings/` on 2026-09-03, when the review-slot apparatus
# was retired: the batch records and the human's verbatim reviews stay as
# history — never modified, only added — and 13 rulings cite them.
APPEND_ONLY_DIRS = ("rulings/", "batches/")


def is_append_only_violation(status: str, path: str) -> bool:
    """True if a `git diff --name-status` entry edits, deletes, renames (or
    does anything but add) a file under an append-only dir."""
    parts = [p for p in path.replace("\\", "/").split("/") if p not in ("", ".")]
    normalised = "/".join(parts)
    return status[:1] != "A" and any(normalised.startswith(d) for d in APPEND_ONLY_DIRS)


def classify_entries(entries):
    """Split `(status, path)` entries into (ledger, blocked) paths.

    A path is blocked if it is not ledger material, or if it is a non-`A`
    entry under an append-only dir (`rulings/`, `batches/` — an edited,
    deleted or renamed ruling, batch record or review). A rename entry
    carries both paths; the old one counts as a deletion."""
    ledger, blocked, seen = [], [], set()
    for status, path in entries:
        path = path.strip()
        if not path or path in seen:
            continue
        seen.add(path)
        if is_ledger_path(path) and not is_append_only_violation(status, path):
            ledger.append(path)
        else:
            blocked.append(path)
    return ledger, blocked


def changed_entries(base: str, head: str = "HEAD", cwd=None):
    """`(status, path)` entries changed by `head` relative to its merge base
    with `base` — `git diff --name-status`. A rename yields two entries, the
    old path as `D` and the new as `R`, so both sides are judged.

    Three-dot: a branch that merged main into itself must be judged on what it
    *adds*, not on everything main moved underneath it, or every long-running
    branch reads as code the moment someone else touches `scripts/`.
    """
    proc = subprocess.run(
        ["git", "diff", "--name-status", f"{base}...{head}"],
        capture_output=True,
        text=True,
        cwd=cwd or Path(__file__).resolve().parents[1],
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise SystemExit(2)
    entries = []
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        fields = line.split("\t")
        status = fields[0].strip()
        if status[:1] in ("R", "C") and len(fields) >= 3:
            if status[:1] == "R":
                entries.append(("D", fields[1]))
            entries.append((status, fields[2]))
        elif len(fields) >= 2:
            entries.append((status, fields[1]))
    return entries


def changed_paths(base: str, head: str = "HEAD", cwd=None):
    """Paths changed by `head` relative to its merge base with `base`."""
    return [path for _, path in changed_entries(base, head, cwd)]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    cls = sub.add_parser("classify", help="ledger-only, or does it hold code?")
    cls.add_argument("paths", nargs="*", help="repo-relative paths (else stdin, else --base)")
    cls.add_argument("--base", help="diff HEAD against the merge base with this ref")
    cls.add_argument("--head", default="HEAD", help="the branch tip to judge (default HEAD)")
    args = parser.parse_args(argv)

    if args.paths:
        paths = args.paths
    elif not sys.stdin.isatty():
        paths = sys.stdin.read().splitlines()
    elif args.base:
        paths = []
    else:
        parser.error("give paths, pipe them in, or pass --base")
        return 2
    # Strip blanks BEFORE the emptiness check, not inside classify(): a stdin
    # of "\n" is one empty string, which is a truthy list, and an unfiltered
    # check would call that "0 ledger paths" and exit 0 — fail-open, on the one
    # question this gate exists to answer.
    paths = [p.strip() for p in paths if p.strip()]
    entries = None
    if args.base and not paths:
        entries = changed_entries(args.base, args.head)
        paths = [path for _, path in entries]

    if not paths:
        # Nothing changed is not "safe to merge" — there is nothing to merge,
        # and the caller must not read exit 0 as "go". Say so and block.
        print("no changed paths — nothing to merge")
        return 1

    # Explicit paths and stdin carry no status, so they are judged on the path
    # alone; a git diff also carries the append-only leg for rulings/.
    ledger, blocked = classify_entries(entries) if entries is not None else classify(paths)
    if blocked:
        print(f"code: {len(blocked)} of {len(ledger) + len(blocked)} path(s) need a human")
        for path in blocked:
            print(f"  {path}")
        return 1
    print(f"ledger-only: {len(ledger)} path(s)")
    for path in ledger:
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
