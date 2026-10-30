"""Contract tests for `cortex.py sync-runs` (schema decision 64): run status from
a PyAutoFit campaign digest — open → running, done with counts, nothing else.

The digest fixtures are written per test in the shape `autofit.campaign.digest`
writes them: `digest.json` (schema 1) with `tasks.jsonl` beside it, one row per
task with `job_id`, `key` (`<job>_<array index>`), `state`, and optionally
`start`/`end`.
"""

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


def _digest(tmp_path: Path, tasks, campaign="example_campaign", schema=1) -> Path:
    d = tmp_path / "campaign"
    d.mkdir(exist_ok=True)
    (d / "digest.json").write_text(json.dumps(
        {"schema": schema, "campaign": campaign, "updated": "2026-09-03T08:00:00Z",
         "totals": {}, "stages": {}}))
    (d / "tasks.jsonl").write_text("".join(json.dumps(t) + "\n" for t in tasks))
    return d / "digest.json"


def _task(job, index, state, start=None, end=None):
    t = {"stage": "s", "key": f"{job}_{index}", "job_id": str(job), "state": state}
    if start:
        t["start"] = start
    if end:
        t["end"] = end
    return t


def _run(*args, root):
    return subprocess.run([sys.executable, str(SCRIPT), *args, "--root", str(root)],
                          capture_output=True, text=True)


def _runs(root):
    led = next(l for l in cortex.load_ledgers(root)[0] if l.key == "example")
    return {r.ident: r.state for r in led.runs}, led


def test_open_run_with_a_started_task_becomes_running(tmp_path):
    root = _copy(tmp_path)
    digest = _digest(tmp_path, [_task(3003, 0, "running"), _task(3002, 0, "pending")])
    r = _run("sync-runs", "example", "--digest", str(digest), "--today", TODAY, root=root)
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines()[0] == "sync-runs: example: 1 changed"
    runs, led = _runs(root)
    assert runs["3003"] == "running"
    assert led.log[0].kind == "run" and "3003 running" in led.log[0].text()
    assert cortex.check_problems(root) == []


def test_all_terminal_tasks_call_done_with_counts_and_wall(tmp_path):
    root = _copy(tmp_path)
    tasks = [_task(3002, i, "completed", "2026-09-01T10:00:00", "2026-09-01T12:30:00")
             for i in range(3)]
    tasks.append(_task(3002, 3, "timeout", "2026-09-01T10:00:00", "2026-09-01T13:05:00"))
    digest = _digest(tmp_path, tasks)
    out = cortex.sync_runs(root, "example", digest, cortex.date.fromisoformat(TODAY))
    assert out[0] == "sync-runs: example: 1 changed"
    runs, led = _runs(root)
    assert "3002_[0-3]" not in runs
    head = led.log[0]
    assert head.kind == "run"
    assert head.text().startswith("3002_[0-3] finished — wall 3:05:")
    assert "3 completed, 1 timeout" in head.text()
    assert cortex.check_problems(root) == []


def test_no_completed_task_is_a_failed_run(tmp_path):
    root = _copy(tmp_path)
    digest = _digest(tmp_path, [_task(3003, 0, "failed")])
    cortex.sync_runs(root, "example", digest, cortex.date.fromisoformat(TODAY))
    _, led = _runs(root)
    assert led.log[0].text().startswith("3003 failed:")


def test_array_ident_only_counts_its_own_indices(tmp_path):
    root = _copy(tmp_path)
    # index 7 is outside 3002_[0-3]: it is still running but must not hold the run open
    tasks = [_task(3002, i, "completed") for i in range(4)] + [_task(3002, 7, "running")]
    cortex.sync_runs(root, "example", _digest(tmp_path, tasks),
                     cortex.date.fromisoformat(TODAY))
    runs, _ = _runs(root)
    assert "3002_[0-3]" not in runs


def test_rerun_is_idempotent(tmp_path):
    root = _copy(tmp_path)
    digest = _digest(tmp_path, [_task(3002, i, "completed") for i in range(4)]
                     + [_task(3003, 0, "running")])
    first = cortex.sync_runs(root, "example", digest, cortex.date.fromisoformat(TODAY))
    text = (root / EX).read_text()
    second = cortex.sync_runs(root, "example", digest, cortex.date.fromisoformat(TODAY))
    assert first[0] == "sync-runs: example: 2 changed"
    assert second[0] == "sync-runs: example: 0 changed"
    assert (root / EX).read_text() == text


