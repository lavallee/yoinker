# Keep a record

Use this when an assessment produces a decision someone will want to find again: any `borrow`, `try`,
or `track`, or a `reject` that would otherwise be argued a second time. A quick explanation needs no
record. Neither does a request where the user asked for no file changes.

A record is one Markdown file per artifact or question. It holds the pinned coordinates, the decision
brief, and a dated log of what happened afterwards.

## Look before you start

Check for an earlier record before gathering evidence:

```bash
python3 scripts/record.py find <url-or-name>
```

Run it from the project directory, with the path to this skill's `scripts/record.py`. It searches the
project's records, the per-user store, and the index of records opened in other projects.

When a record exists, read it first. Compare its pinned revision with the current one and assess what
changed. Update that record; do not open a second one for the same source.

## Where a record goes

The record belongs with the decision it supports, so later work in that project finds it.

1. **In the project the decision is about.** Use the place the project already keeps research or
   decisions if its instructions name one (`--dir <path>`). Otherwise use `docs/yoinker/` at the
   project root.
2. **In the per-user store** when there is no project, the project is not yours to write to, or the
   question is not about one project (`--shared`). The store is `$YOINKER_HOME` if set, otherwise
   `$XDG_DATA_HOME/yoinker`, which defaults to `~/.local/share/yoinker`. Records go in `records/`.

**A public repository is the exception.** A record names local constraints, other projects, and
reasoning its owner may not mean to publish. When the project's repository is public, put the record in
the project's private companion repository if it has one, and otherwise in the per-user store. Put it in
the public repository only when the user asks for that. If you cannot tell whether a repository is
public, ask or use the per-user store.

Never write a record into the skill's own installation directory, and never into a second project you
are not working in. If an assessment finds something for another project, say so in the record and in
your answer, and let that project's owner decide.

Open the record with:

```bash
python3 scripts/record.py new <original-artifact-url> --title "<name>"
python3 scripts/record.py new "<the question>" --shared
```

`new` gives the record a stable name derived from the source, pins a repository on a known forge to its
default-branch commit by asking the remote for one ref, writes the decision brief headings, and adds a
pointer to the per-user index. It does not clone, install, or execute anything. If pinning fails, the
record says so; add a release, version, or access date by hand.

Without Python, do the same by hand: create the file from
[the decision brief](../templates/decision-brief.md) and put the source, revision, and date at the top.

A record in a project is a file change. Leave it uncommitted unless the user asked you to commit, and
tell the user the path.

## What a record must not hold

Keep copied source, captured pages, credentials, and private data out of the record. Cite coordinates:
a URL with a revision, a file and line range, a section, a timestamp. If the project keeps captures,
follow its own custody rules for them.

## Log what happened afterwards

A recommendation is not an outcome. When you later learn what became of a decision, append a dated line
to the record's outcome log:

- a `borrow` that landed, with the commit, pull request, or change it became;
- a `try` that ran, with the result against its threshold, including null and negative results;
- a `track` whose awaited fact arrived, or whose expiry passed;
- a decision that was withdrawn or reversed, and why.

Append; do not rewrite earlier entries or delete a record because its recommendation failed. A wrong
call that stays visible stops the same argument from restarting. When the outcome changes the decision,
update the status line and the bottom line, and leave the log as the history.
