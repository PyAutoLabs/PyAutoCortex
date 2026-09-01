# Batch records — the rolling board

One file per review slot: `<YYYY-MM-DD>-<slot>.md`. This is the ledger of what
was on the board for one slot and what the human ruled — the same genre as the
Mind's batch records, and the evidence base the review-minute estimate is
calibrated from. It is the Mind's schema with what a science batch changes.

It auto-merges (`scripts/ledger_merge.py` — `batches/` is a ledger dir),
because an unattended system that cannot record its own history unattended
will not record it.

## A rolling board, not a dispatch

A dev batch is dispatched at once and reviewed at once. A Cortex batch is a
**live board**: a phase **joins** the review when its results are `pulled`;
nothing in `submitted` or `running` holds review control — those members are
shown as running, and a `leave-to-finish` is the only thing the human can say
about them; the board is the live view of run progress. Each pull appends a
`refreshed:` line — that list is the record of the board filling in.

## Schema

```markdown
# Batch 2026-09-01 pm
- dispatched: 2026-09-01T09:00Z      # when the board was opened
- review-at: 2026-09-01T17:00Z       # stated by the human AT DISPATCH — the shift is dispatch → review-at
- shift: day                         # free-text label the human gives it
- lane: local-dev                    # always — the review happens at the laptop
- review-minutes-planned: 20
- members:
  - <slug>: <phase path> — <runs> — <review-minutes> — <state>
- refreshed: 2026-09-01T11:40Z — <slug> pulled      # one line per pull, appended in order
- refreshed: 2026-09-01T15:05Z — <slug> pulled
- collected: 2026-09-01T17:00Z
- reviewed-at: 2026-09-01T17:10Z     # when they actually sat down
- delivered: <n>/<n>
- packet: batches/packets/<YYYY-MM-DD>-<slot>.html
- review: batches/reviews/<YYYY-MM-DD>-<slot>.md
- review-minutes-actual: <n>
- notes: |
    What actually happened. Anything that stalled, and why.
```

The member line is `<slug>: <phase path> — <runs> — <review-minutes> —
<state>`: the phase file's stem, its repo-relative path, the comma-separated
run stems (or `none`), the review-minute seed, and the phase's state at the
last refresh. `cortex.py check` verifies every member line against its phase
file.

Dropped from the Mind's schema, on purpose: `usage-window-*` (no cloud
sessions are spent by a science batch), `heart-ack:` (the Heart gates
releases, not runs) and `expected-effects:` (the licence for an autonomous
YELLOW acknowledgement; a science batch has no autonomy leg to license).

## The fields that are easy to get wrong

**`delivered:` is not `sacct COMPLETED`.** SLURM's verdict says the process
exited; it does not say the run produced science. A member counts as delivered
only when **all four** hold: the `.err` file is clean, wall < `Budget:`, the
output carries the version stamp of the installed stack, and
`checkpoint.hdf5` is sane (opens, holds the expected step count). A run that
`COMPLETED` with an empty checkpoint is **not delivered**, loudly, at the top
of the packet.

**`review-at:` is the shift, and it is the human's to declare.** There is no
schedule: a slot is whenever they come in, so at dispatch they state when they
expect to be back and the shift is dispatch → `review-at:`. `reviewed-at:` is
the same number measured rather than promised. Per Cortex batch, separately
from any dev batch open the same day: the two surfaces have their own records
and their own `review-at:`.

**`refreshed:` is the board's history.** A member joins on the pull that
fills its results in; the line says when and which. A packet refreshed without
the line is a board whose history cannot be audited.

**`review-minutes-actual:` is the only calibration there is.** The planned
figure is a seed; this is what the slot really cost.

**`packet:` is the page the human actually reviewed, archived** — see
`packets/AGENTS.md`. **`review:` is what the human said, verbatim** — see
`reviews/AGENTS.md`; every ruling `cortex.py rule --batch <slot>` files
traces back to a line in that file.
