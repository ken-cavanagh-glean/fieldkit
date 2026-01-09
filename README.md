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

### v1.3.3 (2026-01-08)

- Replaced anti-patterns (❌) with positive routing examples (✅)
- Semantic signals now reinforce chat association, not tool names

### v1.3.2 (2026-01-08)

- Added "Review my day" to anti-pattern examples
- Added day review example in parallel pattern section

### v1.3.1 (2026-01-08)

- Refined chat-first guidance with clearer "When to Use Specialized Tools" section
- Added critical syntax notes from AIOM playbook:
  - `meeting_lookup` date math (`now-1w`) is unreliable—use explicit dates
  - `user_activity` end_date is exclusive—add 1 day buffer
  - For transcripts, use `search` with `app:gdrive in:"Meet Recordings"` or `app:gong`
- Improved parallel pattern documentation
- Updated descriptions (Option A pair)

### v1.2.0 (2026-01-08)

- **Chat-first enforcement:** Rewrote SKILL.md to make chat-first mandatory, not suggested
- Added explicit "do NOT pattern-match" examples (e.g., "meetings" → meeting_lookup)
- Clarified specialized tools for explicit user requests OR parallel supplementation
- Updated Tool Selection flow to always start with chat

### v1.1.2 (2026-01-08)

- Improved marketplace.json description to clarify chat-first behavior and parallel tool usage

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
