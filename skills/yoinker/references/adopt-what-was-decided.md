# Adopt what was decided

Use this mode only when the user has authorized implementation, in the same request or after reading
the assessment. The assessment still comes first: adoption carries out its per-mechanism decisions, and
adds none of its own.

## Carry the decisions, not the source

- Work from the verdicts. Implement what was judged **borrow**, and a **try** only once its test has
  passed. Leave **track** and **reject** alone, and say that they were left.
- Prefer the mechanism to the code. Reproduce a borrowed mechanism in the local project's own structure
  and vocabulary. Copy code, content or data only when its license allows it and the user wants it, and
  keep the license notice with what was copied.
- Keep the scope the assessment set. A neighbouring improvement noticed on the way is a new finding to
  report, not part of this change.
- Work where the change can be discarded: a branch or a worktree, never the user's working tree.

## Prove it on the same cases

The comparison that showed the gap is the acceptance check. Run it again after the change and show both
results side by side. Then run the local project's own checks: a baseline it already holds must not fall.

If the local check passed the bad result before the change, fix the check as well as the output. Otherwise
the next gap of the same kind is as invisible as this one was.

## Credit what was taken

Say where a mechanism came from wherever a later reader would look for it:

- the changelog or release notes, naming the artifact, its author and its license;
- the code that implements it, in a comment at the mechanism;
- the user-facing documentation, when the project keeps a credits section.

In each place, say what was taken (the idea, the form, the vocabulary, or code) and what was not. Pin the
revision that was examined. Credit the author as the source of the mechanism, not as an endorser of the
result.

## Follow the target's own rules

Read the target project's contribution and release instructions before changing it, and follow them:
its checks, its versioning, its changelog form. When a required step cannot be run, say which one and
why, in the pull request and in the final report. Do not describe a step as done until its result has
been seen.

Publishing is a separate authority from implementing. Release only when the user has said to.

## Report the adoption

Lead with what changed for a user of the local project. Then, for each mechanism: its verdict, what was
done, where it lives, and the evidence that it works. Name what was left and why. Name each decision that
belongs to a person and what was chosen by default, so it can be reversed.
