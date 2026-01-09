# Fieldkit

Agent skills toolkit for Glean field teams.

**Current Version:** 3.0.0

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
| **glean-mcp** | Your work knowledge agent — ask Glean about company, accounts, colleagues, meetings, docs | Glean Field Engineering |
| **context-engineering** | Educational skill for agent design, debugging, and context management | [Muratcan Koylan](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) |
| **browser-automation** | Guidance for effective browser automation with dev-browser | Glean Field Engineering |

## Adding Skills

1. Create folder in `skills/` with a `SKILL.md`
2. Add entry to `.claude-plugin/marketplace.json`
3. Submit PR

---

## Changelog

### v3.0.0 (2026-01-09)

**Breaking change: Chat-only oracle mode**

This release fundamentally reimagines glean-mcp as a "Work Knowledge Agent" — an oracle for enterprise knowledge. Instead of teaching Claude to route between 7+ specialized tools, we now focus entirely on `chat` as the single interface.

**What changed:**
- **Rewrote SKILL.md** from 450 → 240 lines, focused on chat-only usage
- **New framing:** "Ask Glean" as a second-brain / oracle pattern (inspired by [steipete/oracle](https://github.com/steipete/oracle))
- **Removed tool routing:** No more specialized tools (search, email, meetings, etc.) — Glean orchestrates those under the hood
- **Removed hooks:** No longer enforcing chat-first routing (not needed when chat is the only tool)
- **New command:** `/setup-glean-chat-mcp` helps users configure the chat-only MCP server
- **Updated keywords:** `glean`, `enterprise-graph`, `company-search`, `people-search`, `work-activity`, `oracle`

**Why v3.0:** This is a philosophical shift. Previous versions taught Claude to be a Glean power user (pick the right tool). v3 treats Glean as an intelligent agent you simply ask questions to. Simpler, more reliable, better aligned with how Glean chat actually works.

**Migration:** If you have the full Glean MCP (with all tools), this skill still works — it just won't teach Claude about the specialized tools. For best results, switch to the chat-only MCP using `/setup-glean-chat-mcp`.

---

### v2.2.0 (2026-01-09)

- Added PreToolUse hook to enforce chat-first routing
- Hook intercepts specialized Glean tools (search, user_activity, meeting_lookup, etc.)
- Uses prompt-based hook to check if chat was already called
- Denies tool use if chat wasn't called first, with guidance to use chat as primary
- Created plugin.json for proper plugin structure

### v2.1.0 (2026-01-08)

- Added "Always start with chat" behavioral instruction to description
- Description now encodes routing behavior, not just activation triggers
- Positions skill as router: "Routes all Glean tool usage"
- Fixes issue where Claude skipped skill loading because MCP instructions felt sufficient

### v2.0.0 (2026-01-08)

**Breaking change: Skill trigger mechanism overhaul**

- Rewrote skill description from procedural guidance to explicit trigger patterns
- Skills are now opt-in: only `name` + `description` pre-loaded at startup; full SKILL.md loads when triggered
- New description activates on: meeting prep, day reviews, people lookup, email search, document discovery, activity tracking, and work context questions
- Reframed from "enterprise search" to "enterprise knowledge" — reflects inference over the graph, not just retrieval

**Why v2.0:** This fundamentally changes how the skill gets invoked. Previous versions assumed the skill was always loaded; now we optimize for the progressive disclosure model.

### v1.3.4 (2026-01-08)

- Expanded routing examples to show full parallel tool combinations
- Table format: "Review my day" → `chat` + `user_activity` + `meeting_lookup`

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
