# example — Does the example pipeline recover the truth on the fixture lens

Project: example
Issue: example#7

## Now

Wave 2 is on the cluster: the array 3002_[0-3] is running and the joint fit 3003 is queued.
Next: pull wave 2 when 3002 lands and compare the parent sigma against wave 1.

## Runs

- 3002_[0-3] — running — ral — 2026-09-01 — wave 2, four seeds on the corrected settings
- 3003 — open — gpu — 2026-09-02 — joint fit on the same four seeds
  chained after 3002 with afterok

## Log

- 2026-09-02 — run — 3003 submitted: joint fit on the same four seeds
- 2026-09-01 — run — 3002_[0-3] submitted: wave 2, four seeds on the corrected settings
- 2026-09-01 — lesson — the adapt image must be capped at S/N 3 before the mesh reads it; wave 1 was not
- 2026-08-31 — result — wave 1 recovered the parent mean but its sigma is 4x too tight
  the widths are the finding, not the means
- 2026-08-30 — run — 3001_[0-3] finished — wall 12:10: wave 1, four seeds
- 2026-08-29 — run — 3001_[0-3] submitted: wave 1, four seeds
- 2026-08-28 — note — ledger opened
