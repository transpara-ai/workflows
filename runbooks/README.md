# Runbooks

These are the canonical workflow files.

Each file is designed to work as a plain prompt, a slash command, or the body of an agent skill.
Keep them portable unless a platform-specific adapter is clearly needed.

## Shape

Each runbook should read like a guide.
It should take the agent from the start of the job to the final report in ordered steps.
The best test is input to output.
If the file does not transform a clear input into a valuable output, it is probably a skill or helper prompt instead of a workflow.

## Included

- `ticket-to-pr.md`
- `milestone.md`
