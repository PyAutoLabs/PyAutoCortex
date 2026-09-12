# projects/ — one ledger per science project

`projects/<key>.md`, one file per row of `projects.yaml` that is doing
anything. The file is a **history of how the project unfolds**, not a task:
nothing in it is ever done, completed or retired — it only gets older.

## The rules

1. **Every write is a `scripts/cortex.py` verb.** `run` / `running` / `done`
   record what the cluster did; `log` and `now` record what the human said.
   Never edit a ledger by hand in a session, and never write an entry the
   human did not ask for.
2. **Nothing is inferred from results.** A `result` or `lesson` entry is the
   human's words, on the human's ask. An agent reading a results file writes
   nothing here about what it means; it tells the human, and the human says
   what to log.
3. **`## Now` is rewritten, `## Log` is prepended.** Now is the head pointer
   (where am I, what next); the log is the record. The board shows Now, the
   runs on the cluster, and the last five entries.
4. **One line per entry.** `- YYYY-MM-DD — kind — text`, newest first;
   continuation lines are indented two spaces. `--` is read as the dash.
5. **Run `python3 scripts/cortex.py check` before you push.** The
   auto-merge gate runs it on the merged tree and leaves a failing branch for
   a human.

`AGENTS.md` here is doctrine, not an entry: the merge gate treats it as code.
