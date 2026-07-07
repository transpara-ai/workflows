# Runbooks

These are the canonical workflow files.

Each file is designed to work as a plain prompt, a slash command, or the body of an agent skill.
Keep them portable unless a platform-specific adapter is clearly needed.

## Shape

Each runbook should include:

- purpose
- use when
- inputs
- guardrails
- process
- required evidence
- final report
- stop conditions

## Included

- `ticket-to-pr.md`
- `review-change.md`
- `fix-ci.md`
- `investigate.md`
- `release.md`
