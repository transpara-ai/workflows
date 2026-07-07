---
name: ticket-to-pr
description: Take a scoped engineering task from clean start to tested pull request.
argument-hint: "<ticket URL, issue number, or task description>"
---

# Ticket To PR

Run the ticket-to-PR workflow for:

{{args}}

If your agent uses `$ARGUMENTS` instead of `{{args}}`, treat `$ARGUMENTS` as the task input.

## Purpose

Turn a scoped feature, bug fix, or engineering task into a reviewed, tested pull request.

## Use When

- The user asks to implement a feature or bug fix.
- The user provides an issue, ticket, or clear task description.
- The expected output is code plus a branch, commit, or PR.

## Inputs

- Task description, issue, or ticket URL.
- Target branch, default `main`.
- Any requested branch name, commit behavior, or PR behavior.

## Guardrails

- Inspect repo instructions before editing.
- Inspect git status before editing.
- Do not overwrite unrelated user changes.
- Do not make broad refactors unless they are required for the task.
- Do not commit, push, or open a PR unless the user asked for that.
- If requirements are risky or unclear, stop and ask a focused question.

## Process

1. Read project guidance such as `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, or equivalent.
2. Inspect the README and developer docs relevant to the task.
3. Run `git status --short` and note any existing changes.
4. Create a clean branch or worktree when the environment supports it.
5. Restate the task in one or two sentences.
6. Find the smallest set of files needed for the change.
7. Implement the change.
8. Add or update tests when the behavior changed.
9. Run the narrowest useful checks first.
10. Run the broader repo checks expected before PR.
11. Review the final diff for correctness, security, contracts, and test gaps.
12. Fix blocking review findings.
13. Commit only the intended files if the user asked for a commit.
14. Push and open a PR only if the user asked for a PR.

## Required Evidence

- Starting branch and final branch.
- Files changed.
- Tests and checks run, with results.
- Review result.
- Commit hash if committed.
- PR URL if opened.

## Stop If

- The working tree has unrelated changes in files you must edit.
- The task requires credentials, secrets, or production access you do not have.
- Tests fail and the cause is unknown.
- The implementation path would be much larger than the task implies.
- The user asked for a PR but no remote or GitHub access is available.

## Final Report

Return:

- what changed
- where it changed
- checks run
- review result
- branch, commit, and PR details when available
- remaining risks or follow-up work
