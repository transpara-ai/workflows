# Agent Instructions

Be concise and practical.
Use simple words.
Do not use em dashes.

This repository contains reusable agent workflows.
Treat files in `runbooks/` as the canonical source.

When editing a workflow:

- keep the runbook agent-agnostic where possible
- include trigger conditions, inputs, guardrails, process, evidence, and final report
- avoid platform-specific tool names unless the workflow has an adapter section
- do not hide risky behavior behind vague wording
- keep stop conditions explicit
- prefer commands users can adapt over hardcoded project assumptions

When adding install guidance, prefer documented agent behavior and link to primary docs.
