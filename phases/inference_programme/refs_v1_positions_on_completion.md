# Inference_programme — phase 12: InferenceRefs_v1 positions-on completion — pixelization / knn / delaunay_matern (array tasks 11-13)

Project: inference_programme
Phase: 12
State: accepted
Gates:
Witness: all 3 array tasks deliver on their own evidence — wall inside the 6:00 budget, a positions.info file in the run dir, a result row carrying version 2026.8.17.1 and a target_id that recomputes from _targets.py, .err free of Tracebacks, .out ending "Finished." with a .completed marker, zero "Fit Already Completed", no overflow signature; each row's maxLL lands within the 29,800–31,600 band of the accepted positions-on rows rather than 500+ nats below it
Budget: 6:00
Runs: 342241
Ruling: R-20260904-01
Review-minutes: 15
Epic: jax-inference-profiling
Filed: 2026-09-02

## Question

The Phase 1 redo (phase 10, R-20260902-01) certified four positions-on mesh references and
retired the positions-off mesh reference design. Three mesh cells were left without any
citable reference because their only 342091 rows ran positions-off: `pixelization` (t0),
`knn` (t7) and `delaunay_matern` (t8). Do the positions-on replacements — array tasks 11, 12
and 13 of `submit_search_nautilus_inference_refs_v1_array.sh` (autolens_profiling#209), all at
`pos_tauto0.2_f1e8`, n_live 300, seed 0, fp64 — deliver clean reference rows for
`pixelization_pos_fp64`, `knn_pos_fp64` and `delaunay_matern_pos_fp64`?

Under the binding mesh positions rule (R-20260902-01) each run dir must carry `positions.info`;
the accepted positions-on rows sit 520–700 nats above their positions-off twins, so a
replacement row that lands at or below its struck positions-off twin (29,835 / 30,063 /
30,676) is the demagnified basin again and is not accepted.

Dispatch: `sbatch --array=11-13 --requeue` from `hpc/batch_gpu/` on RAL once #209 is on main.

## Witness

all 3 array tasks deliver on their own evidence — wall inside the 6:00 budget, a positions.info file in the run dir, a result row carrying version 2026.8.17.1 and a target_id that recomputes from _targets.py, .err free of Tracebacks, .out ending "Finished." with a .completed marker, zero "Fit Already Completed", no overflow signature; each row's maxLL lands within the 29,800–31,600 band of the accepted positions-on rows rather than 500+ nats below it

## Where to look

- `inference_programme` (project row): `output/searches/nautilus/imaging/{pixelization,knn,delaunay_matern}/hst/pos_tauto0.2_f1e8/hpc_a100_fp64_ref_pos_tauto0.2_f1e8/` — the three run trees, each with `positions.info`
- `logs/output/output.<job>_{11,12,13}.out` and the matching `logs/error/` files on the mirror
- `autolens_profiling/results/searches/nautilus/imaging/{pixelization,knn,delaunay_matern}/hst/hpc_hpc_a100_fp64_ref_pos_tauto0.2_f1e8.json` on RAL (result rows; not pulled to the mirror)
- `autolens_profiling/results/baselines/InferenceRefs_v1/SUBMIT_LIST.md` rows 11–13
- autolens_profiling#209 (array rows), #201 (Phase 1 redo leg), #200 (queue anchor)

## Runs

- 342241_[11-13]: done — gpu — submitted 2026-09-02 — wall 0:55 — three tasks serial on euclid-ral-gpu-2, 20:59 BST 2 Sep → 00:50 BST 3 Sep; wall shown is the longest single task (knn, sampler 3,257 s); sbatch --array=11-13 --requeue from hpc/batch_gpu on RAL, 2026-09-02 ~16:50Z; pending (Resources) at submit
    pulled_to: output/searches/nautilus/imaging

## Ruling

R-20260904-01 — accept
