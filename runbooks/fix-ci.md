---
name: fix-ci
description: Reproduce and fix failing tests, builds, lint, or CI checks.
argument-hint: "<failing command, CI URL, PR URL, or failure summary>"
---

# Fix CI

Use this workflow when a build, test, lint, typecheck, or CI job is failing.

Failure:

```text
{{args}}
```

If your agent uses `$ARGUMENTS`, use that as the failure input instead.

## 1. Get The Real Failure

Start with the failing command, CI URL, log excerpt, or PR check.
Find the first meaningful error.

Do not stop at the final exit code if an earlier error explains the failure.
If logs are missing, ask for them or use the available CI tooling to fetch them.

Stop if the failure depends on secrets, production systems, or credentials you cannot access.

## 2. Reproduce Before Editing

Run the failing command locally when practical.
If local reproduction is impossible, explain why and work from the CI evidence.

Once you reproduce or understand the failure, state the likely root cause in one sentence.
Then inspect the code, tests, config, or recent changes that connect to that cause.

## 3. Fix The Cause

Make the smallest change that addresses the root cause.
Do not weaken tests just to make CI pass unless the test is clearly wrong and you can explain why.

Do not hide lint, type, or build errors with broad ignores.
If an ignore or skip is truly needed, document the reason in the code or final report.

## 4. Prove The Fix

Rerun the exact failing command.
Then run the nearest broader check that could catch related regressions.

If the failure is flaky, run the check enough times to build confidence or report that it remains a flake.
Do not claim the fix is proven if the same check still fails.

Review the diff before finishing.
Make sure the patch is focused on the CI failure and did not include unrelated cleanup.

## Final Report

End with the failure, root cause, fix, exact checks run, result after the fix, and any remaining CI or flake risk.
