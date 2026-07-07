# Agent Workflows

Reusable runbooks for professional software development with coding agents.

Most agent customization today is framed as skills.
Skills are useful, but they are usually about doing one thing well.
This repository is about the larger unit of work: the repeatable flow from trigger to evidence.

```text
Rules     = constraints that always apply
Skills    = reusable capabilities
Workflows = end-to-end runbooks for recurring jobs
```

## Why This Exists

Coding agents are getting better at individual tasks, but real engineering work still fails in boring places.
Agents skip setup, forget tests, review their own changes lightly, leave branches dirty, or need the same process explained again and again.

Workflows make that process explicit.

A workflow says:

- when to use it
- what inputs it needs
- what steps to follow
- what checks prove the work is done
- when to stop
- what evidence to report

That is closer to an engineering runbook than a prompt snippet.

## Workflows vs Skills

Skills teach an agent how to do something well.
Workflows tell an agent how to run a whole job well.

Examples:

| Concept | Example | Scope |
| --- | --- | --- |
| Skill | Review a diff for correctness | One capability |
| Skill | Verify a UI with a browser | One capability |
| Workflow | Take a ticket from idea to PR | Full job |
| Workflow | Fix failing CI | Full job |

The clean model is that workflows can call skills.
A `ticket-to-pr` workflow may use a review skill, a browser verification skill, and a commit skill.
The workflow owns the sequence, gates, and final evidence.

## Included Workflows

V1 starts with three workflows so the style can get sharp before the catalog grows.

| Workflow | Use when |
| --- | --- |
| [`ticket-to-pr`](runbooks/ticket-to-pr.md) | Implementing a scoped feature, bug fix, or ticket |
| [`review-change`](runbooks/review-change.md) | Reviewing a diff, branch, or PR without taking over implementation |
| [`fix-ci`](runbooks/fix-ci.md) | A test, build, lint, or CI check is failing |

Each workflow should read like a step-by-step guide.
It should tell the agent what to do next, when to stop, and what evidence to report.

## Install

The canonical files live in [`runbooks/`](runbooks).
V1 installation is intentionally simple: copy or symlink the Markdown files into the command or skill directory for your agent.

### Neo

Neo supports project and global prompt commands from `.neo/commands/*.md` and `~/.neo/commands/*.md`.

Project install:

```bash
mkdir -p .neo/commands
cp runbooks/*.md .neo/commands/
```

Global install:

```bash
mkdir -p ~/.neo/commands
cp runbooks/*.md ~/.neo/commands/
```

Then run, for example:

```text
/ticket-to-pr Fix the flaky checkout test
```

### Claude Code

Claude Code still supports `.claude/commands/*.md`, but current Claude Code docs describe custom commands as merged into skills.
For the slash-command experience, use:

```bash
mkdir -p .claude/commands
cp runbooks/*.md .claude/commands/
```

For the skills-style install, create one skill folder per workflow and copy the runbook to `SKILL.md`.

```bash
mkdir -p .claude/skills/ticket-to-pr
cp runbooks/ticket-to-pr.md .claude/skills/ticket-to-pr/SKILL.md
```

### Codex

Current Codex docs mark custom prompt slash commands as deprecated and recommend skills for reusable instructions and workflows.
Install these as skills:

```bash
mkdir -p .agents/skills/ticket-to-pr
cp runbooks/ticket-to-pr.md .agents/skills/ticket-to-pr/SKILL.md
```

Repeat for the workflows you want available in a project.
For a user-global install, use `~/.agents/skills/<name>/SKILL.md`.

## Project Labels

Suggested GitHub labels are in [`.github/labels.yml`](.github/labels.yml).
They make it easier to track whether an issue is about a runbook, adapter, documentation, or evaluation.
Repository description and topics are captured in [`.github/repository.yml`](.github/repository.yml) for tools that sync GitHub settings from code.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/workflow-format.md](docs/workflow-format.md).

## Design Principles

- Plain Markdown first.
- No platform lock-in.
- Runbooks should be readable by humans and agents.
- Every workflow should define stop conditions.
- Every workflow should end with evidence.
- Keep capability instructions in skills, not duplicated in every workflow.
- Prefer small, auditable workflows over giant autonomous pipelines.

## References

- [Claude Code skills docs](https://code.claude.com/docs/en/skills)
- [Claude Code commands docs](https://code.claude.com/docs/en/commands)
- [Codex skills docs](https://developers.openai.com/codex/skills)
- [Codex custom prompts deprecation](https://developers.openai.com/codex/custom-prompts)

## Status

Early v1.
The goal is to prove the shape before adding install scripts, generators, or agent-specific packages.

## License

MIT.
