"""Contract tests for `cortex.py library` (schema decision 65): one fact-only
`library` entry naming the PyAutoFit results index a library was built from —
its hash and its state counts, read from the index files, nothing else.

The index fixtures are written per test in the shape `autofit.results.ResultsIndex`
writes them: `index.json` (schema 1) and `records/<sha1>.json`, one
`ResultRecord` dict per result. Where autofit is importable, the hash is also
checked against `autofit.export.index_hash` on an index autofit built itself.
"""

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import cortex  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "cortex.py"
SKELETON = REPO / "tests" / "fixtures" / "skeleton"
TODAY = "2026-09-03"
EX = "projects/example.md"


def _copy(tmp_path: Path) -> Path:
    root = tmp_path / "tree"
    shutil.copytree(SKELETON, root)
    return root


def _record(output_path, state, completed_at=None, **extra):
    rec = {"output_path": output_path, "root": "/results", "state": state,
           "completed_at": completed_at, "schema": 1}
    rec.update(extra)
    return rec


def _index(tmp_path: Path, records, name="dr1_index", manifest_schema=1) -> Path:
    d = tmp_path / name
    (d / "records").mkdir(parents=True)
    (d / "index.json").write_text(json.dumps(
        {"schema": manifest_schema, "roots": ["/results"], "updated": "2026-09-03T08:00:00Z",
         "latest_key": ["path_prefix", "name", "unique_tag"], "counts": {}}))
    for rec in records:
        key = hashlib.sha1(rec["output_path"].encode("utf-8")).hexdigest()
        (d / "records" / f"{key}.json").write_text(json.dumps(rec, indent=1))
    return d


RECORDS = [
    _record("/results/lens_c/abc", "failed"),
    _record("/results/lens_a/abc", "completed", "2026-09-01T10:00:00+00:00"),
    _record("/results/lens_b/abc", "superseded", "2026-08-30T10:00:00+00:00"),
    _record("/results/lens_b/def", "completed", "2026-09-02T10:00:00+00:00"),
    _record("/results/lens_d/abc", "never_started"),
]


def _expected_hash(records) -> str:
    h = hashlib.sha256()
    for rec in sorted(records, key=lambda r: r["output_path"]):
        h.update(f"{rec['output_path']}|{rec['state']}|{rec['completed_at']}\n".encode())
    return h.hexdigest()


def _run(*args, root):
    return subprocess.run([sys.executable, str(SCRIPT), *args, "--root", str(root)],
                          capture_output=True, text=True)


def _ledger(root):
    return next(l for l in cortex.load_ledgers(root)[0] if l.key == "example")


def test_appends_one_library_entry_with_hash_and_counts(tmp_path):
    root = _copy(tmp_path)
    idx = _index(tmp_path, RECORDS)
    r = _run("library", "example", str(idx), "--name", "dr1 v1.0", "--today", TODAY,
             root=root)
    assert r.returncode == 0, r.stderr
    digest = _expected_hash(RECORDS)
    line = (f"- {TODAY} — library — dr1 v1.0: index {digest[:12]} — 5 results "
            f"(completed 2, failed 1, superseded 1, never_started 1)")
    assert (root / EX).read_text().split("## Log\n\n")[1].splitlines()[0] == line
    assert r.stdout.splitlines()[0] == f"library: example: {line.split(' — library — ')[1]}"
    assert r.stdout.splitlines()[1] == f"  index sha256 {digest}"
    assert _ledger(root).log[0].kind == "library"
    assert cortex.check_problems(root) == []


def test_default_name_is_the_index_folder_or_its_parent(tmp_path):
    root = _copy(tmp_path)
    idx = _index(tmp_path, RECORDS[:1], name="euclid_dr1_index")
    cortex.record_library(root, "example", idx, cortex.date.fromisoformat(TODAY))
    assert _ledger(root).log[0].text().startswith("euclid_dr1_index: index ")
    nested = _index(tmp_path / "euclid_dr1", RECORDS[:1], name=".autofit_index")
    cortex.record_library(root, "example", nested, cortex.date.fromisoformat(TODAY))
    assert _ledger(root).log[0].text().startswith("euclid_dr1: index ")


def test_rerun_appends_another_line_never_edits(tmp_path):
    root = _copy(tmp_path)
    idx = _index(tmp_path, RECORDS)
    cortex.record_library(root, "example", idx, cortex.date.fromisoformat(TODAY))
    cortex.record_library(root, "example", idx, cortex.date.fromisoformat("2026-09-04"))
    log = _ledger(root).log
    assert [e.kind for e in log[:2]] == ["library", "library"]
    assert [e.date for e in log[:2]] == ["2026-09-04", TODAY]
    assert log[0].text() == log[1].text()
    assert cortex.check_problems(root) == []


