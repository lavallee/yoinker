# Promotion experiment

Status: proposed. Structural validation of the skill is not behavioral validation.

## Question

Does `yoinker` improve source-grounded explanation and local transfer judgment compared with
the same model, harness, tools, and budget without the skill?

## Cases

Prepare development and private held-out sets across both modes:

- pinned repository against a named project with an existing competing mechanism;
- polished artifact whose README outcome claim is not supported by tests;
- useful mechanism inside a source that should otherwise be rejected;
- candidate with missing license or unsafe installation path;
- focused “what does this do?” question;
- comparison with shared evidence lineage across many summaries;
- broad question where source authority changes by claim;
- question whose honest result is unknown or context-dependent.

Do not publish the held-out expected decisions with the skill.

## Comparison

- Same served model and model settings.
- Same harness, tools, source snapshot, time limit, and output request.
- Randomized paired baseline/variant order.
- Record whether the skill was invoked, tool calls, tokens, cost, latency, and all outputs.

## Independent grading

Grade behavior, not headings:

- correct resolution to original artifacts;
- evidence coordinates that entail the associated claims;
- claim-specific authority and lineage judgment;
- observation / claim / inference / recommendation separation;
- accurate use of supplied local constraints and ownership;
- per-mechanism decision quality and counterevidence;
- falsifiable, proportionate next test;
- absence of unauthorized implementation or commanding work;
- usefulness and time-to-decision for a human reader.

## Promotion gate

Promote only if the variant improves the held-out behavioral result without a material increase in
unsupported claims, operator burden, cost, or latency. Preserve negative and null results with the exact
skill revision. Keep package ownership, isolated execution, model/cost receipts, evidence custody, and
human promotion authority explicit; no participant should grade or promote its own output silently.
