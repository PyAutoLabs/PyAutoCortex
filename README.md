# PyAutoCortex

[![PyAutoScientist GitHub](https://img.shields.io/badge/%F0%9F%94%AD%20PyAutoScientist-GitHub-181717?style=flat-square)](https://github.com/PyAutoLabs/PyAutoScientist) [![PyAutoScientist ReadTheDocs](https://img.shields.io/badge/%F0%9F%93%96%20PyAutoScientist-ReadTheDocs-8CA1AF?style=flat-square)](https://pyautoscientist.readthedocs.io)

**PyAutoCortex is the Cortex of the PyAutoScientist** — where the organism
keeps track of what is true. It holds the **science body map** (every science
project, where it lives, how it syncs) and one **ledger per project**: what was
set off and when, what came back, what you learned, and where you meant to go
next — a history of how each project unfolds, written in your own words, never
a queue of things to finish.

See the **[PyAutoCortex Dashboard](https://pyautolabs.github.io/PyAutoCortex/)**
for how this is used in practice: every active project on one page — where you
are with it, what is on the cluster right now, and the last five things you did
or learned — so a project you have been away from for a while is picked up
where you left it. The markdown twin is [dashboard.md](dashboard.md); both are
generated and never hand-edited.

## How PyAutoCortex works

A project's ledger is one markdown file, `projects/<key>.md`, with three
sections and nothing else:

1. **Now.** Two or three lines, rewritten whenever you touch the project: what
   is running, and what you meant to do next.
2. **Runs.** The jobs on the cluster right now, each `open` (submitted) or
   `running`, with its date and one line saying what it is. A finished run
   leaves this list and becomes a log entry.
3. **Log.** Dated entries, newest first — a run set off or finished, a
   `result` you read off, a `lesson` you want kept, a `note`. Nothing here is
   ever done; it only gets older. The board shows the last five.

Every write goes through `scripts/cortex.py`: `run` records a submission,
`running` and `done` record what the cluster says, `log` and `now` record what
*you* say. Nothing in a ledger is inferred from results — a result or a lesson
is written only when you state it. Checking in is one command from the Brain's
cortex conductor, **`pyauto-brain cortex checkin --apply`** (`/cortex` in
Claude Code): it pulls every active project through that project's own sync
CLI, shows where each run stands, re-renders the board, pushes the ledger where
it is allowed to, and reads the projects back to you one by one.

Each project links to a GitHub issue (`Issue:` in its header) that carries the
detailed run-through; the top of that issue is the same concise ledger the
board shows, regenerated from the project file with `pyauto-brain cortex issue`.

The Cortex is **not a second PyAutoMind**: development work stays in the Mind.
The retired task-and-ruling ledgers of 2026-08/09 are frozen under
[`archive/`](archive/) because the science repos cite their ids.

`scripts/cortex.py` needs Python 3.10+ and **PyYAML** (`python3 -m pip install
pyyaml`), which is how it reads `projects.yaml`; the tests additionally need
`pytest`. Nothing else.

The schema — the ledger file, the run and log line grammars, the `projects.yaml`
fields, how the ledger auto-merges — is in [REFERENCE.md](REFERENCE.md); how
agents should operate this repo is in [AGENTS.md](AGENTS.md); every design
choice is dated in [docs/schema_decisions.md](docs/schema_decisions.md). The
organism this repo is the Cortex of is described once in
[PyAutoBrain/ORGANISM.md](https://github.com/PyAutoLabs/PyAutoBrain/blob/main/ORGANISM.md)
and documented in full at <https://pyautoscientist.readthedocs.io>.
