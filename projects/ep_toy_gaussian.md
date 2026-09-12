# ep_toy_gaussian — NUTS versus three EP fits on the #1405 collapse toy at N=50

Project: ep_toy_gaussian
Issue: ep_toy_gaussian#1

## Now

n50_seed42 is on RAL: NUTS + one-by-one as 342639, EP x3 on identical data as 342640_[0-2]. The one-by-one leg finished (50/50 in 319 s); the EP repeats are turning per-factor Dynesty fits.
Next: pull and run scripts/compare.py --sample n50_seed42; settle first whether a prior factor with only NO_CHANGE rows counts as zero SUCCESS updates.

## Runs

- 342639 — open — ral — 2026-09-10 — nuts_vs_ep_x3_n50: one_by_one + BlackJAX NUTS, partition ral
- 342640 — open — ral — 2026-09-10 — nuts_vs_ep_x3_n50: EP x3 on identical data, array 0-2

## Log

- 2026-09-10 — run — 342640 submitted: nuts_vs_ep_x3_n50 — EP x3 on identical data, array 0-2
- 2026-09-10 — run — 342639 submitted: nuts_vs_ep_x3_n50 — one_by_one + BlackJAX NUTS, partition ral
- 2026-09-10 — note — question: Do three EP fits agree with NUTS at N=50 [archive/tasks/ep_toy_gaussian/nuts_vs_ep_x3_n50.md]
