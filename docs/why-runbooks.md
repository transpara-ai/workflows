# Why Runbooks

Skills are popular because they package repeatable knowledge.
That is useful, but it does not fully solve repeated engineering process.

## The Difference

A skill says:

```text
Here is how to do this capability well.
```

A runbook says:

```text
When this situation happens, run this process from start to finish.
```

For coding agents, that distinction matters.

## Skills Are Good For

- review technique
- browser verification
- commit message conventions
- framework-specific implementation guidance
- writing tests in a project style
- using a tool or API correctly

## Runbooks Are Good For

- ticket to PR
- fixing CI
- release
- incident-style debugging
- dependency updates
- safe refactors
- code review

## Why Not Just Make A Workflow Skill

You can.
The file format can be the same.

The argument for a separate concept is that the promise is different.

A workflow or runbook should own:

- trigger conditions
- prerequisites
- ordered steps
- gates
- stop conditions
- evidence
- final handoff

If everything is called a skill, the list mixes capabilities and full jobs.
That makes discovery weaker and hides the operational contract.

The better model:

```text
Workflows orchestrate skills.
Skills improve steps inside workflows.
```

## What Good Looks Like

A good runbook makes the agent boringly consistent.

It should reduce:

- skipped tests
- unclear branch state
- weak self-review
- missing PR context
- repeated setup instructions
- unsafe release actions

It should increase:

- clear setup
- explicit gates
- better stopping behavior
- handoff quality
- repeatable final reports
