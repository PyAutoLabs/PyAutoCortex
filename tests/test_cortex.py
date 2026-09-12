"""Contract tests for scripts/cortex.py — check, new, run, running, done, log, now, issue, retire.

Two things these tests deliberately do:

1. **The fixture is the witness.** `tests/fixtures/skeleton/` holds four rows
   (two active with ledgers, one retired with a closed ledger, one dormant
   with none) and `tests/fixtures/empty/` an empty map. Both pass `check`
   unchanged, and every writing verb runs on a `copytree` of the skeleton.
2. **Prove each leg FAILS.** Every `check` rule in REFERENCE.md is driven with
   a `tmp_path` mutation that must trip it, asserting the `  - …` line.
"""

import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import cortex  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "cortex.py"
SKELETON = REPO / "tests" / "fixtures" / "skeleton"
EMPTY = REPO / "tests" / "fixtures" / "empty"
TODAY = "2026-09-03"
EX = "projects/example.md"


def _copy(tmp_path: Path, src: Path = SKELETON) -> Path:
    root = tmp_path / "tree"
    shutil.copytree(src, root)
    return root


def _run(*args, root=None):
    cmd = [sys.executable, str(SCRIPT), *args]
    if root is not None:
        cmd += ["--root", str(root)]
    return subprocess.run(cmd, capture_output=True, text=True)


def _problems(root: Path):
    return cortex.check_problems(root)


def _edit(root: Path, rel: str, old: str, new: str):
    p = root / rel
    text = p.read_text()
    assert old in text, f"{old!r} not in {rel}"
    p.write_text(text.replace(old, new, 1))


def _ledger(root: Path, key: str = "example") -> cortex.Ledger:
    leds, _ = cortex.load_ledgers(root)
    return next(l for l in leds if l.key == key)


# --------------------------------------------------------------------------- #
# check
# --------------------------------------------------------------------------- #
def test_the_fixtures_check_clean():
    assert _problems(SKELETON) == []
    assert _problems(EMPTY) == []
    assert _run("check", root=SKELETON).returncode == 0
    assert _run("check", root=EMPTY).returncode == 0


def test_the_live_tree_checks_clean():
    r = _run("check", root=REPO)
    assert r.returncode == 0, r.stdout


def test_check_prints_one_line_per_finding_and_exits_1(tmp_path):
    root = _copy(tmp_path)
    _edit(root, EX, "Issue: example#7", "Issue: nonsense")
    r = _run("check", root=root)
    assert r.returncode == 1
    assert "cortex check: DRIFT" in r.stdout
    assert "  - projects/example.md: `Issue:` must be" in r.stdout


def test_an_active_project_needs_a_ledger(tmp_path):
    root = _copy(tmp_path)
    (root / "projects" / "single.md").unlink()
    assert any("single is active but has no projects/single.md" in p for p in _problems(root))


def test_a_ledger_needs_a_row(tmp_path):
    root = _copy(tmp_path)
    shutil.copy(root / EX, root / "projects" / "stranger.md")
    _edit(root, "projects/stranger.md", "# example —", "# stranger —")
    _edit(root, "projects/stranger.md", "Project: example", "Project: stranger")
    assert any("stranger is not a projects.yaml key" in p for p in _problems(root))


def test_the_file_name_is_the_key(tmp_path):
    root = _copy(tmp_path)
    (root / "projects" / "Example-Two.md").write_text("# x — y\n")
    assert any("file name must be projects/<key>.md" in p for p in _problems(root))


def test_the_title_names_the_key_and_carries_a_short_summary(tmp_path):
    root = _copy(tmp_path)
    _edit(root, EX, "# example — Does", "# other — Does")
    assert any("title must be `# example — <summary>`" in p for p in _problems(root))
    root = _copy(tmp_path / "b")
    _edit(root, EX, "# example — Does the example pipeline recover the truth on the fixture lens",
          "# example — " + " ".join(["word"] * 16))
    assert any("summary is over 15 words" in p for p in _problems(root))


