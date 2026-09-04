# PyAutoCortex reference

The schemas, grammars and conventions for this repo — the file `scripts/cortex.py`
implements and `scripts/cortex.py check` enforces. Agent docs that point at a
schema ("the transition table", "the run-line grammar", "the ruling schema")
resolve here, one link from [AGENTS.md](AGENTS.md).

---

## What a phase looks like

Here is a phase file — `phases/example/05_running_array.md` from the test
fixture — of a project whose GPU array is most of the way through:

````markdown
# Example — phase 5: the nine-lens array

Project: example
Phase: 5
State: running
Gates: PyAutoArray#431
Witness: nine of ten array tasks write a sane checkpoint.hdf5 within 8:00 wall
Budget: 8:00
Runs: 342091, 342102
Ruling: R-20260901-03
Review-minutes: 8
Epic: example-programme
Filed: 2026-08-29

## Question

Does the Delaunay pipeline reach the same theta_E basin on all ten lenses?

## Witness

`output/phase_05/*/checkpoint.hdf5` present for nine lenses, `.err` clean.

## Where to look

- `/mnt/c/Users/Jammy/Science/example/output/phase_05/`

## Runs

- 342091_[0-8,10]: done — gpu — submitted 2026-08-30 — wall 6:12
    pulled_to: /mnt/c/Users/Jammy/Science/example/output/phase_05
- 342091_9: failed — gpu — submitted 2026-08-30 — wall 0:00 — OOM before the first step
- 342102: running — gpu — submitted 2026-09-01 — wall 0:00 — task 9 resubmitted alone
    after: 342091_9

## Ruling

R-20260901-03 — leave-to-finish
````

The header is the Mind's **light header**: line 1 is `# <title>`; `Key: value`
lines within the first 30 lines — the block starts at the first `Key: value`
line after the title and ends at the next blank line; the first occurrence of a
key wins; a list-valued key is a bare `Key:` line followed by `- item` lines; a
key with no value (`Gates:`, `Runs:`, `Ruling:`) may be left empty or omitted.
No YAML frontmatter. The body
sections are fixed: `## Question`, `## Witness`, `## Where to look`, `## Runs`,
`## Ruling`.

**`## Where to look` is rendered, not just parsed.** Its `- ` bullets are the
answer to *which folder do I open* — the dashboard's `## By project` view and
`pyauto-brain cortex checkin` print them verbatim under the phase, and
`collect` resolves the ones that are absolute paths inside the project's roots
to the artefacts it scores. `new` seeds the section with the placeholder
`- (the output path, once there is one)`, which is honest on a `planned` phase
and a hole on any other, so **`check` requires a phase whose `State:` is past
`planned` to carry at least one bullet that is not that placeholder**. A
bullet is free text: a path, a project-row-relative location, a Mind prompt, a
GitHub ref — whatever a human would open.

### Phase header keys

| Key | Value | Notes |
|---|---|---|
| `Project:` | project key | must equal the directory name **and** a `projects.yaml` key |
| `Phase:` | integer | unique per project; revival of a dropped phase is a new number |
| `State:` | `planned \| gated \| ready \| submitted \| running \| pulled \| awaiting-ruling \| accepted \| rerun \| dropped` | |
| `Gates:` | comma-separated GitHub refs | `Repo#N` (owner `PyAutoLabs`) or an issue/PR URL; **no `owner/Repo#N`** form |
| `Reset:` | reason | written by `move ready --reason "<reason>"` when a `submitted \| running` phase goes back to `ready` |
| `Witness:` | free text | **mandatory before `submitted`** — the pre-registered checkable claim |
| `Budget:` | `H+:MM` | wall budget per run |
| `Runs:` | comma-separated job **stems** | the index of the `## Runs` body; equal to the set of body stems |
| `Ruling:` | ruling id | the chain head (see "Rulings") |
| `Review-minutes:` | integer | a seed, not a measurement |
| `Epic:` | slug | OPTIONAL join key to a **Mind** epic; the Cortex keeps no epics file of its own |
| `Filed:` | `YYYY-MM-DD` | |
| `Migrated-from:` | source path or ledger anchor | the Mind prompt, review file or project-ledger entry this phase was transcribed from (phase 4 of the birth epic) |

Gate refs are matched by `GATE_REF_RE`, copied verbatim from
`PyAutoMind/scripts/lifecycle.py`:

```python
GATE_REF_RE = re.compile(
    r"https://github\.com/([\w.-]+)/([\w.-]+)/(?:issues|pull)/(\d+)"
    r"|(?<![\w/])([A-Za-z_][\w.]*)#(\d+)\b"
)
DEFAULT_GATE_OWNER = "PyAutoLabs"
```

