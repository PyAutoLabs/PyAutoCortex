"""Contract tests for scripts/cortex.py — the Cortex's check, gates, rule, move, new.

Two things these tests deliberately do, matching the Mind's `test_lifecycle_check.py`:

1. **The fixture is the witness.** `tests/fixtures/skeleton/` holds one project,
   one phase per state, five rulings (one chain of two), one batch record and
   one review; `tests/fixtures/empty/` is an empty map. Both must pass `check`
   unchanged, and every writing verb runs on a `copytree` of the skeleton.
2. **Prove each leg FAILS.** Every `check` rule in REFERENCE.md is driven with
   a `tmp_path` mutation that must trip it, asserting the `  - …` line; every
   transition the table allows is taken and every one it refuses is refused.
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
TODAY = "2026-09-02"

P = {n: f"phases/example/{n}.md" for n in (
    "01_scope", "02_gated_on_dev", "03_ready_cleared", "04_submitted_override",
    "05_running_array", "06_pulled", "07_awaiting_ruling", "08_accepted",
    "09_rerun", "10_dropped")}


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _copy(tmp_path: Path, src: Path = SKELETON) -> Path:
    root = tmp_path / "tree"
    shutil.copytree(src, root)
    return root


def _run(*args, root=None, stdin=""):
    cmd = [sys.executable, str(SCRIPT), *args]
    if root is not None:
        cmd += ["--root", str(root)]
    return subprocess.run(cmd, input=stdin, capture_output=True, text=True)


def _problems(root: Path):
    return cortex.check_problems(root)


def _edit(root: Path, rel: str, old: str, new: str, count: int = 1):
    p = root / rel
    text = p.read_text()
    assert old in text, f"{old!r} not in {rel}"
    p.write_text(text.replace(old, new, count))


def _fields(root: Path, rel: str):
    return cortex.parse_header((root / rel).read_text())[1]


def _assert_drift(root: Path, *needles: str):
    problems = _problems(root)
    joined = "\n".join(problems)
    for needle in needles:
        assert needle in joined, f"expected {needle!r} in:\n{joined}"
    return problems


def _move(root, rel, state, *extra, today=TODAY):
    return _run("move", rel, state, "--today", today, *extra, root=root)


def _body(tmp_path: Path, text="Accept. The human's words, verbatim.\n") -> Path:
    p = tmp_path / "body.txt"
    p.write_text(text)
    return p


# --------------------------------------------------------------------------- #
# the witness — both fixtures pass check unchanged
# --------------------------------------------------------------------------- #
def test_skeleton_fixture_passes_check():
    result = _run("check", root=SKELETON)
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip() == "cortex check: OK"


def test_empty_fixture_passes_check():
    result = _run("check", root=EMPTY)
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip() == "cortex check: OK"


def test_check_problems_is_quiet_on_the_witness():
    assert _problems(SKELETON) == []
    assert _problems(EMPTY) == []


def test_check_reports_drift_in_lifecycle_shape(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["03_ready_cleared"], "Gates-cleared: 2026-08-30\n", "")
    result = _run("check", root=root)
    assert result.returncode == 1
    lines = result.stdout.splitlines()
    assert lines[0] == "cortex check: DRIFT"
    assert lines[1].startswith("  - phases/example/03_ready_cleared.md: ")


def test_no_import_time_side_effects_and_root_on_every_verb():
    help_text = _run("--help").stdout
    for verb in ("check", "gates", "rule", "move", "new"):
        assert verb in help_text
        assert "--root" in _run(verb, "--help").stdout


# --------------------------------------------------------------------------- #
# the light header and the grammars
# --------------------------------------------------------------------------- #
def test_header_first_occurrence_wins_block_ends_at_blank_line_list_keys():
    text = ("# Title\n\nProject: one\nProject: two\nGates:\n- A#1\n- B#2\nState: ready\n\n"
            "Phase: 99\n")
    title, fields = cortex.parse_header(text)
    assert title == "Title"
    assert fields["Project"] == "one"
    assert fields["Gates"] == "A#1, B#2"
    assert "Phase" not in fields  # after the blank line — body, not header


def test_header_beyond_30_lines_is_body():
    text = "# T\n\n" + "\n".join(f"K{i}: v" for i in range(40)) + "\n"
    _, fields = cortex.parse_header(text)
    assert "K27" in fields and "K28" not in fields


def test_edit_header_preserves_every_other_byte(tmp_path):
    root = _copy(tmp_path)
    before = (root / P["03_ready_cleared"]).read_text()
    after = cortex.edit_header(before, {"State": "submitted"})
    assert after.replace("State: submitted", "State: ready") == before
    # a removed key drops exactly one line; an inserted key lands at its slot
    removed = cortex.edit_header(before, {"Gates-cleared": None})
    assert removed == before.replace("Gates-cleared: 2026-08-30\n", "")
    inserted = cortex.edit_header(removed, {"Gate-override": "why"})
    lines = inserted.splitlines()
    assert lines[lines.index("Gates: PyAutoGalaxy#486") + 1] == "Gate-override: why"


def test_run_line_regex_matches_reference_examples():
    for line in (
        "- 342091_[0-8,10]: done — gpu — submitted 2026-08-30 — wall 6:12",
        "- 342091_9: failed — gpu — submitted 2026-08-30 — wall 0:00 — OOM before the first step",
        "- 342102: running — gpu — submitted 2026-09-01 — wall 0:00 — task 9 resubmitted alone",
    ):
        assert cortex.RUN_LINE_RE.match(line), line
    assert cortex.RUN_CONT_RE.match("    after: 342091_9")
    assert not cortex.RUN_CONT_RE.match("  after: 342091_9")
    assert not cortex.RUN_LINE_RE.match("- 342102: running — GPU — submitted 2026-09-01 — wall 0:00")


def test_double_dash_is_read_as_the_em_dash(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["06_pulled"], " — gpu — submitted 2026-08-31 — wall 3:40 — ",
          " -- gpu -- submitted 2026-08-31 -- wall 3:40 -- ")
    assert _problems(root) == []


def test_gate_ref_regex_rejects_owner_repo_form():
    assert cortex.GATE_REF_RE.fullmatch("PyAutoArray#431")
    assert cortex.GATE_REF_RE.fullmatch("https://github.com/PyAutoLabs/PyAutoFit/pull/1436")
    assert not cortex.GATE_REF_RE.fullmatch("PyAutoLabs/PyAutoArray#431")
    assert cortex.gate_url("PyAutoArray#431") == "https://github.com/PyAutoLabs/PyAutoArray/issues/431"
    assert cortex.gate_url("https://github.com/o/r/pull/7") == "https://github.com/o/r/issues/7"


# --------------------------------------------------------------------------- #
# projects.yaml — the restricted subset
# --------------------------------------------------------------------------- #
def test_comment_only_projects_yaml_parses_to_an_empty_map():
    rows, problems = cortex.parse_projects((REPO / "projects.yaml").read_text())
    assert rows == {} and problems == []
    rows, problems = cortex.parse_projects((EMPTY / "projects.yaml").read_text())
    assert rows == {} and problems == []


def test_projects_parse_matches_pyyaml_on_the_fixture():
    yaml = pytest.importorskip("yaml")
    text = (SKELETON / "projects.yaml").read_text()
    rows, problems = cortex.parse_projects(text)
    assert problems == []
    assert yaml.safe_load(text) == rows


def test_projects_quoted_scalars_and_comments():
    text = ('p:\n  remote: none\n  local_path: "/a: b"   # trailing\n  ral_root: /r\n'
            '  mirror: none\n  sync_cli: "x # y"\n  sync_verbs: [pull]\n  ledger: l\n'
            '  witness_file: "**/*.json"\n  partition: gpu\n  status: active\n')
    rows, problems = cortex.parse_projects(text)
    assert problems == []
    assert rows["p"]["local_path"] == "/a: b"
    assert rows["p"]["sync_cli"] == "x # y"
    assert rows["p"]["sync_verbs"] == ["pull"]
    yaml = pytest.importorskip("yaml")
    assert yaml.safe_load(text) == rows


def test_unknown_projects_field_is_an_error(tmp_path):
    root = _copy(tmp_path)
    _edit(root, "projects.yaml", "  status: active\n", "  status: active\n  colour: blue\n")
    _assert_drift(root, "projects.yaml:15: unknown field `colour` on example")


def test_missing_projects_field_and_bad_enums(tmp_path):
    root = _copy(tmp_path)
    _edit(root, "projects.yaml", "  partition: gpu\n", "  partition: cpu\n")
    _edit(root, "projects.yaml", "  ledger: wiki/project/state.md\n", "")
    _assert_drift(root, "example is missing ledger", "partition must be gpu | ral | both")


def test_projects_outside_the_subset(tmp_path):
    root = _copy(tmp_path)
    _edit(root, "projects.yaml", "  sync_verbs: [pull, submit, jobs, tail]\n",
          "  sync_verbs:\n    - pull\n")
    _assert_drift(root, "sync_verbs must be a flow list", "outside the subset")


# --------------------------------------------------------------------------- #
# check — phases
# --------------------------------------------------------------------------- #
def test_duplicate_phase_number(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["02_gated_on_dev"], "Phase: 2\n", "Phase: 1\n")
    _assert_drift(root, "02_gated_on_dev.md: duplicate Phase: 1 (also phases/example/01_scope.md)")


def test_unknown_project(tmp_path):
    root = _copy(tmp_path)
    shutil.move(root / "phases" / "example", root / "phases" / "other")
    for p in (root / "phases" / "other").glob("*.md"):
        p.write_text(p.read_text().replace("Project: example", "Project: other"))
    _assert_drift(root, "phases/other/01_scope.md: Project: other is not a projects.yaml key")


def test_directory_must_equal_project(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["01_scope"], "Project: example\n", "Project: sample\n")
    _assert_drift(root, "01_scope.md: Project: sample is not the directory name example",
                  "01_scope.md: Project: sample is not a projects.yaml key")


def test_illegal_state_unknown_key_and_missing_section(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["01_scope"], "State: planned\n", "State: queued\nGate-cleared: x\n")
    _edit(root, P["01_scope"], "## Where to look", "## Where")
    _assert_drift(root, "State: 'queued' is not a phase state", "unknown header key Gate-cleared:",
                  "missing section ## Where to look")


def test_owner_repo_gate_form_is_refused(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["02_gated_on_dev"], "Gates: PyAutoArray#431,", "Gates: PyAutoLabs/PyAutoArray#431,")
    _assert_drift(root, "Gates: unrecognised ref 'PyAutoLabs/PyAutoArray#431'")


def test_gated_with_empty_gates(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["02_gated_on_dev"], "Gates: PyAutoArray#431, https://github.com/PyAutoLabs/PyAutoFit/pull/1436\n",
          "Gates:\n")
    _assert_drift(root, "02_gated_on_dev.md: State: gated with an empty Gates:")


@pytest.mark.parametrize("rel,line", [
    (P["03_ready_cleared"], "Gates-cleared: 2026-08-30\n"),
    (P["04_submitted_override"], "Gate-override: the fix is verified locally on the branch; not waiting for the merge\n"),
    (P["08_accepted"], "Gates-cleared: 2026-08-25\n"),
])
def test_gates_invariant_needs_cleared_or_override(tmp_path, rel, line):
    root = _copy(tmp_path)
    _edit(root, rel, line, "")
    _assert_drift(root, f"{rel}: State: {_fields(root, rel)['State']} with Gates: needs "
                        "Gates-cleared: or Gate-override:")


def test_rerun_is_inside_the_gates_invariant(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["09_rerun"], "Budget: 8:00\n", "Budget: 8:00\nGates: PyAutoLens#1\n")
    _assert_drift(root, "09_rerun.md: State: rerun with Gates: needs Gates-cleared: or Gate-override:")


@pytest.mark.parametrize("rel", [P["04_submitted_override"], P["05_running_array"], P["06_pulled"],
                                 P["07_awaiting_ruling"], P["08_accepted"], P["09_rerun"]])
def test_witness_invariant(tmp_path, rel):
    root = _copy(tmp_path)
    witness = _fields(root, rel)["Witness"]
    _edit(root, rel, f"Witness: {witness}\n", "Witness:\n")
    _assert_drift(root, f"{rel}: State: {_fields(root, rel)['State']} needs a Witness:")


def test_planned_phase_may_leave_the_witness_empty():
    assert _fields(SKELETON, P["01_scope"])["Witness"] == ""
    assert _problems(SKELETON) == []


@pytest.mark.parametrize("rel,rid", [(P["08_accepted"], "R-20260901-02"),
                                     (P["09_rerun"], "R-20260901-04"),
                                     (P["10_dropped"], "R-20260901-05")])
def test_ruled_states_need_a_ruling(tmp_path, rel, rid):
    root = _copy(tmp_path)
    _edit(root, rel, f"Ruling: {rid}\n", "Ruling:\n")
    _assert_drift(root, f"{rel}: State: {_fields(root, rel)['State']} needs a Ruling:")


def test_header_body_run_mismatch(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["04_submitted_override"], "Runs: 342001, 342010\n", "Runs: 342001\n")
    _assert_drift(root, "04_submitted_override.md: Runs: header {342001} != body stems {342001, 342010}")


def test_overlapping_task_sets_on_one_stem(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["05_running_array"], "- 342091_9: failed", "- 342091_[7-9]: failed")
    _assert_drift(root, "05_running_array.md: run 342091_[0-8,10] overlaps 342091_[7-9] on stem 342091")


def test_bare_stem_overlaps_every_task_of_that_stem(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["05_running_array"], "- 342091_9: failed", "- 342091: failed")
    _assert_drift(root, "run 342091_[0-8,10] overlaps 342091 on stem 342091")


def test_one_array_may_feed_two_phases():
    """Job ids are unique per phase, not globally: 342120 sits in phases 6 and 7."""
    assert _fields(SKELETON, P["06_pulled"])["Runs"] == "342120"
    assert "342120" in _fields(SKELETON, P["07_awaiting_ruling"])["Runs"]
    assert _problems(SKELETON) == []


def test_run_line_that_does_not_parse_and_stray_continuation(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["06_pulled"], "- 342120_[0-4]: done — gpu — submitted 2026-08-31 — wall 3:40",
          "- 342120_[0-4]: done — gpu — 2026-08-31 — wall 3:40")
    _edit(root, P["04_submitted_override"], "## Runs\n\n", "## Runs\n\n    after: 1\n")
    _assert_drift(root, "06_pulled.md: line 28: run line does not parse",
                  "04_submitted_override.md: line 30: continuation line without a run line")


def test_pulled_needs_a_pulled_to(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["06_pulled"], "    pulled_to: /mnt/c/Users/Jammy/Science/example/output/phase_06\n", "")
    _assert_drift(root, "06_pulled.md: State: pulled needs at least one done | legacy run with pulled_to:")


def test_legacy_needs_where(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["10_dropped"], "    where: /mnt/c/Users/Jammy/Science/example/output/legacy_wrong/phase_10\n", "")
    _assert_drift(root, "10_dropped.md: run 341950_[0-3] is legacy_wrong without where:")


def test_after_and_resumes_name_a_run_of_the_same_phase(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["05_running_array"], "    after: 342091_9", "    after: 342091")
    _edit(root, P["07_awaiting_ruling"], "    resumes: 342110", "    resumes: 342120_[5-9]")
    _assert_drift(root, "05_running_array.md: run 342102 after: 342091 names no other run of this phase",
                  "07_awaiting_ruling.md: run 342120_[5-9] resumes: 342120_[5-9] names no other run")


def test_ruled_continuation_must_resolve(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["08_accepted"], "    ruled: R-20260901-02", "    ruled: R-20260901-09")
    _assert_drift(root, "08_accepted.md: run 342050 ruled: R-20260901-09 does not resolve to a ruling file")


def test_pulled_with_a_live_run_needs_leave_to_finish(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["05_running_array"], "State: running\n", "State: pulled\n")
    assert _problems(root) == []  # R-20260901-03 is a leave-to-finish head
    _edit(root, P["05_running_array"], "Ruling: R-20260901-03\n", "Ruling:\n")
    _assert_drift(root, "05_running_array.md: State: pulled with a live run needs a leave-to-finish ruling head")


def test_stray_file_under_phases(tmp_path):
    root = _copy(tmp_path)
    (root / "phases" / "notes.md").write_text("# stray\n")
    _assert_drift(root, "phases/notes.md: not a phase path")


# --------------------------------------------------------------------------- #
# check — rulings and chains
# --------------------------------------------------------------------------- #
R = "rulings/2026/09/"


def test_dangling_supersedes(tmp_path):
    root = _copy(tmp_path)
    _edit(root, R + "R-20260901-02.md", "Supersedes: R-20260901-01\n", "Supersedes: R-20260831-01\n")
    _assert_drift(root, "R-20260901-02.md: Supersedes: R-20260831-01 does not resolve to a ruling file")


def test_self_supersedes(tmp_path):
    root = _copy(tmp_path)
    _edit(root, R + "R-20260901-02.md", "Supersedes: R-20260901-01\n", "Supersedes: R-20260901-02\n")
    _assert_drift(root, "R-20260901-02.md: Supersedes: itself")


def test_supersedes_must_be_earlier_and_same_phase(tmp_path):
    root = _copy(tmp_path)
    _edit(root, R + "R-20260901-01.md", "Ruling: accept\n", "Ruling: accept\nSupersedes: R-20260901-03\n")
    _assert_drift(root, "R-20260901-01.md: Supersedes: R-20260901-03 is not earlier than R-20260901-01",
                  "R-20260901-01.md: Supersedes: R-20260901-03 names a different project/phase")


def test_duplicate_successor_is_a_tree_not_a_chain(tmp_path):
    root = _copy(tmp_path)
    _edit(root, R + "R-20260901-03.md", "Ruling: leave-to-finish\n",
          "Ruling: leave-to-finish\nSupersedes: R-20260901-01\n")
    _assert_drift(root, "R-20260901-01.md: has 2 successors (R-20260901-02, R-20260901-03) — a chain, not a tree")


def test_superseded_ruling_as_phase_head(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["08_accepted"], "Ruling: R-20260901-02\n", "Ruling: R-20260901-01\n")
    _assert_drift(root, "08_accepted.md: Ruling: R-20260901-01 is not a chain head (superseded by R-20260901-02)")


def test_phase_ruling_must_name_that_phase(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["09_rerun"], "Ruling: R-20260901-04\n", "Ruling: R-20260901-05\n")
    _assert_drift(root, "09_rerun.md: Ruling: R-20260901-05 names phases/example/10_dropped.md, not this phase",
                  "09_rerun.md: Ruling: R-20260901-05 verb 'drop' does not fit State: rerun")


def test_verb_state_mismatch(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["08_accepted"], "State: accepted\n", "State: awaiting-ruling\n")
    _assert_drift(root, "08_accepted.md: Ruling: R-20260901-02 verb 'accept' does not fit State: awaiting-ruling")


def test_ruling_id_filename_title_and_directory(tmp_path):
    root = _copy(tmp_path)
    _edit(root, R + "R-20260901-05.md", "# R-20260901-05 — drop", "# R-20260901-06 — drop")
    (root / "rulings" / "2026" / "08").mkdir()
    shutil.copy(root / R / "R-20260901-04.md", root / "rulings" / "2026" / "08" / "R-20260901-04.md")
    (root / "rulings" / "2026" / "stray.md").write_text("# stray\n")
    _assert_drift(root, "R-20260901-05.md: title must be `# R-20260901-05`",
                  "rulings/2026/08/R-20260901-04.md: filed under 2026/08 but the id is dated 2026-09",
                  "duplicate ruling id R-20260901-04",
                  "rulings/2026/stray.md: not a ruling path")


def test_ruling_runs_subset_phase_path_verb_and_batch(tmp_path):
    root = _copy(tmp_path)
    _edit(root, R + "R-20260901-03.md", "Runs: 342091, 342102\n", "Runs: 342091, 342999\n")
    _edit(root, R + "R-20260901-03.md", "Batch: 2026-09-01-pm\n", "Batch: 2026-09-01-am\n")
    _edit(root, R + "R-20260901-04.md", "Ruling: rerun\n", "Ruling: redo\n")
    _edit(root, R + "R-20260901-05.md", "Phase: phases/example/10_dropped.md\n", "Phase: phases/example/11.md\n")
    _assert_drift(root, "R-20260901-03.md: Runs: {342999} not in the phase's runs",
                  "R-20260901-03.md: Batch: 2026-09-01-am names no batches/2026-09-01-am.md",
                  "R-20260901-04.md: Ruling: 'redo' is not a ruling verb",
                  "R-20260901-05.md: Phase: phases/example/11.md does not resolve to a phase file")


def test_ruling_follow_up_uses_the_gate_grammar(tmp_path):
    root = _copy(tmp_path)
    _edit(root, R + "R-20260901-02.md", "Follow-ups: PyAutoLens#901\n", "Follow-ups: PyAutoLabs/PyAutoLens#901\n")
    _assert_drift(root, "R-20260901-02.md: Follow-ups: unrecognised ref 'PyAutoLabs/PyAutoLens#901'")


def test_two_chains_of_one_on_a_phase_are_fine(tmp_path):
    """leave-to-finish then accept need not chain; Supersedes: replaces, never sequences."""
    root = _copy(tmp_path)
    _move(root, P["05_running_array"], "pulled", "--partial")
    _move(root, P["05_running_array"], "awaiting-ruling")
    r = _run("rule", P["05_running_array"], "accept", "--body", str(_body(tmp_path)),
             "--today", TODAY, root=root)
    assert r.returncode == 0, r.stderr
    assert _problems(root) == []
    assert _fields(root, P["05_running_array"])["Ruling"] == "R-20260902-01"
    assert "Supersedes" not in _fields(root, "rulings/2026/09/R-20260902-01.md")


# --------------------------------------------------------------------------- #
# check — batches and reviews
# --------------------------------------------------------------------------- #
B = "batches/2026-09-01-pm.md"
V = "batches/reviews/2026-09-01-pm.md"


def test_batch_member_lines(tmp_path):
    root = _copy(tmp_path)
    _edit(root, B, "  - 06_pulled: phases/example/06_pulled.md — 342120 — 5 — pulled",
          "  - 06_pull: phases/example/06_pulled.md — 342120, 1 — five — parked")
    _edit(root, B, "  - 09_rerun: phases/example/09_rerun.md — 341900 — 5 — awaiting-ruling",
          "  - 09_rerun: phases/example/09_rerun.md — 341900 — 5")
    _edit(root, B, "  - 10_dropped: phases/example/10_dropped.md", "  - 10_dropped: phases/example/10_drop.md")
    _assert_drift(root, "2026-09-01-pm.md: member slug '06_pull' != phase stem '06_pulled'",
                  "member 06_pull: runs {1} not in the phase's runs",
                  "member 06_pull: review-minutes 'five' is not an integer",
                  "member 06_pull: state 'parked' is not a phase state",
                  "line 12: member line does not parse",
                  "member 10_dropped: phases/example/10_drop.md does not exist")


def test_review_grammar(tmp_path):
    root = _copy(tmp_path)
    _edit(root, V, "## 10_dropped — FAILED", "## 10_dropped — BROKEN")
    _edit(root, V, "## 09_rerun — SUSPECT\n- decision: rerun", "## 09_rerun — SUSPECT\n- decision: tweak")
    _edit(root, V, "## 08_accepted — HEALTHY\n- decision: accept\n- ruled: yes",
          "## 08_accepted — HEALTHY\n- decision: accept\n- ruled: maybe")
    _edit(root, V, "## 06_pulled — HEALTHY\n- decision: (none)\n- ruled: no",
          "## 06_pulled — HEALTHY\n- decision: (none)\n- ruled: yes")
    _edit(root, V, "## 05_running_array — RUNNING", "## 05_running — RUNNING")
    _assert_drift(root, "10_dropped: health 'BROKEN' not in HEALTHY | SUSPECT | FAILED | RUNNING",
                  "09_rerun: decision 'tweak' is not a ruling verb or (none)",
                  "08_accepted: ruled 'maybe' is not yes | no",
                  "06_pulled: ruled: yes needs a verb, not (none)",
                  "section '05_running' names no member of batches/2026-09-01-pm.md")


def test_review_title_and_record_must_exist(tmp_path):
    root = _copy(tmp_path)
    shutil.move(root / V, root / "batches" / "reviews" / "2026-09-01-am.md")
    _assert_drift(root, "2026-09-01-am.md: title must be `# Batch review 2026-09-01-am`",
                  "2026-09-01-am.md: no batch record batches/2026-09-01-am.md",
                  "2026-09-01-pm.md: review: batches/reviews/2026-09-01-pm.md does not exist")


# --------------------------------------------------------------------------- #
# move — every legal transition, every refused one
# --------------------------------------------------------------------------- #
def test_planned_to_gated_or_ready_by_gates(tmp_path):
    root = _copy(tmp_path)
    r = _move(root, P["01_scope"], "gated")
    assert r.returncode == 1 and "Gates: is empty — planned → ready" in r.stderr
    r = _move(root, P["01_scope"], "ready")
    assert r.returncode == 0 and r.stdout.strip() == "phases/example/01_scope.md: planned → ready"
    assert _fields(root, P["01_scope"])["State"] == "ready"
    _edit(root, P["01_scope"], "State: ready\nGates:\n", "State: planned\nGates: PyAutoLens#1\n")
    r = _move(root, P["01_scope"], "ready")
    assert r.returncode == 1 and "Gates: is non-empty — planned → gated" in r.stderr
    assert _move(root, P["01_scope"], "gated").returncode == 0
    assert _problems(root) == []


def test_gated_to_ready_needs_override_or_gates_write(tmp_path):
    root = _copy(tmp_path)
    r = _move(root, P["02_gated_on_dev"], "ready")
    assert r.returncode == 1 and "gates --grade --write" in r.stderr and "--override" in r.stderr
    r = _move(root, P["02_gated_on_dev"], "ready", "--override", "verified on the branch")
    assert r.returncode == 0
    f = _fields(root, P["02_gated_on_dev"])
    assert f["State"] == "ready" and f["Gate-override"] == "verified on the branch"
    assert _problems(root) == []


def test_ready_to_gated_is_gates_write_only(tmp_path):
    root = _copy(tmp_path)
    r = _move(root, P["03_ready_cleared"], "gated")
    assert r.returncode == 1 and "gates --grade --write" in r.stderr


def test_ready_to_submitted_needs_witness_and_run(tmp_path):
    root = _copy(tmp_path)
    r = _move(root, P["03_ready_cleared"], "submitted")
    assert r.returncode == 1 and "--run" in r.stderr
    _edit(root, P["03_ready_cleared"], "Witness: anchor lens theta_E within 0.01 arcsec of the published value\n",
          "Witness:\n")
    r = _move(root, P["03_ready_cleared"], "submitted", "--run", "350000")
    assert r.returncode == 1 and "Witness: is empty" in r.stderr
    _edit(root, P["03_ready_cleared"], "Witness:\n", "Witness: theta_E within 0.01\n")
    before = (root / P["03_ready_cleared"]).read_text()
    r = _move(root, P["03_ready_cleared"], "submitted", "--run", "350000", "--note", "first wave")
    assert r.returncode == 0, r.stderr
    after = (root / P["03_ready_cleared"]).read_text()
    assert "- 350000: submitted — gpu — submitted 2026-09-02 — wall 0:00 — first wave\n" in after
    f = _fields(root, P["03_ready_cleared"])
    assert f["State"] == "submitted" and f["Runs"] == "350000"
    # the body outside `## Runs` and the rest of the header are untouched
    assert after.split("## Runs")[0].replace("State: submitted", "State: ready") \
        .replace("Runs: 350000\n", "") == before.split("## Runs")[0]
    assert after.split("## Ruling")[1] == before.split("## Ruling")[1]
    assert _problems(root) == []


def test_run_self_loop_appends_a_wave_and_keeps_state(tmp_path):
    root = _copy(tmp_path)
    r = _move(root, P["04_submitted_override"], "submitted", "--run", "342020", "--after", "342010")
    assert r.returncode == 0 and "appended run 342020" in r.stdout
    text = (root / P["04_submitted_override"]).read_text()
    assert "- 342020: submitted — gpu — submitted 2026-09-02 — wall 0:00\n    after: 342010\n" in text
    f = _fields(root, P["04_submitted_override"])
    assert f["State"] == "submitted" and f["Runs"] == "342001, 342010, 342020"
    r = _move(root, P["05_running_array"], "running", "--run", "342103", "--resumes", "342091_9")
    assert r.returncode == 0
    assert _fields(root, P["05_running_array"])["State"] == "running"
    assert _problems(root) == []


def test_run_self_loop_refuses_overlap_and_dangling_after(tmp_path):
    root = _copy(tmp_path)
    r = _move(root, P["05_running_array"], "running", "--run", "342091_[9-10]")
    assert r.returncode == 1 and "overlaps" in r.stderr
    r = _move(root, P["05_running_array"], "running", "--run", "342200", "--after", "999")
    assert r.returncode == 1 and "names no run of this phase" in r.stderr
    r = _move(root, P["03_ready_cleared"], "ready", "--run", "1")
    assert r.returncode == 1 and "already ready" in r.stderr


def test_submitted_to_running_and_back_to_ready(tmp_path):
    root = _copy(tmp_path)
    assert _move(root, P["04_submitted_override"], "running").returncode == 0
    r = _move(root, P["04_submitted_override"], "ready", "--reason", "node failure")
    assert r.returncode == 1 and "still submitted | running" in r.stderr
    _edit(root, P["04_submitted_override"], "- 342010: submitted", "- 342010: failed")
    r = _move(root, P["04_submitted_override"], "ready")
    assert r.returncode == 1 and "--reason" in r.stderr
    r = _move(root, P["04_submitted_override"], "ready", "--reason", "both waves died on node failure")
    assert r.returncode == 0, r.stderr
    f = _fields(root, P["04_submitted_override"])
    assert f["State"] == "ready" and f["Reset"] == "both waves died on node failure"
    assert _problems(root) == []
    # a phase whose runs all succeeded has nothing to reset from
    _edit(root, P["03_ready_cleared"], "State: ready\n", "State: running\n")
    _edit(root, P["03_ready_cleared"], "## Runs\n\n", "## Runs\n\n- 1: done — gpu — submitted 2026-09-01 — wall 1:00\n")
    _edit(root, P["03_ready_cleared"], "Runs:\n", "Runs: 1\n") if "Runs:" in (root / P["03_ready_cleared"]).read_text() \
        else _edit(root, P["03_ready_cleared"], "Budget: 5:00\n", "Budget: 5:00\nRuns: 1\n")
    r = _move(root, P["03_ready_cleared"], "ready", "--reason", "x")
    assert r.returncode == 1 and "no failed | timeout | void run" in r.stderr


def test_running_to_pulled_and_partial(tmp_path):
    root = _copy(tmp_path)
    r = _move(root, P["05_running_array"], "pulled")
    assert r.returncode == 1 and "--partial" in r.stderr
    r = _move(root, P["05_running_array"], "pulled", "--partial")
    assert r.returncode == 0
    assert _problems(root) == []  # the leave-to-finish head closes the partial pull
    _edit(root, P["05_running_array"], "- 342102: running", "- 342102: done")
    _edit(root, P["05_running_array"], "State: pulled\n", "State: running\n")
    assert _move(root, P["05_running_array"], "pulled").returncode == 0


def test_running_to_pulled_writes_pulled_to(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["04_submitted_override"], "State: submitted\n", "State: running\n")
    _edit(root, P["04_submitted_override"], "- 342010: submitted", "- 342010: done")
    r = _move(root, P["04_submitted_override"], "pulled")
    assert r.returncode == 1 and "--pulled-to" in r.stderr
    r = _move(root, P["04_submitted_override"], "pulled", "--pulled-to", "/mnt/c/out/phase_04")
    assert r.returncode == 0, r.stderr
    text = (root / P["04_submitted_override"]).read_text()
    assert "- 342010: done — gpu — submitted 2026-09-01 — wall 0:00\n    pulled_to: /mnt/c/out/phase_04\n" in text
    assert "- 342001: failed — gpu — submitted 2026-08-31 — wall 0:00 — node failure before the first step\n- 342010" in text
    assert _problems(root) == []


def test_pulled_to_awaiting_ruling_and_rerun_to_ready(tmp_path):
    root = _copy(tmp_path)
    assert _move(root, P["06_pulled"], "awaiting-ruling").returncode == 0
    assert _move(root, P["09_rerun"], "ready").returncode == 0
    assert _problems(root) == []


def test_legacy_born_ready_to_pulled(tmp_path):
    root = _copy(tmp_path)
    _edit(root, P["09_rerun"], "State: rerun\nWitness: the legacy run's mask edge matches the released mask within one pixel\n",
          "State: ready\nWitness:\n")
    r = _move(root, P["09_rerun"], "pulled")
    assert r.returncode == 1 and "Witness: is empty" in r.stderr
    _edit(root, P["09_rerun"], "Witness:\n", "Witness: mask edge within one pixel\n")
    assert _move(root, P["09_rerun"], "pulled").returncode == 0
    _edit(root, P["09_rerun"], "State: pulled\n", "State: ready\n")
    _edit(root, P["09_rerun"], "- 341900: legacy", "- 341900: done")
    r = _move(root, P["09_rerun"], "pulled")
    assert r.returncode == 1 and "legacy-born" in r.stderr


@pytest.mark.parametrize("rel,to,needle", [
    (P["07_awaiting_ruling"], "accepted", "rule <phase> accept"),
    (P["07_awaiting_ruling"], "rerun", "rule <phase> rerun"),
    (P["07_awaiting_ruling"], "dropped", "rule <phase> drop"),
    (P["01_scope"], "dropped", "rule <phase> drop"),
    (P["08_accepted"], "rerun", "--supersedes"),
    (P["10_dropped"], "ready", "terminal"),
    (P["04_submitted_override"], "pulled", "no edge submitted → pulled"),
    (P["03_ready_cleared"], "running", "no edge ready → running"),
    (P["06_pulled"], "ready", "no edge pulled → ready"),
    (P["01_scope"], "flying", "not a phase state"),
])
def test_refused_edges(tmp_path, rel, to, needle):
    root = _copy(tmp_path)
    before = (root / rel).read_text()
    r = _move(root, rel, to)
    assert r.returncode == 1, r.stdout
    assert needle in r.stderr, r.stderr
    assert (root / rel).read_text() == before


# --------------------------------------------------------------------------- #
# rule
# --------------------------------------------------------------------------- #
def _rule(root, rel, verb, body, *extra, today=TODAY):
    return _run("rule", rel, verb, "--body", str(body), "--today", today, *extra, root=root)


def test_rule_assigns_ids_in_sequence_and_moves_the_phase(tmp_path):
    root = _copy(tmp_path)
    body = _body(tmp_path)
    r = _rule(root, P["07_awaiting_ruling"], "accept", body, "--batch", "2026-09-01-pm",
              "--minutes", "4", "--follow-up", "PyAutoLens#902")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "wrote rulings/2026/09/R-20260902-01.md"
    rf = _fields(root, "rulings/2026/09/R-20260902-01.md")
    assert rf["Phase"] == P["07_awaiting_ruling"] and rf["Ruling"] == "accept"
    assert rf["Runs"] == "342110, 342120" and rf["Batch"] == "2026-09-01-pm"
    assert rf["Review-minutes-actual"] == "4" and rf["Follow-ups"] == "PyAutoLens#902"
    assert rf["Reviewed-at"].startswith("2026-09-02T")
    text = (root / "rulings/2026/09/R-20260902-01.md").read_text()
    assert text.startswith("# R-20260902-01 — accept example phase 7\n")
    assert "## Ruling\n\nAccept. The human's words, verbatim.\n\n## Evidence\n\n- " in text
    pf = _fields(root, P["07_awaiting_ruling"])
    assert pf["State"] == "accepted" and pf["Ruling"] == "R-20260902-01"
    assert "R-20260902-01 — accept" in (root / P["07_awaiting_ruling"]).read_text().split("## Ruling")[1]
    assert _problems(root) == []
    # the second ruling of the day is -02
    _move(root, P["06_pulled"], "awaiting-ruling")
    r = _rule(root, P["06_pulled"], "rerun", body)
    assert r.stdout.strip() == "wrote rulings/2026/09/R-20260902-02.md"
    assert _fields(root, P["06_pulled"])["State"] == "rerun"
    assert _problems(root) == []


def test_rule_supersedes_an_accepted_ruling(tmp_path):
    root = _copy(tmp_path)
    body = _body(tmp_path, "REWIND: the gates were wrong.\n")
    r = _rule(root, P["08_accepted"], "rerun", body)
    assert r.returncode == 1 and "--supersedes R-20260901-02" in r.stderr
    r = _rule(root, P["08_accepted"], "rerun", body, "--supersedes", "R-20260901-01")
    assert r.returncode == 1 and "already has a successor" in r.stderr
    r = _rule(root, P["08_accepted"], "accept", body, "--supersedes", "R-20260901-02")
    assert r.returncode == 1 and "only rerun | drop" in r.stderr
    r = _rule(root, P["08_accepted"], "rerun", body, "--supersedes", "R-20260901-02")
    assert r.returncode == 0, r.stderr
    rf = _fields(root, "rulings/2026/09/R-20260902-01.md")
    assert rf["Supersedes"] == "R-20260901-02"
    pf = _fields(root, P["08_accepted"])
    assert pf["State"] == "rerun" and pf["Ruling"] == "R-20260902-01"
    assert _problems(root) == []


def test_rule_also_fans_out_with_one_batch(tmp_path):
    root = _copy(tmp_path)
    body = _body(tmp_path, "Drop the lot.\n")
    _move(root, P["06_pulled"], "awaiting-ruling")
    r = _rule(root, P["07_awaiting_ruling"], "drop", body, "--batch", "2026-09-01-pm",
              "--also", P["06_pulled"], "--also", P["08_accepted"], "--also", P["01_scope"])
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines() == [f"wrote rulings/2026/09/R-20260902-0{n}.md" for n in (1, 2, 3, 4)]
    for n, rel in ((1, P["07_awaiting_ruling"]), (2, P["06_pulled"]), (3, P["08_accepted"]), (4, P["01_scope"])):
        rf = _fields(root, f"rulings/2026/09/R-20260902-0{n}.md")
        assert rf["Batch"] == "2026-09-01-pm" and rf["Phase"] == rel and rf["Ruling"] == "drop"
        assert "Drop the lot." in (root / f"rulings/2026/09/R-20260902-0{n}.md").read_text()
        assert _fields(root, rel)["State"] == "dropped"
    # the accepted --also phase superseded its own head
    assert _fields(root, "rulings/2026/09/R-20260902-03.md")["Supersedes"] == "R-20260901-02"
    assert _problems(root) == []


def test_rule_refuses_a_verb_the_table_forbids(tmp_path):
    root = _copy(tmp_path)
    body = _body(tmp_path)
    for rel, verb, needle in (
        (P["05_running_array"], "accept", "not allowed from State: running"),
        (P["06_pulled"], "rerun", "not allowed from State: pulled"),
        (P["10_dropped"], "drop", "terminal"),
        (P["01_scope"], "leave-to-finish", "running | pulled | awaiting-ruling"),
        (P["09_rerun"], "accept", "not allowed from State: rerun"),
    ):
        before = (root / rel).read_text()
        r = _rule(root, rel, verb, body)
        assert r.returncode == 1, (rel, verb, r.stdout)
        assert needle in r.stderr, r.stderr
        assert (root / rel).read_text() == before
    assert not list((root / "rulings" / "2026" / "09").glob("R-20260902-*"))


def test_rule_leave_to_finish_keeps_state(tmp_path):
    root = _copy(tmp_path)
    r = _rule(root, P["06_pulled"], "leave-to-finish", _body(tmp_path, "Wait.\n"))
    assert r.returncode == 0, r.stderr
    f = _fields(root, P["06_pulled"])
    assert f["State"] == "pulled" and f["Ruling"] == "R-20260902-01"
    assert _problems(root) == []


def test_rule_refuses_to_touch_an_existing_ruling(tmp_path):
    root = _copy(tmp_path)
    r = _rule(root, P["07_awaiting_ruling"], "accept", _body(tmp_path), today="2026-09-01")
    assert r.returncode == 0  # -06 is free on 2026-09-01
    assert r.stdout.strip() == "wrote rulings/2026/09/R-20260901-06.md"
    existing = root / "rulings/2026/09/R-20260901-06.md"
    before = existing.read_text()
    # an id that exists somewhere unexpected is still taken
    (root / "rulings" / "2026" / "10").mkdir()
    for n in range(7, 100):
        (root / "rulings" / "2026" / "09" / f"R-20260901-{n:02d}.md").write_text("# x\n")
    _move(root, P["06_pulled"], "awaiting-ruling")
    r = _rule(root, P["06_pulled"], "accept", _body(tmp_path), today="2026-09-01")
    assert r.returncode == 1 and "99 rulings already filed" in r.stderr
    assert existing.read_text() == before


def test_rule_validates_batch_follow_up_and_body(tmp_path):
    root = _copy(tmp_path)
    body = _body(tmp_path)
    r = _rule(root, P["07_awaiting_ruling"], "accept", body, "--batch", "2026-09-09-x")
    assert r.returncode == 1 and "names no batches/2026-09-09-x.md" in r.stderr
    r = _rule(root, P["07_awaiting_ruling"], "accept", body, "--follow-up", "PyAutoLabs/PyAutoLens#1")
    assert r.returncode == 1 and "--follow-up" in r.stderr
    r = _rule(root, P["07_awaiting_ruling"], "accept", _body(tmp_path, "\n\n"))
    assert r.returncode == 1 and "--body is empty" in r.stderr
    assert _fields(root, P["07_awaiting_ruling"])["State"] == "awaiting-ruling"


# --------------------------------------------------------------------------- #
# gates
# --------------------------------------------------------------------------- #
def test_gates_offline_lists_gated_phases():
    r = _run("gates", root=SKELETON)
    assert r.returncode == 0
    assert r.stdout.splitlines() == [
        "gates: 1 phase(s)",
        "  phases/example/02_gated_on_dev.md: gated — PyAutoArray#431, "
        "https://github.com/PyAutoLabs/PyAutoFit/pull/1436",
    ]
    r = _run("gates", root=EMPTY)
    assert r.returncode == 0 and r.stdout.strip() == "gates: no gated phase"


def _pr(merged: bool, state: str = "closed"):
    return {"state": state, "state_reason": None, "merged_at": "2026-09-01T00:00:00Z" if merged else None,
            "is_pr": True}


def _issue(state: str, reason=None):
    return {"state": state, "state_reason": reason, "merged_at": None, "is_pr": False}


ARRAY = "https://github.com/PyAutoLabs/PyAutoArray/issues/431"
FIT_PR = "https://github.com/PyAutoLabs/PyAutoFit/issues/1436"
GALAXY = "https://github.com/PyAutoLabs/PyAutoGalaxy/issues/486"
LENS = "https://github.com/PyAutoLabs/PyAutoLens/issues/900"
FIT_ISSUE = "https://github.com/PyAutoLabs/PyAutoFit/issues/1400"


def _grade(root, states, write=False, today=date(2026, 9, 2)):
    lines, rc = cortex.gates_report(root, grade=True, write=write, fetch=lambda urls: states, today=today)
    return "\n".join(lines), rc


def test_grade_gate_verdicts():
    assert cortex.grade_gate(_pr(True))[0] == "cleared"
    assert cortex.grade_gate(_pr(False))[0] == "dead"
    assert cortex.grade_gate(_pr(False, "open"))[0] == "open"
    assert cortex.grade_gate(_issue("closed", "completed"))[0] == "cleared"
    assert cortex.grade_gate(_issue("closed"))[0] == "cleared"
    assert cortex.grade_gate(_issue("closed", "not_planned"))[0] == "dead"
    assert cortex.grade_gate(_issue("closed", "duplicate"))[0] == "dead"
    assert cortex.grade_gate(_issue("open"))[0] == "open"
    assert cortex.grade_gate("unreadable: HTTP 404")[0] == "unreadable"


def test_grade_reports_without_writing(tmp_path):
    root = _copy(tmp_path)
    before = (root / P["02_gated_on_dev"]).read_text()
    out, rc = _grade(root, {ARRAY: _issue("closed", "completed"), FIT_PR: _pr(True),
                            GALAXY: _issue("closed"), LENS: _issue("closed"), FIT_ISSUE: _issue("closed")})
    assert rc == 0
    assert "02_gated_on_dev.md: gated\n    PyAutoArray#431 → cleared (issue closed (completed))\n" in out
    assert "→ cleared (PR merged)" in out
    assert "verdict: cleared (gates --grade --write flips it to ready)" in out
    assert (root / P["02_gated_on_dev"]).read_text() == before


def test_grade_write_flips_gated_to_ready(tmp_path):
    root = _copy(tmp_path)
    out, rc = _grade(root, {ARRAY: _issue("closed", "completed"), FIT_PR: _pr(True),
                            GALAXY: _issue("closed"), LENS: _issue("closed"), FIT_ISSUE: _issue("closed")},
                     write=True)
    assert rc == 0 and "gated → ready, Gates-cleared: 2026-09-02" in out
    f = _fields(root, P["02_gated_on_dev"])
    assert f["State"] == "ready" and f["Gates-cleared"] == "2026-09-02"
    assert _problems(root) == []


@pytest.mark.parametrize("info,needle", [
    (_pr(False), "dead gate"),
    (_issue("closed", "not_planned"), "dead gate"),
    (_issue("open"), "verdict: waiting"),
    ("unreadable: HTTP 404", "unreadable ref — fails closed, nothing flipped"),
])
def test_grade_write_does_not_flip_dead_open_or_unreadable(tmp_path, info, needle):
    root = _copy(tmp_path)
    out, rc = _grade(root, {ARRAY: info, FIT_PR: _pr(True), GALAXY: _issue("closed"),
                            LENS: _issue("closed"), FIT_ISSUE: _issue("closed")}, write=True)
    assert needle in out
    assert _fields(root, P["02_gated_on_dev"])["State"] == "gated"
    assert rc == (1 if "unreadable" in needle else 0)


def test_grade_write_demotes_ready_on_reopen_but_not_with_override(tmp_path):
    root = _copy(tmp_path)
    states = {ARRAY: _issue("open"), FIT_PR: _pr(False, "open"), GALAXY: _issue("open"),
              LENS: _issue("open"), FIT_ISSUE: _issue("open")}
    out, rc = _grade(root, states)
    assert "03_ready_cleared.md: ready" in out and "(gates --grade --write demotes it to gated)" in out
    assert _fields(root, P["03_ready_cleared"])["State"] == "ready"
    out, rc = _grade(root, states, write=True)
    assert "03_ready_cleared.md: ready\n    PyAutoGalaxy#486 → open (issue open)\n    verdict: reopened PyAutoGalaxy#486 — ready → gated" in out
    f = _fields(root, P["03_ready_cleared"])
    assert f["State"] == "gated" and "Gates-cleared" not in f
    # submitted+ phases: reported, never enforced; override: kept ready
    assert "04_submitted_override.md: submitted\n    PyAutoLens#900 → open (issue open)\n    verdict: reopened PyAutoLens#900 — reported, never enforced past ready" in out
    assert "08_accepted.md" not in out  # accepted is not graded
    assert _fields(root, P["04_submitted_override"])["State"] == "submitted"
    _edit(root, P["03_ready_cleared"], "State: gated\n", "State: ready\nGate-override: on purpose\n")
    out, rc = _grade(root, states, write=True)
    assert "Gate-override: present, kept ready" in out
    assert _fields(root, P["03_ready_cleared"])["State"] == "ready"
    assert _problems(root) == []


def test_grade_unreadable_ready_phase_is_not_demoted(tmp_path):
    root = _copy(tmp_path)
    out, rc = _grade(root, {GALAXY: "unreadable: HTTP 500"}, write=True)
    assert rc == 1
    assert _fields(root, P["03_ready_cleared"])["State"] == "ready"


def test_gh_jq_shape_and_http_fallback_user_agent():
    assert cortex.GATE_JQ == ('{state, state_reason, merged_at: .pull_request.merged_at, '
                              'is_pr: (.pull_request != null)}')
    src = SCRIPT.read_text()
    assert '"User-Agent": "pyautocortex"' in src


# --------------------------------------------------------------------------- #
# new
# --------------------------------------------------------------------------- #
def test_new_writes_a_parseable_phase(tmp_path):
    root = _copy(tmp_path)
    r = _run("new", "example", "11_next", "--phase", "11", "--gates", "PyAutoLens#1, https://github.com/o/r/pull/2",
             "--epic", "example-programme", "--budget", "6:00", "--minutes", "5", "--witness", "a claim",
             "--today", TODAY, root=root)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "wrote phases/example/11_next.md"
    text = (root / "phases/example/11_next.md").read_text()
    assert text.startswith("# Example — phase 11: 11 next\n\nProject: example\nPhase: 11\nState: planned\n")
    f = _fields(root, "phases/example/11_next.md")
    assert f["Gates"] == "PyAutoLens#1, https://github.com/o/r/pull/2" and f["Lane"] == "local-dev"
    assert f["Filed"] == TODAY and f["Budget"] == "6:00" and f["Review-minutes"] == "5"
    for name in cortex.PHASE_SECTIONS:
        assert f"\n## {name}\n" in text
    assert _problems(root) == []
    assert _move(root, "phases/example/11_next.md", "gated").returncode == 0


def test_new_refuses_duplicates_and_unknown_projects(tmp_path):
    root = _copy(tmp_path)
    r = _run("new", "example", "03_again", "--phase", "3", root=root)
    assert r.returncode == 1 and "phase 3 already exists: phases/example/03_ready_cleared.md" in r.stderr
    r = _run("new", "example", "03_ready_cleared", "--phase", "11", root=root)
    assert r.returncode == 1 and "already exists" in r.stderr
    r = _run("new", "nobody", "x", "--phase", "1", root=root)
    assert r.returncode == 1 and "not a projects.yaml key" in r.stderr
    r = _run("new", "example", "x", "--phase", "11", "--gates", "PyAutoLabs/PyAutoLens#1", root=root)
    assert r.returncode == 1 and "no owner/Repo#N form" in r.stderr
    assert not (root / "phases/example/x.md").exists()


def test_new_legacy_born_phase_is_ready_and_pullable(tmp_path):
    root = _copy(tmp_path)
    r = _run("new", "example", "12_legacy", "--phase", "12", "--legacy-run", "300000",
             "--legacy-wrong", "300001_[0-3]", "--today", TODAY, root=root)
    assert r.returncode == 1 and "--where" in r.stderr
    r = _run("new", "example", "12_legacy", "--phase", "12", "--legacy-run", "300000",
             "--legacy-wrong", "300001_[0-3]", "--where", "/mnt/q", "--witness", "w", "--today", TODAY, root=root)
    assert r.returncode == 0, r.stderr
    f = _fields(root, "phases/example/12_legacy.md")
    assert f["State"] == "ready" and f["Runs"] == "300000, 300001"
    text = (root / "phases/example/12_legacy.md").read_text()
    assert "- 300000: legacy — gpu — submitted 2026-09-02 — wall 0:00 — pre-Cortex run, migrated\n    where: /mnt/q\n" in text
    assert "- 300001_[0-3]: legacy_wrong — gpu" in text
    assert _problems(root) == []
    assert _move(root, "phases/example/12_legacy.md", "pulled").returncode == 0
    text = (root / "phases/example/12_legacy.md").read_text()
    # the reusable run gets pulled_to: (its where:), the wrong one does not
    assert "    where: /mnt/q\n    pulled_to: /mnt/q\n- 300001_[0-3]: legacy_wrong" in text
    assert text.count("pulled_to:") == 1
    assert _problems(root) == []
    # legacy_wrong-only: nothing to pull — rule drop is the door
    r = _run("new", "example", "14", "--phase", "14", "--legacy-wrong", "2", "--where", "/q",
             "--witness", "w", root=root)
    assert r.returncode == 0, r.stderr
    r = _move(root, "phases/example/14.md", "pulled")
    assert r.returncode == 1 and "no legacy run to pull" in r.stderr
    r = _run("new", "example", "13", "--phase", "13", "--legacy-run", "1", "--where", "/q",
             "--gates", "PyAutoLens#1", root=root)
    assert r.returncode == 1 and "cannot be gated" in r.stderr


def test_partition_comes_from_the_project_row_or_the_flag(tmp_path):
    root = _copy(tmp_path)
    _edit(root, "projects.yaml", "  partition: gpu\n", "  partition: both\n")
    r = _move(root, P["03_ready_cleared"], "submitted", "--run", "1")
    assert r.returncode == 1 and "--partition" in r.stderr
    r = _move(root, P["03_ready_cleared"], "submitted", "--run", "1", "--partition", "ral")
    assert r.returncode == 0
    assert "- 1: submitted — ral — " in (root / P["03_ready_cleared"]).read_text()


def test_bad_root_and_bad_today():
    r = _run("check", root=Path("/nonexistent/tree"))
    assert r.returncode == 2
    r = _run("move", P["01_scope"], "ready", "--today", "yesterday", root=SKELETON)
    assert r.returncode == 1 and "--today must be YYYY-MM-DD" in r.stderr
