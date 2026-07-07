# Installation

These workflows are plain Markdown.
Install them by copying or symlinking the files in `runbooks/` into the directory your coding agent reads.

## Neo

Neo loads prompt commands from:

- project: `.neo/commands/*.md`
- user: `~/.neo/commands/*.md`

Project install:

```bash
mkdir -p .neo/commands
cp /path/to/workflows/runbooks/*.md .neo/commands/
```

User install:

```bash
mkdir -p ~/.neo/commands
cp /path/to/workflows/runbooks/*.md ~/.neo/commands/
```

Invoke:

```text
/ticket-to-pr Fix the login redirect bug
```

## Claude Code

Claude Code still supports `.claude/commands/*.md`.
Current Claude Code documentation says custom commands have been merged into skills, and existing `.claude/commands/` files keep working.

Slash-command install:

```bash
mkdir -p .claude/commands
cp /path/to/workflows/runbooks/*.md .claude/commands/
```

Skill install:

```bash
mkdir -p .claude/skills/ticket-to-pr
cp /path/to/workflows/runbooks/ticket-to-pr.md .claude/skills/ticket-to-pr/SKILL.md
```

Invoke:

```text
/ticket-to-pr Fix the login redirect bug
```

## Codex

Current Codex documentation marks custom prompts as deprecated and recommends skills for reusable instructions and workflows.

Project install:

```bash
mkdir -p .agents/skills/ticket-to-pr
cp /path/to/workflows/runbooks/ticket-to-pr.md .agents/skills/ticket-to-pr/SKILL.md
```

User install:

```bash
mkdir -p ~/.agents/skills/ticket-to-pr
cp /path/to/workflows/runbooks/ticket-to-pr.md ~/.agents/skills/ticket-to-pr/SKILL.md
```

Invoke explicitly by mentioning the skill, or let Codex invoke it when the task matches the description.

## Symlink Install

Symlinks make local iteration easier.

```bash
mkdir -p ~/.neo/commands
ln -s /path/to/workflows/runbooks/ticket-to-pr.md ~/.neo/commands/ticket-to-pr.md
```

Use symlinks only when your agent supports them and your team is comfortable with the target path.

## Notes

- Slash commands are best for explicit user-driven workflows.
- Skills are best when the agent should discover and invoke the workflow from the task description.
- Keep the canonical content in `runbooks/`.
- Add adapter docs when an agent needs special frontmatter, placeholders, or packaging.
