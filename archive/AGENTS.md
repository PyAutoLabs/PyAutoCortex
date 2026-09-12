# archive/ — frozen

The task, ruling and batch ledgers the Cortex kept between 2026-08-31 and
2026-09-11, retired on 2026-09-12 (schema decision 60) when the Cortex became
one ledger per project. Nothing writes here any more, nothing reads it at
render time, and `scripts/ledger_merge.py` classifies **any** change under
this directory — an addition included — as code, which is a human's turn.

It stays because the science repos' own ledgers cite these files by id
(`R-20260910-04`, `tasks/euclid_dr1_prelim/ordered_rerun_catalogue_parity.md`).
Every entry that mattered was carried into `projects/<key>.md` on the day of
the migration, in the words already on file, with a `[archive/tasks/…]` link
back to the question it came from.

- `tasks/<project>/<slug>.md` — the pre-registered questions and their run lines
- `rulings/<YYYY>/<MM>/R-<YYYYMMDD>-<nn>.md` — the 37 verdicts, the human's words verbatim
- `batches/` — the three 2026-08/09 review-slot records and their reviews
