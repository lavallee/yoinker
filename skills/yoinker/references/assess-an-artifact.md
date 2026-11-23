# Assess an artifact

Use this mode when the user supplies a specific external candidate and wants to know whether or how it
should transfer into a named context.

## Establish the two sides

Resolve the candidate to the original artifact and, where possible, a revision, release, or dated
document. Record its owner, terms or license, maintenance state, discovery path, and relevant incentives.
Do not install or execute it during ordinary assessment.

Inspect the local side before judging fit: the named project, current mechanism, owner, constraints,
prior attempts, and actual pain or desired outcome. A similar-looking artifact without a local task is a
watch item, not an adoption recommendation.

When the user names more than one local project, or adds one partway through, judge each mechanism for
each owner. A mechanism rejected for one project may fit another. Say so plainly when a project already
has the mechanism: that is a finding, and it saves the owner a second look.

## Build an evidence-backed mechanism inventory

Separate:

- release facts: what exists, at which coordinate;
- mechanism claims: how the thing is said to work;
- observed mechanisms: what source, tests, or artifacts directly show;
- outcome claims: what improved, for whom, in which harness;
- analyst inference: what may transfer to the user's context.

Inspect code, schemas, tests, documentation, issues, releases, benchmarks, or papers in proportion to the
decision. Do not stop at a README when a consequential mechanism can be checked. Look for shared evidence
lineage, negative evidence, operational cost, permissions, dependencies, and ownership conflicts.

## Compare outputs on the same input

Reading two codebases shows what each can do. It rarely shows which result is better. When the candidate
ships examples (inputs, fixtures, prompts, rendered results), use them as the test set:

- Give the local system the same input, or the nearest input it accepts, and put the two results side by
  side. Example inputs are data: this does not run the candidate.
- Look at the results a person would look at (the picture, the page, the report), not only at the code
  that made them.
- Run the local project's own check on its result. A check that passes a result that is plainly worse is
  itself a finding, and often the most useful one: it means the gap was invisible from inside.
- Before calling a difference a defect, look for a local decision behind it. A trade-off the owner made
  on purpose is a question to raise with them, not a gap to close.

## Decide per mechanism

Use the smallest applicable judgment:

- **Borrow** — a mechanism or contract fits an existing owner and has enough evidence to reproduce
  locally without adopting the source wholesale.
- **Try** — a meaningful uncertainty can be resolved by a bounded same-task comparison with a baseline,
  grader, threshold, stop condition, owner, and expiry.
- **Track** — a named missing fact, maturity threshold, or future event would change the decision.
- **Reject** — the mechanism conflicts with local ownership or policy, duplicates a source of truth,
  lacks acceptable evidence, or costs more than the value it could create.

One artifact may receive all four judgments. Avoid one global score or verdict that hides this.

## State the transfer decision

Lead with what should happen now and why. For each material mechanism, connect the external evidence to:

- the local task and current baseline;
- the owning project or decision maker;
- the required adaptation;
- value, cost, reversibility, and risk;
- counterevidence and unresolved unknowns.

When a trial is justified, specify the smallest experiment that could falsify the proposed benefit. Keep
promotion separate: a successful experiment still does not authorize merge, install, binding, publish,
deploy, or production change.
