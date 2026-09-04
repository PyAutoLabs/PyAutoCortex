# Inference_programme — phase 10: InferenceRefs_v1 redo — the Phase 1 restart wave (array 342091)

Project: inference_programme
Phase: 10
State: accepted
Gates:
Witness: all 10 array tasks deliver on their own evidence — wall inside the 6:00 budget, a result row carrying version 2026.8.17.1 and a matching target_id, `.err` free of Tracebacks, `.out` ending "Finished." with a `.completed` marker, zero "Fit Already Completed" and no overflow signature
Budget: 6:00
Runs: 342091
Ruling: R-20260902-01
Review-minutes: 20
Epic: jax-inference-profiling
Filed: 2026-08-31
Migrated-from: PyAutoMind/batches/2026-08-31-pm.md § member jax-inference-phase1-refs

## Question

The restart point the REWIND named: Phase 1, the `InferenceRefs_v1` reference baselines, redone
step by step under batch-and-review. Do the 10 cells of the refs array deliver clean reference
rows on the current stack?

Dispatched from the laptop 2026-08-31T21:08Z as RAL job 342091,
`sbatch --array=0-8,10 --requeue` from `hpc/batch_gpu/`. Task 9 (`mge_pos`) was held back under
the MGE reuse rule and became phase 7.

These are pre-Cortex runs, so they enter the ledger as `legacy` lines with `where:` pointing at
the active mirror tree they actually landed in (not a quarantine path) and `pulled_to:` the same.

**No ruling yet.** R-20260901-03 spent the mesh rows' citability — a mesh row produced without
a `PositionsLH` positions penalty is not a citable reference — so this wave's mesh rows must be
checked against that before certification. The human rules the wave in the next slot.

## Witness

All 10 tasks COMPLETED 0:0 on euclid-ral-gpu-2, each classified DELIVERED from artefacts rather
than `sacct`: wall 10–23 % of the 6 h budget; result row with version `2026.8.17.1` and matching
`target_id`; `.err` carrying only the 222 B mask-padding UserWarning and no Traceback; `.out`
ending "Finished." with a `.completed` marker; zero "Fit Already Completed"; no overflow
signature.

maxLL / logZ against truth 31,521.744:

| task | cell | maxLL | logZ |
|---|---|---:|---:|
| t0 | pixelization | 29,835.4509 | 29,778.0569 |
| t1 | delaunay_nn | 30,650.8283 | 30,591.1280 |
| t2 | delaunay_nn pos-0.3 | 31,351.3909 | 31,275.2300 |
| t3 | slam_source_pix | 31,026.6354 | 30,951.7885 |
| t4 | slam_source_pix pos-auto | 31,547.2396 | 31,452.0997 |
| t5 | slam_source_pix_nn | 30,750.9893 | 30,684.1146 |
| t6 | slam_source_pix_nn pos-auto | 31,405.6282 | 31,324.8382 |
| t7 | knn | 30,062.6117 | 29,995.6676 |
| t8 | delaunay_matern | 30,675.9711 | 30,615.1603 |
| t10 | delaunay pos-auto | 31,338.4344 | 31,264.8345 |

t4 is the only row above truth (+25.50). The stale-knn flag is CLOSED: task 7's real run
replaced the stashed 30,077.028 with 30,062.612 — 14.4 nats lower still and ~494 below the
Prodigy arm bar 30,557.03, so the knn cell genuinely underperforms.

## Where to look

- `inference_programme` (project row): `output/searches/nautilus/imaging/` — the 10 run trees
- `logs/output/output.342091_{0-8,10}.out` and the matching `logs/error/` files on the mirror
- `autolens_profiling/results/notes/inference/PROGRAMME.md` — the rewind restart point
- autolens_profiling#200 (queue anchor), #201 (this leg), docs-only PR #202

## Runs

- 342091_[0-8,10]: legacy — gpu — submitted 2026-08-31 — wall 1:24 — pre-Cortex run, migrated; 10 tasks run serially on one A100, 22:00:39 BST 31 Aug → 08:08:54 BST 1 Sep (10 h 08 m end to end); wall shown is the longest single task. Task 9 (mge_pos) held back under the MGE reuse rule — see phase 7
    where: output/searches/nautilus/imaging
    pulled_to: output/searches/nautilus/imaging

## Ruling

R-20260902-01 — accept
