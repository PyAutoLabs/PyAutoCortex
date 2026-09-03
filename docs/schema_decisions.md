# Schema decisions — 2026-09-01

Every choice made in phase 1 of the Cortex birth epic (PyAutoMind#379) that
the epic ledger's "The decision" (2026-09-01) did not already fix. Phase 2's
conductor reads these; nobody re-derives them. Each entry: the decision, then
one line of why. The human's fixed inputs — the organ, the state model, rulings
of record (Option A), gates as GitHub refs, the remotes, the epic split, the
rolling board — are in the epic ledger and are not repeated here.

1. **Ruling id `R-YYYYMMDD-nn`, a two-digit per-day sequence, global.**
   Why: date-first sorts the ledger chronologically on disk and the per-day
   counter is small enough to assign by listing one directory; global rather
   than per-project so one id space is enough to cite from any ledger.
2. **One ruling file per phase; a multi-phase ruling is N files joined by
   `Batch:`.** Why: `check` then has one phase per file to validate against,
   and the REWIND case (one verdict over five phases) stays expressible via
   `rule --also`.
3. **Chains, not trees: at most one successor per ruling; supersede the
   head.** Why: "which ruling stands" must have one answer; a tree would need
   a tiebreak.
4. **`accepted` is not terminal — a later ruling may supersede the
   acceptance (`rule --supersedes`), moving the phase to `rerun` or
   `dropped`.** Why: the 2026-08-31 REWIND superseded accepted gates;
   a terminal `accepted` would have needed a new phase number for a verdict
   about the same runs.
5. **`submitted` / `running` self-loops: `--run <id>` appends a wave, a
   chained job or a checkpoint resubmit without changing state.** Why: real
   phases have several waves (`342091_[0-8,10]` then `342102`); one state
   change per wave would be noise.
6. **`move pulled --partial` on a running phase, which `check` expects
   closed by a `leave-to-finish` ruling.** Why: partial arrays are routine;
   the board needs the nine finished tasks now and the ruling records that
   the tenth is still owed.
7. **Legacy-born phases: `new --legacy-run` writes a phase whose every run is
   `legacy | legacy_wrong`, moving `ready → pulled` directly; the witness is
   still mandatory.** Why: phase 4 migrates pre-Cortex runs, which were never
   submitted through the Cortex but must still be ruled on.
8. **`void` is a run state: cancelled, or never produced a step.** Why: a
   job that was killed at submit time is neither `failed` (it never ran) nor
   absent (the id exists in `sacct`).
9. **A gate is cleared when: a PR has `merged_at != null`; an issue is
   `closed` with `state_reason ∈ {completed, null}`. Closed-unmerged PRs and
   `not_planned` / `duplicate` issues are dead gates, reported. Unreadable
   refs fail closed.** Why: "closed" alone would clear a gate on a rejected
   PR.
10. **`gates --grade` reports; `--write` flips.** Why: the hand tool must be
    safe to run from any session; phase 2 schedules the write.
11. **Reopen demotion `ready → gated` is `--write`-only, refused when
    `Gate-override:` is present, and for `submitted`+ phases reported but
    never enforced.** Why: a run already on the queue is not un-submitted by
    a reopened issue; the human overrode on purpose.
12. **`projects.yaml` is code, not ledger, and is written in a restricted
    YAML subset parsed by the stdlib.** Why: `sync_cli` and `local_path` are
    paths a conductor executes under (worse than `repos.yaml`, which is
    already code in the Mind); the subset keeps `cortex.py` stdlib-only while
    a PyYAML parity test keeps the file real YAML.
13. **No `owner/Repo#N` gate form.** Why: `GATE_REF_RE`'s lookbehind rejects
    it; another owner is spelled as a URL, one grammar shared with the Mind.
14. **Run lines in strict SLURM notation with structured facts on indented
    continuation lines (`pulled_to:`, `after:`, `resumes:`, `where:`,
    `ruled:`), never in the note.** Why: a fact in prose cannot be checked;
    `--` accepted for `—` because phones cannot type the em dash.
15. **Job ids are unique per phase, not globally.** Why: one array fed two
    phases in the real ledgers (`342120_[0-4]` / `_[5-9]` in the fixture).
16. **No `skills/` and no `install.sh` change in phase 1.** Why: the Cortex
    exposes no commands yet; `install.sh`'s `ORGAN_REPOS` is a hardcoded list
    only Brain's `AGENTS.md` uses.
17. **No Mind PR for the session-hook fan-out.** Why:
    `session_hook_propagate.yml` reads every `repos.yaml` row and the Cortex
    row already exists (phase 0).
18. **The fixture is the witness: `tests/fixtures/skeleton/` holds one
    project, one phase per state, five rulings (one chain of two), one batch
    record and one review; `tests/fixtures/empty/` passes `check`.** Why: a
    schema nobody can instantiate is prose.
19. **`ledger_merge.yml` runs `cortex.py check` on the trial-merge tree,
    after `git merge --no-ff` and before `git push`.** Why: that is the only
    place two branches that both assigned `R-…-03` are seen together.

Choices made while writing the files, beyond the plan:

20. **A header key with no value may be omitted or left empty (`Gates:`,
    `Runs:`, `Ruling:`).** Why: `new` writes the empty key so a human sees
    the slot; a migrated file may not carry it; both parse the same.
21. **`State ∈ accepted | rerun | dropped` ⇒ `Ruling:` present.** Why: those
    states are reachable only through `rule`, so a file in one of them with
    no ruling is a contradiction `check` should name.
22. **The ruling id also lives in the title line (`# <id>` or `# <id> —
    <summary>`), and `check` requires it to equal the filename.** Why: the
    plan says "id == filename" and the file must state its id somewhere a
    human reads.
23. **A run line's `<partition>` is a bare SLURM partition name
    (`^[a-z][a-z0-9_-]*$`), not an enumeration.** Why: the project row's
    `partition: gpu | ral | both` is a capability; the run records the
    actual queue.
24. **An `after:` / `resumes:` target is the verbatim identifier of another
    run line in the same phase (`342091_9`, `342091_[0-8,10]`), not a bare
    stem.** Why: a checkpoint resubmit resumes one task, not the array.
25. **A `ruled:` continuation must resolve to a ruling file.** Why: it is a
    pointer and a dangling pointer is drift.
26. **Rulings on one phase need not chain: `leave-to-finish` followed by
    `accept` is two chains of one; `Supersedes:` replaces a verdict, never
    sequences.** Why: the plan makes `--supersedes` an explicit flag; forcing
    every later ruling to supersede would make it redundant.
27. **`Batch:` on a ruling must name an existing `batches/<slot>.md`.** Why:
    it is the join key; a typo would silently orphan the ruling from its
    slot.
28. **Review grammar: `<HEALTH>` ∈ `HEALTHY | SUSPECT | FAILED | RUNNING`;
    `- decision: (none)` + `- ruled: no` is an untouched member; a verb with
    `ruled: no` is a leaning the human did not tick.** Why: the Mind's
    packet has the same tick/decision split; `(none)` keeps the four-verb
    vocabulary pure while listing every member.
29. **Batch record keys keep the Mind's names (`dispatched:` = when the
    board opened) and drop `usage-window-*`, `heart-ack:` and
    `expected-effects:`; `- refreshed:` is a repeated line.** Why: one
    parser in the Brain can read both record kinds; the dropped fields
    license cloud sessions and autonomous YELLOW acks, which a science batch
    never spends. The member `<state>` is the state at the last refresh and
    `check` requires it legal, not current.
