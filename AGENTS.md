# PyAutoCortex — Agent Guidance

This file is for AI coding agents (Claude Code, Codex, Cursor, etc.) and humans
discovering this repository. PyAutoCortex is the **Cortex** organ of the PyAuto
organism — where the organism keeps track of what is true.

<!-- repos_sync:map:begin -->
**You are one organ of the PyAuto organism** — an agentic ecosystem for
human-led, natural-language software development. The organs below are
peer repositories; this repo is one of them, not a part of another.
Canonical boundaries live in `PyAutoBrain/ORGANISM.md`; the full body map
(every repo, not just organs) is `PyAutoMind/repos.yaml`.

| Organ | Repo | Role |
|-------|------|------|
| **Brain** | PyAutoBrain | Reasoning/orchestration layer; how work is decomposed and routed; the specialist agents. |
| **Mind** | PyAutoMind | Intent, goals, priorities, workflow state; every task starts as a markdown prompt here. |
| **Cortex** | PyAutoCortex | The Cortex — where the organism keeps track of what is true: the science body map (`projects.yaml`) and one ledger per science project (what was run, what came back, what was learned, where to pick up); the science mirror of the Mind (runs and a dated log, not prompts and PRs). |
| **Memory** | PyAutoMemory | Long-term scientific/software/project knowledge (see science pointer below). |
| **Heart** | PyAutoHeart | Health/readiness — the authoritative "is it safe to release?" verdict. |
| **Hands** | PyAutoHands | Packaging, tagging, notebook generation, PyPI release execution. |
| **Nerves** | PyAutoNerves | The Nerves — the configuration/serialization layer connecting workspace conventions to libraries (layered config, version handshake, test_mode), delivered as the `autonerves` package. |
| **Gut** | PyAutoGut | Owns the lifecycle of condemned self-material (stale branches, stashes, dead code/tests): holds it as durable, recoverable git refs through a transit window and voids it on a sweep. The storage mirror of Memory (retention vs release). |

Call chain (always this order): **Brain → Heart (gate) → Build (execute)**. Brain agents are **conductors** (front-door; a human drives them; they decide *and* act) or **faculties** (read-only opinions the conductors consult; they judge and stop). New capability grows as a faculty, not a new organ, unless it owns state or effects no existing organ can.

Generated from `PyAutoMind/repos.yaml` + `PyAutoBrain/ORGANISM.md`; edit there, then run `python3 PyAutoMind/scripts/repos_sync.py --write`.
<!-- repos_sync:map:end -->
## What this repo is

**The Mind decides what to build, the Brain routes the work and executes
nothing, the Cortex keeps track of what is true.** The Cortex is a
**project ledger**: `project → runs → log`. It owns two pieces of state no
other organ holds — the **science body map** (`projects.yaml`: every science
project, where it lives on the laptop and on RAL, how it syncs, where its own
commentary ledger is) and **one ledger per project** (`projects/<key>.md`:
where the human is with it, what is on the cluster, and a dated history of
what they set off, saw and learned).

It is **not a second PyAutoMind**, and it is **not a task tracker**
(2026-09-12, schema decision 60). Science is not worked as a queue of
pre-registered questions that get done and retired: the human does runs, looks
at results, thinks, and organically decides where to go next. So a ledger
holds no state machine, no witness, no verdict — it holds a **Now**, the
**Runs** on the cluster, and a **Log** that only ever gets longer. The board is
a live view of what has been going through the human's head on each project,
and the thing that makes a project easy to pick up after time away.

**Nothing in a ledger is inferred from results.** A run's submission, start
and end are cluster facts and the script records them. A `result` or a
`lesson` is the human's own words, written on their ask. An agent that reads a
results file tells the human what it sees; the human says what to log.

The schema — the ledger file, the run and log line grammars, the
`projects.yaml` subset — and the `scripts/cortex.py` verbs are in
[REFERENCE.md](REFERENCE.md). Every choice is dated in
[docs/schema_decisions.md](docs/schema_decisions.md); read decisions there, do
not re-derive them.

## Layout (operational)

