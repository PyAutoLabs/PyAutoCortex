# stars_dm_slope_hst — Can HST imaging of SLACS-like lenses constrain a stars plus gNFW inner slope

Project: stars_dm_slope_hst
Issue: none

## Now

Pilot slice finished 2026-11-28 and is pulled. Submitted 2026-11-28 on the human's word: the remaining 85 fits (417595, 417602) and an 8-task pilot of the slope profile with f_dm free (417659), which replaces the f_dm grid maps. The other 72 profiles wait for that pilot and the human's go.

## Runs

- 417595 — open — ral — 2026-11-28 — reference fits, the 7 mocks not in the pilot (campaign indices 1-2, 4-8)
- 417602 — open — ral — 2026-11-28 — free fits n_live 400, the 78 not in the pilot (indices 10-14, 16-71, 73-89): P1-inv, P1p-f-inv, P1 on 9 mocks, 3 seeds
- 417659 — open — ral — 2026-11-28 — pilot: slope profiles with f_dm free (slope_profile.py), realisation 0 of each of the 8 lenses (indices 90, 100, ..., 160)

## Log

- 2026-11-28 — run — 417659 submitted: pilot: slope profiles with f_dm free (slope_profile.py), realisation 0 of each of the 8 lenses (indices 90, 100, ..., 160)
- 2026-11-28 — run — 417602 submitted: free fits n_live 400, the 78 not in the pilot (indices 10-14, 16-71, 73-89): P1-inv, P1p-f-inv, P1 on 9 mocks, 3 seeds
- 2026-11-28 — run — 417595 submitted: reference fits, the 7 mocks not in the pilot (campaign indices 1-2, 4-8)
- 2026-11-28 — run — 417576 finished — wall 5:15: pilot slice: information-test likelihood maps A_g10_r0 and B_g15_r0 (indices 90, 120) — 2/2 maps complete, 3.0 h and 5.2 h, peak 2.9 GB
- 2026-11-27 — run — 417573 finished — wall 1:23: pilot slice: free fits n_live 400, P1-inv on A, P1 on A, P1-inv on I (indices 9, 15, 72) — 3/3 tasks completed, 1.0-1.4 h each, peak 5.9 GB
- 2026-11-27 — run — 417571 finished — wall 0:14: pilot slice: reference fits, mocks A and F (campaign indices 0, 3) — 2/2 tasks completed (ref_A, ref_F), 13-14 min each, peak 5.7 GB
- 2026-11-27 — run — 417576 submitted: pilot slice: information-test likelihood maps A_g10_r0 and B_g15_r0 (indices 90, 120)
- 2026-11-27 — run — 417573 submitted: pilot slice: free fits n_live 400, P1-inv on A, P1 on A, P1-inv on I (indices 9, 15, 72)
- 2026-11-27 — run — 417571 submitted: pilot slice: reference fits, mocks A and F (campaign indices 0, 3)
- 2026-11-27 — note — ledger opened
