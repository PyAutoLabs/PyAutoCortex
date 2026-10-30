# PyAutoCortex — Reference

The schema of the Cortex, in full. Everything `scripts/cortex.py check`
enforces is written here; nothing it enforces is not. Design choices are dated
in [docs/schema_decisions.md](docs/schema_decisions.md).

## The ledger file

One file per project, `projects/<key>.md`, where `<key>` is a row of
`projects.yaml` (`^[a-z][a-z0-9_]*$`). Every `status: active` row must have
one; a `dormant`, `planned` or `retired` row may.

```markdown
# <key> — <one-line summary, at most 15 words>

Project: <key>
Issue: <Repo#N | https://github.com/<owner>/<repo>/issues/N | none>

## Now

Two or three lines, rewritten whenever the project is touched: what is on the
cluster and what the human meant to do next. May not be empty on an active
project.

## Runs

- <jobid> — <open | running> — <partition> — <YYYY-MM-DD> — <what it is>
  an optional continuation line, indented two spaces

## Log

- <YYYY-MM-DD> — <run | result | lesson | note> — <text>
  an optional continuation line, indented two spaces
```

The header holds exactly `Project:` and `Issue:`; `Project:` must equal the
key. The three sections appear in that order and no other section exists.
` -- ` is read as ` — ` everywhere (phone keyboards).

### Run lines (`## Runs`)

| Field | Grammar | Meaning |
|---|---|---|
| jobid | `342301`, `342301_3`, `342301_[0-9]`, `342301_[0,2,4-9]` | the SLURM id, array task or task set |
| state | `open` \| `running` | `open` = submitted and not yet seen running. There is no third state: a run that has finished is removed by `done` and becomes a log entry |
| partition | a bare word (`ral`, `gpu`) | must agree with the row's `partition:` unless that is `both` |
| date | `YYYY-MM-DD` | the submission date |
| what | free text, one line | what the run is — the human's description at submission |

A job id appears once per file. A retired project lists no runs.

### Log lines (`## Log`)

Newest first — `check` refuses a date that is later than the entry above it.
Four kinds:

| Kind | Written by | What it is |
|---|---|---|
| `run` | `cortex.py run` / `done` / `sync-runs` | `<jobid> submitted: <what>` · `<jobid> running: <what> — <counts> (digest …)` · `<jobid> finished — wall H:MM: <what>` · `<jobid> failed: <what>` |
| `result` | `cortex.py log --kind result` | what the human read off the results, in their words |
| `lesson` | `cortex.py log --kind lesson` | something the human wants kept — a trap, a rule, a fact about the setup |
| `note` | `cortex.py log` (default), `new`, `retire` | anything else: a thought, a plan, `ledger opened`, `retired: <why>` |

The board and the issue block show the newest `LOG_WINDOW = 5` entries; the
file keeps them all. An entry is never edited or removed: a wrong entry is
answered by a newer one.

### The issue block

`cortex.py issue <project> [-n 5]` prints the concise ledger that sits at the
top of the project's GitHub issue: the title line and status, `**Now**`, the
runs on the cluster, and the last `n` entries, fenced by

```
<!-- cortex:ledger begin — regenerated from projects/<key>.md; edit there -->
…
<!-- cortex:ledger end -->
```

The Brain's `cortex issue --apply` replaces exactly that span in the issue
body (or prepends it when the markers are absent) and leaves everything under
it — the detailed, agent-friendly run-through — untouched. The Cortex never
creates an issue; `Issue:` is set with `new --issue` or `link`.

## `scripts/cortex.py` — the verb reference

| Verb | Writes | Refuses when |
|---|---|---|
| `check` | nothing | — (exit 1 on any finding) |
| `new <project> --summary "…" [--issue REF] [--now "…"]` | a fresh `projects/<key>.md` from the template, with one `note — ledger opened` | the key is not a row; the file exists; the summary is over 15 words; the ref is malformed |
| `run <project> <jobid> "<what>" [--partition P]` | a run line (`open`) + a `run` entry | the id is not SLURM-shaped; it is already listed; the row is `both` and no `--partition` |
| `running <project> <jobid>` | the run line's state | the id is not under `## Runs` |
| `done <project> <jobid> [--failed] [--wall H:MM] [--note "…"]` | removes the run line, prepends a `run` entry | the id is not under `## Runs`; `--wall` is not `H:MM` |
| `log <project> "<text>" [--kind KIND]` | one entry at the head of the log | empty text; a `--today` earlier than the head entry |
| `now <project> "<text>"` | the body of `## Now` | empty text |
| `issue <project> [-n N]` | nothing (prints) | — |
| `link <project> <ref>` | the `Issue:` header line | the ref is not `Repo#N`, an issue URL or `none` |
| `retire <project> --why "…"` | `projects.yaml` (`status: retired`, `note:`), one `note` entry | the row is already retired; the ledger still lists a run; `--why` holds `"` |
| `sync-runs <project> [--digest PATH] [--dry-run]` | each run line the digest settles: `open` → `running` (+ a `run` entry), or `done` with the task counts | the digest is not a schema-1 `digest.json` with a readable `tasks.jsonl` beside it; no `--digest` and no `digest:` in the row |

