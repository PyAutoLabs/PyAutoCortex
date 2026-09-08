# slope_hierarchy_scale — scale the hierarchical slope recovery to N=25–50

Project: slope_hierarchy_scale
Summary: Does hierarchical slope recovery hold at N=25 to 50
State: gated
Gates: PyAutoFit#1405, PyAutoFit#1558, PyAutoFit#1560, PyAutoFit#1562
Witness: an N=25–50 parity table in the same shape as the N=5 one, committed under `results/`, plus the scaling measurements (VRAM ceiling, JAX compile time vs model size, sampler ladder at 3N+1 dims, gradient-utilisation sanity)
Budget: 48:00
Runs:
Ruling:
Review-minutes: 20
Epic: graphical-ep
Filed: 2026-07-22
Migrated-from: PyAutoMind/draft/research/graphical_ep/slope_hierarchy_n25_scale_up.md

## Question

Gate evidence (phase 2 of the `graphical-ep` epic is issued and shipped): the Mind record
`PyAutoMind/complete/2026/09/ep-scale-collapse-basin-cure-or-caveat.md`, the phase-2 review
bundle PyAutoFit#1572 / #1573 / #1574 / #1576, and the stale-mask fixed-point fix
PyAutoFit#1580. `Gates:` carries PyAutoFit#1405 — the collapse-basin umbrella, deliberately
still open pending the moment-matching cure decision — alongside PyAutoFit#1558, #1560 and
#1562, the phase-2 EP defects this scale-up rests on, so `gates` surfaces all four for the
human's `move … ready`.

Borrowed from: this task's project was reborn 2026-09-08 as `slope_hierarchy_scale`
(`/mnt/c/Users/Jammy/Science/slope_hierarchy_scale`), scaffolded fresh with the code borrowed
from `slope_hierarchy`, which was wrapped up at N=5 on 2026-07-22 and vaulted intact at
`/mnt/c/Users/Jammy/Science/z_projects_complete/slope_hierarchy`. The N=5 baseline of record
is `results/ep_history_n5_maxsteps12/` inside that vault; the datasets are **re-simulated** at
N=25 in the new tree, never copied.

The `slope_hierarchy` project answered all four of its goals at N=5 and was wrapped up on
2026-07-22. This is the *optional* scale-up that was left on the table, not a blocker or an open
defect. Final N=5 parity (converged, `results/ep_history_n5_maxsteps12/`):

| parent | truth | draws | NUTS | EP (converged) |
|---|---|---|---|---|
| mean | 2.0 | 2.023 | 2.028 [2.000, 2.063] | 2.051 ± 0.0001 |
| sigma | 0.1 | 0.099 | 0.143 [0.117, 0.185] | 0.026 ± 0.00001 |

Does the picture hold at survey-relevant N?

- Does **NUTS** stay the trustworthy method for the parent scatter as N grows — and does the
  scatter estimate tighten toward truth 0.1 the way more data should make it?
- Does **EP**'s ~4×-low scatter get *better* with N (more groups → more information in the
  parent factor) or *worse* (more per-group messages to over-shrink)? Either answer is
  publishable: the framing is **NUTS headline, EP cautionary**, and the EP arm is here to
  characterise the failure mode at scale, not to be rescued.
- Does the collapse basin documented in PyAutoFit#1405 show up more or less often at larger N?

**The traps** (carried from the retired active.md entry): edit the simulator's `N` and
re-simulate; submit with the `submit_*` scripts using `--array`; `rm output/<sample>/*` before
refits, or stale output silently resumes and returns the old answer; force-sync the truth files
to the cluster, or the recovery scoring goes quietly wrong; verify the RAL PyAutoFit mirror
commit before trusting a run (`HPCPullPyAuto`); `export JAX_ENABLE_X64=True` explicitly in the
sbatch script — it is ambient locally but **not** inherited by `sbatch`, and float32 silently
ruins a gradient run (verify `grep -c "truncated to dtype float32" *.err` == 0); the repo is on
`autonerves`.

Cost note: RAL GPU contention has been severe (multi-day queues as of 2026-07-20). N=25–50 ×
per-lens fits is a large array job — check the queue before committing to it, and consider the
CPU `ral` partition for the EP arm (finiteness, not throughput).

## Witness

An N=25–50 parity table in the same shape as the N=5 one, committed under `results/` in
`slope_hierarchy_scale`. (The old N=5 witness was commented on Jammy2211/slope_hierarchy#1;
the new tree has no remote yet, so the committed table is the whole witness until a human
runs `gh repo create`.)

Scaling measurements to capture while the runs are up anyway (the EP campaign needs them):

- **VRAM ceiling** — peak GPU memory vs N on the A100 arm; the N at which the joint fit no
  longer fits.
- **JAX compile time vs model size** — wall time of the first likelihood/grad call vs N; is
  compilation a fixed cost worth caring about at N=100+? (This is the *graphical factor-graph*
  trace, a different graph from the lensing-side compile-time work.)
- **Sampler ladder at high dimension** — at 3N+1 ≈ 76–151 dims, time at least one alternative
  gradient sampler beside NUTS on the same problem.
- **Gradient utilisation sanity** — confirm the run exercises the JAX gradients end to end (x64
  on, no silent float32, no numpy fallback in the hot path).

Each number goes in the committed results table beside the parity numbers.

## Where to look

- `slope_hierarchy` (retired project row, vaulted at `/mnt/c/Users/Jammy/Science/z_projects_complete/slope_hierarchy`): `results/ep_history_n5_maxsteps12/` — the N=5 baseline
- `slope_hierarchy_scale` (this project's row): `results/` — where the N=25 parity table and the scaling measurements land
- Jammy2211/slope_hierarchy#1 — the project issue the parity table is commented on
- Mind `research/graphical_ep/ep_campaign.md` phase 3 — the campaign rows this feeds
- Mind `draft/research/graphical_ep/slope_hierarchy_methods_writeup.md` — the write-up it feeds
- PyAutoFit#1405 — the collapse basin

## Runs

## Ruling

(none)