The lookbehind `(?<![\w/])` is what rejects `owner/Repo#N`: the shorthand is
`Repo#N` with the default owner, and any other owner is spelled as a URL.

---

## How a phase flows

```
  planned ──(Gates: non-empty)──► gated ──(move ready: the human judged the refs)──► ready
     │                                                                                   │
     └──────(Gates: empty)───────────────────────────────────────────────────────────────┤
                                                                                         ▼
  ready ──(Witness: + --run)──► submitted ──► running ──(no live run)──► pulled ──► awaiting-ruling
    ▲                              │              │                                      │
    │       (no live run, ≥1 failed|timeout|void, --reason)                              │ rule
    └──────────────────────────────┴──────────────┘                                      ▼
                                                              accepted  │  rerun ──► ready  │  dropped
                                                                 │ rule --supersedes
                                                                 └──► rerun | dropped
```

`cortex.py move` owns every edge except the ruling edges, which `cortex.py rule`
owns. The full table:

| from | to | condition |
|---|---|---|
| planned | gated / ready | `Gates:` non-empty / empty |
| gated | ready | `move <phase> ready` — a human read `gates`, opened the refs and judged them cleared. No flag, and nothing written but `State:` |
| ready | gated | not an edge: re-gating a `ready` phase is a judgement, so it is a hand edit of the header |
| ready | submitted | `Witness:` non-empty AND `--run <id>` supplied |
| ready | pulled | legacy-born phase: every run line is `legacy\|legacy_wrong` (`new --legacy-run` / `move pulled`); `Witness:` still mandatory; every `legacy` run gets a `pulled_to:` (`--pulled-to`, else its own `where:`); refused when no run is `legacy` (nothing to review — `rule drop`) |
| submitted / running | same | `--run <id>` appends a wave, a chained job or a checkpoint resubmit (`resumes:`); state unchanged |
| submitted | running | — |
| submitted / running | ready | no run line in `submitted\|running` AND ≥1 `failed\|timeout\|void`; `--reason` required (→ writes `Reset:`) |
| running | pulled | no run line live; or `--partial` (a partial array), which `check` expects closed by a `leave-to-finish` ruling; `--pulled-to <path>` writes `pulled_to:` on every `done` run lacking one, and the move is refused when no `done` run would carry one |
| pulled | awaiting-ruling | — (the phase joins the rolling board) |
| awaiting-ruling | accepted / rerun / dropped | **`rule` only** |
| running / pulled / awaiting-ruling | same | `rule leave-to-finish` (state unchanged) |
| accepted | rerun / dropped | `rule --supersedes <current Ruling:>` only (the REWIND case) |
| rerun | ready | — (the witness may be re-registered; run history is kept) |
| any non-terminal | dropped | `rule drop` only |
| dropped | — | terminal (revival = a new phase number) |