def test_the_header_holds_project_and_issue_only(tmp_path):
    root = _copy(tmp_path)
    _edit(root, EX, "Issue: example#7", "Issue: example#7\nState: running")
    assert any("unknown header key(s) State" in p for p in _problems(root))
    root = _copy(tmp_path / "b")
    _edit(root, EX, "Issue: example#7\n", "")
    assert any("header is missing `Issue:`" in p for p in _problems(root))
    root = _copy(tmp_path / "c")
    _edit(root, EX, "Project: example", "Project: other")
    assert any("`Project:` must be example" in p for p in _problems(root))


def test_issue_grammar():
    for ok in ("none", "example#7", "PyAutoCortex#12",
               "https://github.com/Jammy2211/ic50_workspace/issues/3"):
        assert cortex.ISSUE_RE.match(ok), ok
    for bad in ("PyAutoLabs/example#7", "example", "#7", ""):
        assert not cortex.ISSUE_RE.match(bad), bad
    assert cortex.issue_url("example#7") == "https://github.com/PyAutoLabs/example/issues/7"


def test_the_three_sections_in_order_and_nothing_else(tmp_path):
    root = _copy(tmp_path)
    _edit(root, EX, "## Runs", "## Jobs")
    assert any("sections must be exactly ## Now · ## Runs · ## Log" in p for p in _problems(root))
    root = _copy(tmp_path / "b")
    _edit(root, EX, "## Log", "## Notes\n\n## Log")
    assert any("sections must be exactly" in p for p in _problems(root))


def test_an_active_project_must_say_where_it_is(tmp_path):
    root = _copy(tmp_path)
    p = root / EX
    text = p.read_text()
    a, b = text.index("## Now"), text.index("## Runs")
    p.write_text(text[:a] + "## Now\n\n" + text[b:])
    assert any("`## Now` is empty on an active project" in p for p in _problems(root))


def test_run_lines_parse_to_open_or_running_with_a_partition_and_a_date(tmp_path):
    led = _ledger(SKELETON)
    assert [(r.ident, r.state, r.partition, r.date) for r in led.runs] == [
        ("3002_[0-3]", "running", "ral", "2026-09-01"),
        ("3003", "open", "gpu", "2026-09-02")]
    assert led.runs[1].text() == "joint fit on the same four seeds chained after 3002 with afterok"
    root = _copy(tmp_path)
    _edit(root, EX, "- 3003 — open — gpu", "- 3003 — submitted — gpu")
    assert any("run line does not parse" in p for p in _problems(root))
    root = _copy(tmp_path / "b")
    _edit(root, EX, "- 3003 — open — gpu", "- 3003 — open — cpu")
    assert not any("3003" in p and "partition" in p for p in _problems(root))  # `both` allows any
    _edit(root, "projects/single.md", "## Runs\n", "## Runs\n\n- 9 — open — gpu — 2026-09-01 — x\n")
    assert any("run 9 is on `gpu` but the project runs on `ral`" in p for p in _problems(root))


def test_a_run_is_listed_once_and_a_retired_project_lists_none(tmp_path):
    root = _copy(tmp_path)
    _edit(root, EX, "- 3003 — open — gpu — 2026-09-02 — joint fit",
          "- 3003 — open — gpu — 2026-09-02 — joint fit\n- 3003 — open — gpu — 2026-09-02 — again")
    assert any("run 3003 listed twice" in p for p in _problems(root))
    root = _copy(tmp_path / "b")
    _edit(root, "projects/wound_down.md", "## Runs\n", "## Runs\n\n- 1 — open — ral — 2026-09-01 — x\n")
    assert any("a retired project still lists runs" in p for p in _problems(root))


def test_the_dash_may_be_typed_as_two_hyphens():
    led = cortex.parse_ledger(
        "# k -- summary\n\nProject: k\nIssue: none\n\n## Now\n\nx\n\n## Runs\n\n"
        "- 1 -- open -- ral -- 2026-09-01 -- a run\n\n## Log\n\n- 2026-09-01 -- note -- hi\n",
        "k", Path("k.md"), "projects/k.md")
    assert led.problems == []
    assert led.summary == "summary" and led.runs[0].state == "open" and led.log[0].kind == "note"


