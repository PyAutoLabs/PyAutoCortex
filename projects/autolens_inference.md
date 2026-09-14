# autolens_inference — Do the PyAutoLens inference backends agree on the HST SLaM posterior

Project: autolens_inference
Issue: autolens_inference#4

## Now

The four A100 base legs are done (dense and sparse, seeds 0-1, all five stages): sparse costs 1.5x dense and buys nothing measurable, and at the same seed the two routes agree to 0.0-0.6 sigma while seeds of the SAME leg disagree by up to 0.9 sigma and ~3 nats — so the slam_hst_base witness bands (2 nats, 0.2 sigma) are tighter than Nautilus's own seed reproducibility on this cell, which is a finding about the bands. Running now: the same chain with a 1250-vertex Hilbert/Delaunay source (343143 dense, 343145 sparse, seeds 0-1) on the A100. Next: pull both, compare seed-paired against slam_base, and decide whether the parity bands need rewriting before the four CPU legs are submitted.

## Runs

- 343143_[0-1] — open — gpu — 2026-09-15 — slam_hst_delaunay_1250: A100 leg, dense inversion, seeds 0-1, hpc/batch_gpu/submit_slam_delaunay1250_hst_jax_gpu_dense (config hpc_a100_jax_gpu_dense_fp64, variant delaunay_1250) — 1250-vertex Hilbert/Delaunay source with AdaptSplit, against the slam_base rectangular 28x28 rows; 24h containment, 96gb, 8 cpus (the mesh's qhull pure_callback deadlocks a narrow thread pool)
- 343145_[0-1] — open — gpu — 2026-09-15 — slam_hst_delaunay_1250: A100 leg, sparse inversion, seeds 0-1, hpc/batch_gpu/submit_slam_delaunay1250_hst_jax_gpu_sparse (config hpc_a100_jax_gpu_sparse_fp64, variant delaunay_1250) — same mesh, sparse operator route

## Log

- 2026-09-15 — run — 343145_[0-1] submitted: slam_hst_delaunay_1250: A100 leg, sparse inversion, seeds 0-1, hpc/batch_gpu/submit_slam_delaunay1250_hst_jax_gpu_sparse (config hpc_a100_jax_gpu_sparse_fp64, variant delaunay_1250) — same mesh, sparse operator route
- 2026-09-15 — run — 343143_[0-1] submitted: slam_hst_delaunay_1250: A100 leg, dense inversion, seeds 0-1, hpc/batch_gpu/submit_slam_delaunay1250_hst_jax_gpu_dense (config hpc_a100_jax_gpu_dense_fp64, variant delaunay_1250) — 1250-vertex Hilbert/Delaunay source with AdaptSplit, against the slam_base rectangular 28x28 rows; 24h containment, 96gb, 8 cpus (the mesh's qhull pure_callback deadlocks a narrow thread pool)
- 2026-09-14 — result — "the first runs looks good" (human, 2026-09-14) — the four A100 base legs, dense and sparse at seeds 0 and 1, all five stages complete. Next, on the same ask: the same chain with a 1250-vertex Delaunay source instead of the 28x28 rectangular one, on the A100, both inversion routes.
- 2026-09-14 — run — 342801_[0-1] finished — wall 1:07: slam_hst_base: A100 leg, sparse inversion, seeds 0-1, hpc/batch_gpu/submit_slam_hst_jax_gpu_sparse (config hpc_a100_jax_gpu_sparse_fp64); the 09-12 ask: one hardware type first, GPU; rate-probe 342695 tree moved aside so no stage resumes — sparse A100 leg, seeds 0-1: all five stages completed, 66.4 and 66.9 min search wall, mass_total[1] logZ 31589.52 / 31592.44
- 2026-09-14 — run — 342799_[0-1] finished — wall 0:48: slam_hst_base: A100 leg, dense inversion, seeds 0-1, hpc/batch_gpu/submit_slam_hst_jax_gpu_dense (config hpc_a100_jax_gpu_dense_fp64); the 09-12 ask: one hardware type first, GPU; rate-probe 342695 tree moved aside so no stage resumes — dense A100 leg, seeds 0-1: all five stages completed, 42.8 and 47.7 min search wall, mass_total[1] logZ 31592.70 / 31596.11
- 2026-09-12 — run — 342801_[0-1] submitted: slam_hst_base: A100 leg, sparse inversion, seeds 0-1, hpc/batch_gpu/submit_slam_hst_jax_gpu_sparse (config hpc_a100_jax_gpu_sparse_fp64); the 09-12 ask: one hardware type first, GPU; rate-probe 342695 tree moved aside so no stage resumes
- 2026-09-12 — run — 342799_[0-1] submitted: slam_hst_base: A100 leg, dense inversion, seeds 0-1, hpc/batch_gpu/submit_slam_hst_jax_gpu_dense (config hpc_a100_jax_gpu_dense_fp64); the 09-12 ask: one hardware type first, GPU; rate-probe 342695 tree moved aside so no stage resumes
- 2026-09-11 — note — question: Do six backend legs agree on the HST SLaM posterior? — ready, never run [archive/tasks/autolens_inference/slam_hst_base.md]
