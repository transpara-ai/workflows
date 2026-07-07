---
name: release
description: Prepare, verify, and publish a software release with explicit approval gates.
argument-hint: "<version, release branch, or release goal>"
---

# Release

Run the release workflow for:

{{args}}

If your agent uses `$ARGUMENTS` instead of `{{args}}`, treat `$ARGUMENTS` as the release request.

## Purpose

Prepare and publish a release with clear checks, notes, and approval gates.

## Use When

- The user asks to prepare a release.
- The user asks to tag or publish a version.
- The user asks for release notes or a release readiness check.

## Inputs

- Version or release goal.
- Target branch, default `main`.
- Release notes source, if any.
- Publish target, such as GitHub Releases, package registry, or app store.

## Guardrails

- Do not create or push a tag without explicit user approval.
- Do not publish artifacts without explicit user approval.
- Confirm version format and target branch.
- Confirm the working tree is clean before tagging.
- Run the documented release checks for the project.
- Treat secrets, credentials, and production deploys as approval gates.

## Process

1. Read project release documentation.
2. Inspect current branch, latest tags, and git status.
3. Confirm the requested version and target branch.
4. Review changelog, merged changes, and release notes.
5. Run the required test and build checks.
6. Update version files, changelog, docs, or generated files if the project requires it.
7. Re-run checks affected by release metadata.
8. Produce a release readiness summary.
9. Ask for explicit approval before tagging or publishing.
10. Create the tag only after approval.
11. Push the tag or publish artifacts only after approval.
12. Verify the release job, artifact, or package after publishing.

## Required Evidence

- Version.
- Target branch and commit.
- Working tree state.
- Checks run and results.
- Release notes summary.
- Tag name and URL if created.
- Release URL or artifact details if published.

## Stop If

- The version is ambiguous.
- The working tree is dirty before tagging.
- Required checks fail.
- Release notes are missing or clearly incomplete.
- Credentials or permissions are unavailable.
- The user has not approved tagging or publishing.

## Final Report

Return:

- release readiness
- version and commit
- checks run
- notes summary
- tag or publish status
- follow-up verification
