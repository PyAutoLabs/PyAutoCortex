# Inference_programme — phase 14: the legacy MGE Prodigy-reliability evidence behind GATE B part 1

Project: inference_programme
Phase: 14
State: accepted
Gates:
Witness: the 35 legacy Prodigy runs behind Gate B part 1 are health-clean on the current stack (2026.8.17.1), and the hit counts, the 15/15 fresh-seed record and the wall ratio recompute from their committed result rows
Budget: 0:15
Runs: 338523, 338524, 338525, 338526, 339065, 339066, 339070
Ruling: R-20260902-09
Lane: local-dev
Review-minutes: 12
Epic: jax-inference-profiling
Filed: 2026-09-02
Migrated-from: autolens_profiling/results/notes/inference/DECISIONS.md § 2026-08-23 — GATE B part 1 CALLED (human-ratified)

## Question

Programme Phase 3 — *Final MultiStartProdigy investigation (MGE, from broad priors, no
positions)* / CP-3 — asked whether any `n_starts ≤ 256` gives ≥ 99 % reliability at a cost
below the nested-sampling budget. The 2026-08-31 REWIND left the answer standing but
**provisional**: all of this phase's evidence is MGE and sits in `output/legacy/`, reusable
only after a human ruling in a batch packet.

**The gate wording, verbatim from `DECISIONS.md` § 2026-08-23:**

> **Decision (human, 2026-08-23, on the post-adversarial-review narrowed reading; PR #157
> merged same day):** Gate B part 1's failure condition ("no n_starts ≤ 256 gives ≥99%
> reliability at cost below the nested-sampling budget") is **NOT met**. MultiStartProdigy —
> n_starts=256, clip=prior_box, no scaler, auto-convergence on, positions OFF — is ratified as
> a global MAP searcher for the MGE-class parametric cell.

and its scope limits, verbatim:

> **Scope limits carried with the call (RESULTS.md caveats (a)–(h)):** demonstrated at n=256
> ONLY (no smaller n reaches 99% at 95% confidence; n128 fresh-seed tier queued); single cell
> (imaging/mge/hst), single tier (A100 fp64), positions-off; MAP-only — nested sampling retains
> posterior + evidence duty; p̂ conditional on the stop rule; compile not split;
> `target_id`/Phase-1 tolerance infrastructure still missing; `likelihood_evals` field wrong
> for MultiStart artifacts.

The 2026-08-24 entry adds one same-day human call: **caveat (a) "n=256 only" STANDS** — the
n128 fresh-seed 5/5 is consistent but cannot demonstrate ≥ 99 % at 95 % confidence.

**The question for this ruling:** does the legacy evidence stand, and does GATE B part 1 move
from PROVISIONAL back to CALLED?

**What the redo standard requires.** Under the MGE reuse rule these runs are reusable
*pending a human ruling in a packet*; they are not to be resubmitted. Unlike phase 13, **every
run here is MGE** — there is no mesh leg, so nothing in this phase is touched by
R-20260901-03 (the demagnified-source drop) or R-20260902-01 (the mesh `positions.info`
rule). All 36 runs carry the current stack stamp `2026.8.17.1`. The one comparator that is not
Prodigy — 339070, the Nautilus MGE re-baseline that supplies the wall denominator — is already
accepted by R-20260901-02.

## Witness

Every run-level number below was recomputed from the committed result rows in
`autolens_profiling/results/searches/multi_start_prodigy_autoconv/imaging/mge/hst/**` and
`.../nautilus/imaging/mge/hst/hpc_hpc_a100_fp64.json` on `main`, not copied from the write-up.
Run SUCCESS is Phase 3's own coded rule: ≥ 1 lane at ≥ 31784.782 (the Nautilus truth bar
31786.782 minus the Phase-1 2-nat tolerance); at run level the artifact's
`max_log_likelihood` is the best lane, so the rule is checkable from the row alone.

**Run success, recomputed** (RESULTS.md lines 31–33, 192–196):

| tier | job | seeds | success | max logL per seed |
|---|---|---|---|---|
| n16 wave 1 | 338523_[0-4] | 0–4 | **1/5** | 31787.9144 · −95708.55 · −134315.34 · −125319.15 · 26076.81 |
| n64 wave 1 | 338524_[0-4] | 0–4 | **5/5** | 31787.9068 … 31787.9180 |
| n256 wave 1 | 338525_[0-4] | 0–4 | **5/5** | 31787.9062 … 31787.9161 |
| θ_E diagnostic (n16) | 338526_[0-4] | 0–4 | **3/5** | 31787.8921 · 31787.9197 · 26076.81 · 31787.9100 · −128632.11 |
| n128 fresh | 339065_[0-4] | 100–104 | **5/5** | 31787.8858 … 31787.9181 |
| n256 fresh | 339066_[0-9] | 105–114 | **10/10** | 31787.8807 … 31787.9175 |

