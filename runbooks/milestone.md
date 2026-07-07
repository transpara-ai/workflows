---
name: milestone
description: Work through every ticket in a milestone until each one has a high quality PR.
argument-hint: "<milestone URL, milestone name, or ticket list>"
---

# Milestone

Input: one milestone, release scope, or ordered list of tickets.
Output: a clear goal with every ticket worked through to a high quality PR or an explicit blocker.

Use this workflow when the user wants an agent to work through a group of related tickets, not just one task.

Milestone:

```text
{{args}}
```

If your agent uses `$ARGUMENTS`, use that as the milestone input instead.

## 1. Create The Goal

Start by turning the milestone into one explicit goal.
The goal should name the milestone, the expected output, and the stop condition.

Use the agent's goal primitive if it has one.
For example, create a goal such as:

```text
Work through milestone <name> until every ticket has a high quality PR or a documented blocker.
```

The goal is the source of truth for the run.
Use it to track progress across tickets, compaction, handoffs, or resumed sessions.

## 2. Build The Ticket List

Find the tickets in the milestone.
If the milestone comes from GitHub, Linear, Jira, Notion, or another tracker, read the live ticket data when tools are available.
If tools are not available, work from the ticket list the user gave you.

Create a short queue with the ticket id, title, status, and any dependency notes.
Do not start implementation until the queue is clear enough to work from.

If tickets are missing acceptance criteria, mark them as unclear.
Ask only for the details that block the next useful step.

## 3. Choose The Next Ticket

Pick the next ticket that is unblocked, small enough to finish, and likely to reduce milestone risk.
Prefer dependency unlocks, failing tests, and foundational fixes before polish.

Before starting, say which ticket you chose and why.
Then run the `ticket-to-pr` workflow for that ticket.

Do not batch unrelated tickets into one PR unless the milestone explicitly calls for that.
Small, reviewable PRs are usually the output you want.

## 4. Finish Or Block The Ticket

For each ticket, end in one of two states.

The ticket is done when it has a high quality PR with checks run, self-review completed, and enough context for a human reviewer.
Record the branch, commit, PR URL, checks, and remaining risk.

The ticket is blocked when progress needs missing product input, unavailable credentials, broken external systems, or a dependency that must land first.
Record the blocker clearly and move to the next useful ticket.

Do not hide a blocked ticket by calling the milestone done.

## 5. Keep The Goal Current

After each ticket, update the goal state.
Track which tickets are done, blocked, skipped, or still queued.

If new work appears while implementing a ticket, decide whether it belongs in the current ticket, a new ticket, or a blocker note.
Do not let the milestone sprawl without telling the user.

If the milestone becomes too large for one run, stop at a clean boundary.
Leave a resume note with the ticket queue, completed PRs, blockers, and the recommended next ticket.

## 6. Close The Milestone Run

When the queue is empty, review the milestone as a whole.
Check that every ticket has either a PR or a blocker.
Look for duplicated work, missing dependency order, and PRs that need follow-up.

End with a milestone report.
Include the goal status, completed PRs, blocked tickets, checks run, risks, and the next human decision needed.

If every ticket has a PR and no blockers remain, say the milestone workflow is complete.
