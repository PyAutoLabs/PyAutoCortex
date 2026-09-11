# Euclid_dr1 — does the sep1 DR1 delivery reproduce the ten euclid_dr1_prelim lenses by eye

Project: euclid_dr1
Summary: Does the sep1 DR1 delivery reproduce the prelim ten lenses
State: submitted
Gates:
Witness: all 10 tiles finish both stages (vis_lp then vis_pix) on RAL from the euclid_dr1 clone on the sep1 delivery; a per-tile side-by-side sheet (new vis_pix fit PNG beside prelim run 342629's) shows the same lens configuration by eye on 10/10 tiles; effective Einstein radius per tile is tabulated against prelim 342629 and any tile differing by more than 10 % is named
Budget: 36:00
Runs: 342650
Ruling:
Review-minutes: 25
Epic: euclid-dr1-prep
Filed: 2026-09-11

## Question

The DR1 data delivery has just arrived — `Segmentation.zip`, the sep1 segmentation run over
15032 tiles, every tile already written in the pipeline's dataset layout. Nothing has been
fitted from it yet. Before anything is built on top of 15032 lenses, the first thing to settle
is the cheapest one: **is this data good to use?**

The test is a reproduction. The ten `euclid_dr1_prelim` lenses have been fitted, re-fitted and
argued over for two weeks; their fits are the one thing in this project we already know the
shape of. The same ten tiles are present in the sep1 delivery, so this task refits them from
the new delivery, through a route **identical to prelim's** (the two-stage CPU submit,
`vis_lp` then `vis_pix`, from a clone of `euclid_strong_lens_modeling_pipeline` main), and asks
whether the same lenses come back.

**Small differences are expected, and are not the question.** The segmentation, the positions
and the mask were all regenerated for this delivery, so the inputs are genuinely different:
tile 102005065, for instance, now carries a mask radius of 5.65" against prelim's 3.32" and
four positions against two. Seven of the ten tiles are also recentred by 0.8–2.2 arcsec and so
carry a different tile name (the pairs are in `## Notes`). Different mask, different positions,
different numbers.

**The comparison is therefore by eye, not numerical parity.** This is a deliberate choice, made
because the numerical version of this question has already been asked and answered: the prelim
`ordered_rerun_catalogue_parity` task refitted the *same* tiles with the *same* code on the
*same* data and found run-to-run scatter with a median of z ≈ 15 between reruns. A numerical
witness on top of a regenerated mask and regenerated positions would be measuring that scatter,
not the delivery — it would be meaningless. What a human can judge, and what actually decides
whether the data is usable, is whether the lens that comes out **looks like the same lens**:
the same arcs in the same places, the same mass configuration, a comparable Einstein radius.

One other deliberate difference from prelim: the clone puts the `config/visualize` colormap back
to the `autoarray` default, so the figures this task produces are the standard ones.

## Witness

Three clauses, pre-registered before submission. A missed clause is a finding to rule on, not a
threshold to relax.

1. **Completion.** All 10 tiles finish **both** stages — `vis_lp` then `vis_pix` — on RAL, run
   from the `euclid_dr1` clone against the sep1 delivery in `dataset/dr1_sep1/`. A tile that
   fails, times out or is pinned by the positions penalty is named with its stage and its reason.
2. **By-eye agreement.** A per-tile **side-by-side sheet** — the new `vis_pix` fit PNG beside the
   corresponding prelim run 342629 fit PNG — shows the **same lens configuration by eye on 10/10
   tiles**: the same arcs in the same places, the same source structure, no tile where the new
   fit has found a different lens.
3. **Einstein radius table.** The **effective Einstein radius per tile** is tabulated against
   prelim 342629, and **any tile differing by more than 10 % is named** (named, not failed — the
   number is the flag that sends a human to that tile's sheet).

Products, committed in `euclid_dr1`:

- the per-tile `vis_pix` fit PNGs pulled from RAL,
- the per-tile side-by-side sheet (new beside prelim 342629),
- the Einstein-radius table (new vs prelim 342629, per tile, with the percentage difference).

## Where to look

- `euclid_dr1` (project row `euclid_dr1`): `output/dr1_sep1/` once pulled — the new runs; the
  delivery itself is `dataset/dr1_sep1/`, and the route is
  `hpc/batch_cpu/submit_initial_lens_model_two_stage`
- `euclid_dr1` `wiki/project/state.md` — this project's own ledger (the commentary; the ruling
  of record is the Cortex's)
- `euclid_dr1_prelim` (project row `euclid_dr1_prelim`): `output/dr1_prelim_grade_ab` and
  `inspect/dr1_prelim_grade_ab_342629/` (including `lens_mass.csv`) — **the by-eye reference**,
  run 342629
- `autolens_assistant/skills/euclid_prepare_data.md`, `euclid_setup_pipeline.md`,
  `euclid_model_lens.md`, `euclid_hpc_runs.md` — how this pipeline is driven

## Notes

- 2026-09-11 — **the delivery, and the ten tiles.** `Segmentation.zip` is 14.8 GB and holds
  three nested batch zips, `eclipse_catalogue_fits_sep1-segmentation_batch{1,2,3}`, for 15032
  tile folders in total; every tile is **already** in the pipeline's dataset layout, so no
  conversion step is needed. The nested stored zips were read **in place with Python
  `zipfile`** (no intermediate extraction of the 14.8 GB), and the first ten tiles — the ten
  `euclid_dr1_prelim` lenses — were extracted into the sample `dataset/dr1_sep1/`. The **array
  index order is the list order below**: array task *n* is the *n*-th pair.

  Three tiles match the prelim name exactly; seven are recentred by 0.8–2.2 arcsec and so carry
  a new name. prelim → sep1:

  | # | prelim tile | sep1 tile | offset |
  |---|---|---|---|
  | 1 | `Tile102005065RA0135279431487DECNEG0701599765928` | same | exact |
  | 2 | `Tile102007299RA0702283866574DECNEG0660415308762` | same | exact |
  | 3 | `Tile102007899RA0631694872236DECNEG0650584220817` | `Tile102007899RA0631697483678DECNEG0650586413593` | 0.88" |
  | 4 | `Tile102007903RA0668831429074DECNEG0648901814905` | `Tile102007903RA0668824944366DECNEG0648906250124` | 1.88" |
  | 5 | `Tile102008165RA0109664211519DECNEG0642902327064` | `Tile102008165RA0109661927007DECNEG0642904268129` | 0.79" |
  | 6 | `Tile102008219RA0727851454839DECNEG0644382776514` | `Tile102008219RA0727857418392DECNEG0644388277074` | 2.19" |
  | 7 | `Tile102008468RA3567390985250DECNEG0647172046261` | `Tile102008468RA3567393529734DECNEG0647169093056` | 1.13" |
  | 8 | `Tile102008475RA0039777627054DECNEG0637715426503` | same | exact |
  | 9 | `Tile102008532RA0683495100072DECNEG0642073858939` | `Tile102008532RA0683486015030DECNEG0642073552911` | 1.43" |
  | 10 | `Tile102008848RA0601376380877DECNEG0634605061157` | `Tile102008848RA0601371893270DECNEG0634606579714` | 0.91" |

  The regenerated `info.json` / `positions.json` differ from prelim's — tile 102005065 carries a
  mask radius of 5.65" against 3.32", and 4 positions against 2 — which is why the witness above
  is by eye and not numerical.

## Runs

- 342650: submitted — ral — submitted 2026-09-11 — wall 0:00

## Ruling

(none)
