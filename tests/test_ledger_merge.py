"""Tests for scripts/ledger_merge.py — the auto-merge safety gate.

This gate decides what lands on `main` with no human in the loop, so the
properties that matter are the refusals: default deny for anything
unclassified, no traversal or dotfile route past the ledger prefix, no
pytest-collectable file smuggled in beside a ledger, every code home the repo
has (scripts/, tests/, .github/, policy/, docs/, projects.yaml, the prose
pages) staying on the human side of the line, no doctrine file (AGENTS.md,
TEMPLATE.md) riding along because it sits under `projects/` — and the frozen
`archive/` (the retired task, ruling and batch ledgers) never auto-merging.

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


def test_ledger_dir_and_registry_files_are_ledger():
    for path in (
        "projects/example.md",
        "projects/newproject.md",
        "checkin.yaml",
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
        "tests/fixtures/skeleton/projects/example.md",
        ".github/workflows/ledger_merge.yml",
        ".github/workflows/cortex_check.yml",
        ".github/workflows/dashboard_refresh.yml",
        ".github/workflows/pages_dashboard.yml",
        ".gitignore",
        ".claude/settings.json",
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


def test_the_archive_is_frozen_even_for_additions():
    """The retired ledgers are history the science repos cite by id; nothing
    writes there, so an added file is as much a human's call as an edit."""
    for path in (
        "archive/tasks/example/01_scope.md",
        "archive/rulings/2026/09/R-20260901-01.md",
        "archive/rulings/2026/09/R-20260999-01.md",
        "archive/batches/2026-09-01-pm.md",
        "archive/batches/reviews/2026-09-01-pm.md",
        "archive/anything_new.md",
    ):
        assert not ledger_merge.is_ledger_path(path), path


def test_unclassified_paths_default_to_deny():
    """A root file or top-level folder nobody has thought about is code."""
    for path in ("brand_new_root_file.md", "newfolder/thing.md", "notes.txt",
                 "skills/x/SKILL.md", "tasks/example/x.md", "rulings/2026/09/R-1.md"):
        assert not ledger_merge.is_ledger_path(path), path


def test_traversal_cannot_smuggle_code_behind_a_ledger_prefix():
    for path in ("projects/../scripts/evil.py", "projects/../../etc/passwd", ".."):
        assert not ledger_merge.is_ledger_path(path), path


def test_dot_paths_are_never_ledger_wherever_they_sit():
    for path in ("projects/.github/workflows/x.yml", "projects/.hidden", ".projects/x.md"):
        assert not ledger_merge.is_ledger_path(path), path


def test_collectable_tests_do_not_ride_along():
    for path in ("projects/conftest.py", "projects/test_thing.py", "projects/thing_test.py"):
        assert not ledger_merge.is_ledger_path(path), path


def test_doctrine_under_the_ledger_dir_needs_a_human():
    """`projects/` holds entries; `AGENTS.md` and `TEMPLATE.md` inside it are
    the doctrine that says what an entry may be. A branch that could
    auto-merge them could edit the rule governing its own merge."""
    for path in ("projects/AGENTS.md", "projects/TEMPLATE.md"):
        assert not ledger_merge.is_ledger_path(path), path
    assert ledger_merge.is_ledger_path("projects/example.md")


def test_every_tracked_file_under_the_ledger_dir_gets_the_right_verdict():
    out = subprocess.run(["git", "ls-files", "projects"], cwd=REPO,
                         capture_output=True, text=True, check=True).stdout.split()
    assert out, "no ledger paths tracked"
    for path in out:
        doctrine = Path(path).name in ("AGENTS.md", "TEMPLATE.md")
        assert ledger_merge.is_ledger_path(path) is not doctrine, path


def test_every_tracked_archive_file_is_code():
    out = subprocess.run(["git", "ls-files", "archive"], cwd=REPO,
                         capture_output=True, text=True, check=True).stdout.split()
    assert out, "no archive paths tracked"
    for path in out:
        assert not ledger_merge.is_ledger_path(path), path


def test_classify_splits_and_dedupes_preserving_order():
    ledger, blocked = ledger_merge.classify(
        ["checkin.yaml", "scripts/x.py", "checkin.yaml", "projects/a.md", "", "  "]
    )
    assert ledger == ["checkin.yaml", "projects/a.md"]
    assert blocked == ["scripts/x.py"]


def test_classify_entries_blocks_the_archive_whatever_the_status():
    entries = [("A", "projects/a.md"), ("M", "projects/b.md"), ("D", "projects/c.md"),
               ("A", "archive/rulings/2026/09/R-20260901-09.md"),
               ("M", "archive/tasks/example/01_scope.md")]
    ledger, blocked = ledger_merge.classify_entries(entries)
    assert ledger == ["projects/a.md", "projects/b.md", "projects/c.md"]
    assert blocked == ["archive/rulings/2026/09/R-20260901-09.md",
                       "archive/tasks/example/01_scope.md"]


