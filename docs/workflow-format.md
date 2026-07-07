# Workflow Format

A workflow is a runbook for a recurring agent job.

It should be usable as:

- a plain prompt
- a slash command
- a skill body
- a reference for a more advanced orchestrator

## Frontmatter

Use simple metadata:

```yaml
---
name: ticket-to-pr
description: Take a scoped engineering task from clean start to tested pull request.
argument-hint: "<ticket URL, issue number, or task description>"
---
```

The `name` should be short and command-friendly.
The `description` should start with the trigger use case.
The `argument-hint` should show the minimum useful input.

## Body

Use this structure:

```md
# Name

Run the workflow for:

{{args}}

If your agent uses `$ARGUMENTS` instead of `{{args}}`, treat `$ARGUMENTS` as the task input.

## Purpose

## Use When

## Inputs

## Guardrails

## Process

## Required Evidence

## Stop If

## Final Report
```

## Writing Rules

- Prefer verbs over vague guidance.
- Use ordered steps for the main process.
- Make stop conditions concrete.
- Require evidence, not confidence.
- Keep implementation-specific commands out unless they are broadly expected.
- Put agent-specific syntax in install docs when possible.