def test_log_lines_carry_a_date_a_kind_and_text_newest_first(tmp_path):
    led = _ledger(SKELETON)
    assert [e.kind for e in led.log] == ["run", "run", "lesson", "result", "run", "run", "note"]
    assert led.log[3].text() == ("wave 1 recovered the parent mean but its sigma is 4x too "
                                 "tight the widths are the finding, not the means")
    assert led.updated() == "2026-09-02"
    assert [e.date for e in led.recent(2)] == ["2026-09-02", "2026-09-01"]
    root = _copy(tmp_path)
    _edit(root, EX, "- 2026-09-01 — lesson —", "- 2026-09-01 — verdict —")
    assert any("log line does not parse" in p for p in _problems(root))
    root = _copy(tmp_path / "b")
    _edit(root, EX, "- 2026-08-28 — note — ledger opened", "- 2026-09-09 — note — out of order")
    assert any("log is not newest-first" in p for p in _problems(root))
    root = _copy(tmp_path / "c")
    _edit(root, EX, "- 2026-08-28 — note", "- 2026-02-30 — note")
    assert any("not a real date" in p for p in _problems(root))


def test_a_continuation_line_needs_something_to_continue(tmp_path):
    root = _copy(tmp_path)
    _edit(root, EX, "## Log\n\n", "## Log\n\n  orphan\n")
    assert any("continuation line without a log line" in p for p in _problems(root))


def test_projects_yaml_is_validated(tmp_path):
    root = _copy(tmp_path)
    _edit(root, "projects.yaml", "  partition: both\n  status: active\n  note: \"the fixture project\"",
          "  partition: moon\n  status: active\n  note: \"the fixture project\"")
    assert any("example.partition must be gpu | ral | both" in p for p in _problems(root))
    root = _copy(tmp_path / "b")
    _edit(root, "projects.yaml", "  status: active\n  note: \"the fixture project\"",
          "  status: active\n  colour: red\n  note: \"the fixture project\"")
    assert any("unknown field `colour` on example" in p for p in _problems(root))


# --------------------------------------------------------------------------- #
# the writing verbs
# --------------------------------------------------------------------------- #
def test_new_opens_a_ledger_for_a_row_and_refuses_the_rest(tmp_path):
    root = _copy(tmp_path)
    (root / "projects" / "single.md").unlink()
    r = _run("new", "single", "--summary", "A fresh question", "--issue", "single#1",
             "--today", TODAY, root=root)
    assert r.returncode == 0, r.stderr
    led = _ledger(root, "single")
    assert led.summary == "A fresh question" and led.issue == "single#1"
    assert led.now.startswith("Just opened")
    assert led.log[0].text() == "ledger opened" and led.log[0].date == TODAY
    assert _problems(root) == []
    assert _run("new", "single", "--summary", "again", root=root).returncode == 1
    r = _run("new", "nobody", "--summary", "x", root=root)
    assert r.returncode == 1 and "not a projects.yaml key" in r.stderr
    r = _run("new", "sleeping", "--summary", " ".join(["w"] * 16), root=root)
    assert r.returncode == 1 and "over 15 words" in r.stderr
    r = _run("new", "sleeping", "--summary", "x", "--issue", "PyAutoLabs/x#1", root=root)
    assert r.returncode == 1 and "--issue must be" in r.stderr


