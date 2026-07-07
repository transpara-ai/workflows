# Workflow Format

A workflow is a runbook that turns a clear input into a valuable output.

Examples:

- ticket to high quality PR
- milestone to completed PRs

If the file only teaches the agent to perform one step well, it is probably a skill.

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

Input: ...
Output: ...

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
- State the input and output near the top.
- Write the workflow as a step-by-step guide.
- Avoid making the whole file a bullet list.
- Make stop conditions concrete.
- Require evidence, not confidence.
- Keep implementation-specific commands out unless they are broadly expected.
- Put agent-specific syntax in install docs when possible.
