# Batch packets — the review pages, archived

One **self-contained** HTML page per slot: `<YYYY-MM-DD>-<slot>.html`. This is
the page the human actually opens to review a board — every member with its
question, witness, health evidence, readout, ruling block, follow-ups, local
"where to look" pointers and figures — and, once the slot is over, the
permanent record of what they were shown. The batch record's `packet:` field
points here.

Rules:

- **Self-contained means self-contained.** Figures are embedded as data URIs,
  styles and script are inline; the archive must render identically in ten
  years with no external fetch. Keep a page under ~5 MB; downsize figures.
- **A rolling board.** The page opens with every phase on the board — the
  `submitted` / `running` ones as RUNNING entries with no review control —
  and carries `generated:` / `refreshed:` stamps. Each pull regenerates the
  member that just joined **in place** (same `id`) and bumps the `refreshed`
  stamp; the batch record gets the matching `refreshed:` line.
- **Never rewritten after the review is submitted.** The archived page plus
  the `batches/reviews/` file together are the audit pair: what was shown,
  what was ruled. A correction gets a new dated page, not an edit.
- **Pointers are local paths** (the laptop mirror each project's sync CLI
  fills — the `mirror:` of its `projects.yaml` row), because the review
  happens at the laptop. A pointer may stay remote only when the pull cannot
  fetch it by design, and must say so.
- **Not hand-written.** The renderer is `pyauto-brain batch collect --kind
  cortex --apply` (phase 5 of the birth epic); it writes this page and appends
  each member as it joins. A member still `submitted`/`running` renders with
  **no review control** — no ruling chips, no ruled box — because there is
  nothing to rule on yet; carry-forward, not a ruling, moves it to the next
  board. The follow-ups block a review submits is a `###` heading: `cortex.py
  check` requires every `##` in a review to name a member.

**Visibility.** Packets and reviews are public in this repository, as the
Mind's are (ruled 2026-08-31): science numbers, figures and run paths in a
packet are thereby on the open internet. A project whose data may not be
shown (Euclid) keeps its figures out of the packet and points at the local
path instead.