def test_skips_unreadable_and_other_schema_records_as_autofit_does(tmp_path):
    idx = _index(tmp_path, RECORDS[:2] + [_record("/results/lens_z/abc", "completed",
                                                   "2026-09-01", schema=2)])
    (idx / "records" / "broken.json").write_text("{ not json")
    (idx / "records" / "partial.json").write_text(json.dumps({"output_path": "/x"}))
    (idx / "records" / "notes.txt").write_text("not a record")
    text, digest = cortex.library_entry(idx, "n")
    assert digest == _expected_hash(RECORDS[:2])
    assert text.endswith("— 2 results (completed 1, failed 1)")


def test_empty_records_dir_is_zero_results(tmp_path):
    root = _copy(tmp_path)
    idx = _index(tmp_path, [])
    r = _run("library", "example", str(idx), "--today", TODAY, root=root)
    assert r.returncode == 0, r.stderr
    head = _ledger(root).log[0]
    assert head.text() == f"dr1_index: index {hashlib.sha256().hexdigest()[:12]} — 0 results"
    assert cortex.check_problems(root) == []


def test_dry_run_changes_nothing(tmp_path):
    root = _copy(tmp_path)
    before = (root / EX).read_text()
    r = _run("library", "example", str(_index(tmp_path, RECORDS)), "--dry-run",
             "--today", TODAY, root=root)
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines()[0].startswith("library: example: dr1_index: index ")
    assert r.stdout.splitlines()[0].endswith(" (dry run)")
    assert (root / EX).read_text() == before


@pytest.mark.parametrize("make, message", [
    (lambda tmp: tmp / "nowhere", "no such results index folder"),
    (lambda tmp: (tmp / "bare").mkdir() or tmp / "bare", "no index.json"),
    (lambda tmp: _index(tmp, RECORDS, manifest_schema=2), "not a schema-1 results index"),
])
def test_refuses_a_missing_or_foreign_index(tmp_path, make, message):
    root = _copy(tmp_path)
    before = (root / EX).read_text()
    r = _run("library", "example", str(make(tmp_path)), "--today", TODAY, root=root)
    assert r.returncode == 1
    assert message in r.stderr
    assert (root / EX).read_text() == before


def test_refuses_an_unknown_project(tmp_path):
    root = _copy(tmp_path)
    r = _run("library", "nosuch", str(_index(tmp_path, RECORDS)), "--today", TODAY,
             root=root)
    assert r.returncode == 1
    assert "nosuch is not a projects.yaml key" in r.stderr


def test_refuses_a_date_before_the_log_head(tmp_path):
    root = _copy(tmp_path)
    before = (root / EX).read_text()
    r = _run("library", "example", str(_index(tmp_path, RECORDS)), "--today", "2026-01-01",
             root=root)
    assert r.returncode == 1
    assert "newest-first" in r.stderr
    assert (root / EX).read_text() == before


def test_never_writes_result_lesson_runs_or_now(tmp_path):
    root = _copy(tmp_path)
    before = _ledger(root)
    cortex.record_library(root, "example", _index(tmp_path, RECORDS),
                          cortex.date.fromisoformat(TODAY))
    after = _ledger(root)
    assert after.now == before.now
    assert [r.line() for r in after.runs] == [r.line() for r in before.runs]
    assert [(e.date, e.kind, e.text()) for e in after.log[1:]] == \
        [(e.date, e.kind, e.text()) for e in before.log]


def test_log_verb_cannot_write_a_library_entry(tmp_path):
    root = _copy(tmp_path)
    r = _run("log", "example", "hand-typed", "--kind", "library", "--today", TODAY, root=root)
    assert r.returncode == 2


def test_hash_matches_autofit_index_hash(tmp_path):
    """The Cortex hash equals `autofit.export.index_hash`: on an index autofit
    built from synthetic results, and on the hand-written fixture loaded by
    autofit."""
    pytest.importorskip("autofit")
    from autofit.export import index_hash
    from autofit.results import ResultsIndex

    out = tmp_path / "output"
    for i, kind in enumerate(["completed", "completed", "failed", "never_started"]):
        d = out / "prefix" / f"fit_{i}" / "abc"
        (d / "files").mkdir(parents=True)
        (d / "files" / "search.json").write_text("{}")
        if kind == "completed":
            (d / ".completed").write_text("")
        if kind == "failed":
            Path(f"{d}.status.json").write_text(json.dumps(
                {"state": "failed", "updated": "2026-09-03T08:00:00+00:00"}))
    built = ResultsIndex(out, index_dir=tmp_path / "built_index")
    built.update()
    text, digest = cortex.library_entry(built.index_dir, "built")
    assert digest == index_hash(built)
    counts = built.counts()  # every ResultState, in autofit's order, zeros included
    assert tuple(counts) == cortex.RESULT_STATES
    shown = ", ".join(f"{s} {n}" for s, n in counts.items() if n)
    assert text.endswith(f"— 4 results ({shown})")

    hand = _index(tmp_path, RECORDS)
    _, digest = cortex.library_entry(hand, "hand")
    assert digest == index_hash(ResultsIndex(tmp_path, index_dir=hand)) == _expected_hash(RECORDS)
