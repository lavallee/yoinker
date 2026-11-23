# Changelog

All notable changes to Yoinker will be documented here. Versions follow semantic versioning.

## [Unreleased]

## [0.2.0] - 2026-11-23

### Added

- **Adoption mode.** A new reference, `adopt-what-was-decided.md`, for requests that authorize
  implementation: adopt only what the assessment supports, prefer the mechanism to the code, repeat the
  comparison after the change, credit what was taken wherever a later reader would look, and follow the
  target project's own contribution and release rules.
- **Compare outputs on the same input.** Artifact assessment now says to run a candidate's example
  inputs through the local system and put the results side by side, to run the local project's own check
  on its result, and to treat a check that passes a worse result as a finding.
- Assessment across several local projects: judge each mechanism for each owner, and say when a project
  already has it.
- An optional adoption record in the decision brief, and three cases and one grading line in the
  evaluation protocol for the new behavior.

### Changed

- **Invocation scope.** The skill no longer excludes requests that already authorize implementation: it
  assesses first, then adopts. This widens when the skill applies. `RELEASING.md` counts a scope change
  as major; this is released as a minor version because the project is before 1.0 and nothing an
  existing request relied on is removed.
- A looked-for local decision comes before calling a difference a defect: a trade-off an owner made on
  purpose is a question for them.
- Reworked the public site around a source-linked example, direct GitHub and release routes,
  copyable Codex and Claude Code installation, and usable mobile layouts.

### Evidence

- These changes come from one real session, in which the skill was asked to assess a diagram library
  against a canvas tool with implementation authorized. Reading both codebases suggested the local tool
  already did the same things; drawing the candidate's examples with the local tool showed a result its
  own check scored 98 of 100 with an arrow through a panel. The paired held-out comparison in
  `evaluation/protocol.md` has not been run for this release, as it had not been for 0.1.0.

## [0.1.0] - 2026-08-30

### Added

- Initial release-candidate skill with artifact-assessment and open-question modes.
- Evidence, authority, transfer, and human-approval boundaries.
- Optional decision brief and a held-out evaluation protocol.
- Public repository documentation, static landing page, CI, and release checks.
