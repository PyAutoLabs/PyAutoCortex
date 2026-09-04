# Inference_programme — phase 19: sweep the point-source families out of the RAL active output/ tree into output/legacy_point/

Project: inference_programme
Phase: 19
State: planned
Gates: autolens_profiling#205
Witness: `output/legacy_point/` exists on RAL and on the laptop mirror holding all three point-source families (`image_plane`/`source_plane` fits, `Cluster`, `point_source`) with their directory structure preserved; the active `output/` tree no longer contains them; the certified `InferenceRefs_v1` mesh rows (R-20260902-01, R-20260904-01) are STILL PRESENT in the active tree and were not moved; a spot check finds any moved run under its new path; nothing deleted; a dated one-line note appended beside the ledger
Budget: 2:00
Runs:
Ruling:
Review-minutes: 5
Filed: 2026-09-01
Migrated-from: PyAutoMind/draft/maintenance/autolens_profiling/legacy_point_output_sweep.md

## Question

Can the RAL active `output/` tree be reduced to only what the redo can cite, by
moving (never deleting) the spent **point-source** families into
`output/legacy_point/` — while leaving the certified mesh references in place?

Note: autolens_profiling#205 was opened 2026-09-01 as this work's Cortex gate ref —
reuse it, never open a second.

**Re-scope 2026-09-04 — the mesh rows STAY.** The 2026-09-01 directive's "all
mesh results" clause is **superseded** by the two rulings that certified the
positions-on mesh baselines: **R-20260902-01** (phase 10 — `pos_tauto0.2_f1e8`
is the confirmed physical configuration for a mesh source; a mesh run *with*
`positions.info` is citable, one without is not) and **R-20260904-01** (phase 12
— rows 11–13 joined `InferenceRefs_v1`, now 9 certified baselines). Those mesh
rows in the active tree ARE the `InferenceRefs_v1` references the redo cites,
so moving them would move exactly the evidence this sweep exists to protect.
The sweep is therefore **three families, not four**: only the point-source
material leaves the active tree.

### Where this came from

The 2026-08-31-pm batch review's `delaunay-fp64-retro-baseline` rejection
(2026-09-01) carried a programme-wide finding *and* an output-tree directive.
The human inspected
`output/legacy_wrong/searches/nautilus/imaging/delaunay/hst/hpc_a100_fp64/` and
identified the solution as a demagnified-source unphysical solution — the
classic Inversion bias `PositionsLH` exists to remove. The binding consequence
for the redo is that every mesh / pixelization run must carry a `PositionsLH`
positions penalty; mesh rows produced without it are not citable as references.

The directive this phase enacts is the second half of that ruling, recorded
verbatim in `autolens_profiling/results/notes/inference/DECISIONS.md` (entry
"2026-09-01 — Batch 2026-08-31-pm review rulings", lines 1553-1559):

> **Output-tree consequence (human directive, verbatim intent):** clear the RAL
> active `output/` of all mesh results, the `image_plane`/`source_plane` point
> source fits, the `Cluster` folder and the `point_source` folder — moved (not
> deleted) to a new `output/legacy_point/` folder, so the active tree is clean and
> updates with each task. Laptop action, queued as a local-dev prompt in the Mind.

### What to do

**Move, do not delete.** Exactly the three families named below are relocated
into a new `output/legacy_point/` folder that mirrors the source tree's shape,
so any of it can be cited or pulled back:

1. the `image_plane` and `source_plane` point-source fits;
2. the `Cluster` folder;
3. the `point_source` folder.

**Do NOT move the mesh rows.** Per the 2026-09-04 re-scope above, the mesh /
pixelization results in the active tree that carry `positions.info` are the
certified `InferenceRefs_v1` references (R-20260902-01, R-20260904-01) and must
stay exactly where they are. If a mesh run in the active tree has *no*
`positions.info`, it is unreliable under R-20260902-01's binding rule — that is
a separate question and is not this phase's business either way.

Do the same on the laptop mirror (`/mnt/c/Users/Jammy/Science/inference_programme/`)
so the two trees stay in step — a sweep on one side only reintroduces the drift
this is meant to remove.

**This is a laptop action.** It needs the SSH endpoint to RAL and the local
mirror, so it cannot run in a cloud session. Nothing is submitted, cancelled or
modified on the cluster — this is a file move, which is why `Runs:` stays empty.

### Why it matters

The active `output/` tree is what each new task reads and updates. Leaving the
quarantined and superseded families in it means every subsequent read has to
know which subtrees are spent, which is exactly the state the 2026-08-31 rewind
was meant to end. After the sweep the active tree holds only work the redo can
actually cite.

## Witness

- `output/legacy_point/` exists on RAL and on the laptop mirror and holds all
  **three** point-source families named above, with their directory structure
  preserved.
- The active `output/` tree no longer contains those three families.
- The certified `InferenceRefs_v1` mesh rows (R-20260902-01, R-20260904-01) are
  still present in the active `output/` tree — the sweep did not touch them.
- Nothing was deleted — a spot check can find any moved run under its new path.
- A one-line note appended beside the ledger recording that the sweep ran, on
  what date, and that the mesh clause was superseded.

## Where to look

- `/mnt/ral/jnightin/autolens_profiling/output/` — the three point-source
  families are what moves; nothing under `output/searches/nautilus/imaging/`
  carrying `positions.info` does
- `/mnt/c/Users/Jammy/Science/inference_programme/`
- `autolens_profiling/results/notes/inference/DECISIONS.md` (2026-09-01 entry —
  its "all mesh results" clause is superseded, see the re-scope above)
- `autolens_profiling/results/baselines/InferenceRefs_v1/SUBMIT_LIST.md` — the
  certified mesh rows that must NOT be moved
- `rulings/2026/09/R-20260902-01.md`, `rulings/2026/09/R-20260904-01.md`

## Runs

## Ruling