**n256 cumulative 15/15** (RESULTS.md 196): wave 1 5/5 + fresh 10/10, every max logL in
**[31787.8807, 31787.9175]** — matching the recorded 31787.881–31787.918 band and sitting
+1.10 to +1.14 nats above the Nautilus bar 31786.782, so no impostor basin. The n128 band is
[31787.8858, 31787.9181], matching the recorded 31787.886–31787.918.

**Wilson-95 lower bounds on per-run success**, recomputed: 15/15 → **0.7961** (recorded 0.80);
5/5 → **0.5656** (recorded 0.57). Caveat (a) survives its own arithmetic.

**Cost, 3.4–4.5× and 3.1–4.3×** (RESULTS.md 66–68, 208–212). Wave-1 n256 total walls:
224.77 · 216.51 · 176.52 · 172.18 · 191.40 s → the recorded 172–225 s. Fresh n256:
164.87–184.13 s → the recorded 165–184 s. Against the *recorded* 772.7 s Nautilus sampler wall
that is 3.44–4.49× (the "3.4–4.5×" headline); against the same-night re-baseline 339070
(`sampler_wall_s = 706.50`, `total_wall_s = 775.11`) the cumulative n256 band 164.87–224.77 s
is **3.14–4.29×** (the "3.1–4.3×" reconciliation). The 523 s figure is retired.

**Auto-convergence never hit the ceiling** (RESULTS.md 161–167): every run's own wall is
105.9–284.0 s against an `n_steps` ceiling of 3000, and the whole 20-run wave 1 costs
0.96 A100-h against a 5.5 h worst-case budget — reproduced here from the run walls.

**What this phase did NOT re-verify, and must not be read as verified.** The lane-level
figures are read out of per-lane arrays inside each artifact, not from the run-level rows, and
were not recomputed here: p̂_hit = 61/1280 = **0.048** with Clopper–Pearson 95 % [0.037, 0.061]
(RESULTS.md 45–51) — the 61 is the sum of the recorded per-seed hit counts 13+8+17+13+10, which
does add to 61, but the counts themselves come from the arrays; the tier-dependence finding
(n16/n64 are prefixes of n256's draw table, hit-index overlap 14.2× enriched, p = 1.2e-08,
RESULTS.md 35–43); the joint-95 % worst-case reliability 0.92/0.95/0.990 at n = 96/128/256 and
ρ ≤ 0.0057 (RESULTS.md 53–62); **~half of all lanes end pinned** — n16 7–12/16, n64 25–32/64,
n256 115–130/256, and no pinned lane is ever a hit (RESULTS.md 96–105); the non-physical
ellipticity scan — 1,252/6,240 lane best points (20.1 %) and 1,964 final points (31.5 %) at
|`ell_comps`| ≥ 1, 216/1280 wave-1 n256 lanes, re-based p̂ = 61/1064 = 0.057, cumulative
193/3840 = 0.0503 (RESULTS.md 107–133); and the zero-impostor parameter recovery across all 80
hit lanes, θ_E ∈ [1.599476, 1.599881] (RESULTS.md 86–94). Each of those is checkable from the
artifacts in the run dirs below if the human wants it before ruling.

**Health evidence, checked from artefacts** — `.completed` present in each run's identifier
dir; the SLURM `.err`; the `.out` tail; the row's version stamp; wall against the 0:15 budget.
Every one of the 36 `.err` files is 222 bytes / 2 lines / 2 distinct lines, holding only the
`mask_2d_util.py:564` mask-padding `UserWarning` — no `Traceback` anywhere. Every `.out` ends
`Finished.` followed by the job's closing `date`. No `Fit Already Completed` and no
`Resuming …` marker on any of the 36.

| job | arm | `.completed` | `.err` | `.out` ends | version | longest wall vs 0:15 |
|---|---|---|---|---|---|---|
| 338523_[0-4] | prodigy n16, seeds 0–4 | yes (5/5) | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 0:05 |
| 338524_[0-4] | prodigy n64, seeds 0–4 | yes (5/5) | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 0:05 |
| 338525_[0-4] | prodigy n256, seeds 0–4 | yes (5/5) | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 0:04 |
| 338526_[0-4] | prodigy n16 θ_E diagnostic | yes (5/5) | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 0:05 |
| 339065_[0-4] | prodigy n128, seeds 100–104 | yes (5/5) | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 0:04 |
| 339066_[0-9] | prodigy n256, seeds 105–114 | yes (10/10) | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 0:04 |
| 339070 | nautilus mge re-baseline | yes | 222 B, 2 lines, clean | `Finished.` | 2026.8.17.1 | 0:13 |

`log_evidence` is `NaN` on every Prodigy row — Prodigy is MAP-only, which is caveat (f) of the
call, not a defect of these runs.

## Where to look

