# slacs_bells_subhalo_grid — Dark-subhalo 2x2 grid search on SLACS, BELLS and simulated lenses

Project: slacs_bells_subhalo_grid
Issue: none

## Now

Set up 2026-11-26; first chains for slacs0946+1006 and slacs1430+4105.

## Runs

- 417097 — open — ral — 2026-11-26 — SLaM chain, slacs0946+1006 (task 13) and slacs1430+4105 (task 32), ral 4 CPU numba
- 417099 — open — ral — 2026-11-26 — subhalo none + 2x2 grid, slacs0946+1006 (tasks 26-27), afterok 417097_13
- 417100 — open — ral — 2026-11-26 — subhalo none + 2x2 grid, slacs1430+4105 (tasks 64-65), afterok 417097_32
- 417110 — open — ral — 2026-11-27 — SLaM chain (setup=auto: SP on JAX, rest numba sparse 4 workers), 60 lenses, tasks 0-12,14-31,33-61
- 417111 — open — ral — 2026-11-27 — subhalo[none], same 60 lenses, aftercorr 417110
- 417112 — open — ral — 2026-11-27 — subhalo[1]_[grid] 2x2 dark NFW, same 60 lenses, aftercorr 417110

## Log

- 2026-11-27 — run — 417112 submitted: subhalo[1]_[grid] 2x2 dark NFW, same 60 lenses, aftercorr 417110
- 2026-11-27 — run — 417111 submitted: subhalo[none], same 60 lenses, aftercorr 417110
- 2026-11-27 — run — 417110 submitted: SLaM chain (setup=auto: SP on JAX, rest numba sparse 4 workers), 60 lenses, tasks 0-12,14-31,33-61
- 2026-11-26 — run — 417100 submitted: subhalo none + 2x2 grid, slacs1430+4105 (tasks 64-65), afterok 417097_32
- 2026-11-26 — run — 417099 submitted: subhalo none + 2x2 grid, slacs0946+1006 (tasks 26-27), afterok 417097_13
- 2026-11-26 — run — 417097 submitted: SLaM chain, slacs0946+1006 (task 13) and slacs1430+4105 (task 32), ral 4 CPU numba
- 2026-11-26 — note — ledger opened
