# cowls_diana_v2 — SLaM chain (no subhalo) for 9 COWLS JWST F277W lenses, RAL CPU

Project: cowls_diana_v2
Issue: none

## Now

Set up 2026-11-26: 9 lenses, 3.0" minimum mask, sdssj0946_subhalo_v2 chain on RAL CPU; first submissions COSJ100018+022138 and COSJ100140+020632.

## Runs


## Log

- 2026-11-28 — run — 417195 failed — wall 18:51: resubmit of 417101 with BLAS/OpenMP threads pinned to 1 (numba sparse, 4 workers, 3.0 arcsec mask): tasks 5 COSJ100018+022138 and 8 COSJ100140+020632; Pix1 resumes from checkpoint — task 8 COSJ100140+020632 COMPLETED in 18:51 (SP to mass_total[1], plus the unused source_tune[1]); task 5 COSJ100018+022138 FAILED after 7:28, exit 1: SP to light[1] complete, then a Nautilus likelihood worker died by SIGSEGV about 450 calls into mass_total[1]
- 2026-11-27 — note — chain now ends at mass_total[1] (human): source_tune[1] dropped as in slacs_bells_subhalo_grid faea4ce, since it only refined SDSSJ0946's source for the He et al. 2025 comparison; 417195_5/_8 loaded the old code and will fit one unused source_tune[1] at the end, later submissions use the new code
- 2026-11-27 — run — 417195 submitted: resubmit of 417101 with BLAS/OpenMP threads pinned to 1 (numba sparse, 4 workers, 3.0 arcsec mask): tasks 5 COSJ100018+022138 and 8 COSJ100140+020632; Pix1 resumes from checkpoint
- 2026-11-27 — run — 417101 failed — wall 12:26: resubmit of 417095 with setup=auto (JAX dense SP, numba sparse Pix1 on): ral CPU array tasks 5 COSJ100018+022138 and 8 COSJ100140+020632; SP loads from disk, Pix1 resumes from checkpoint — cancelled on purpose: submitted without BLAS/OpenMP thread pins, Pix1 ran ~5 likelihoods/min; resubmitted as 417195 with the pins
- 2026-11-26 — run — 417101 submitted: resubmit of 417095 with setup=auto (JAX dense SP, numba sparse Pix1 on): ral CPU array tasks 5 COSJ100018+022138 and 8 COSJ100140+020632; SP loads from disk, Pix1 resumes from checkpoint
- 2026-11-26 — run — 417095 failed — wall 2:36: SLaM chain (SP to source_tune, no subhalo), ral CPU array tasks 5 COSJ100018+022138 and 8 COSJ100140+020632, 3.0 arcsec mask — cancelled on purpose: pipeline used use_jax=True (JAX dense) for every search; resubmitted as 417101 with setup=auto (numba sparse for pixelized searches)
- 2026-11-26 — run — 417095 submitted: SLaM chain (SP to source_tune, no subhalo), ral CPU array tasks 5 COSJ100018+022138 and 8 COSJ100140+020632, 3.0 arcsec mask
- 2026-11-26 — note — ledger opened
