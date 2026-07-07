# Contributing

Thanks for improving Agent Workflows.

This repo is about reusable runbooks for coding agents.
Keep contributions small, clear, and easy to adapt.

## Add A Workflow

Add new canonical workflows to `runbooks/`.

A workflow should include:

- purpose
- use when
- inputs
- guardrails
- process
- required evidence
- stop conditions
- final report

Good workflows are specific enough to change agent behavior, but not so specific that they only work in one codebase.

## Add Agent Support

Put agent-specific guidance in `docs/installation.md` or a focused adapter doc.

Use primary docs when possible.
If behavior is based on local testing rather than docs, say so.

## Review Bar

Before opening a PR:

- check for clear wording
- check that the workflow has evidence and stop conditions
- avoid broad platform claims without sources
- avoid duplicating capability guidance that belongs in skills
