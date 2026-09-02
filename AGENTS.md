# PyAutoCortex — Agent Guidance

This file is for AI coding agents (Claude Code, Codex, Cursor, etc.) and humans
discovering this repository. PyAutoCortex is the **Cortex** organ of the PyAuto
organism — where the organism learns what is true.

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
| **Cortex** | PyAutoCortex | The Cortex — where the organism learns what is true: the science body map (`projects.yaml`) and the rulings of record for every science run; the science mirror of the Mind (runs and rulings, not prompts and PRs). |
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
nothing, the Cortex learns what is true.** The Cortex is a **run-and-ruling
registry**: `project → phase → runs → rulings`. It owns two pieces of state no
other organ holds — the **science body map** (`projects.yaml`: every science
project, where it lives on the laptop and on RAL, how it syncs, where its own
commentary ledger is) and the **rulings ledger of record** (`rulings/`: every
verdict a human has passed on a science run, append-only).

It is **not a second PyAutoMind.** The Mind is PR-shaped all the way down —
prompts, issues, branches, completion records, "delivered = a PR with a diff
and checks". The Cortex's unit is a **phase** of a **project**, which spawns
**runs** (SLURM job ids) and ends in a **ruling**. Development tasks a science
phase waits on stay in the Mind and are named here only as **gates** — GitHub
issue/PR refs in a phase's `Gates:` header, one grammar, one direction. The
Mind learns nothing about the Cortex beyond a render-time badge.

The schemas — phase files, the run-line grammar, rulings, batches, the
restricted `projects.yaml` subset — and the `scripts/cortex.py` verbs are in
[REFERENCE.md](REFERENCE.md). Every choice the birth epic did not fix is dated
in [docs/schema_decisions.md](docs/schema_decisions.md); read decisions there,
do not re-derive them.

## The ruling of record

**A verdict recorded only outside the Cortex does not exist.** `rulings/` is
canonical. A project's own ledger (`DECISIONS.md`, `state.md`, `RESULTS.md`)
remains as scientific commentary — evidence, reasoning, consequences — and
cites the ruling id. Rulings are **append-only**: a wrong ruling is superseded
by a new one (`Supersedes: R-…`) and never edited; `scripts/ledger_merge.py`
treats any modification or deletion under `rulings/` as code, which is a
human's turn. Full rules in [rulings/AGENTS.md](rulings/AGENTS.md).

## Layout (operational)

- **`projects.yaml`** — the science body map. One row per project. **This is
  code, not ledger**: `sync_cli` and `local_path` are paths a conductor will
  execute under, so a change to it is always a human's turn. It is written in a
  restricted YAML subset that `cortex.py` parses with the stdlib (REFERENCE.md
  "The restricted YAML subset").
- **`phases/<project>/<slug>.md`** — one file per phase, with the Mind's light
  header (`Key: value` lines, no YAML frontmatter) and a `## Runs` body in the
  SLURM run-line grammar. `State:` is one of `planned | gated | ready |
  submitted | running | pulled | awaiting-ruling | accepted | rerun | dropped`.
  `legacy` and `legacy_wrong` are states of a **run**, never of a phase.
- **`rulings/<YYYY>/<MM>/R-<YYYYMMDD>-<nn>.md`** — the ledger of record.
- **`batches/`** — the rolling review board: one record per slot, the archived
  packet page under `packets/`, the human's verbatim review under `reviews/`.
- **`epics.md`** — the Cortex half of every split epic; `- mind-half:` names
  the Mind entry by slug.
- **`scripts/cortex.py`** — the one lifecycle script (stdlib only):
  - `check` — every structural rule, hermetic; `cortex check: OK` or `DRIFT`
    with one `  - …` line per finding, exit 1.
  - `gates [--grade [--write]]` — offline: the gated phases and their refs;
    `--grade` polls GitHub and reports which gates cleared; `--write` flips
    `gated → ready` (and `ready → gated` on a reopened gate).
  - `rule <phase> <verb> --body <file> …` — assigns the next ruling id, writes
    the ruling file(s), updates the phase's `Ruling:` and `State:`. The only
    door to `accepted`, `rerun`, `dropped` and `leave-to-finish`.
  - `move <phase> <state> …` — every other transition, per the table in
    REFERENCE.md; refuses the ruling edges.
  - `new <project> <slug> --phase <n> …` — writes a phase file from the
    template.