def test_run_records_a_submission_as_open_and_logs_it(tmp_path):
    root = _copy(tmp_path)
    r = _run("run", "example", "3004_[0-9]", "wave 3, ten seeds", "--partition", "ral",
             "--today", TODAY, root=root)
    assert r.returncode == 0, r.stderr
    led = _ledger(root)
    assert [x.ident for x in led.runs] == ["3002_[0-3]", "3003", "3004_[0-9]"]
    assert led.runs[-1].state == "open" and led.runs[-1].partition == "ral"
    assert led.log[0].kind == "run" and led.log[0].text() == "3004_[0-9] submitted: wave 3, ten seeds"
    assert _problems(root) == []
    # again → refused; a project on both partitions needs --partition; a bad id is refused
    assert _run("run", "example", "3004_[0-9]", "x", "--partition", "ral", root=root).returncode == 1
    r = _run("run", "example", "3005", "x", root=root)
    assert r.returncode == 1 and "--partition" in r.stderr
    r = _run("run", "example", "job-five", "x", "--partition", "ral", root=root)
    assert r.returncode == 1 and "not a SLURM job id" in r.stderr
    # a one-partition project needs no flag
    assert _run("run", "single", "77", "first run", "--today", TODAY, root=root).returncode == 0
    assert _ledger(root, "single").runs[0].partition == "ral"


def test_running_flips_the_state_and_done_moves_the_run_into_the_log(tmp_path):
    root = _copy(tmp_path)
    assert _run("running", "example", "3003", root=root).returncode == 0
    assert _ledger(root).runs[1].state == "running"
    assert "already running" in _run("running", "example", "3003", root=root).stdout
    r = _run("done", "example", "3002_[0-3]", "--wall", "20:05", "--note", "all four landed",
             "--today", TODAY, root=root)
    assert r.returncode == 0, r.stderr
    led = _ledger(root)
    assert [x.ident for x in led.runs] == ["3003"]
    assert led.log[0].text() == ("3002_[0-3] finished — wall 20:05: wave 2, four seeds on the "
                                 "corrected settings — all four landed")
    r = _run("done", "example", "3003", "--failed", "--today", TODAY, root=root)
    assert r.returncode == 0
    led = _ledger(root)
    assert led.runs == [] and led.log[0].text().startswith("3003 failed: joint fit")
    assert _problems(root) == []
    r = _run("done", "example", "3003", root=root)
    assert r.returncode == 1 and "is not under ## Runs" in r.stderr
    r = _run("done", "single", "1", "--wall", "20", root=root)
    assert r.returncode == 1 and "--wall must be H:MM" in r.stderr


def test_log_writes_the_humans_words_newest_first(tmp_path):
    root = _copy(tmp_path)
    r = _run("log", "example", "the sigma is the finding, not the mean", "--kind", "lesson",
             "--today", TODAY, root=root)
    assert r.returncode == 0, r.stderr
    led = _ledger(root)
    assert led.log[0].kind == "lesson" and led.log[0].date == TODAY
    assert len(led.log) == 8 and _problems(root) == []
    assert _run("log", "example", "plain", "--today", TODAY, root=root).returncode == 0
    assert _ledger(root).log[0].kind == "note"
    r = _run("log", "example", "backdated", "--today", "2026-08-01", root=root)
    assert r.returncode == 1 and "newest-first" in r.stderr
    r = _run("log", "example", "   ", root=root)
    assert r.returncode == 1
    r = _run("log", "example", "x", "--kind", "verdict", root=root)
    assert r.returncode == 2


def test_now_rewrites_the_head_pointer_and_nothing_else(tmp_path):
    root = _copy(tmp_path)
    before = _ledger(root)
    r = _run("now", "example", "Pulled wave 2.\nNext: compare against wave 1.", root=root)
    assert r.returncode == 0, r.stderr
    led = _ledger(root)
    assert led.now == "Pulled wave 2.\nNext: compare against wave 1."
    assert [x.ident for x in led.runs] == [x.ident for x in before.runs]
    assert len(led.log) == len(before.log)
    assert _problems(root) == []
    assert _run("now", "example", "", root=root).returncode == 1


def test_a_verb_refuses_a_ledger_that_does_not_parse(tmp_path):
    root = _copy(tmp_path)
    _edit(root, EX, "- 3003 — open — gpu", "- 3003 — weird — gpu")
    r = _run("log", "example", "x", root=root)
    assert r.returncode == 1 and "does not parse clean" in r.stderr
    r = _run("log", "nobody", "x", root=root)
    assert r.returncode == 1 and "no ledger for nobody" in r.stderr


