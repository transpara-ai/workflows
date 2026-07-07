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

Use a guide structure, not a checklist of metadata sections.

````md
# Name

Use this workflow when...

Task:

```text
{{args}}
```

If your agent uses `$ARGUMENTS`, use that as the task instead.

## 1. Start With...

Explain what the agent should do first and what decision it should make.

## 2. Do The Next Thing

Explain the next action in plain language.

## 3. Prove The Result

## Final Report
````

## Writing Rules

- Prefer verbs over vague guidance.
- Write the workflow as a step-by-step guide.
- Avoid making the whole file a bullet list.
- Make stop conditions concrete.
- Require evidence, not confidence.
- Keep implementation-specific commands out unless they are broadly expected.
- Put agent-specific syntax in install docs when possible.
