# autolens_inference — Do the PyAutoLens inference backends agree on the HST SLaM posterior

Project: autolens_inference
Issue: autolens_inference#4

## Now

Born 2026-09-10 as the from-scratch restart of inference_programme; slam_hst_base is the first question and is ready to submit — nothing has run yet.
Next: hpc/sync submit the six backend legs on the HST SLaM dataset and record the job ids here.

## Runs

- 342799_[0-1] — open — gpu — 2026-09-12 — slam_hst_base: A100 leg, dense inversion, seeds 0-1, hpc/batch_gpu/submit_slam_hst_jax_gpu_dense (config hpc_a100_jax_gpu_dense_fp64); the 09-12 ask: one hardware type first, GPU; rate-probe 342695 tree moved aside so no stage resumes
- 342801_[0-1] — open — gpu — 2026-09-12 — slam_hst_base: A100 leg, sparse inversion, seeds 0-1, hpc/batch_gpu/submit_slam_hst_jax_gpu_sparse (config hpc_a100_jax_gpu_sparse_fp64); the 09-12 ask: one hardware type first, GPU; rate-probe 342695 tree moved aside so no stage resumes

## Log

- 2026-09-12 — run — 342801_[0-1] submitted: slam_hst_base: A100 leg, sparse inversion, seeds 0-1, hpc/batch_gpu/submit_slam_hst_jax_gpu_sparse (config hpc_a100_jax_gpu_sparse_fp64); the 09-12 ask: one hardware type first, GPU; rate-probe 342695 tree moved aside so no stage resumes
- 2026-09-12 — run — 342799_[0-1] submitted: slam_hst_base: A100 leg, dense inversion, seeds 0-1, hpc/batch_gpu/submit_slam_hst_jax_gpu_dense (config hpc_a100_jax_gpu_dense_fp64); the 09-12 ask: one hardware type first, GPU; rate-probe 342695 tree moved aside so no stage resumes
- 2026-09-11 — note — question: Do six backend legs agree on the HST SLaM posterior? — ready, never run [archive/tasks/autolens_inference/slam_hst_base.md]
