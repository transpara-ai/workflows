---
name: review-change
description: Review a diff, branch, or pull request without taking over implementation.
argument-hint: "<diff, branch, PR URL, or review focus>"
---

# Review Change

Use this workflow when the user asks for a review and does not want you to take over implementation.

Review target:

```text
{{args}}
```

If your agent uses `$ARGUMENTS`, use that as the review target instead.

## 1. Find The Exact Change

Start from the actual diff, branch, or PR.
If the user did not name a target, review the current uncommitted and staged changes.

Do not review from memory.
Inspect the changed files and enough surrounding code to understand the behavior.

Stop if the review target cannot be found or is too large to review responsibly in one pass.
Ask the user to narrow the scope.

## 2. Understand The Intent

Infer what the change is trying to do from the ticket, PR body, commit message, tests, or changed code.
If the intent is unclear, say what you are assuming before judging the code.

Look at callers, configuration, data flow, and tests when they are relevant.
A review that ignores the surrounding contract is only a style pass.

## 3. Look For Real Risks First

Prioritize issues that could break users, data, security, compatibility, or tests.
Check edge cases, nil or empty values, error handling, permissions, concurrency, and generated files when they apply.

Then check whether the tests prove the behavior.
A test gap is worth reporting when the bug could plausibly return.

Avoid comments that are only personal taste.
Do not invent findings if the change is sound.

## 4. Report Findings Clearly

Lead with findings.
Order them by severity.
Use file and line references when possible.

For each finding, explain the concrete risk and the smallest likely fix.
Separate blocking issues from nits.

If there are no findings, say that plainly.
Name any residual risk, such as checks you did not run or areas you could not inspect.

## Final Report

Return findings first, then open questions, test gaps, and a short summary.
Do not edit files unless the user explicitly asks for fixes.