30. **`ledger_merge.yml` keeps a blocking `cortex.py check` on the branch tip
    in addition to the trial-merge check.** Why: `workflow_dispatch` in
    `audit` mode never merges, so without it audit mode reports nothing.
31. **`cortex_check.yml` triggers on its own path too.** Why: a workflow edit
    that does not run itself is invisible until the next ledger push.

Choices made while writing `cortex.py` (slice B), beyond the plan:

32. **`Reset:` is a phase header key, written by `move ready --reason`.**
    Why: the table demands a reason for `submitted | running → ready` and the
    key table gave it no home; a reason in prose cannot be found again.
33. **`move pulled` writes `pulled_to:` — `--pulled-to <path>`, or for a
    `legacy` run its own `where:` — and is refused when no `done | legacy`
    run would carry one.** Why: `check` requires it on a pulled phase, and a
    verb that writes a state its own check rejects is a trap.
34. **An unknown header key, a missing body section, a `gated` phase with an
    empty `Gates:`, or a `Lane:` other than `local-dev` is drift.** Why:
    `Gate-cleared:` is one letter from `Gates-cleared:` and would otherwise
    pass silently while the invariant it carries fails.
35. **The run-line partition on `move --run` and `new --legacy-run` is the
    project's `partition:` row when that is `gpu | ral`; `both` requires
    `--partition`.** Why: the row is a capability, the run records the
    actual queue (decision 23), and the verb should not guess between two.