Every verb takes `--root <dir>` (default: this checkout) and every dated verb
`--today YYYY-MM-DD`, so the tests run against a copy of the fixture with a
fixed clock. A verb that would leave a file `check` cannot read refuses and
writes nothing.

## `projects.yaml`

The science body map. **Code, not ledger** — `sync_cli` and `local_path` are
paths a conductor executes under. Real YAML read with `yaml.safe_load`; the
shape is validated by `cortex.py`. A project key may appear only once — since
`yaml.safe_load` silently keeps the last of a repeated key, `cortex.py check`
scans the raw column-0 keys and reports every duplicate with its line numbers:

| Field | Value | Notes |
|---|---|---|
| `remote` | `owner/repo` or `none` | PyAutoLabs for active projects; a personal remote is a fact with a `note:` |
| `local_path` | absolute path | the laptop checkout — the workspace-paths exception (AGENTS.md) |
| `ral_root` | absolute path | the project root on RAL |
| `mirror` | absolute path or `none` | the laptop pull root the sync CLI fills |
| `sync_cli` | path relative to `local_path` | the project's own sync CLI — the only thing that reaches a cluster |
| `sync_verbs` | flow list of bare words | the verbs that CLI has; `pull` is what `checkin` runs, `jobs` what it shows |
| `ledger` | path relative to `local_path` | the project's own commentary ledger (a `wiki/project/state.md`, a `NOTES.md`) |
| `assistant` | a workspace-relative repo name or `none` | the domain assistant the project's work enters through; named, never read |
| `witness_file` | glob relative to the mirror | kept for the projects' own tooling; the Cortex no longer scores it |
| `partition` | `gpu` \| `ral` \| `both` | which SLURM partition(s) the project runs on; `run` needs `--partition` on `both` |
| `status` | `active` \| `dormant` \| `planned` \| `retired` | `retire` writes the last |
| `note` | free text, **optional** | an empty `note:` is drift |
| `campaign_file` | path relative to `local_path` (or absolute), **optional** | the project's PyAutoFit `campaign.yaml`; must end `.yaml`/`.yml`, no `..` |
| `digest` | path relative to `local_path` (or absolute), **optional** | the pulled campaign `digest.json` `sync-runs` reads by default; must name a `digest.json`, no `..` |

**Partition rule (human, 2026-09-30).** `both` means a project has GPU jobs *and*
CPU jobs, each on its own partition — never a CPU-only array submitted as
`ral,gpu`/`gpu,ral` or to `gpu`, even when `ral` is drained or busy (the jobs
wait for `ral`). On 2026-09-30 euclid_dr1 CPU arrays on `ral,gpu` took all 124
CPUs on euclid-ral-gpu-1/-2 and left all 8 A100s idle but unschedulable for
hours. Only exemption: small CPU timing legs on `gpu` without `--gres` with ≤8
CPUs/task, throttle ≤`%2` and no pending gres/gpu jobs (`squeue -p gpu -t PD`).
Record a run as GPU only after `scontrol show job` shows `gres/gpu` in its TRES.
Never reorder, hold or cancel another campaign's jobs without the human's OK.

## Run status from a campaign digest (`sync-runs`)

A project whose runs are PyAutoFit campaigns (`autofit.campaign`) has a
`digest.json` with a `tasks.jsonl` beside it, pulled from the cluster by the
project's sync CLI. `sync-runs` reads them and brings `## Runs` in line:

- **The key is the SLURM job id.** A run line `3002_[0-3]` is matched to the
  `tasks.jsonl` rows whose `job_id` is `3002` and whose `key`
  (`<job>_<array index>`) falls in `0–3`; a bare `3002` takes every task of
  the array. The digest's `campaign` name is reported, not matched on.
- An `open` run with a task in `running`/`timeout_pending` or already ended
  becomes `running`, with one `run` entry giving the task counts.
- A run whose matched tasks have all ended (`completed`, `failed`, `timeout`,
  `oom`, `node_fail`, `cancelled`, `preempted`) goes through `done`: the counts
  are its note, the wall is first start → last end, and it is `failed` when no
  task completed.
- A run with no tasks in the digest, and a digest job with no run line, are
  printed and left alone — `sync-runs` never adds a run (`run` records a
  submission) and never removes one it cannot account for.
- It is idempotent, `--dry-run` writes nothing, and the first line printed is
  `sync-runs: <project>: <n> changed`. Exit 0 on success (changes or not),
  1 on a malformed digest.

**The boundary.** Run status is a cluster fact, so a script may record it
from the scheduler's accounting. What the runs *mean* is the human's: a
`result` or `lesson` entry and `## Now` are only ever written on their ask, and
`sync-runs` writes neither (schema decision 64).

## Repository layout

