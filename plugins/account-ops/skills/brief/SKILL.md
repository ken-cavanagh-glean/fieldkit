---
name: brief
description: "Get a pre-meeting briefing for any account. Usage: /brief {account name}. Returns checklist progress, hours remaining, last interaction, missed comms, and open to-dos."
---

# Account Briefing

Quick situational awareness before client calls. Combine local checklist with real-time Glean data.

## Usage

```
/brief Snap
/brief northbeam
/brief golden gate bridge
```

## Workflow

When invoked with an account name, execute these steps:

### Step 1: Parse Account Name

The account name is provided as the argument. Normalize it for file lookup (lowercase, spaces preserved for file paths).

### Step 2: Read Local Entity File

Read the entity file from `exo/entities/orgs/{account name}.md`:

```
Read: exo/entities/orgs/{account}.md
```

Extract:
- **Deployment Checklist** — count `[x]` vs `[ ]` items, identify next incomplete item
- **Deal table** — TCV, seats, package, region, dates, team members
- **Next Steps** — local to-do items
- **Risks** — known blockers
- **Context** — situational notes

### Step 3: Query Glean Account Status Agent

Run the agent query script to call the Account Status Agent directly via the Glean API:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/query_account_status.py "{account name}"
```

**Required environment variables:**
- `GLEAN_API_TOKEN` — API token for Glean
- `GLEAN_INSTANCE` — Glean instance (defaults to `scio-prod`)

The script returns JSON with:
```json
{
  "account": "Snap",
  "status": "...",
  "sources": [{"title": "...", "url": "..."}]
}
```

The agent returns:
1. **Last Meeting** — most recent calendar event with this customer + Gong summary
2. **Open To-Dos** — action items from meetings/emails since last interaction
3. **Missed Communications** — unanswered Slack/email since last meeting
4. **Internal Flags** — concerns flagged by AE/DEM/Support in internal channels
5. **Hours** — hours used vs. remaining from Rocketlane

**Agent ID:** `ccdc8e55722e48f98ef04d548f2b7e58`

### Step 4: Synthesize Briefing

Combine the data into a structured briefing:

```markdown
## [[{Account}]] Status Briefing

**Checklist Progress:** X/Y complete
- Last completed: {most recent [x] item}
- Next up: {first [ ] item} {(scheduled/not scheduled)}

**Hours:** {used}/{total} ({remaining} remaining)

**Last Interaction:** {date} {meeting title}
- {key points from Gong summary}

**Needs Attention:**
- {unread messages count and from whom}
- {pending emails}

**Risks/Notes:**
- {items from Risks section}
- {relevant context notes}

**Open To-Dos:**
- [ ] {from agent + local Next Steps}
```

## Checklist Parsing

The deployment checklist in entity files follows this structure:

```markdown
## Deployment Checklist

### Setup
- [x] Kickoff call completed
- [x] Client has launched Glean

### Enablement
- [ ] Enablement session scheduled
- [ ] Enablement session completed

### Success Planning
- [ ] Success planning workshop scheduled
- [ ] Success planning workshop completed

### Training
- [ ] Platform fundamentals training scheduled
- [ ] Platform fundamentals training completed
- [ ] Agent fundamentals training scheduled
- [ ] Agent fundamentals training completed
- [ ] Advanced Agents training scheduled
- [ ] Advanced Agents training completed

### Governance & Review
- [ ] Agent Governance Workshop completed
- [ ] First Quarterly Business Review completed
```

Count all items with `[x]` as completed, `[ ]` as pending.

## Entity File Locations

All account entity files live at:
```
exo/entities/orgs/{account name}.md
```

File names use lowercase with spaces (e.g., `golden gate bridge.md`, `snap.md`).

## Error Handling

- **File not found:** Report "No entity file found for {account}. Check exo/entities/orgs/"
- **No Glean data:** Report what's available from local file only
- **Partial data:** Always output what's available, note missing sections

---

*Part of account-ops plugin for fieldkit*
