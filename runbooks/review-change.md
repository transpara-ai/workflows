---
name: review-change
description: Review a diff, branch, or pull request without taking over implementation.
argument-hint: "<diff, branch, PR URL, or review focus>"
---

# Review Change

Run the review workflow for:

{{args}}

If your agent uses `$ARGUMENTS` instead of `{{args}}`, treat `$ARGUMENTS` as the review target.

## Purpose

Find correctness, security, contract, and test risks in a proposed change.

## Use When

- The user asks for a review.
- The user wants confidence before committing, pushing, or merging.
- The user provides a PR, branch, staged diff, or uncommitted diff.

## Inputs

- Review target, default current diff.
- Review focus, if provided.
- Base branch, if reviewing a branch or PR.

## Guardrails

- Default to read-only.
- Do not edit files unless the user explicitly asks for fixes.
- Review from actual diff and source files, not memory.
- Prioritize real bugs over style preferences.
- Do not invent findings to appear useful.

## Process

1. Identify the review target.
2. Inspect git status and the relevant diff.
3. Read changed files with enough context to understand behavior.
4. Check affected callers, tests, configuration, and docs.
5. Look for correctness bugs first.
6. Check broken contracts, compatibility, security, data loss, and concurrency risks.
7. Check whether tests would fail without the change.
8. Separate blocking findings from nits.
9. If no issues are found, say that clearly and name residual risk.

## Required Evidence

- Review target.
- Files inspected.
- Findings with file and line references where possible.
- Test gaps or residual risk.

## Stop If

- The diff cannot be found.
- The target branch or PR is unavailable.
- The change is too large to review responsibly in one pass.
- Required generated files, schemas, or artifacts are missing.

## Final Report

Lead with findings, ordered by severity.

Use this shape:

1. Findings
2. Open questions
3. Test gaps
4. Short summary

If there are no findings, say so plainly.
