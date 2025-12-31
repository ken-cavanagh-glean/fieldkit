# Fieldkit

Agent skills toolkit for Glean field teams.

## What Are Skills?

Skills are instructions loaded into Claude's context that shape behavior. They're not code that runs - they're reference knowledge Claude consults when relevant tasks arise.

## Installation

```bash
# Add fieldkit as a marketplace source
/plugin marketplace add ken-cavanagh-glean/fieldkit

# Install skills
/plugin install glean-mcp@fieldkit
/plugin install context-engineering@fieldkit
```

Or copy manually to `~/.claude/skills/` or `.claude/skills/`.

## Skills

| Skill | Description | Credit |
|-------|-------------|--------|
| **glean-mcp** | Teaches Claude how and when to use Glean tools effectively | Glean Field Engineering |
| **context-engineering** | Educational skill for agent design, debugging, and context management | [Muratcan Koylan](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) |

## Adding Skills

1. Create folder in `skills/` with a `SKILL.md`
2. Add entry to `.claude-plugin/marketplace.json`
3. Submit PR
