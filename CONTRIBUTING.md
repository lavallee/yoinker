# Contributing to Yoinker

Yoinker should make an agent's judgment more inspectable without turning every answer into a form or
every useful example into a universal rule.

## Set up

The repository has no runtime dependencies. Run the release checks with Python 3.11 or newer:

```bash
python scripts/check_repo.py
```

If the Codex skill-authoring tools are installed locally, also run their structural validator:

```bash
python /path/to/skill-creator/scripts/quick_validate.py skills/yoinker
```

## Make a change

- Keep the discovery description concise enough to route only relevant requests.
- Put shared boundaries in `SKILL.md`; keep mode-specific detail in the relevant reference.
- Preserve user authority. Assessing or recommending a change does not authorize implementing it.
- Add guidance only when it changes a consequential decision or fixes a demonstrated failure.
- Keep examples sanitized. Do not commit private paths, credentials, captured source material, internal
  project names, or held-out expected answers.
- Preserve attribution and applicable license terms when borrowing an external mechanism.

Behavior changes should update [`evaluation/protocol.md`](evaluation/protocol.md) or add a sanitized
development case. A structural check is not evidence that the skill improves an agent's decisions.

## Before a pull request

Run `python scripts/check_repo.py`, inspect the complete diff, and explain:

1. which realistic request the change improves;
2. what evidence supports the change;
3. whether the change affects invocation, permissions, or release compatibility.
