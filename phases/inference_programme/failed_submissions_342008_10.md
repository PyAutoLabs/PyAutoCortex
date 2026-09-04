# Inference_programme — phase 6: the three submissions that died in a second (CWD trap)

Project: inference_programme
Phase: 6
State: dropped
Gates:
Witness: the three submissions produce result rows; they did not — each died in about one second before writing any output
Budget: 6:00
Runs: 342008, 342009, 342010
Ruling: R-20260901-04
Review-minutes: 1
Epic: jax-inference-profiling
Filed: 2026-08-29
Migrated-from: PyAutoMind/batches/2026-08-31-am.md § member failed-submissions-342008-10

## Question

Three hand submissions from the 2026-08-29 night wave died in about a second each. Why, and is
anything recoverable from them?

The answer is the CWD trap: the jobs were submitted from a directory the batch scripts could
not resolve their paths against. Carried into the 2026-08-31-am packet as `UNREVIEWED`, the one
member the human left untouched, and carried again past the pm slot.

## Witness

Result rows under the active `output/searches/` tree for the three job ids.

None exist. Each job died in ~1 s before writing a run directory, so there is no output to
pull, nothing to quarantine but the job ids themselves, and no `.out` log reached the mirror.

## Where to look

- `inference_programme` (project row): nothing under `output/` — the runs wrote no directory
- `PyAutoMind/batches/2026-08-31-am.md` — member `failed-submissions-342008-10`, `UNREVIEWED, carried to next packet`
- `autolens_profiling/results/notes/inference/DECISIONS.md` — the 2026-08-31 REWIND entry that superseded the question

## Runs

- 342008: legacy_wrong — gpu — submitted 2026-08-29 — wall 0:00 — pre-Cortex run, migrated; died in ~1 s under the CWD trap — no run directory, no output, no .out log on the mirror
    where: output/legacy_wrong/
- 342009: legacy_wrong — gpu — submitted 2026-08-29 — wall 0:00 — pre-Cortex run, migrated; died in ~1 s under the CWD trap — no run directory, no output, no .out log on the mirror
    where: output/legacy_wrong/
- 342010: legacy_wrong — gpu — submitted 2026-08-29 — wall 0:00 — pre-Cortex run, migrated; died in ~1 s under the CWD trap — no run directory, no output, no .out log on the mirror
    where: output/legacy_wrong/

## Ruling

R-20260901-04 — drop
