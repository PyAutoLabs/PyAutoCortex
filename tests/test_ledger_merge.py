"""Tests for scripts/ledger_merge.py — the auto-merge safety gate.

This gate decides what lands on `main` with no human in the loop, so the
properties that matter are the refusals: default deny for anything
unclassified, no traversal or dotfile route past the ledger prefixes, no
pytest-collectable file smuggled in beside a packet, every code home the repo
has (scripts/, tests/, .github/, policy/, docs/, projects.yaml, the prose
pages) staying on the human side of the line, no doctrine file (AGENTS.md,
TEMPLATE.md) riding along because it happens to sit under a ledger dir — and,
the Cortex's own addition, a MODIFIED, DELETED or RENAMED ruling never
auto-merging (rulings/ is append-only).

The one thing this gate must NOT refuse is the generated board: `dashboard.md`
and `dashboard.html` are rendered from the ledger and self-healed on main, so
they are ledger too.
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import ledger_merge  # noqa: E402

SCRIPT = Path(ledger_merge.__file__)
REPO = SCRIPT.resolve().parents[1]


def test_ledger_dirs_and_registry_files_are_ledger():
    for path in (
        "phases/example/01_scope.md",
        "phases/newproject/01_first.md",
        "rulings/2026/09/R-20260901-01.md",
        "batches/2026-09-01-pm.md",
        "batches/reviews/2026-09-01-pm.md",
        "epics.md",
        # generated from the ledger, self-healed on main by dashboard_refresh.yml
        "dashboard.md",
        "dashboard.html",
    ):
        assert ledger_merge.is_ledger_path(path), path


def test_every_code_home_needs_a_human():
    for path in (
        "scripts/cortex.py",
        "scripts/ledger_merge.py",
        "tests/test_cortex.py",
        "tests/fixtures/skeleton/phases/example/01_scope.md",
        ".github/workflows/ledger_merge.yml",
        ".github/workflows/cortex_check.yml",
        ".github/workflows/dashboard_refresh.yml",
        ".github/workflows/pages_dashboard.yml",
        ".gitignore",
        ".claude/settings.json",
        ".claude/hooks/session-start.sh",
        "policy/never_rewrite_history.md",
        "docs/schema_decisions.md",
        # CODE: sync_cli and local_path are paths the conductor executes under.
        "projects.yaml",
        "README.md",
        "AGENTS.md",
        "CLAUDE.md",
        "REFERENCE.md",
        "LICENSE",
    ):
        assert not ledger_merge.is_ledger_path(path), path


def test_unclassified_paths_default_to_deny():
    """A root file or top-level folder nobody has thought about is code."""
    for path in ("brand_new_root_file.md", "newfolder/thing.md", "notes.txt", "skills/x/SKILL.md"):
        assert not ledger_merge.is_ledger_path(path), path


def test_traversal_cannot_smuggle_code_behind_a_ledger_prefix():
    for path in ("phases/../scripts/evil.py", "rulings/../../etc/passwd", ".."):
        assert not ledger_merge.is_ledger_path(path), path


def test_dot_paths_are_never_ledger_wherever_they_sit():
    for path in ("phases/.github/workflows/x.yml", "batches/.hidden", ".phases/x.md"):
        assert not ledger_merge.is_ledger_path(path), path


def test_inert_assets_ride_along_but_collectable_tests_do_not():
    assert ledger_merge.is_ledger_path("batches/reviews/2026-09-01-pm.md")
    for path in (
        "batches/conftest.py",
        "phases/example/test_thing.py",
        "rulings/2026/09/thing_test.py",
    ):
        assert not ledger_merge.is_ledger_path(path), path


def test_doctrine_under_a_ledger_dir_needs_a_human():
    """A ledger dir holds entries; `AGENTS.md` and `TEMPLATE.md` inside one are
    not entries, they are the doctrine that says what an entry may be and the
    template every future entry is stamped from. A branch that could auto-merge
    `rulings/AGENTS.md` could edit the rule governing its own merge."""
    for path in (
        "rulings/AGENTS.md",
        "batches/AGENTS.md",
        "batches/reviews/AGENTS.md",
        # by name, not by that fixed list — a doctrine file in a dir nobody has
        # created yet is code on the day it appears
        "phases/example/AGENTS.md",
    ):
        assert not ledger_merge.is_ledger_path(path), path
    # ordinary entries beside them still merge
    assert ledger_merge.is_ledger_path("batches/2026-09-01-pm.md")
    assert ledger_merge.is_ledger_path("batches/reviews/2026-09-01-pm.md")


def test_every_tracked_file_under_a_ledger_dir_gets_the_right_verdict():
    """The witness on the live tree: every tracked path under phases/, rulings/
    and batches/ is ledger unless it is doctrine."""
    out = subprocess.run(["git", "ls-files", "phases", "rulings", "batches"], cwd=REPO,
                         capture_output=True, text=True, check=True).stdout.split()
    assert out, "no ledger-dir paths tracked"
    for path in out:
        doctrine = Path(path).name in ("AGENTS.md", "TEMPLATE.md")
        assert ledger_merge.is_ledger_path(path) is not doctrine, path


def test_classify_splits_and_dedupes_preserving_order():
    ledger, blocked = ledger_merge.classify(
        ["epics.md", "scripts/x.py", "epics.md", "phases/a/b.md", "", "  "]
    )
    assert ledger == ["epics.md", "phases/a/b.md"]
    assert blocked == ["scripts/x.py"]


# --------------------------------------------------------------------------- #
# append-only rulings/ and batches/
# --------------------------------------------------------------------------- #
def test_added_ledger_of_record_is_ledger_but_any_other_status_is_code():
    """`rulings/` is append-only because a ruling is superseded, never edited;
    `batches/` joined it on 2026-09-03 when the slot apparatus was retired and
    the records became history — never modified, only added."""
    for rel in ("rulings/2026/09/R-20260901-01.md", "batches/2026-09-01-pm.md",
                "batches/reviews/2026-09-01-pm.md"):
        assert not ledger_merge.is_append_only_violation("A", rel), rel
        for status in ("M", "D", "R100", "R", "T", "C75", "U"):
            assert ledger_merge.is_append_only_violation(status, rel), (rel, status)
    # a modified phase file is still ledger — phases move, that is their job
    assert not ledger_merge.is_append_only_violation("M", "phases/example/01_scope.md")


def test_classify_entries_blocks_a_modified_ruling_or_record():
    ledger, blocked = ledger_merge.classify_entries([
        ("A", "rulings/2026/09/R-20260901-06.md"),
        ("M", "rulings/2026/09/R-20260901-01.md"),
        ("M", "phases/example/08_accepted.md"),
        ("D", "batches/2026-09-01-pm.md"),
        ("A", "scripts/new.py"),
    ])
    assert ledger == ["rulings/2026/09/R-20260901-06.md", "phases/example/08_accepted.md"]
    assert blocked == ["rulings/2026/09/R-20260901-01.md", "batches/2026-09-01-pm.md",
                       "scripts/new.py"]


def _git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True)


def _repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "t")
    (repo / "rulings" / "2026" / "09").mkdir(parents=True)
    (repo / "phases" / "p").mkdir(parents=True)
    (repo / "rulings/2026/09/R-20260901-01.md").write_text("# R-20260901-01\n\nRuling: accept\n")
    (repo / "phases/p/01_a.md").write_text("# a\n\nState: ready\n")
    (repo / "epics.md").write_text("# Epics\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")
    _git(repo, "checkout", "-q", "-b", "claude/work")
    return repo


def test_changed_entries_reads_name_status_from_git(tmp_path):
    repo = _repo(tmp_path)
    (repo / "rulings/2026/09/R-20260901-02.md").write_text("# R-20260901-02\n")
    (repo / "phases/p/01_a.md").write_text("# a\n\nState: submitted\n")
    (repo / "rulings/2026/09/R-20260901-01.md").write_text("# R-20260901-01\n\nRuling: drop\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "work")
    entries = ledger_merge.changed_entries("main", cwd=repo)
    assert sorted(entries) == [("A", "rulings/2026/09/R-20260901-02.md"),
                               ("M", "phases/p/01_a.md"),
                               ("M", "rulings/2026/09/R-20260901-01.md")]
    ledger, blocked = ledger_merge.classify_entries(entries)
    assert blocked == ["rulings/2026/09/R-20260901-01.md"]
    assert set(ledger) == {"rulings/2026/09/R-20260901-02.md", "phases/p/01_a.md"}


def test_a_renamed_or_deleted_ruling_is_code_but_added_ones_merge(tmp_path):
    repo = _repo(tmp_path)
    _git(repo, "mv", "rulings/2026/09/R-20260901-01.md", "rulings/2026/09/R-20260901-03.md")
    _git(repo, "commit", "-q", "-m", "rename")
    entries = ledger_merge.changed_entries("main", cwd=repo)
    _, blocked = ledger_merge.classify_entries(entries)
    assert "rulings/2026/09/R-20260901-01.md" in blocked
    assert "rulings/2026/09/R-20260901-03.md" in blocked
    # a branch that only ADDS rulings and moves phases is ledger-only
    _git(repo, "checkout", "-q", "main")
    _git(repo, "checkout", "-q", "-b", "claude/clean")
    (repo / "rulings/2026/09/R-20260901-04.md").write_text("# R-20260901-04\n")
    (repo / "phases/p/01_a.md").write_text("# a\n\nState: accepted\n")
    (repo / "epics.md").write_text("# Epics\n\n## x\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "clean")
    ledger, blocked = ledger_merge.classify_entries(ledger_merge.changed_entries("main", cwd=repo))
    assert blocked == [] and len(ledger) == 3


def _run(*args, stdin=""):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "classify", *args],
        input=stdin,
        capture_output=True,
        text=True,
    )


def test_cli_exit_codes_separate_ledger_from_code():
    assert _run("epics.md", "phases/a/b.md", "rulings/2026/09/R-20260901-01.md").returncode == 0
    result = _run("epics.md", "scripts/cortex.py")
    assert result.returncode == 1
    assert "scripts/cortex.py" in result.stdout


def test_explicit_paths_carry_no_status_and_stay_path_only():
    """Without a git diff there is no status to read, so a ruling path given
    by hand is judged on its path alone — as in the Mind."""
    assert _run("rulings/2026/09/R-20260901-01.md").returncode == 0
    assert _run(stdin="rulings/2026/09/R-20260901-01.md\n").returncode == 0


def test_an_empty_diff_is_not_permission_to_merge():
    """Exit 0 means 'go'. Nothing to merge must never read as go."""
    result = _run(stdin="\n")
    assert result.returncode == 1
    assert "nothing to merge" in result.stdout


def test_every_fixture_path_is_classified():
    """The witness: every path under tests/fixtures/ gets a verdict, and it is
    code — `tests/` is a code home, whatever shape the files inside take."""
    out = subprocess.run(["git", "ls-files", "tests/fixtures"], cwd=REPO,
                         capture_output=True, text=True, check=True).stdout.split()
    assert out, "no fixture paths tracked"
    for path in out:
        assert not ledger_merge.is_ledger_path(path), path


def test_this_repos_own_workflow_cannot_auto_merge_itself():
    """Self-consistency: the gate is on the code side of its own line."""
    assert not ledger_merge.is_ledger_path(".github/workflows/ledger_merge.yml")
    assert not ledger_merge.is_ledger_path("scripts/ledger_merge.py")


def test_workflow_invokes_the_script_as_implemented():
    workflow = (REPO / ".github" / "workflows" / "ledger_merge.yml").read_text()
    assert "python3 scripts/ledger_merge.py classify --base origin/main" in workflow
    assert "python3 scripts/cortex.py check" in workflow


def test_every_workflow_this_repo_has_is_code():
    """Enumeration, not a sample: no workflow file may ever auto-merge, and the
    two added with the dashboard (one of which pushes to main) are named here so
    the list cannot silently fall behind the directory."""
    tracked = set(subprocess.run(["git", "ls-files", ".github/workflows"], cwd=REPO,
                                 capture_output=True, text=True, check=True).stdout.split())
    for name in ("cortex_check.yml", "ledger_merge.yml", "dashboard_refresh.yml",
                 "pages_dashboard.yml"):
        assert f".github/workflows/{name}" in tracked, name
    for path in tracked:
        assert not ledger_merge.is_ledger_path(path), path


def test_the_page_workflow_spells_the_conductor_as_implemented():
    """`--cortex` is a flag of the SUBCOMMAND, not a global: `dashboard --cortex
    . --check` runs, `--cortex . dashboard --check` exits 2 (argparse) and the
    check() wrapper would report a renderer failure. Pin the spelling."""
    refresh = (REPO / ".github" / "workflows" / "dashboard_refresh.yml").read_text()
    assert 'python3 "$BRAIN" dashboard --cortex . --check' in refresh
    assert 'python3 "$BRAIN" dashboard --cortex . --apply' in refresh
    assert "git add dashboard.md dashboard.html" in refresh


def test_no_scheduled_job_mutates_the_ledger():
    """Gate grading was the one cron that wrote phase headers; it was retired
    on 2026-09-03. Nothing schedules a ledger write any more."""
    workflows = (REPO / ".github" / "workflows")
    for path in sorted(workflows.glob("*.yml")):
        text = path.read_text()
        if "schedule:" not in text:
            continue
        assert "git add phases" not in text, path.name
        assert "git add rulings" not in text, path.name
