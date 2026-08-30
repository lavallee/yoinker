# Releasing Yoinker

Yoinker is an Agent Skill and dual-harness plugin, not a Python package. There is no PyPI artifact. A
release consists of the exact skill tree, synchronized plugin manifests, repository documentation, a
GitHub tag and release, the static site, and marketplace entries that resolve to the released source.

## Versioning

Yoinker follows semantic versioning. The canonical version is in `VERSION`; the same version appears in
both plugin manifests, `README.md`, `CHANGELOG.md`, and the landing page.

- **Patch** — corrections or clarifications that preserve decisions and invocation scope.
- **Minor** — a new backward-compatible mode, verdict, template, or supported request class.
- **Major** — a change to invocation scope, evidence semantics, verdict meanings, authorization
  boundaries, or required output contract.

## Release checklist

1. Start from a clean `main` and inspect every change since the previous tag.
2. Run the repository, skill, and plugin checks:

   ```bash
   python scripts/check_repo.py
   python /path/to/skill-creator/scripts/quick_validate.py skills/yoinker
   python /path/to/plugin-creator/scripts/validate_plugin.py .
   claude plugin validate . --strict
   ```

3. Run the paired evaluation in [`evaluation/protocol.md`](evaluation/protocol.md) against the exact
   candidate revision. Preserve model, tool, cost, latency, grader, and negative/null-result receipts.
4. Bump `VERSION`, both plugin manifests, the README status, the landing-page badge/status, and the
   dated `CHANGELOG.md` entry in lockstep.
5. Re-run the checks after the version bump. A release is blocked by any failure, by an unreviewed
   permission expansion, or by a held-out result that does not earn promotion.
6. Publish the source repository before updating the marketplace. Pin both marketplace catalogs to the
   same verified release commit so installs resolve to the bytes that passed these checks.
7. Commit a clean `chore(release): X.Y.Z`, create an annotated `vX.Y.Z` tag, and push `main` plus the
   tag only after explicit publication approval.
8. Create a GitHub release with focused notes and a compare link. Enable GitHub Pages from `main/docs`
   and verify the live page, links, and version badge.
9. Update and validate both marketplace catalogs, install the plugin in each harness, and verify the
   exact installed version from a fresh session.

Do not describe a local check, commit, tag, push, package entry, or Pages configuration as a completed
public release until its corresponding remote and live state has been verified.
