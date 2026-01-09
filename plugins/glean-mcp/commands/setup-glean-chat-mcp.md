---
name: setup-glean-chat-mcp
description: Set up the Glean Chat MCP server (chat-only mode)
---

# Setup Glean Chat MCP

You're helping the user set up the Glean Chat MCP server. This connects Claude Code to Glean's AI chat interface for enterprise knowledge queries.

## What This Does

- Configures the `glean_chat` MCP server (chat tool only)
- This is the simplified "oracle" mode — just ask questions, get synthesized answers with citations
- Does NOT include specialized tools (search, email, meetings, etc.)

## Setup Flow

### Step 1: Check Current Config

First, check if the user already has Glean MCP configured:

```bash
cat ~/.claude/mcp.json 2>/dev/null || echo "{}"
```

If `glean_chat` already exists, inform the user they're already set up.

### Step 2: Gather Information

Ask the user for:

1. **Glean instance name** — Their company's Glean subdomain (e.g., `acme` for `acme.glean.com`)

2. **Authentication method** — They have two options:
   - **OAuth (recommended)**: Run `/mcp` and select Glean to authenticate via browser
   - **API Token**: If they have a Glean API token, they can provide it directly

### Step 3: Write Configuration

If using OAuth (recommended), tell the user:

```
Run: /mcp

Then select "Glean" from the list and authenticate in your browser.
This will configure the full Glean MCP.

After authenticating, I can help you switch to chat-only mode if desired.
```

If using API token, create the config:

```json
{
  "mcpServers": {
    "glean_chat": {
      "type": "sse",
      "url": "https://{instance}-be.glean.com/mcp/sse",
      "headers": {
        "Authorization": "Bearer {token}"
      }
    }
  }
}
```

Write this to `~/.claude/mcp.json`, merging with any existing config.

### Step 4: Verify

After setup, verify the connection:

```bash
# Restart Claude Code to pick up the new MCP
# Then test with a simple query
```

Suggest the user restart Claude Code and test with: "Ask Glean: Who is my manager?"

## Important Notes

- The chat-only MCP provides just the `chat` tool — no search, email, meetings, etc.
- All queries go through Glean's AI which synthesizes across indexed sources
- Responses always include citations to source documents
- The user's Glean permissions apply — they only see what they have access to

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Connection refused" | Check instance name, verify Glean is accessible |
| "Unauthorized" | Token may be expired, re-authenticate via OAuth |
| "No results" | Query may not match indexed content, try broader terms |