def _git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True)


def _repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "t")
    (repo / "projects").mkdir()
    (repo / "projects" / "a.md").write_text("# a — x\n")
    (repo / "archive").mkdir()
    (repo / "archive" / "old.md").write_text("old\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "base")
    _git(repo, "checkout", "-qb", "claude/x")
    return repo


def test_changed_entries_reads_name_status_from_git(tmp_path):
    repo = _repo(tmp_path)
    (repo / "projects" / "a.md").write_text("# a — y\n")
    (repo / "projects" / "b.md").write_text("# b — z\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "ledger")
    entries = ledger_merge.changed_entries("main", cwd=repo)
    assert sorted(entries) == [("A", "projects/b.md"), ("M", "projects/a.md")]
    ledger, blocked = ledger_merge.classify_entries(entries)
    assert not blocked


def test_a_change_under_the_archive_is_code_on_a_real_diff(tmp_path):
    repo = _repo(tmp_path)
    (repo / "archive" / "old.md").write_text("edited\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "touch the archive")
    ledger, blocked = ledger_merge.classify_entries(ledger_merge.changed_entries("main", cwd=repo))
    assert blocked == ["archive/old.md"]


def test_a_rename_out_of_the_ledger_dir_is_code(tmp_path):
    repo = _repo(tmp_path)
    _git(repo, "mv", "projects/a.md", "renamed.md")
    _git(repo, "commit", "-qm", "rename")
    entries = ledger_merge.changed_entries("main", cwd=repo)
    ledger, blocked = ledger_merge.classify_entries(entries)
    assert "renamed.md" in blocked


def _cli(*args, stdin=""):
    return subprocess.run([sys.executable, str(SCRIPT), "classify", *args],
                          input=stdin, capture_output=True, text=True)


def test_cli_exit_codes_separate_ledger_from_code():
    assert _cli("projects/a.md", "checkin.yaml").returncode == 0
    assert _cli("projects/a.md", "scripts/cortex.py").returncode == 1
    assert _cli("archive/rulings/2026/09/R-20260901-01.md").returncode == 1


def test_stdin_paths_are_read():
    assert _cli(stdin="projects/a.md\n").returncode == 0
    assert _cli(stdin="projects/a.md\nREADME.md\n").returncode == 1


def test_an_empty_diff_is_not_permission_to_merge():
    r = _cli(stdin="")
    assert r.returncode == 1


def test_every_fixture_path_is_classified():
    for p in (REPO / "tests" / "fixtures").rglob("*"):
        if p.is_file():
            assert not ledger_merge.is_ledger_path(p.relative_to(REPO).as_posix())


def test_this_repos_own_workflow_cannot_auto_merge_itself():
    assert not ledger_merge.is_ledger_path(".github/workflows/ledger_merge.yml")


def test_workflow_invokes_the_script_as_implemented():
    text = (REPO / ".github" / "workflows" / "ledger_merge.yml").read_text()
    assert "scripts/ledger_merge.py classify --base origin/main" in text
    assert "scripts/cortex.py check" in text


def test_every_workflow_this_repo_has_is_code():
    for p in (REPO / ".github" / "workflows").glob("*.yml"):
        assert not ledger_merge.is_ledger_path(p.relative_to(REPO).as_posix())


def test_the_workflows_watch_the_ledger_dir_not_the_retired_ones():
    for name in ("cortex_check.yml", "dashboard_refresh.yml"):
        text = (REPO / ".github" / "workflows" / name).read_text()
        assert '- "projects/**"' in text, name
        assert '- "tasks/**"' not in text and '- "rulings/**"' not in text, name


def test_the_page_workflow_spells_the_conductor_as_implemented():
    text = (REPO / ".github" / "workflows" / "dashboard_refresh.yml").read_text()
    assert "agents/conductors/cortex/_cortex.py" in text
    assert "dashboard --cortex . --check" in text
    assert "dashboard --cortex . --apply" in text


def test_no_scheduled_job_mutates_the_ledger():
    """The only scheduled writer renders the two generated pages."""
    for p in (REPO / ".github" / "workflows").glob("*.yml"):
        text = p.read_text()
        if "schedule:" in text:
            assert p.name == "dashboard_refresh.yml", p.name
            assert "git add dashboard.md dashboard.html" in text
            assert "projects/" not in text.split("git add", 1)[1].split("\n")[0]
