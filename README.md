# Fieldkit

Agent skills toolkit for Glean field teams.

**Current Version:** 2.0.0

## What Are Skills?

Skills are instructions loaded into Claude's context that shape behavior. They're not code that runs—they're reference knowledge Claude consults when relevant tasks arise.

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

---

## Changelog

### v1.1.1 (2026-01-08)

- Fixed plugin isolation issue where skills cross-contaminated between plugins
- Fixed YAML parsing error in glean-mcp description (unquoted colons)
- Improved marketplace.json description to encourage frequent Glean usage

### v1.1.0 (2026-01-07)

**glean-mcp skill rewrite:**

- **Chat First:** `chat` is now the default tool for almost everything. Previous versions treated `search` and `chat` as equals; now `chat` is the primary entry point.
- **Parallel Pattern:** Added "chat as meta-synthesizer" pattern for parallel calls.
- **employee_search clarification:** Explicitly documented as a lookup tool (exact names only), not a search engine. Natural language queries don't work.
- **NOT for sections:** Added explicit "NOT for" guidance to each specialized tool.
- **Removed Setup section:** Setup instructions moved elsewhere; skill now focuses on usage patterns.

**Migration:** If you have workflows that default to `search`, they'll still work but may be suboptimal. Prefer `chat` for synthesis/analysis, use `search` only when you need to browse all matching documents.

### v1.0.0 (2025-12-xx)

Initial release with glean-mcp, context-engineering, and browser-automation skills.
