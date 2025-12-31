# Fieldkit

Agent skills toolkit for Glean field teams. A Claude Code plugin marketplace providing enterprise search integration and context engineering best practices.

## How Skills Work

**Skills are not code that runs** - they're instructions loaded into Claude's context that shape behavior. Think of them as "reference docs Claude consults" rather than "functions that execute."

When you install a skill:
1. Claude sees the skill name + description (lightweight)
2. When a task matches, Claude reads and applies the full skill content
3. The skill influences Claude's reasoning and tool choices

### Two Types of Skills

| Type | Example | What It Does |
|------|---------|--------------|
| **Actionable** | `glean-mcp` | Direct guidance: "When X, do Y" - tells Claude which tools to use |
| **Educational** | `context-engineering` | Conceptual knowledge that shapes how Claude thinks about problems |

## Quick Start

### Installation via Claude Code Plugin Marketplace

```bash
# 1. Add fieldkit as a marketplace source
/plugin marketplace add ken-cavanagh-glean/fieldkit

# 2. Install the skills you need
/plugin install glean-mcp@fieldkit
/plugin install context-engineering@fieldkit
```

### Manual Installation

Copy skill folders to your Claude Code skills directory:

```bash
# Global installation
cp -r skills/glean-mcp ~/.claude/skills/
cp -r skills/context-engineering ~/.claude/skills/

# Or project-specific
cp -r skills/glean-mcp .claude/skills/
cp -r skills/context-engineering .claude/skills/
```

## Available Skills

### glean-mcp

**Use Glean MCP as the primary search and knowledge tool for enterprise context.**

Provides comprehensive guidelines for using Glean tools effectively:
- `search` - Document discovery with filters
- `chat` - AI-powered analysis and synthesis
- `code_search` - Internal code repository search
- `employee_search` - People and org chart queries
- `gmail_search` - Email discovery
- `meeting_lookup` - Calendar and transcript search
- `read_document` - Full document content retrieval

### context-engineering

**Educational skill for agent design, debugging, and effective LLM usage.**

This is a *conceptual* skill - it teaches Claude (and you!) how to think about context management. It doesn't tell Claude to use specific tools, but rather shapes how Claude reasons about problems.

**When it helps:**
- Designing or building agent systems
- Debugging weird agent behavior ("why is my agent forgetting things?")
- Understanding why long conversations degrade
- Making better use of tools like Glean (context-engineering explains *why* selective retrieval beats dumping all docs)

**What Claude learns:**

| Category | Skills | Key Concepts |
|----------|--------|--------------|
| **Foundational** | context-fundamentals, context-degradation, context-compression | "Lost-in-middle" effect, attention budgets, when context hurts |
| **Architectural** | multi-agent-patterns, memory-systems, tool-design | Sub-agents isolate context, file-system-as-memory pattern |
| **Operational** | context-optimization, evaluation, advanced-evaluation | Compaction triggers, LLM-as-judge, observation masking |

**How it complements glean-mcp:**
- Explains *why* Glean's selective search is better than stuffing context with docs
- Teaches the "WRITE-SELECT-COMPRESS-ISOLATE" framework that Glean tools support
- Helps debug when Glean queries return too much/too little

## Skill Structure

Each skill follows the Agent Skills specification:

```
skill-name/
├── SKILL.md              # Required: instructions + YAML frontmatter
├── scripts/              # Optional: executable code
└── references/           # Optional: additional documentation
```

## Adding New Skills

1. Create a new folder in `skills/`
2. Add a `SKILL.md` with YAML frontmatter:
   ```yaml
   ---
   name: your-skill-name
   description: Brief description of what the skill does
   ---
   ```
3. Update `.claude-plugin/marketplace.json` with the new skill entry
4. Submit a PR

## Credits

- **glean-mcp**: Glean Field Engineering
- **context-engineering**: Originally by [Muratcan Koylan](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering), adapted for fieldkit

## License

MIT License - see LICENSE file for details.