- **`dashboard.md` / `dashboard.html`** — GENERATED, never hand-edited: the
  board, rendered by the Brain's cortex conductor and self-healed on `main`
  (see "Driving the Cortex" below). They are ledger for the merge gate.
- **`scripts/ledger_merge.py`** — the default-deny classifier behind
  `.github/workflows/ledger_merge.yml`: a `claude/**` push whose whole diff is
  ledger (`phases/`, `rulings/`, `batches/`, `epics.md`, the two generated
  dashboards) lands on `main` by itself; anything else waits for a human — and
  that "anything else" includes an `AGENTS.md` or `TEMPLATE.md` *inside* a
  ledger dir, which is doctrine, not an entry. `python3
  scripts/ledger_merge.py classify --base origin/main` predicts the verdict.

## Driving the Cortex

The Cortex holds state and checks itself; it does not reason. The reasoning
lives in the Brain's **cortex conductor** — `pyauto-brain cortex <verb>`, or
`python3 PyAutoBrain/agents/conductors/cortex/_cortex.py <verb> --cortex
<checkout>` with no Brain install. It is read-mostly: it renders, it plans and
it scores. The only bytes it writes of its own are the two generated pages;
every change to a *phase* goes through `scripts/cortex.py`, which owns the
state table.

| Verb | What it does |
|------|--------------|
| `census [--json]` | what the Cortex is holding, by state — the one-screen answer |
| `dashboard --check` \| `--apply` | render `dashboard.md` + `dashboard.html`; `--check` exits **1 on drift**, **2 on bad args**, anything else = the renderer could not run |
| `gates [--grade] [--apply]` | the gate refs; `--grade` polls GitHub, `--apply` flips `gated → ready` (and `ready → gated` on a reopen) |
| `plan [--budget N]` | which `ready` phases fit a laptop slot, cheapest first; it hands over a command, never a decision |
| `collect [--slot S] [--pull] [--refreshed ISO] [--apply]` | score a pulled run's legs into a packet member; `--pull` is opt-in and runs the *project's own* sync CLI |

The batch conductor is the **slot door** over the same two verbs:
`pyauto-brain batch plan --kind cortex` and `batch collect --kind cortex` drive
this `plan` and `collect` for one review slot and write `batches/` — the record,
its `refreshed:` lines and the packet (`batches/AGENTS.md`).