def test_dry_run_changes_nothing(tmp_path):
    root = _copy(tmp_path)
    before = (root / EX).read_text()
    digest = _digest(tmp_path, [_task(3003, 0, "completed")])
    r = _run("sync-runs", "example", "--digest", str(digest), "--dry-run", root=root)
    assert r.returncode == 0
    assert r.stdout.splitlines()[0] == "sync-runs: example: 1 changed (dry run)"
    assert "3003: done" in r.stdout
    assert (root / EX).read_text() == before


def test_unknown_digest_job_and_absent_run_are_reported_not_acted_on(tmp_path):
    root = _copy(tmp_path)
    before = (root / EX).read_text()
    digest = _digest(tmp_path, [_task(9999, 0, "completed")])
    r = _run("sync-runs", "example", "--digest", str(digest), root=root)
    assert r.returncode == 0
    assert r.stdout.splitlines()[0] == "sync-runs: example: 0 changed"
    assert "not in the digest" in r.stdout
    assert "1 digest job(s) are not runs" in r.stdout and "9999" in r.stdout
    assert (root / EX).read_text() == before


def test_never_writes_result_lesson_or_now(tmp_path):
    root = _copy(tmp_path)
    _, before = _runs(root)
    digest = _digest(tmp_path, [_task(3002, i, "completed") for i in range(4)]
                     + [_task(3003, 0, "running")])
    cortex.sync_runs(root, "example", digest, cortex.date.fromisoformat(TODAY))
    _, after = _runs(root)
    new = after.log[: len(after.log) - len(before.log)]
    assert new and all(e.kind == "run" for e in new)
    keep = [(e.date, e.kind, e.text()) for e in before.log if e.kind in ("result", "lesson")]
    assert [(e.date, e.kind, e.text()) for e in after.log
            if e.kind in ("result", "lesson")] == keep
    assert after.now == before.now


@pytest.mark.parametrize("bad", ["not json", json.dumps({"schema": 2})])
def test_malformed_digest_exits_nonzero(tmp_path, bad):
    root = _copy(tmp_path)
    d = tmp_path / "bad"
    d.mkdir()
    (d / "digest.json").write_text(bad)
    (d / "tasks.jsonl").write_text("")
    r = _run("sync-runs", "example", "--digest", str(d / "digest.json"), root=root)
    assert r.returncode != 0
    assert r.stdout == ""


def test_missing_tasks_or_bad_row_exits_nonzero(tmp_path):
    root = _copy(tmp_path)
    digest = _digest(tmp_path, [])
    (digest.parent / "tasks.jsonl").unlink()
    assert _run("sync-runs", "example", "--digest", str(digest), root=root).returncode != 0
    (digest.parent / "tasks.jsonl").write_text('{"job_id": "1"}\n')
    assert _run("sync-runs", "example", "--digest", str(digest), root=root).returncode != 0


def test_digest_folder_and_projects_yaml_default(tmp_path):
    root = _copy(tmp_path)
    digest = _digest(tmp_path, [_task(3003, 0, "running")])
    yml = root / "projects.yaml"
    yml.write_text(yml.read_text().replace(
        '  note: "the fixture project"',
        f'  note: "the fixture project"\n  digest: {digest}\n  campaign_file: campaign.yaml', 1))
    assert cortex.check_problems(root) == []
    r = _run("sync-runs", "example", root=root)
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines()[0] == "sync-runs: example: 1 changed"
    # the folder works as well as the file
    r = _run("sync-runs", "example", "--digest", str(digest.parent), root=root)
    assert r.stdout.splitlines()[0] == "sync-runs: example: 0 changed"


def test_no_digest_anywhere_is_refused(tmp_path):
    root = _copy(tmp_path)
    r = _run("sync-runs", "example", root=root)
    assert r.returncode == 1
    assert "--digest" in r.stderr


@pytest.mark.parametrize("field,value,message", [
    ("campaign_file", "campaign.txt", "campaign_file must be a .yaml file"),
    ("digest", "out/summary.json", "digest must name a digest.json"),
    ("digest", "../other/digest.json", "must not climb out"),
    ("campaign_file", '""', "campaign_file is empty"),
])
def test_check_validates_the_campaign_fields(tmp_path, field, value, message):
    root = _copy(tmp_path)
    yml = root / "projects.yaml"
    yml.write_text(yml.read_text().replace(
        '  note: "the fixture project"', f'  note: "the fixture project"\n  {field}: {value}', 1))
    assert any(message in p for p in cortex.check_problems(root)), cortex.check_problems(root)