```
projects.yaml            the body map (code)
projects/<key>.md        one ledger per project (ledger)
projects/AGENTS.md       doctrine for the folder (code)
checkin.yaml             the last-check-in stamp (ledger)
dashboard.md, .html      generated board (ledger; never hand-edited)
archive/                 frozen 2026-08/09 tasks, rulings, batches (code)
scripts/cortex.py        the lifecycle script
scripts/ledger_merge.py  the auto-merge classifier
tests/                   pytest; fixtures/skeleton and fixtures/empty
docs/schema_decisions.md every dated choice
```

## How the ledger lands (`ledger_merge.yml`)

A push to `claude/**` whose whole diff is ledger — `projects/*.md` (not
`AGENTS.md` / `TEMPLATE.md`), `checkin.yaml`, `dashboard.md`,
`dashboard.html` — is merged into `main` with `--no-ff` and the branch
deleted. Anything else waits for a human: `scripts/`, `tests/`, `.github/`,
`policy/`, `docs/`, `projects.yaml`, the prose pages, anything under
`archive/`, and anything unclassified (default deny). `cortex.py check` runs
on the branch tip and again on the trial-merge tree, so two branches that
each edited the same ledger are caught before either lands. `python3
scripts/ledger_merge.py classify --base origin/main` predicts the verdict
(exit 0 ledger · 1 code · 2 could not classify). `--base` reads the diff from git and
never stdin, so it is safe from a web/mobile session whose stdin is a harness
socket that never closes; piped paths are read only when neither explicit
paths nor `--base` is given.

## Check-in

`pyauto-brain cortex checkin` (the Brain's cortex conductor) is the one door:

```bash
pyauto-brain cortex checkin --dry-run              # what it would pull; reaches nothing
pyauto-brain cortex checkin --apply                # pull, show jobs, render, push
pyauto-brain cortex checkin --apply --no-push
pyauto-brain cortex checkin --apply --project subhalo_validation
pyauto-brain cortex checkin --apply --skip-pull
```

It sweeps every `status: active` row plus any project whose ledger lists a
run, runs **that project's own** `<local_path>/<sync_cli> pull` (a failing
pull is recorded against its project and the sweep continues), runs its `jobs`
verb where the row has one and prints the output verbatim, writes
`checkin.yaml`, re-renders the two pages, pushes the ledger on
`claude/checkin-<date>` when `gh` is logged in and the checkout is clean on
`main`, and prints last a summary keyed by project: Now, the runs, the last
five entries, and the `cortex.py` lines the human is likely to type next. It
flips no state and writes no entry of its own — the jobs output is read by
the human or the agent in the session and recorded with `running` / `done`.

### Drift

`pyauto-brain cortex drift` checks the body map against the laptop Science
tree, `<root>/<category>/<project>` with categories `active`, `development`,
`complete`, `archive` (the root is derived from the rows' `local_path`s;
`--science-root` overrides). Errors: a folder in `active/` or `development/`
with no row; a non-retired row whose `local_path` is gone; a folder whose
category disagrees with its status (`active`/`development` hold
`active|dormant|planned`, `complete`/`archive` hold `retired|dormant`); a
derived root that does not exist while other rows' folders do. Warnings: an
unregistered folder in `complete/` or `archive/` (storage), a non-retired
row whose `ral_root` category differs from its `local_path` category. Rows
outside the Science tree (repo-backed roots under the workspace) are exempt
from the category rules. It writes nothing; `census` and `checkin` print one
summary line, off the laptop a skip.

### Birth

A new project is scaffolded by its domain assistant (`start-new-project`)
into `<Science root>/<active|development>/<key>/`, then registered with
`pyauto-brain cortex birth <key> --category … --assistant … --summary …`,
which derives the row from the folder and the other rows and writes it
through `scripts/cortex.py birth` on `claude/birth-<key>`. `cortex.py birth`
appends the row in field order at the end of `projects.yaml`, reads it back
(restoring the file on any problem) and opens the ledger with `new`. The
diff — one row plus `projects/<key>.md` — is a birth to `ledger_merge.py`,
so the branch lands on `main` by itself.

### `checkin.yaml`

```yaml
refreshed: 2026-09-10T19:41Z
```

Written by `checkin --apply` before the pages are rendered, so a doc-only
push that re-renders the board cannot fake freshness. The HTML board reddens
the stamp on the viewer's clock once it is an hour old.

## The board

`dashboard.md` and `dashboard.html`, rendered by the conductor: a counts table
(**Running**, **Open**, **Projects** — the Brain board reads these three
rows), the check-in chip and stamp, a four-column **Summary** (`Project ·
Running · Open · Last update` — deliberately no free text, so it fits a
phone), then one card per project with a ledger: the facts line, **Now**, the
**Runs**, the **Last 5** entries, and a single 📋 **resume** chip for an active
project — the paste that has an agent read the ledger and the project's own
state file and say where you left off. Retired projects fold into one line
each; dormant rows with no ledger are a small table. No chip on the page
submits, scores or decides anything.

## Bootstrap

```bash
python3 -m pip install pyyaml pytest
python3 scripts/cortex.py check
python3 -m pytest -q
```