`accepted` is **not** terminal: a later ruling may supersede the acceptance
(2026-08-31's REWIND superseded accepted gates). `dropped` is.

Offline invariants `check` enforces on top of the table:

- `State ∈ submitted..accepted` (and `rerun`) ⇒ `Witness:` non-empty.
- `State ∈ accepted | rerun | dropped` ⇒ `Ruling:` present (those states are
  reachable only through `rule`).
- `State = pulled` AND any run line `submitted | running` ⇒ `Ruling:` present
  and its head verb is `leave-to-finish` (the `--partial` case).
- `State = gated` ⇒ `Gates:` non-empty (a gate that does not exist cannot
  clear).
- A header key outside the table is drift (`Gate:` must not pass as a silent
  typo for `Gates:`); the five body sections are present; `Phase:` and
  `Review-minutes:` are integers, `Budget:` is `H+:MM` and `Filed:` is
  `YYYY-MM-DD`. A key with an empty value is read as absent.

---

## Repository layout

```
PyAutoCortex/
├── README.md                ← short front page
├── AGENTS.md                ← agent guidance (generated blocks: organism map, remote sessions, history)
├── CLAUDE.md                ← GENERATED pointer (@AGENTS.md) — repos_sync --write
├── REFERENCE.md             ← this file (schemas + grammars)
├── LICENSE  .gitignore
│
├── projects.yaml            ← the science body map — CODE, not ledger (read with PyYAML)
├── checkin.yaml             ← `refreshed: <UTC ISO>` — the last check-in stamp; LEDGER
├── dashboard.md             ← GENERATED board — cortex conductor (`dashboard --apply`); LEDGER
├── dashboard.html           ← GENERATED board, the Pages index; LEDGER
│
├── phases/<project>/<slug>.md          ← one file per phase (LEDGER)
├── rulings/AGENTS.md                   ← the append-only rule
├── rulings/<YYYY>/<MM>/R-<YYYYMMDD>-<nn>.md   ← the ledger of record (LEDGER, append-only)
├── batches/AGENTS.md                   ← "closed history: never modified, only added"
├── batches/<YYYY-MM-DD>-<slot>.md      ← the 2026-08/09 records (LEDGER, append-only)
├── batches/reviews/{AGENTS.md,<slot>.md}   ← the human's verbatim reviews (LEDGER, append-only)
│
├── docs/schema_decisions.md ← every dated choice the epic did not fix
├── policy/never_rewrite_history.md  policy/remote_sessions.md   ← copies of the Mind's; spliced into AGENTS.md
│
├── scripts/cortex.py        ← check · gates · rule · move · new (stdlib + PyYAML)
├── scripts/ledger_merge.py  ← the default-deny ledger classifier (+ append-only on rulings/, batches/)
├── tests/test_cortex.py  tests/test_ledger_merge.py
├── tests/fixtures/skeleton/ ← one project, one phase per state, five rulings — the witness
├── tests/fixtures/empty/    ← an empty map passes `check`
│
├── .github/workflows/cortex_check.yml       ← check + pytest on push/PR
├── .github/workflows/ledger_merge.yml       ← lands ledger-only `claude/**` branches
├── .github/workflows/dashboard_refresh.yml  ← renders the board; self-heals main
├── .github/workflows/pages_dashboard.yml    ← publishes dashboard.html to Pages
└── .claude/hooks/session-start.sh  .claude/settings.json   ← GENERATED — repos_sync --write
```

No `skills/` — the Cortex exposes no commands of its own; the conductor that
drives it lives in the Brain (`pyauto-brain cortex …`, AGENTS.md "Driving the
Cortex"), and the workflows above are the only things that run it unattended.

---

## Run lines (`## Runs`)

SLURM notation, strict grammar. One line per job or per task set of an array;
structured facts on **indented continuation lines**, never in the note.

```
- <stem>[_<task>|_[<a>-<b>,<c>]]: <run-state> — <partition> — submitted <YYYY-MM-DD> — wall <H+:MM>[ — <note>]
    pulled_to: <path>   |  after: <run>  |  resumes: <run>  |  where: <path>  |  ruled: <id>
```

- `<stem>` — the SLURM job id, digits. `_<task>` — one array task.
  `_[<set>]` — an array task set: comma-separated integers and `a-b` ranges,
  ascending, no spaces (`342091_[0-8,10]`).
- `<run-state>` ∈ `submitted | running | done | failed | timeout | void |
  legacy | legacy_wrong`. `void` = cancelled or never produced a step.
  `legacy` / `legacy_wrong` = quarantine (reusable / not) — **a run state,
  never a phase state**.
- `<partition>` — the SLURM partition the job went to, a bare word
  (`^[a-z][a-z0-9_-]*$`, e.g. `gpu`). The project's `partition:` row says
  which it may use.
- `submitted <YYYY-MM-DD>` — the submission date. `wall <H+:MM>` — wall time
  used so far (`0:00` for a job that never ran).
- `<note>` — free text after a fourth ` — `; never carries a structured fact.
- Continuation lines — exactly four spaces then `<key>: <value>`, keys:
  `pulled_to:` (laptop path the results were pulled to), `after:` (SLURM
  `afterok` dependency), `resumes:` (a checkpoint resubmit of that run),
  `where:` (the quarantine path of a `legacy*` run), `ruled:` (a ruling id
  naming this run).
- The em dash `—` is canonical; `--` is accepted for it (phone keyboards).
  `check` reads both as the same separator; the writing verbs emit `—`.

The regex, as `check` applies it (after `--` → `—` normalisation):

```python
RUN_LINE_RE = re.compile(
    r"^- (?P<stem>\d+)"
    r"(?:_(?P<task>\d+)|_\[(?P<tasks>\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*)\])?"
    r": (?P<state>submitted|running|done|failed|timeout|void|legacy|legacy_wrong)"
    r" — (?P<partition>[a-z][a-z0-9_-]*)"
    r" — submitted (?P<date>\d{4}-\d{2}-\d{2})"
    r" — wall (?P<wall>\d+:\d{2})"
    r"(?: — (?P<note>.+))?$"
)
RUN_CONT_RE = re.compile(
    r"^    (?P<key>pulled_to|after|resumes|where|ruled): (?P<value>\S.*)$"
)
```

`check` enforces:

- every non-blank line under `## Runs` matches `RUN_LINE_RE` or `RUN_CONT_RE`;
  a continuation line follows a run line;
- task sets on one stem are **disjoint within a phase** (job ids are unique
  per phase, not globally — one array may feed two phases);
- the `Runs:` header equals the set of body stems (both empty when the phase
  has no runs);
- `State: pulled` ⇒ at least one `done | legacy` run carries `pulled_to:`;
- a `legacy | legacy_wrong` run carries `where:`;
- an `after:` / `resumes:` target is the identifier (the text before the
  colon — `342091`, `342091_9` or `342091_[0-8,10]`) of another run line of
  the **same phase**;
- a `ruled:` value resolves to a ruling file.

---

## Rulings

`rulings/<YYYY>/<MM>/R-<YYYYMMDD>-<nn>.md`. The id is `R-YYYYMMDD-nn` — a
two-digit per-day sequence, global across projects; `rule` assigns it; the
filename equals the id and so does the title line (`# <id>` or
`# <id> — <one-line summary>`).

````markdown
# R-20260901-02 — re-accept phase 8 with the corrected evidence pointer

Project: example
Phase: phases/example/08_accepted.md
Runs: 342050
Ruling: accept
Supersedes: R-20260901-01
Batch: 2026-09-01-pm
Reviewed-at: 2026-09-01T17:20Z
Review-minutes-actual: 6
Follow-ups: PyAutoLens#901

## Ruling

The human's words, verbatim.

## Evidence

- pointers into the pulled results, the project ledger, figures
````

| Key | Value | Notes |
|---|---|---|
| `Project:` | project key | |
| `Phase:` | one phase path | repo-relative, `phases/<project>/<slug>.md` |
| `Runs:` | comma-separated stems, or empty | ⊆ the phase's `Runs:` |
| `Ruling:` | `accept \| rerun \| drop \| leave-to-finish` | the verb |
| `Supersedes:` | one ruling id | optional; see the chain rules |
| `Batch:` | `<YYYY-MM-DD>-<slot>` | optional-**historical**; the 2026-08/09 rulings' join, nothing writes new ones |
| `Reviewed-at:` | timestamp | |
| `Review-minutes-actual:` | integer | |
| `Follow-ups:` | comma-separated GitHub refs | `GATE_REF_RE`; **the issue is created before `rule` runs** |
| `Migrated-from:` | source path or ledger anchor | the review file or project-ledger entry a backfilled ruling was transcribed from |

Body: `## Ruling` — the human's words verbatim; `## Evidence` — pointers.

**One ruling file per phase.** A multi-phase ruling (a REWIND) is N `rule`
invocations with the same body — one per phase.

**Chain rules** (`check`):

- the id is unique, equals the filename stem and the title, and its date is
  the file's `<YYYY>/<MM>` directory; the body has `## Ruling` and
  `## Evidence`;
- `Supersedes:` resolves to an existing ruling, is not the ruling itself, is
  lexically smaller (earlier), and names the same project **and** phase;
- **at most one successor per ruling** — a chain, not a tree: supersede the
  head;
- the phase's `Ruling:` is a chain head (no ruling supersedes it) whose
  `Phase:` is that phase;
- the head's verb matches the phase's state: `accept ⇒ accepted`,
  `drop ⇒ dropped`, `rerun ⇒ rerun | ready | submitted | running | pulled |
  awaiting-ruling` (the phase has moved on), `leave-to-finish ⇒ any
  non-terminal state`;
- the ruling's `Runs:` ⊆ the phase's runs;
- `Batch:`, when present, names an existing `batches/<slot>.md`.

A phase may hold rulings that are not chained to each other — a
`leave-to-finish` followed by an `accept` is two chains of one. `Supersedes:`
is for replacing a verdict, not for sequencing.

The rest of the rule — append-only, supersede-never-edit, *a verdict recorded
only outside the Cortex does not exist* — is [rulings/AGENTS.md](rulings/AGENTS.md).

---

## Batches — closed history

`batches/<YYYY-MM-DD>-<slot>.md` and the human's verbatim reviews under
`batches/reviews/` are read-only history: three records from 2026-08/09, cited
by 13 rulings, kept because *a verdict recorded only outside the Cortex does
not exist*. They are **append-only** for the merge gate — never modified, only
added — and `check` no longer has a schema for them: the review-slot apparatus
that produced them (the packet page, the scored members, the review-minute
budget, the `-r<N>` sittings) was retired on 2026-09-03, and nothing writes a
new record.

A ruling's `Batch:` field is therefore **optional-historical**: where present
it must still name an existing `batches/<slot>.md`, and nothing writes a new
one.

---

## `projects.yaml`

Ordinary YAML, read with `yaml.safe_load` (PyYAML is `cortex.py`'s one
dependency; the hand-rolled restricted-subset parser it replaced was retired
on 2026-09-03, its own parity test having proved it equivalent). The document
is a mapping of project key → field mapping:

```yaml
<key>:                        # ^[a-z][a-z0-9_]*$
  <field>: <scalar>           # fixed field set, unknown field = error
  sync_verbs: [pull, push]    # a list of bare words
  note: "free text"           # the one optional field
```

What `check` validates is the **fields**, not the syntax: the document is a
mapping of rows, every key matches the key grammar, every field is in the set
below, `sync_verbs` is a list of bare words, and each value passes the rules
listed here. A document PyYAML cannot read is reported as one problem.

- Fields (required): `remote` (`owner/repo` | `none` — PyAutoLabs for active
  projects; a personal remote is recorded as a fact with a `note:`),
  `local_path` (absolute laptop path — the Cortex-only exception to the
  workspace-paths rule), `ral_root`, `mirror` (path | `none`), `sync_cli`,
  `sync_verbs`, `ledger`, `witness_file` (glob), `partition`
  (`gpu | ral | both`), `status` (`active | dormant | planned`).
- `note` (free text) is the **one optional field**: a row may omit it, an
  empty `note:` is drift, and any other field is still an unknown-field
  error. A note holding `:` or `#` is quoted like any other scalar.
- Science repos are **not** added to `PyAutoMind/repos.yaml` — that map is the
  workspace, this one is the science.
- A file with no rows parses to an empty map (`{}`); PyYAML returns `None`
  for a comment-only document, so the `yaml.safe_load(text) == parse(text)`
  parity test runs on the fixture, which has a row.

---

## How the ledger lands (`ledger_merge.yml`)

A push to a `claude/**` branch whose whole diff is **ledger** is merged into
`main` by `.github/workflows/ledger_merge.yml` and the branch deleted — no PR,
no session step. The line is drawn by `scripts/ledger_merge.py`, **default
deny**:

| Ledger — merged automatically | Code — always a human |
|---|---|
| `phases/**`, `rulings/**`, `batches/**` | `scripts/`, `tests/`, `.github/`, `policy/`, `docs/` |
| `checkin.yaml` | `projects.yaml`, `README.md`, `AGENTS.md`, `REFERENCE.md`, … |
| `dashboard.md`, `dashboard.html` (generated) | **`AGENTS.md` / `TEMPLATE.md` inside a ledger dir** |
| | anything unclassified — a new root file, a new top-level folder |
| | **any modification or deletion under `rulings/` or `batches/`** (append-only) |

Three exceptions inside the ledger dirs. Two are the Mind's: a **dot-path**
anywhere, and a file pytest would **collect** (`conftest.py`, `test_*.py`,
`*_test.py`). The third is the Cortex's own **doctrine carve-out** —
`rulings/AGENTS.md`, `batches/AGENTS.md` and `batches/reviews/AGENTS.md` are
ledger by location but instructional by content: they say what an entry may be and what
every future entry is stamped from, so a change to one is a change to
behaviour. Auto-merging a rewrite of `rulings/AGENTS.md` would let a branch
edit the rule that governs its own merge.

Pulling the other way, the two **generated** board pages are ledger: a branch
that moves a phase re-renders them in the same push, and
`dashboard_refresh.yml`'s self-heal commit has to land without a human.

And a fourth Cortex rule on *kind* rather than path: `ledger_merge.py`
classifies via `git diff --name-status`, and an `M`, `D` or `R` entry under
`rulings/**` or `batches/**` is code. `rulings/` because a ruling is
superseded, never edited; `batches/` since 2026-09-03, when the review-slot
apparatus was retired and its records became history — never modified, only
added.

The blocking check is `python3 scripts/cortex.py check` run on the **trial-merge
tree** — after `git merge --no-ff`, before `git push` — which is what catches
the ruling-id race (two branches both assign `R-…-03`: each passes alone, the
merge fails). A failing check resets the trial merge and leaves the branch for
a human. Predict the verdict before you push:

```bash
python3 scripts/ledger_merge.py classify --base origin/main   # exit 0 = will auto-merge
python3 scripts/cortex.py check                               # exit 0 = will not block
```

---

## `scripts/cortex.py` — the verb reference

Stdlib only; `main(argv)`; no import-time side effects; every verb takes
`--root <dir>` (default: the repo root the script lives in). Every leg of
`check` takes `root: Path`, so tests run it against a `tmp_path` copy.

- **`check`** — every rule in this file: phase headers and states, the witness
  invariant, `## Where to look` naming somewhere past `planned`, run lines,
  ruling ids and chains, the verb↔state agreement, every project named by a
  phase path is a `projects.yaml` key, and `projects.yaml`'s own fields. Hermetic (no network, no git). Output in `lifecycle.py`'s shape —
  `cortex check: OK` or `cortex check: DRIFT` followed by one `  - …` line per
  finding; exit 1 on drift.
- **`gates`** — read-only and offline: every `gated` phase, its refs and the
  URL each ref resolves to (`GATE_REF_RE` → `gate_url`). Nothing polls GitHub
  and nothing flips a state. Grading was retired on 2026-09-03 — in its whole
  life it saw 2 gated refs and flipped 0, while schema decision 54 routes
  sequencing through prose `Ready when:` lines. A human reads the listing,
  opens the refs and types `move <phase> ready`.
- **`rule <phase> <verb> --body <file> [--supersedes <id>] [--batch <slot>]
  [--minutes n] [--follow-up <ref>]...`** — assigns the next id for today,
  writes the ruling file, updates the phase's `Ruling:` and `State:` per the
  table (and appends `<id> — <verb>` to the phase's
  `## Ruling`); the ruling's `Runs:` is the phase's, its `## Evidence` is the
  phase's `## Where to look`; refuses to touch an existing ruling; refuses a
  verb the table does not allow from the phase's state; validates everything
  before writing anything.
- **`move <phase> <state> [--run <id>] [--reason ..]
  [--partial] [--pulled-to <path>] [--partition ..] [--after <run>]
  [--resumes <run>] [--note ..]`** — the table; refuses every ruling edge
  with a message naming `rule`. `--run` on `submitted`/`running` appends a
  run line and keeps the state; the appended line is
  `- <id>: submitted — <partition> — submitted <today> — wall 0:00[ — <note>]`
  with `after:` / `resumes:` continuations from the flags, and its
  partition is the project's `partition:` row unless that is `both`, when
  `--partition` is required. Every edit is an in-place header edit or an
  appended run line; every other byte of the file is preserved.
- **`new <project> <slug> --phase <n> [--gates ..] [--epic ..]
  [--legacy-run <id>]... [--legacy-wrong <id>]... [--where <path>]
  [--partition ..] [--witness ..] [--budget ..] [--minutes n] [--title ..]`**
  — writes `phases/<project>/<slug>.md` from the template in `planned` (or
  `ready` when `--legacy-run` / `--legacy-wrong` is given and every run is
  legacy); each legacy run line is written with today's date, `wall 0:00`
  and the note `pre-Cortex run, migrated` — the human corrects the date and
  wall by hand — and `--where` (required) as its `where:`; a legacy-born
  phase refuses `--gates`. Refuses a duplicate phase number, an existing
  file or an unknown project.

---

## Check-in

**One command.** `pyauto-brain cortex checkin` is the door the human types when
they want to know where their science is:

```bash
pyauto-brain cortex checkin --dry-run             # what it would pull and score
pyauto-brain cortex checkin --apply               # pull, score, move, render, push
pyauto-brain cortex checkin --apply --no-push     # ... without the push
pyauto-brain cortex checkin --apply --project subhalo_validation
pyauto-brain cortex checkin --apply --skip-pull   # re-score what is already here
```

It sweeps every `status: active` row of `projects.yaml`, plus any project that
owns a phase in `submitted | running`, and runs **that project's own**
`<local_path>/<sync_cli> pull` — the verb all seven implement. Nothing else
reaches a cluster; the conductor adds no SSH. A pull that exits non-zero is
recorded against its project and the sweep continues. Then it scores every live
phase (the six legs below), moves `running → pulled → awaiting-ruling`,
re-renders `dashboard.md` + `dashboard.html`, and prints a summary keyed **by
project** — the last thing on screen, so a chat sees it first.

### `checkin.yaml` — the last-check-in stamp

One key, one line, committed and pushed with the ledger:

```yaml
refreshed: 2026-09-04T14:03:00Z
```

It records the last **check-in**, not the last render: `checkin --apply` (and
`collect --apply`) writes it from the same stamp it scored against, before the
pages are rendered, so a doc-only push that re-renders the board cannot fake
freshness. The board reads it back as "Last check-in"; the HTML twin computes
the age on the *viewer's* clock and reddens it past sixty minutes, because a
static page cannot know when it is being read. Absent, the board says "never
checked in". The file is stable between renders, so `dashboard --check` needs
no rule for it.

### The by-project view

The summary is a tree, and it is the same tree in three places: the
`## By project` section of `dashboard.md` / `dashboard.html`, the text
`pyauto-brain cortex census --by-project` prints from the checkout alone, and
the closing summary of a real `checkin` (which is the only one of the three
carrying pull results and six-leg health). One builder, three renderings — a
prompt added to a state appears in all of them.

Per project: the three folders it lives in (`local_path`, `mirror` when it has
one, `ral_root`), what came of its pull, its phase counts by state, then every
phase that is still **open** — awaiting a ruling, still out there, ready to
submit, gated, planned — each with its state and health, its `## Where to look`
bullets verbatim, and a copy chip per prompt its state carries. `accepted`,
`rerun` and `dropped` phases are history and appear only in the counts. A
project gets a block when its `projects.yaml` row is `status: active`, or when
it still holds an open phase; every other project folds into one line.

On the board `## By project` is the **first** section, above the state lists:
those are cross-project, so every row has to be read to find out whose it is,
while this one answers "where is everything" a screen per project. The counts
table sits above it and keeps the urgency sections one tap away; the counts
strip itself is unchanged (the Brain board reads it).

### The five starting prompts

Every phase row hands the reader a command rather than a decision. Which
prompts a phase carries is its **state**, and nothing else:

| Prompt | States | What it says |
|---|---|---|
| rule on it | `pulled`, `awaiting-ruling` | read the witness and the pulled evidence, draft the ruling body, `rule <phase> <verb> --body <file>` |
| the results are good — accept and open phase N+1 | `pulled`, `awaiting-ruling` | `rule <phase> accept --body <file>`, then open the next phase (below) |
| run it again | `pulled`, `awaiting-ruling`, `running` | `rule <phase> rerun --body <file>`, `move <phase> ready`, the project's own submit, `move <phase> submitted --run <jobid>` |
| where the jobs stand | `submitted`, `running` | the project's own `<sync_cli> jobs` |
| submit it | `ready` | the phase, the project's own submit verb, `move <phase> submitted --run <jobid>` |

(`gated` and `planned` phases carry the one-line `gates` / `move … ready`
command they always had.)

**Accept and open phase N+1** is two commands in one prompt because they are
one decision: an accept that opens nothing leaves the programme where it was.
Its second half prefills from the tree — when the project already holds a
phase numbered N+1 in `planned` or `gated`, the prompt opens *that* phase
(`move … ready` + the launch) rather than writing a second one beside it;
when N+1 is taken by a phase that has already run, it says so and offers the
lowest free number instead. The `new` line carries the phase's own `Epic:` and
spells out the title rule: **`new` writes `# <Project> — phase N: ` in front
of `--title` itself**, so `--title` takes the tail alone.

**Run it again** is a ruling first: `rerun` is the only verb that puts a phase
back on the board, so the verdict on what came back is what makes the next
submission a rerun rather than a repeat. Its `move … submitted --run` line
carries the reminder that it is one run per call (`--after <run>` chains the
next).

The payloads are short on purpose. They are pasted into a fresh chat, not run
as scripts: every one of them ends in a human's own reading, and the `<file>`,
`<script>`, `<slug>` and `<jobid>` placeholders are where that reading lands.

### `.cortex/pull.json` — the pull manifest

After a successful pull the door writes the manifest at the top of that
project's pull root (its `mirror` if it has one, else its `local_path`) —
the same file `collect`'s checkpoint leg reads:

| Key | Written by | Meaning |
|---|---|---|
| `project` | the check-in | the `projects.yaml` key this tree belongs to |
| `pulled_at` | the check-in | UTC `YYYY-MM-DDTHH:MMZ` of the pull that just finished |
| `cmd` | the check-in | the pull as a human would type it (`cd <local_path> && <sync_cli> pull`) |
| `rc` | the check-in | that pull's exit code — `0`, or the manifest is not written |
| `phases_live` | the check-in | the phase paths that were `submitted \| running` when it ran |
| `schema` | a project's own CLI | `1` where the CLI writes the richer shape; absent = the older `runs`-only one |
| `checkpoints` | a project's own CLI | `{"<run dir, relative to the pull root>": {"bytes": N, "mtime": ISO}}` |
| `runs` | a project's own CLI | `{"<jobid|jobid_task>": {"checkpoint_bytes": N, "checkpoint_mtime": ISO}}` |

**Merged, never clobbered.** `autolens_profiling`'s own `hpc/sync` already
writes `checkpoints` / `runs` here — the only window onto the RAL-only
`search_internal/checkpoint.hdf5`, which no pull mirrors. The check-in adds its
five keys and leaves every other key exactly as it found it, so the richer
manifest keeps making the checkpoint leg scorable. Without a manifest that leg
is `UNOBSERVABLE`, not `FAIL`.

The manifests live **outside** this repository, in the science trees, so
`cortex.py check` says nothing about them; the check-in's own note line
(`<project>: pulled → <path>`) is the record that one was written.

### The push

`--push` is allowed only when **`gh auth status` succeeds** *and* **this
checkout is clean on `main`** — checked before anything is written, since
"clean" stops being true the moment the phases move. That is the cloud/laptop
split and it is also the default: a laptop pushes without asking, a cloud
session cannot and says so. The push cuts `claude/checkin-<YYYY-MM-DD>` from a
fresh `origin/main`, commits the changed paths explicitly and pushes;
`ledger_merge.yml` then merges it into `main` and deletes the branch (below).
`scripts/ledger_merge.py classify` is asked **first** and a code-classified
diff — `projects.yaml`, `scripts/`, the prose pages — is refused before the
branch is cut. Never `main` directly, never `--force`.

## Driving the Cortex — the conductor and the workflows

The Cortex is state plus `cortex.py`. The reasoning over it — the board and the
check-in — is the Brain's **cortex conductor**:

```bash
pyauto-brain cortex checkin [--dry-run|--apply] [--push|--no-push] [--project KEY] [--skip-pull] [--refreshed ISO]
pyauto-brain cortex census [--json]                  # what is held, by state
pyauto-brain cortex census --by-project              # ... by project: folders, open phases, prompts
pyauto-brain cortex dashboard --check | --apply      # render the two pages
pyauto-brain cortex gates                            # the gated phases and their refs
pyauto-brain cortex collect [--phase REL] [--pull] [--refreshed ISO] [--apply] [--out F]
```

`checkin` composes the others (above). `collect` with no `--phase` scopes to
**every** phase in `submitted | running` — the scorer on its own.

With no Brain install, or from a workflow:

```bash
python3 ../PyAutoBrain/agents/conductors/cortex/_cortex.py dashboard --cortex . --check
```

`--cortex` is a flag of the **subcommand**, not a global one: it follows the
verb. (`--cortex . dashboard --check` exits 2.) The root is resolved
`--cortex` → `$PYAUTO_CORTEX` → `PyAutoCortex` beside the Brain checkout.

**Two spellings of the same flag.** The conductor writes with `--apply` (the
Brain's house spelling); `scripts/cortex.py` writes with `--write`. Every edit
to a phase is `cortex.py`'s either way.

**The `--check` exit-code contract** (`dashboard_refresh.yml` depends on it):

| Code | Meaning | What the caller does |
|---|---|---|
| 0 | the committed pages match a fresh render | nothing |
| 1 | **drift** — and nothing else | error on a PR, self-heal on main |
| 2 | bad args — this Brain has no such verb/flag | report a renderer failure |
| other | the renderer could not run (a Brain/Cortex skew) | report a renderer failure |

Treating 2 as drift sends whoever reads the log to fix `dashboard.md` when the
broken thing is the Brain: `dashboard_refresh.yml` wraps the call in `check()`
for exactly that reason.

### What each workflow may write

| Workflow | Trigger | Writes |
|---|---|---|
| `cortex_check.yml` | push/PR on `phases/ rulings/ batches/ projects.yaml checkin.yaml dashboard.* scripts/ tests/` | nothing (`cortex.py check` + pytest) |
| `dashboard_refresh.yml` | push to main + PR on the ledger paths and the two pages, nightly **03:35 UTC**, dispatch | `dashboard.md`, `dashboard.html` on main (3-attempt fetch/reset/render/commit/push); a PR run errors instead of healing |
| `pages_dashboard.yml` | push to `dashboard.html`, dispatch | nothing in git — publishes `dashboard.html` as the Pages index |
| `ledger_merge.yml` | push to `claude/**`, dispatch | merges a ledger-only branch into main |

**No scheduled job mutates the ledger.** A daily gate-grading cron did until
2026-09-03; retiring gate grading retired it with no replacement.

Every workflow that can push to main shares `concurrency: group:
cortex-main-writers, cancel-in-progress: false` — `dashboard_refresh.yml` and
`ledger_merge.yml` — so two bot writers never race for the tip.
`pages_dashboard.yml` keeps its own `group: pages`.

A push made with `GITHUB_TOKEN` triggers **no** workflow, so each writer
re-dispatches by name what its push should have woken: `dashboard_refresh.yml`
asks for `pages_dashboard.yml` (on both paths — fresh *and* healed; folding the
fresh one away is the bug that stranded the Mind's published board), and
`ledger_merge.yml` asks for `cortex_check.yml`.

The board is published at **<https://pyautolabs.github.io/PyAutoCortex/>**.

---

## Bootstrap

```bash
cd ~/Code/PyAutoLabs
git clone https://github.com/PyAutoLabs/PyAutoCortex.git
python3 PyAutoMind/scripts/repos_sync.py --write      # CLAUDE.md, .claude/, the AGENTS.md blocks
python3 PyAutoCortex/scripts/cortex.py check           # OK on an empty tree
```

The checkout directory must be named `PyAutoCortex`; the organism's sync and
drift scripts address it by that name.