- `inference_programme` (project row), the 35 Prodigy runs:
  `output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n{16,64,256}_s3000_seed{0-4}/hpc_a100_fp64_n{16,64,256}_seed{0-4}`,
  `.../n16_s3000_seed{0-4}/hpc_a100_fp64_n16_seed{0-4}_diag_theta_e`,
  `.../n128_s3000_seed{100-104}/hpc_a100_fp64_n128_seed{100-104}`,
  `.../n256_s3000_seed{105-114}/hpc_a100_fp64_n256_seed{105-114}`
- The wall denominator:
  `output/legacy/searches/nautilus/imaging/mge/hst/hpc_a100_fp64/181b13114ba3c2298191185ff74f90d8`
- `logs/output/output.<job>_<task>.out` and `logs/error/error.<job>_<task>.err` on the mirror
  for all 36 — each `.out` names the result row it wrote (`Results JSON saved to:`), which is
  how the job → config-dir map above was established rather than assumed
- `autolens_profiling/results/notes/inference/phase_03_prodigy_reliability/RESULTS.md` and
  `ADVERSARIAL_REVIEW.md` (the attack record kept as provenance for this gate call)
- `autolens_profiling/results/notes/inference/DECISIONS.md` § 2026-08-23 (the call),
  § 2026-08-24 (caveat (a) stands; the wall reconciliation) and § 2026-08-31 (the REWIND)
- Committed result rows on `main`:
  `autolens_profiling/results/searches/multi_start_prodigy_autoconv/imaging/mge/hst/hpc_hpc_a100_fp64_n{16,64,128,256}_seed*.json`
  and `.../diagnostic_theta_e/hpc_hpc_a100_fp64_n16_seed{0-4}_diag_theta_e.json`
- The ruling already standing on 339070: R-20260901-02 (accept)

## Runs

- 338523_[0-4]: legacy — gpu — submitted 2026-08-23 — wall 0:05 — CP-3 wave 1, n_starts 16, seeds 0-4 (longest task 245.8 s)
    where: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n16_s3000_seed{0-4}/hpc_a100_fp64_n16_seed{0-4}
    pulled_to: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n16_s3000_seed{0-4}/hpc_a100_fp64_n16_seed{0-4}
- 338524_[0-4]: legacy — gpu — submitted 2026-08-23 — wall 0:05 — CP-3 wave 1, n_starts 64, seeds 0-4 (longest task 280.0 s)
    where: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n64_s3000_seed{0-4}/hpc_a100_fp64_n64_seed{0-4}
    pulled_to: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n64_s3000_seed{0-4}/hpc_a100_fp64_n64_seed{0-4}
- 338525_[0-4]: legacy — gpu — submitted 2026-08-23 — wall 0:04 — CP-3 wave 1, n_starts 256, seeds 0-4: the tier the gate was called at (longest task 224.8 s)
    where: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n256_s3000_seed{0-4}/hpc_a100_fp64_n256_seed{0-4}
    pulled_to: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n256_s3000_seed{0-4}/hpc_a100_fp64_n256_seed{0-4}
- 338526_[0-4]: legacy — gpu — submitted 2026-08-23 — wall 0:05 — the theta_E ~ U(0.2,8) diagnostic arm, n16, seeds 0-4 (longest task 284.0 s)
    where: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n16_s3000_seed{0-4}/hpc_a100_fp64_n16_seed{0-4}_diag_theta_e
    pulled_to: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n16_s3000_seed{0-4}/hpc_a100_fp64_n16_seed{0-4}_diag_theta_e
- 339065_[0-4]: legacy — gpu — submitted 2026-08-23 — wall 0:04 — fresh-seed tier, n128, seeds 100-104 (longest task 198.3 s)
    where: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n128_s3000_seed{100-104}/hpc_a100_fp64_n128_seed{100-104}
    pulled_to: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n128_s3000_seed{100-104}/hpc_a100_fp64_n128_seed{100-104}
- 339066_[0-9]: legacy — gpu — submitted 2026-08-23 — wall 0:04 — fresh-seed tier, n256, seeds 105-114: the 10 that make 15/15 (longest task 184.1 s)
    where: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n256_s3000_seed{105-114}/hpc_a100_fp64_n256_seed{105-114}
    pulled_to: output/legacy/searches/multi_start_prodigy_autoconv/imaging/mge/hst/n256_s3000_seed{105-114}/hpc_a100_fp64_n256_seed{105-114}
- 339070: legacy — gpu — submitted 2026-08-24 — wall 0:13 — Nautilus MGE re-baseline; the wall denominator that retired the 523 s figure, already accepted
    where: output/legacy/searches/nautilus/imaging/mge/hst/hpc_a100_fp64/181b13114ba3c2298191185ff74f90d8
    pulled_to: output/legacy/searches/nautilus/imaging/mge/hst/hpc_a100_fp64/181b13114ba3c2298191185ff74f90d8
    ruled: R-20260901-02

## Ruling

R-20260902-09 — accept