- **`projects.yaml`** — the science body map. One row per project. **This is
  code, not ledger**: `sync_cli` and `local_path` are paths a conductor will
  execute under, so a change to it is always a human's turn. `cortex.py` reads
  it with PyYAML and validates the fields (REFERENCE.md "projects.yaml").
- **`projects/<key>.md`** — one ledger per project (REFERENCE.md "The
  ledger file"). Title `# <key> — <one-line summary>`; header `Project:` and
  `Issue:` (`Repo#N`, an issue URL, or `none`); then exactly three sections:
  `## Now`, `## Runs` (`open | running`), `## Log` (newest first, kind
  `run | result | lesson | note`). Every `status: active` row must have one.
  `projects/AGENTS.md` is the doctrine for the folder.
- **`archive/`** — frozen: the 2026-08/09 task, ruling and batch ledgers,
  kept because the science repos cite their ids. Nothing writes there; any
  change under it is code for the merge gate.
- **`checkin.yaml`** — one key, `refreshed: <UTC ISO 8601>`: when the science
  state was last actually checked in, written by `pyauto-brain cortex checkin
  --apply` and read back by the board. It means *last check-in*, never last
  render; the HTML board reddens it on the reader's own clock once it is more
  than an hour old.
- **`scripts/cortex.py`** — the one lifecycle script (PyYAML + stdlib):
  - `check` — every structural rule, hermetic; `cortex check: OK` or `DRIFT`
    with one `  - …` line per finding, exit 1.
  - `new <project> --summary "<one line>" [--issue Repo#N]` — opens a ledger
    for a row of `projects.yaml`.
  - `run <project> <jobid> "<what>" [--partition P]` — records a submission:
    the run goes under `## Runs` as `open` and the log gets a `run` entry.
  - `running <project> <jobid>` / `done <project> <jobid> [--failed] [--wall
    H:MM] [--note …]` — what the cluster said; `done` moves the run into the
    log.
  - `log <project> "<text>" [--kind note|result|lesson]` — the human's words,
    dated today, at the head of the log.
  - `now <project> "<text>"` — rewrites `## Now`.
  - `issue <project>` — prints the concise block that sits at the top of the
    project's GitHub issue (Now, Runs, the last five entries) between two
    markers; the Brain's `cortex issue --apply` writes it there.
  - `retire <project> --why "<one line>"` — the only verb that writes
    `projects.yaml`: the row's `status:` becomes `retired`, its `note:`
    records why, and the ledger logs it. It refuses while the ledger still
    lists a run.
- **`dashboard.md` / `dashboard.html`** — GENERATED, never hand-edited: the
  board, rendered by the Brain's cortex conductor and self-healed on `main`.
  They are ledger for the merge gate.
- **`scripts/ledger_merge.py`** — the default-deny classifier behind
  `.github/workflows/ledger_merge.yml`: a `claude/**` push whose whole diff is
  ledger (`projects/`, `checkin.yaml`, the two generated dashboards) lands on
  `main` by itself; anything else waits for a human — `projects/AGENTS.md`
  included (doctrine, not an entry), and anything under `archive/`. `python3
  scripts/ledger_merge.py classify --base origin/main` predicts the verdict.

## Driving the Cortex

The Cortex holds state and checks itself; it does not reason. The reasoning
lives in the Brain's **cortex conductor** — `pyauto-brain cortex <verb>`, or
`python3 PyAutoBrain/agents/conductors/cortex/_cortex.py <verb> --cortex
<checkout>` with no Brain install. It is read-mostly: it pulls, it shows, it
renders. The only bytes it writes of its own are the two generated pages and
`checkin.yaml`; every change to a *ledger* goes through `scripts/cortex.py`.

| Verb | What it does |
|------|--------------|
| `checkin [--dry-run \| --apply] [--push \| --no-push] [--project KEY] [--skip-pull]` | **the check-in** — the one door: pull every active project through its own `sync_cli`, run its `jobs` verb where it has one and show the output verbatim, re-render the board, push the ledger where the rule allows, and summarise **by project** (Now, runs, the last five entries, the commands you are likely to type next). `--dry-run` is the default and reaches nothing |
| `census [--json]` | what the Cortex is holding, by project — the one-screen answer |
| `dashboard --check` \| `--apply` | render `dashboard.md` + `dashboard.html`; `--check` exits **1 on drift**, **2 on bad args**, anything else = the renderer could not run |
| `issue [--project KEY] [--apply]` | the concise ledger block for each project's GitHub issue; `--apply` writes it into the issue body between the markers (needs `gh`) |

**`--apply` here, `--write` there.** The conductor's verbs spell the writing
flag `--apply` (the Brain's house spelling); `scripts/cortex.py` verbs write
directly and take `--today` for tests.

**Nothing here submits a job by itself.** A submission is made only on the
human's ask — by the human, or by the agent in the session — with the
project's own `sync_cli submit` line, followed at once by `cortex.py run
<project> <jobid> "<what>"`. `running` and `done` may be typed by the agent
from what `jobs` printed, because those are cluster facts; `log --kind result`
and `--kind lesson` are typed only for words the human said. `checkin` is the
only leg that shells out, and only to the project's own CLI — the conductor
adds no SSH of its own.

### What runs by itself

Three workflows, and only these may write:

| Workflow | Trigger | May write |
|---|---|---|
| `cortex_check.yml` | push/PR on the ledger, scripts, tests, the dashboards | **nothing** — `cortex.py check` + pytest |
| `dashboard_refresh.yml` | push to main, PR, nightly 03:35 UTC, dispatch | `dashboard.md`, `dashboard.html` (self-heal on main; a PR run errors instead of healing) |
| `pages_dashboard.yml` | push to `dashboard.html`, dispatch | nothing in the repo — it publishes to Pages |
| `ledger_merge.yml` | push to `claude/**`, dispatch | merges a ledger-only branch to main |

**No scheduled job mutates the ledger.** The main-writers share `concurrency:
group: cortex-main-writers`, so two bots never race for the tip of main, and
each re-dispatches by name what its `GITHUB_TOKEN` push cannot wake.

The board is published at **<https://pyautolabs.github.io/PyAutoCortex/>** —
`dashboard.html` as the index.

## The workspace-paths exception

Every other organ keeps its paths inside the workspace. The Cortex is the one
exception, and it is confined to `projects.yaml`: a project's `local_path` and
`mirror` are absolute laptop paths **outside** the workspace (the Science
folder under `/mnt/c/…`), because that is where the datasets, the `output/`
trees and the pulled results live and the review happens at the laptop. The
exception is stated in the file's header and here, and nowhere else — a ledger
points into a project through its `projects.yaml` row, never with a bare
absolute path of its own.

## What is out of scope, and why

Quoted verbatim from `PyAutoMind/complete/archive/shelved/batch_science_lane.md`
so nobody re-derives these:

> - **RAL as canonical home for the science project.** Refused above. The datasets
>   and `output/` stay under `/mnt/c/…/Science/`.
> - **A git-courier cron on the RAL login node.** Its value collapses once the
>   laptop is canonical: the laptop has to be on to hold and push the data anyway,
>   so a courier saves almost nothing.
> - **Globus Compute endpoint / self-hosted GitHub runner on the login node.**
>   Same reasoning, plus both are persistent login-node processes needing an
>   operator conversation.
> - Recorded so nobody re-derives them: SSH from a Claude container is a
>   non-starter in every variant (HTTPS-only proxied egress, no keys); Open
>   OnDemand is an admin-installed inbound portal; Cirun cannot reach someone
>   else's SLURM.

Every Cortex project therefore runs from the laptop.

## Hard rules

1. **Never rewrite history on any branch with a remote** (block below).
2. **Pull before edit.** `git fetch && git status` first, every time.
3. **Never write a result or a lesson the human did not say.** Cluster facts
   (`run`, `running`, `done`) are the script's to record; meaning is the
   human's.
4. **Never edit a ledger by hand in a session.** Every write is a
   `scripts/cortex.py` verb, and `python3 scripts/cortex.py check` runs
   before you push; `ledger_merge.yml` runs it on the trial-merge tree and a
   failing check leaves the branch for a human.
5. **Never touch `archive/`.** It is frozen; the merge gate refuses it.
6. **No hand-written HTML.** `dashboard.html` is rendered by the cortex
   conductor; a hand edit is drift that `dashboard_refresh.yml` will overwrite
   on the next push to `main`.

<!-- repos_sync:remote:begin -->
## Remote sessions (Claude Code on web and mobile)

Three facts, all measured in a web/mobile container, where this file is loaded
and little else is. They ride in every organ because a session may hold any
subset of them — and the session that needs this most is the one holding
several, which is exactly the session no hook fires in.

- **Bootstrap in the first turn, unconditionally** — before the first test
  command, not as a remedy once something looks wrong:

  ```
  bash PyAutoMind/scripts/session_bootstrap.sh          # ~10s cold, ~1s warm
  bash PyAutoMind/scripts/session_bootstrap.sh --check  # report only
  ```

  A session holding several organs registers no SessionStart hook — Claude Code
  reads project hooks from the project directory, which in that layout is the
  repos' *parent*, not a repo — so nothing has set this session up. It was once
  phrased as a remedy keyed to `No module named pytest` or collection
  `ImportError`s naming `yaml`; that symptom stopped appearing when the
  container image moved to Python 3.12, while the environment is still wrong in
  ways that read like a bad command rather than a stale session (`pytest -n
  auto` → `unrecognized arguments: -n`). The bootstrap also **unshallows the
  clones**: a remote session clones shallow, and `git merge-base --is-ancestor`
  then answers "not an ancestor" for a commit whose ancestry is merely absent —
  the answer the ship and close-out procedures act on when proving a branch
  merged.

- **Then run the suite in parallel.** 4 cores, subprocess-heavy suites, no
  single slow test: about 3.5x. `python3 -m pytest -q -n auto`, with
  `pytest-xdist` supplied by the bootstrap above.

- **There is no `gh`, and installing one does not help.** A remote session
  reaches GitHub through the `mcp__github__*` tools, already scoped to the
  session's repos. `gh` installs in two seconds and is a trap: it authenticates,
  then 403s every repo-scoped call, because the egress proxy serves neither the
  REST repo paths nor GraphQL beyond a pinned set of PR-review operations — a
  binary that looks healthy and fails everything that matters. It also defeats
  the surface probe, which keys off `gh auth status`. Read
  `PyAutoBrain/skills/GITHUB_ACCESS.md` at the top of any run that touches
  GitHub; it maps each `gh` operation onto its MCP tool. Spell that path from
  the workspace root, as written: a multi-organ session is cwd'd at the repos'
  *parent*, so a bare `skills/…` reads as a missing file rather than a missing
  repo prefix.
<!-- repos_sync:remote:end -->
## When in doubt

Read [README.md](README.md) and [REFERENCE.md](REFERENCE.md). The birth epic's
ledger is `PyAutoMind/complete/archive/epics/cortex_birth_epic.md`; the
2026-09-12 redesign is schema decision 60.

<!-- repos_sync:history:begin -->
## Never rewrite history

Never rewrite pushed history on any repo with a remote — no `git init` over a
tracked repo, no force-push to `main`, no fresh-start "Initial commit", no
`filter-repo` / `filter-branch` / `rebase -i` on pushed branches. To get a
clean tree: `git fetch origin && git reset --hard origin/main && git clean -fd`.
<!-- repos_sync:history:end -->
<!-- repos_sync:deliverable:begin -->
## Sessions end at their deliverable

A session ends when it reports its deliverable — never arm anything that
outlives the turn to wait for CI, a review or a merge: no `send_later`, no
`subscribe_pr_activity`, no `CronCreate`, no `ScheduleWakeup`, no `/loop`, no
`RemoteTrigger` create/update/run. Judge once, report, stop; the human re-runs
`/prm` (or the batch review) when it is green. Measured: five batch members
armed hourly check-ins on 2026-08-31, and a mobile `/prm` re-armed a 60-minute
`send_later` hourly all night on 2026-09-03 with no task active, draining usage.
<!-- repos_sync:deliverable:end -->
