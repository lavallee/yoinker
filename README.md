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

## What Yoinker does not do

Yoinker does not install or execute the thing it assesses. It does not certify security, create work,
merge code, publish, or turn a recommendation into permission. Popularity, a polished demo, or a long
list of citations does not count as proof of fit or outcomes.

“Yoink” means carrying over a permitted mechanism with its evidence, attribution, and license duties
intact. It does not mean copying code or content without rights.

## Repository map

- [`skills/yoinker/SKILL.md`](skills/yoinker/SKILL.md) — the shared entrypoint and safety boundaries.
- [`references/assess-an-artifact.md`](skills/yoinker/references/assess-an-artifact.md) — the specific
  artifact mode.
- [`references/answer-an-open-question.md`](skills/yoinker/references/answer-an-open-question.md) — the
  explanation and comparison mode.
- [`templates/decision-brief.md`](skills/yoinker/templates/decision-brief.md) — an optional durable
  handoff.
- [`evaluation/protocol.md`](evaluation/protocol.md) — the held-out promotion test.
- [`docs/index.html`](docs/index.html) — the static GitHub Pages landing page.

## Status

Version **0.1.0** is the initial MIT-licensed release. The skill and dual-harness plugin package pass
structural and repository checks. The proposed held-out behavioral comparison has not yet been run;
availability is not evidence of improved outcomes. See [`RELEASING.md`](RELEASING.md) for the release
and evaluation contract.
