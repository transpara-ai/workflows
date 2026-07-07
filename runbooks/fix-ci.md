---
name: fix-ci
description: Reproduce and fix failing tests, builds, lint, or CI checks.
argument-hint: "<failing command, CI URL, PR URL, or failure summary>"
---

# Fix CI

Run the fix-CI workflow for:

{{args}}

If your agent uses `$ARGUMENTS` instead of `{{args}}`, treat `$ARGUMENTS` as the failure input.

## Purpose

Turn a failing automated check into a small, verified fix.

## Use When

- CI is red.
- A test, build, typecheck, lint, or formatting check fails.
- The user asks why a check is failing.

## Inputs

- CI URL, failing command, log excerpt, or failure summary.
- Target branch or PR if relevant.
- Expected behavior if the failure is a test regression.

## Guardrails

- Reproduce the failure before changing code when practical.
- Fix the cause, not just the symptom.
- Do not weaken tests unless the test is clearly wrong.
- Do not silence lint or type errors without explaining why.
- Keep the patch focused on the failing check.

## Process

1. Gather the failing command, log, or CI job output.
2. Identify the first meaningful failure, not only the final exit code.
3. Reproduce the failure locally when possible.
4. Inspect the relevant code, tests, and recent changes.
5. State the suspected root cause.
6. Make the smallest fix.
7. Rerun the exact failing command.
8. Run nearby checks that could catch related regressions.
9. Review the diff for accidental broad changes.
10. Report what failed, why, and how it was verified.

## Required Evidence

- Failing command or CI job.
- Root cause.
- Files changed.
- Exact checks rerun.
- Result after the fix.

## Stop If

- Logs or failure details are unavailable.
- The failure depends on credentials or services you cannot access.
- The failure is flaky and cannot be reproduced or reasoned about.
- The fix would require changing product behavior outside the task scope.

## Final Report

Return:

- failure summary
- root cause
- fix summary
- checks run before and after
- remaining CI or flake risk
