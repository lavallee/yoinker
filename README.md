# yoinker

## Understand how it works. Yoink what transfers.

Interesting tools rarely arrive as clean yes-or-no choices. A repository may contain one useful
mechanism inside an operating model you should reject. A persuasive article may explain an approach
well without proving that it works. A familiar-looking technique may solve the wrong local problem.

Yoinker gives an agent a disciplined way through that mess. Give it a link or a question. It follows
the evidence to the original artifact, explains the mechanism, checks it against the situation you
actually have, and identifies exactly what—if anything—is worth borrowing.

It is built for two ordinary requests:

- **Assess this:** “Here is a repository. Would it help this project, and how should we think about
  adopting it?”
- **Explain this:** “What does this tool actually do? How do these approaches differ?”

The answer is not a universal score. It is an inspectable explanation and, when local context exists,
a mechanism-by-mechanism decision: **borrow, try, track, or reject**.

**[See a worked example and install Yoinker →](https://lavallee.github.io/yoinker/)**

## Install

Install Yoinker from the `lyra-forge` marketplace, then start a new session so the harness loads the
skill:

```text
# Claude Code
/plugin marketplace add lyra-forge/marketplace
/plugin install yoinker@lyra-forge

# Codex
codex plugin marketplace add lyra-forge/marketplace
codex plugin add yoinker@lyra-forge
```

Invoke the installed skill as `/yoinker:yoinker` in Claude Code or `$yoinker:yoinker` in Codex.

Other skill-compatible agents can load [`SKILL.md`](skills/yoinker/SKILL.md) and its referenced files
directly. Codex users can also ask `$skill-installer` to install the skill from this repository's
[`skills/yoinker/`](skills/yoinker/) directory without installing the marketplace plugin.

## Try it

Ask about a specific artifact:

> Use `$yoinker` on this repository. Explain what it does, whether it helps the project in this
> directory, and what—if anything—we should borrow.

Or ask an open question:

> Use `$yoinker` to explain what GraphRAG changes compared with ordinary full-text retrieval. Separate
> what is directly supported from what depends on my data and workload.

Yoinker will inspect available local context before claiming local fit. If that context is missing, it
will explain the general mechanism and name the facts that would change the decision.

## What changes in the answer

- Discovery links become leads; original artifacts become evidence.
- Authority is judged for each claim instead of assigned once to a publisher.
- Observations, source claims, inferences, recommendations, experiments, and outcomes remain distinct.
- Useful mechanisms can be separated from a source that should otherwise be rejected.
- Uncertainty becomes a bounded test with a baseline and stop condition—not an indefinite “explore.”

## Where the decisions go

A decision you will want again is kept as one Markdown record per artifact or question:

- **with the project it concerns**, in `docs/yoinker/` unless the project already names a place for
  research and decisions, so the reasoning accrues in the repository it changed;
- **outside a public repository** by default: in its private companion if it has one, because a record
  names local constraints and reasoning you may not mean to publish;
- **in a per-user store** when no project fits: `$YOINKER_HOME` if set, otherwise
  `$XDG_DATA_HOME/yoinker` (`~/.local/share/yoinker` by default).

Each record carries the pinned source, the per-mechanism decisions, and a dated outcome log. Yoinker
checks for an earlier record before assessing the same thing again, including records opened from other
projects on the same machine. A bundled, dependency-free helper does the bookkeeping; it never clones,
installs, or executes what is being assessed. See
[`references/keep-a-record.md`](skills/yoinker/references/keep-a-record.md).

## What Yoinker does not do

Yoinker does not install or execute the thing it assesses. It does not certify security, create work,
merge code, commit, publish, or turn a recommendation into permission. When you authorize
implementation, it assesses first and adopts only what the assessment supports, with credit for what
it took. Otherwise the only file it writes is the decision record, and only when the decision is worth
keeping. Popularity, a polished demo, or a long
list of citations does not count as proof of fit or outcomes.

“Yoink” means carrying over a permitted mechanism with its evidence, attribution, and license duties
intact. It does not mean copying code or content without rights.

## Repository map

- [`skills/yoinker/SKILL.md`](skills/yoinker/SKILL.md) — the shared entrypoint and safety boundaries.
- [`references/assess-an-artifact.md`](skills/yoinker/references/assess-an-artifact.md) — the specific
  artifact mode.
- [`references/answer-an-open-question.md`](skills/yoinker/references/answer-an-open-question.md) — the
  explanation and comparison mode.
- [`references/adopt-what-was-decided.md`](skills/yoinker/references/adopt-what-was-decided.md) — carrying
  out an assessment's decisions once implementation is authorized.
- [`references/keep-a-record.md`](skills/yoinker/references/keep-a-record.md) — where records go, how
  earlier ones are found, and how outcomes are logged.
- [`scripts/record.py`](skills/yoinker/scripts/record.py) — the record helper.
- [`templates/decision-brief.md`](skills/yoinker/templates/decision-brief.md) — an optional durable
  handoff.
- [`evaluation/protocol.md`](evaluation/protocol.md) — the held-out promotion test.
- [`docs/index.html`](docs/index.html) — the static GitHub Pages landing page.

## Status

Version **0.2.0** adds an adoption mode and output comparison to the 0.1.0 skill, under the MIT license.
The skill and dual-harness plugin package pass structural and repository checks. The proposed held-out behavioral comparison has not yet been run;
availability is not evidence of improved outcomes. See [`RELEASING.md`](RELEASING.md) for the release
and evaluation contract.
