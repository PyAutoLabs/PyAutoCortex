# Inference_programme — phase 18: multi-band compile census completion — A100/multi-core + hetero GPU rows

Project: inference_programme
Phase: 18
State: dropped
Gates:
Witness: the A100/multi-core and `datacube_img_hetero` GPU rows present in the multi-band census results, each with its backend verified from the results path rather than the SLURM partition, plus a written verdict on the two remaining secondary levers in `scripts/misc/jax_compile/README.md`
Budget: 12:00
Runs:
Ruling: R-20260904-05
Review-minutes: 20
Filed: 2026-07-30
Migrated-from: PyAutoMind/draft/research/autolens_profiling/multiband_compile_census_completion.md

## Question

Do the confirmatory census legs of the multi-band compile matrix — the rows that
were out of scope when the dominant driver was fixed at the source — change the
picture?

Follow-up to the multiband-pyloop-batching ship (PyAutoFit#1430 → PR#1431 +
autolens_profiling#95, merged 2026-07-30). The dominant driver is fixed at the
source (Python-loop batching + jitted broad-start filter in
`AbstractMultiStartGradient`); these are the confirmatory legs left over:

1. **A100 / multi-core rows** for the multi-band matrix (`datacube_img` /
   `datacube_img_hetero` × `pyloop_vag` / `laxmap_vag` at production widths) —
   re-run `sbatch /mnt/ral/jnightin/pixgrad_logs/census_gpu.sbatch` (or the
   local pattern in `scripts/misc/jax_compile/probe.py`) once the RAL A100s
   free up. Verify backend from the results path, never the partition (the
   silent-CPU-fallback trap from #93).
2. **`datacube_img_hetero` GPU rows** on the laptop RTX 2060 — quantify the
   heterogeneity multiplier under the CUDA pipeline (the laptop GPU rows so far
   are homogeneous only; the scan explosion proved CPU-backend-specific, tags
   `mb_homo_cold_{pyloop,laxmap}_gpu`).
3. **Verdict on the remaining secondary levers** — with the transform fixed,
   reassess whether the band-padding/shape-canonicalization helper and the
   per-factor jit boundary (heterogeneity-multiplier attacks, README verdict
   bullets) are still worth building, and either file them or close them in
   `scripts/misc/jax_compile/README.md`.

## Witness

The A100/multi-core rows and the `datacube_img_hetero` GPU rows present in the
census results with the backend read off the results path (not the partition),
and the secondary-lever verdict written into
`scripts/misc/jax_compile/README.md` — filed as follow-ups or closed, not left open.

## Where to look

- `autolens_profiling/results/notes/multiband_pyloop_productized.md`
- `autolens_profiling/scripts/misc/jax_compile/README.md` (multi-band section)
- `/mnt/ral/jnightin/pixgrad_logs/census_gpu.sbatch`

## Runs

## Ruling

R-20260904-05 — drop
