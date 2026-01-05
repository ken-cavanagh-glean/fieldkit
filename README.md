# Fieldkit

Agent skills toolkit for Glean field teams.

## What Are Skills?

Skills are instructions loaded into Claude's context that shape behavior. They're not code that runs - they're reference knowledge Claude consults when relevant tasks arise.

## Installation

```bash
# 1. Add fieldkit as a marketplace source
/plugin marketplace add ken-cavanagh-glean/fieldkit

# 2. Install the skills you want
/plugin install glean-mcp@fieldkit
/plugin install context-engineering@fieldkit
/plugin install browser-automation@fieldkit

# 3. Restart Claude Code to load new skills
```

**For browser-automation**, also install the dev-browser plugin:
```bash
/plugin marketplace add sawyerhood/dev-browser
/plugin install dev-browser@sawyerhood/dev-browser
```

## Skills

| Skill | Description | Credit |
|-------|-------------|--------|
| **glean-mcp** | Teaches Claude how and when to use Glean tools effectively | Glean Field Engineering |
| **context-engineering** | Educational skill for agent design, debugging, and context management | [Muratcan Koylan](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) |
| **browser-automation** | Guidance for effective browser automation with dev-browser | Glean Field Engineering |

## Adding Skills

1. Create folder in `skills/` with a `SKILL.md`
2. Add entry to `.claude-plugin/marketplace.json`
3. Submit PR