**`--apply` here, `--write` there.** The conductor's verbs spell the writing
flag `--apply` (the Brain's house spelling, as intake does); `scripts/cortex.py`
spells it `--write`. `cortex gates --grade --apply` is a thin wrapper over
`cortex.py gates --grade --write` — same edit, two doors.

**Nothing here submits a job.** `plan` prints the project's own `sync_cli
submit` line and the `cortex.py move <phase> submitted --run <jobid>` follow-up;
a human runs both. `collect --pull` is the one leg that shells out, and only to
the project's own CLI.

### What runs by itself

Four workflows, and only these may write:

| Workflow | Trigger | May write |
|---|---|---|
| `cortex_check.yml` | push/PR on ledger, scripts, tests, the dashboards | **nothing** — `cortex.py check` + pytest |
| `dashboard_refresh.yml` | push to main, PR, nightly 03:35 UTC, dispatch | `dashboard.md`, `dashboard.html` (self-heal on main; a PR run errors instead of healing) |
| `pages_dashboard.yml` | push to `dashboard.html` / `batches/packets/**`, dispatch | nothing in the repo — it publishes to Pages |
| `gates_grade.yml` | daily 06:47 UTC, dispatch | phase headers — **`State:` and `Gates-cleared:` only**, and only `gated → ready` (or `ready → gated` on a reopened gate) |
| `ledger_merge.yml` | push to `claude/**`, dispatch | merges a ledger-only branch to main |

`gates_grade.yml` is **the one scheduled job that mutates the ledger**. It never
rules, never submits, never edits a run line. An unreadable gate ref fails
closed: the phase is skipped, whatever else flipped is still committed, and the
job then goes red so a human sees the ref.

All three main-writers share `concurrency: group: cortex-main-writers`, so two
bots never race for the tip of main. And because a `GITHUB_TOKEN` push triggers
no workflow at all, each of them re-dispatches by name what its push should have
woken (`pages_dashboard.yml` after a heal; `cortex_check.yml` +
`dashboard_refresh.yml` after a grading commit).

The board is published at **<https://pyautolabs.github.io/PyAutoCortex/>** —
`dashboard.html` as the index, archived packets under `/packets/`.

## The workspace-paths exception

Every other organ keeps its paths inside the workspace. The Cortex is the one
exception, and it is confined to `projects.yaml`: a project's `local_path` and
`mirror` are absolute laptop paths **outside** the workspace (the Science
folder under `/mnt/c/…`), because that is where the datasets, the `output/`
trees and the pulled results live and the review happens at the laptop. The
exception is stated in the file's header and here, and nowhere else — a phase
file or a ruling points into a project through its `projects.yaml` row, never
with a bare absolute path of its own.

## The laptop lane — what is out of scope, and why

Quoted verbatim from `PyAutoMind/draft/research/euclid/batch_science_lane.md`
so nobody re-derives these:

> ## What is now out of scope, and why
>
> - **RAL as canonical home for the science project.** Refused above. The datasets
>   and `output/` stay under `/mnt/c/…/Science/`.
> - **A git-courier cron on the RAL login node.** Its value collapses once the
>   laptop is canonical: the laptop has to be on to hold and push the data anyway,
>   so a courier saves almost nothing. It was the right answer to a question no
>   longer being asked.
> - **Globus Compute endpoint / self-hosted GitHub runner on the login node.**
>   Same reasoning, plus both are persistent login-node processes needing an
>   operator conversation. Not worth it for a lane the human is happy to drive.
> - Recorded so nobody re-derives them: SSH from a Claude container is a
>   non-starter in every variant (HTTPS-only proxied egress, no keys); Open
>   OnDemand is an admin-installed inbound portal; Cirun cannot reach someone
>   else's SLURM. And phases 4, 6a and 6b of `euclid-dr1-prep` say in their own
>   prompts that they are human-driven and supervised with a judged verdict as the
>   deliverable — **no transport was ever going to make those unattended.**

Every Cortex phase is therefore `Lane: local-dev`, always; the field exists so
the batch conductor's lane filter reads one vocabulary across both surfaces.

## Hard rules

1. **Never rewrite history on any branch with a remote** (block below).
2. **Pull before edit.** `git fetch && git status` first, every time.
3. **Never edit a ruling.** Supersede it. `ledger_merge.py` refuses to
   auto-merge a modified or deleted file under `rulings/`.
4. **Run `python3 scripts/cortex.py check` before you push** a phase, ruling
   or batch change; `ledger_merge.yml` runs it on the trial-merge tree and a
   failing check leaves the branch for a human.
5. **No hand-written HTML.** `dashboard.html` is rendered by the cortex
   conductor and packets by the batch conductor; a hand edit is drift that
   `dashboard_refresh.yml` will overwrite on the next push to `main`.

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
ledger is `PyAutoMind/draft/feature/pyautocortex/cortex_birth_epic.md`.

<!-- repos_sync:history:begin -->
## Never rewrite history

Never rewrite pushed history on any repo with a remote — no `git init` over a
tracked repo, no force-push to `main`, no fresh-start "Initial commit", no
`filter-repo` / `filter-branch` / `rebase -i` on pushed branches. To get a
clean tree: `git fetch origin && git reset --hard origin/main && git clean -fd`.
<!-- repos_sync:history:end -->