# --------------------------------------------------------------------------- #
# the issue block
# --------------------------------------------------------------------------- #
def test_issue_prints_the_concise_ledger_between_markers():
    r = _run("issue", "example", "-n", "3", root=SKELETON)
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert out.startswith(cortex.ISSUE_BEGIN.format(key="example"))
    assert out.rstrip().endswith(cortex.ISSUE_END)
    assert "**Now**" in out and "Wave 2 is on the cluster" in out
    assert "`3002_[0-3]` — running — ral" in out
    assert "**Last 3**" in out
    assert out.count("\n- `") == 2  # two runs
    assert out.count("\n- 2026-") == 3  # three entries
    assert "2026-08-31 — *result*" not in out  # the fourth entry is outside the window


def test_issue_block_names_the_home_when_given():
    led = _ledger(SKELETON)
    block = cortex.issue_block(led, {"status": "active"}, 5, home="https://github.com/x/y")
    assert "(https://github.com/x/y/blob/main/projects/example.md)" in block


# --------------------------------------------------------------------------- #
# retire
# --------------------------------------------------------------------------- #
def test_retire_flips_the_row_logs_it_and_refuses_over_live_runs(tmp_path):
    root = _copy(tmp_path)
    r = _run("retire", "example", "--why", "done", "--today", TODAY, root=root)
    assert r.returncode == 1 and "still lists runs" in r.stderr
    r = _run("retire", "single", "--why", "never started", "--today", TODAY, root=root)
    assert r.returncode == 0, r.stderr
    rows, _ = cortex.load_projects(root)
    assert rows["single"]["status"] == "retired"
    assert rows["single"]["note"] == f"retired {TODAY}: never started"
    assert _ledger(root, "single").log[0].text() == "retired: never started"
    assert _problems(root) == []
    assert _run("retire", "single", "--why", "again", root=root).returncode == 1
    r = _run("retire", "sleeping", "--why", "no ledger, still fine", "--today", TODAY, root=root)
    assert r.returncode == 0
    assert (root / "projects.yaml").read_text().count("status: retired") == 3


def test_retire_preserves_every_other_byte_of_projects_yaml(tmp_path):
    root = _copy(tmp_path)
    before = (root / "projects.yaml").read_text()
    _run("retire", "sleeping", "--why", "x", "--today", TODAY, root=root)
    after = (root / "projects.yaml").read_text()
    diff = [(a, b) for a, b in zip(before.split("\n"), after.split("\n")) if a != b]
    assert diff == [("  status: dormant", "  status: retired"),
                    ('  note: "no ledger yet"', f'  note: "retired {TODAY}: x"')]


# --------------------------------------------------------------------------- #
# the CLI surface
# --------------------------------------------------------------------------- #
def test_every_verb_is_registered():
    parser = cortex.build_parser()
    verbs = set(parser._subparsers._group_actions[0].choices)
    assert verbs == {"check", "new", "run", "running", "done", "log", "now", "issue", "retire"}


def test_a_bad_root_is_a_usage_error(tmp_path):
    assert _run("check", root=tmp_path / "nowhere").returncode == 2


def test_no_verb_of_the_old_schema_survives():
    text = SCRIPT.read_text()
    for gone in ("def move_task", "def rule_task", "def gates_report", "awaiting-ruling",
                 "def load_tasks", "def load_rulings"):
        assert gone not in text, gone


def test_today_is_injectable_and_validated(tmp_path):
    root = _copy(tmp_path)
    r = _run("log", "example", "x", "--today", "yesterday", root=root)
    assert r.returncode == 1 and "--today must be YYYY-MM-DD" in r.stderr
    assert _run("log", "example", "x", root=root).returncode == 0
    assert _ledger(root).log[0].date == date.today().isoformat()