36. **`rule --also` on an `accepted` phase supersedes that phase's own
    `Ruling:`; the primary phase takes `--supersedes` explicitly.** Why: the
    REWIND is N accepted phases with N different heads, and spelling N ids by
    hand is the error-prone form of the same instruction.
37. **`gates --grade --write` removes `Gates-cleared:` when it demotes
    `ready → gated`; `--grade` exits 1 when any ref is unreadable.** Why: a
    stale cleared-date on a gated phase misreads as cleared; an unreadable
    ref fails closed and a scheduled run must notice.

Choices made in phase 2 — the conductor, the board and the workflows
(PyAutoMind#380):

38. **The dashboard normaliser strips the generated-comment line AND the
    visible `Last updated <date>` banner, in both `dashboard.md` and
    `dashboard.html`, before comparing.** Why: the Mind strips only the
    comment, so its banner changes date every night and `--check` reports
    drift on an unchanged registry — 348 self-heal commits in 30 days for a
    page nobody had touched. A no-op night here commits nothing.
39. **`collect` scores each leg PASS / FAIL / **UNOBSERVABLE**, and a member's
    `<HEALTH>` is FAILED if any leg failed, SUSPECT if any leg is
    unobservable, HEALTHY otherwise; a record's `delivered:` counts the
    HEALTHY members.** Why: two of the four delivery legs cannot be seen from
    the laptop today — the checkpoint is excluded from both projects' pulls,
    and `subhalo_validation` writes no structured version stamp — and scoring
    an unobservable leg as PASS would manufacture evidence while scoring it
    FAIL would cry wolf. SUSPECT says exactly what is true: nobody looked.
40. **(amended by 51)** **The pull manifest is
    `<mirror or local_path>/.cortex/pull.json`:
    `{"pulled_at": <ISO>, "runs": {"<jobid>": {"checkpoint_bytes": <int>,
    "checkpoint_mtime": <ISO>}}}` (decision 51 adds `schema` and
    `checkpoints`), written by each project's own sync CLI
    (phase 3), read by `collect` when present.** Why: "when was this pulled,
    and did the checkpoint grow?" is knowable only at the moment of the pull;
    the puller is the only process that can record it. Until the CLIs write
    it, the checkpoint leg stays UNOBSERVABLE, tagged `RAL only`.
41. **`collect --pull` is opt-in and shells out to the project's own
    `sync_cli pull`; nothing in the Cortex or the conductor ever submits a
    job.** Why: the laptop lane is human-driven by ruling (AGENTS.md); the
    conductor may refresh what is already on disk when asked, but a
    submission is a spend of the machine and of the human's attention, and it
    stays a typed command.
42. **The Brain conductor spells the writing flag `--apply`; `scripts/cortex.py`
    spells it `--write`.** Why: `--apply` is the Brain's house spelling across
    every conductor and the phase-2 prompt asked for it; `--write` is already
    the Cortex script's, documented and tested. `cortex gates --grade --apply`
    is a thin wrapper — one edit, two doors — and neither vocabulary is bent to
    the other.
43. **`gates_grade.yml` is the only scheduled job that mutates the ledger, and
    it may only move `gated → ready` (or `ready → gated` on a reopened gate).**
    Why: "is issue #380 closed?" is a fact GitHub answers, not a judgement, and
    a phase arriving in `ready` costs nothing until a human admits it into a
    slot. Everything else on a timer reads or re-renders. It commits what
    flipped **before** it fails on an unreadable ref, so a red run never means
    the flips were lost.
44. **Every workflow that can push to `main` shares `concurrency: group:
    cortex-main-writers, cancel-in-progress: false`.** Why: the race is not
    between two merges, it is between two writers of the tip —
    `ledger_merge.yml`'s merge, `dashboard_refresh.yml`'s self-heal and
    `gates_grade.yml`'s flips would otherwise burn their retry loops against
    each other. Queue, never cancel: a cancelled run can leave a branch merged
    and undeleted. `pages_dashboard.yml` keeps GitHub's own `group: pages`.
45. **`AGENTS.md` and `TEMPLATE.md` under a ledger dir are CODE**
    (`EXCLUDED_NAMES`), so `rulings/AGENTS.md`, `batches/AGENTS.md`,
    `batches/packets/{AGENTS.md,TEMPLATE.md}` and `batches/reviews/AGENTS.md`
    never auto-merge. Why: they are ledger by location and instructional by
    content — they say what an entry may be and what every future entry is
    stamped from. Auto-merging a rewrite of `rulings/AGENTS.md` would let a
    branch edit the rule that governs its own merge.
46. **`dashboard.md` and `dashboard.html` are LEDGER** (`LEDGER_FILES`). Why:
    they are generated from the ledger and hand-edited by nobody; a branch that
    moves a phase re-renders them in the same push, and
    `dashboard_refresh.yml`'s self-heal commit must land without a human. If
    they were code, every ordinary ledger branch would stop for review on two
    files nobody wrote.
47. **PyAutoBrain's tests for the cortex conductor depend on a real
    PyAutoCortex checkout beside the Brain** (a third checkout in `tests.yml`;
    the tests `pytest.skip` when it is absent). Why: the renderer's contract is
    with this repo's fixtures (`tests/fixtures/skeleton`), and a copy of them
    inside the Brain would drift from the schema they are the witness for.
48. **The page's GitHub home is read from the repo's own `README.md` /
    `AGENTS.md` links, falling back to the git remote — never from a hard-coded
    org.** Why: the render must be byte-identical on the laptop and inside
    `dashboard_refresh.yml`, or `--check` would report permanent drift and the
    self-heal would commit a page every night; a file that travels with the
    repo is readable in both places, whereas a git remote is not guaranteed in
    every CI container. A fork's Cortex renders its own owner.

49. **Four `collect` scoring rules fixed while implementing it (2026-09-01).**
    A `<hash>.zip` beside a run directory outranks the directory — seven subhalo
    dirs were stale partial extractions, so `search.summary` is read through
    `zipfile` when the zip exists. An `.err` that is non-empty, not all warnings
    and carries no fatal marker is UNOBSERVABLE (named first unexplained line),
    never PASS or FAIL — the machine cannot score it. "Newer than submitted"
    means newer than the phase's *first* submission, so a resubmit does not
    stale the real witness. Witness hits are ranked (run stem or `Where to look`
    leaf in the path first) because `witness_file` is project-wide and phases
    share one tree. Also: `submitted → pulled` is not an edge, so a `submitted`
    member is scored but left with a note rather than moved.

50. **`projects.yaml` gains `status: planned` and one optional field,
    `note:`; every other field stays required and an unknown field stays an
    error.** Why: phase 3 seeds the map with rows the phase-1 grammar could
    not spell. `euclid_dr1_prelim` exists as a decision before it exists as a
    directory — `planned` says "these are the paths it will have" without
    lying that the project is `active`, and without the row being invented
    twice later. And a third of the seeded rows are only intelligible with a
    sentence attached: why `euclid` has no PyAutoLabs remote, that a dormant
    row's `ral_root` is planned rather than observed, that a personal remote
    is a recorded fact and not a target. That sentence had nowhere to live but
    a comment, and a comment is not readable by the conductor. `note` is
    optional because most rows do not need one, and the field set stays closed
    (`PROJECT_FIELDS + PROJECT_OPTIONAL_FIELDS`) so a typo is still caught; an
    empty `note:` is drift, exactly like an empty required field.

51. **The pull manifest is v1 — `schema`, `checkpoints`, `runs` — and
    `checkpoints` is the table that is always filled** (supersedes the shape
    in decision 40, which stands as the record of why the manifest exists):
    ```json
    {"schema": 1,
     "pulled_at": "<ISO UTC>",
     "checkpoints": {"<run dir relative to the pull root>":
                     {"bytes": <int>, "mtime": "<ISO>"}},
     "runs": {"<jobid or jobid_task>":
              {"checkpoint_bytes": <int>, "checkpoint_mtime": "<ISO>"}}}
    ```
    Why the second table: decision 40 assumed the puller knows which job id
    produced which checkpoint, and one of the two projects cannot — the
    profiling CLI pulls a results tree that carries no job id at all. The run
    directory path *is* nameable on both sides, so `checkpoints` is keyed by
    it (relative to the pull root, the same root `collect` resolves the run
    directory under) and is always written; `runs` is written only where the
    CLI can link a job id to a run directory (subhalo's `.out` names the
    sample). `collect` therefore looks up `runs[ident]` → `runs[stem]` →
    `checkpoints[<run dir rel>]`, and a manifest with no `schema` key is read
    as the phase-2 shape so nothing that already exists breaks.
    Gathered in **one** `ssh "$HPC_HOST" "find '<ral_root>/output' -name
    checkpoint.hdf5 -printf '%s %T@ %p\n'"` over the existing ControlMaster
    mux, immediately before the manifest is written — one round trip, and the
    sizes are RAL's own, not the laptop's guess. The write is **dry-run
    guarded** (`status` calls `pull --dry-run`, and a dry run must not
    manufacture evidence that a pull happened), and `.cortex/` is gitignored
    in every project: it is pull state, like `output/`.
    Key shape, corrected by the first real pull: the checkpoint lives at
    `<run dir>/files/search_internal/checkpoint.hdf5`, so the `checkpoints` key is the
    run directory — the grandparent of the file — with any trailing `/files` stripped.

52. **`Science/euclid` gets `remote: none` by ruling, and the dormant rows
    follow three rules.** The euclid ruling (2026-09-01): it tracks a
    DR1-derived catalogue keyed by tile/RA/DEC
    (`catalogue/inspection/failure_mode_breakdown_consensus75.csv`), it
    already pushes to the personal remote `Jammy2211/euclid-dr1-modeling`, it
    nests the Overleaf paper repo, and it is 34 GB with an `output/` too large
    to `du`. Any one of those refuses a PyAutoLabs remote under the
    no-Euclid-data rule; together they settle it. Nothing is lost, because the
    project's code half is already at
    `PyAutoLabs/euclid_strong_lens_modeling_pipeline` at parity — what stays
    outside the org is data and prose. The row is still written, because the
    Cortex must be able to name a project it will never host.
    The dormant rules: **(a) git repos only** — `subhalo`, `euclid_group` and
    the `z_*` trees are storage, and storage is not a project with a
    lifecycle; **(b) an assistant clone is not a project** — `aris_PJ011646`
    is a copy of a workspace, so `pj011646` is the row and the clone is not;
    **(c) a personal remote is recorded as a fact, never as a target** —
    `slope_hierarchy`, `pj011646`, `concr` and `ic50_workspace` push to
    `Jammy2211/…` and the row says so in `remote:` with the reason in
    `note:`, so nobody re-derives the answer to "should this move into the
    org?" once a quarter.

53. **Provenance header: `Migrated-from:` joins `PHASE_KEYS` and `RULING_KEYS`**
    (one tuple edit each, plus the REFERENCE key tables and a test); its value
    is the Mind path or ledger anchor the file was transcribed from. Batch
    records may carry `- migrated-from:` (there is no key check on a record).
    Why: phase 4's whole job is moving records that were written somewhere
    else, and a migrated file that cannot name its source is a claim without a
    provenance. The prompt already required the line; without the key the
    current schema would have flagged every migrated file as unknown-key
    drift, so the requirement and the checker had to be reconciled — in favour
    of the requirement.

54. **Intra-Cortex sequencing is a body line, not a gate.** `Gates:` stays
    GitHub-refs-only. A phase that waits on another *Cortex* phase's ruling is
    `State: planned` with a line under `## Question` reading `Ready when:
    <phase> accepted (ruling R-…)`; the human moves it to `ready` once that
    ruling lands. A phase whose development gate has no issue yet is likewise
    `planned`, with `Ready when: <Mind prompt> is issued — add its ref to
    Gates: and move to gated`.
    Why: `gates --grade` polls GitHub, and the daily grader is the one
    scheduled job that mutates the ledger. A gate it cannot poll would either
    have to fail closed for ever or teach the grader a second, non-GitHub
    vocabulary. A science phase waiting on a sibling phase is waiting on a
    *human ruling*, which is exactly the thing the Cortex refuses to automate,
    so it belongs in prose the human reads and not in a field a robot grades.

55. **A Cortex-spawned development follow-up gets its issue at filing, without
    leaving `draft/`.** The Mind prompt carries a body line `Issue: <url>
    (opened <date> as a Cortex gate ref; reuse in start_dev — never open a
    second)`, and `create_issue` reuses that ref instead of opening another;
    Mind `REFERENCE.md` gains the rule. The same mechanism is what gives the
    euclid 3b gate its ref.
    Why: `Gates:` is GitHub-refs-only (decision 54), so a Cortex phase gated on
    work the Mind has not started yet has nothing to point at. The alternatives
    were to promote the prompt to `active/` before anyone works it — which
    lies about the workflow state — or to leave the phase ungated and hope. An
    issue is cheap, is the organism's real join key, and is the one artefact
    both halves can name; the `Issue:` line stops the second, duplicate issue
    that `start_dev` would otherwise open.

56. **Legacy-born encodings: how pre-Cortex history enters the ledger.** A run
    that happened before the Cortex existed is a `legacy` (reusable) or
    `legacy_wrong` (quarantined) run line carrying `where:`; a phase whose runs
    are *all* `legacy_wrong` is ruled `drop` straight from `ready`, because it
    cannot be pulled — there is nothing reviewable to pull. A programme-wide
    directive such as the 2026-08-31 REWIND is one ruling on a synthetic phase
    (`inference_programme/rewind_2026_08_31`) whose runs are the ids the
    directive itself names, with the directive verbatim as the ruling body. A
    multi-lens project gets one phase per lens. Transcribed batch records are
    rewritten in the Cortex grammar (member slug = phase slug) and the Mind
    originals stay intact with a `- moved-to:` line rather than being reduced
    to stubs; dev-only members of a mixed slot are noted in the record's
    `notes:`, never transcribed as science members.
    Why: the alternative — inventing `done` run lines for runs nobody reviewed
    — would let quarantined evidence re-enter the programme through the back
    door, which is the precise failure the REWIND was called to stop. Keeping
    the Mind originals verbatim is a deviation from the prompt's "stub": a
    history that only survives in `git log` is a history the next reader will
    not find, and two records that disagree are worse than one record and a
    pointer.

57. **A rolling slot is ruled more than once: `batches/reviews/<slot>-r<N>.md`,
    N ≥ 2** (2026-09-02, PyAutoBrain#341 — after phase 1). The first review
    stays `<slot>.md`; every later sitting is a numbered file in the same
    grammar, titled for its own stem or for the slot, ruling only on the
    members that had landed. The record carries one `- review:` line per file
    — the key repeats — and `check` resolves a numbered review to
    `batches/<slot>.md` and applies every review rule to it unchanged.
    Why: the board was rolling but the review was not. One file per slot meant
    the first sitting closed it, so a human who ruled on the two members that
    had arrived could only rule on the third by editing a ledger file that is
    already someone's evidence. Numbering the sittings keeps each file
    append-only and leaves one record resolving them all.
