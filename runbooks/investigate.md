---
name: investigate
description: Diagnose an unclear bug or technical question before implementing a fix.
argument-hint: "<bug report, symptom, or investigation question>"
---

# Investigate

Run the investigation workflow for:

{{args}}

If your agent uses `$ARGUMENTS` instead of `{{args}}`, treat `$ARGUMENTS` as the investigation target.

## Purpose

Understand a problem well enough to recommend a fix, write a repro, or decide no change is needed.

## Use When

- The user asks why something is happening.
- The bug report is unclear.
- The right fix is not known yet.
- A change would be risky without diagnosis first.

## Inputs

- Symptom, bug report, trace, or question.
- Expected behavior.
- Environment details, if relevant.

## Guardrails

- Do not start with production edits.
- Separate facts from hypotheses.
- Prefer a small repro over broad speculation.
- Keep notes with file and command evidence.
- Ask only when missing information blocks progress.

## Process

1. Restate the question and expected output.
2. Gather repo guidance and relevant docs.
3. Inspect the code paths involved.
4. Search for related tests, issues, docs, and recent changes.
5. Build a minimal reproduction or reasoning path.
6. Form hypotheses and try to falsify them.
7. Identify the most likely root cause.
8. Recommend one or more fixes with tradeoffs.
9. If the fix is small and the user asked for implementation, proceed through the ticket workflow.
10. Otherwise stop with a clear investigation report.

## Required Evidence

- Files and code paths inspected.
- Commands run and results.
- Reproduction steps, if available.
- Confirmed facts.
- Hypotheses ruled out.
- Recommendation.

## Stop If

- The issue depends on unavailable production data.
- The issue cannot be reproduced and evidence is too weak.
- The likely fix has product or architecture implications that need approval.

## Final Report

Return:

- short answer
- evidence
- root cause or strongest hypothesis
- options
- recommended next step
