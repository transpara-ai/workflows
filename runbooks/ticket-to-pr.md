---
name: ticket-to-pr
description: Take a scoped engineering task from clean start to tested pull request.
argument-hint: "<ticket URL, issue number, or task description>"
---

# Ticket To PR

Input: one scoped ticket, issue, bug report, or task description.
Output: one high quality pull request, or a clear blocker if a PR cannot be produced safely.

Use this workflow when the user wants a scoped change implemented and, when asked, published as a pull request.

Task:

```text
{{args}}
```

If your agent uses `$ARGUMENTS`, use that as the task instead.

## 1. Start With The Local Rules

Before touching files, read the project guidance.
Look for files such as `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, the README, and any developer docs that clearly apply to the task.

Use those files to learn the repo's commands, style, generated files, and safety rules.
If the project says generated files must come from a generator, edit the generator rather than the generated output.

## 2. Check The Starting State

Run `git status --short`.
If there are existing changes, decide whether they are part of the user's task.

Stop if you need to edit a file that already has unrelated user changes.
Ask the user how to proceed instead of overwriting or cleaning up their work.

If the tree is clean, create a task branch or worktree when that is normal for the environment.
Use a short, descriptive name.

## 3. Understand The Change

Restate the task in one or two plain sentences.
Then find the code path that owns the behavior.

Read before editing.
Look at nearby tests, callers, docs, configuration, and prior patterns.
Do not start with a broad refactor.

If the task is ambiguous in a way that could change the product behavior, ask one focused question.
If the ambiguity is small, make a conservative assumption and mention it later.

## 4. Make The Smallest Complete Change

Edit only the files needed for the task.
Match the repo's existing style.
Add or update tests when behavior changes.

Keep notes as you work: what changed, why it changed, and what needs verification.
If the implementation grows beyond the original scope, stop and explain the new scope before continuing.

## 5. Verify The Work

Run the narrowest useful check first.
For example, run the specific test package, focused unit test, typecheck, or build that proves the changed behavior.

Then run the broader check expected before a PR.
Use the repo docs to choose the command.

If a check fails, fix the cause when it is related to your change.
If the failure is unrelated or unclear, stop and report what failed, what you tried, and why you cannot safely continue.

## 6. Review Your Own Diff

Inspect `git diff`.
Review the change as if another developer wrote it.

Look for wrong behavior, broken contracts, missing error handling, unsafe data handling, missing tests, and accidental unrelated edits.
Fix blocking issues before moving on.
Leave nits alone unless they affect clarity or correctness.

## 7. Commit And Publish Only When Asked

If the user asked for a commit, stage only the files that belong to this task.
Write one clear commit message.

If the user asked for a push or pull request, push the branch and open the PR after the commit.
Use the PR body to explain what changed, why it changed, and how it was checked.

Do not tag, release, deploy, or publish packages from this workflow.

## Final Report

End with a short report that includes the changed files, checks run, self-review result, branch name, commit hash if any, PR URL if any, and remaining risk.
