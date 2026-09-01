# PyAutoCortex

**PyAutoCortex is the Cortex of the PyAutoScientist** — where the organism
learns what is true. The Mind decides what to build, the Brain routes the work
and executes nothing, the Cortex learns what is true: it holds the **science
body map** (every science project, where it lives, how it syncs) and the
**rulings of record** — every verdict a human has passed on a science run,
append-only, superseded but never edited.

## How PyAutoCortex works

The unit is a **phase** of a **project**, which spawns **runs** (SLURM job ids)
and ends in a **ruling**:

1. **Declare the phase.** A markdown file under `phases/<project>/` states the
   question, the pre-registered witness, the wall budget and the GitHub issues
   it waits on (`Gates:`). It starts `planned` or `gated`.
2. **Run it.** When the gates clear the phase is `ready`; a submission makes
   it `submitted` and then `running`, with every job id recorded in the file's
   `## Runs` block in SLURM notation.
3. **Pull and review.** When the results are pulled to the laptop the phase
   joins the **rolling review board** (`batches/`); a member joins when its
   results are in hand, never mid-flight.
4. **Rule.** The human's verdict — `accept`, `rerun`, `drop` or
   `leave-to-finish` — is written into `rulings/` with a permanent id. *A
   verdict recorded only outside the Cortex does not exist.*

The Cortex is **not a second PyAutoMind**: development tasks stay in the Mind
and are named here only as gates. Its one script, `scripts/cortex.py`, checks
the tree and moves phases between states; the ledger folders auto-merge from
any surface that can push.

The schemas — phase files, the run-line grammar, rulings, batches, the
`projects.yaml` subset — are in [REFERENCE.md](REFERENCE.md); how agents should
operate this repo is in [AGENTS.md](AGENTS.md); every design choice the birth
epic did not fix is dated in [docs/schema_decisions.md](docs/schema_decisions.md).
The organism this repo is the Cortex of is described once in
[PyAutoBrain/ORGANISM.md](https://github.com/PyAutoLabs/PyAutoBrain/blob/main/ORGANISM.md)
and documented in full at <https://pyautoscientist.readthedocs.io>.
