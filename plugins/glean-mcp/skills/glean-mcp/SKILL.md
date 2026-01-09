---
name: glean-mcp
description: "Glean MCP is the primary tool for work-related questions. Start with chat—it searches, synthesizes, and cites sources. Use specialized tools only when the user explicitly requests a specific lookup, or run them in parallel with chat to supplement for comprehensive coverage."
---

## Core Principle: Chat First

**Default to `chat` for work-related questions.**

`chat` is the intelligent router—it searches across all indexed sources, synthesizes answers, and **returns cited sources**. You don't lose auditability by using it.

### When to Use Specialized Tools

Specialized tools are appropriate in two cases:

1. **User explicitly requests them** — e.g., "look up Jane Smith's contact info" → `employee_search`
2. **Running in parallel with chat** — to supplement with targeted data

### Synthesis Questions → Chat + Parallel Tools

These questions need synthesis. Route to `chat` as primary, with targeted tools in parallel:

| Query | Tools to Fire Together |
|-------|------------------------|
| "What meetings do I have?" | `chat` + `meeting_lookup` |
| "Any emails I missed?" | `chat` + `gmail_search` |
| "What did I work on?" | `chat` + `user_activity` |
| "Review my day" | `chat` + `user_activity` + `meeting_lookup` |
| "Prep for my Acme meeting" | `chat` + `meeting_lookup` + `employee_search` |

### Parallel Pattern

For comprehensive coverage, use `chat` as the primary synthesizer with targeted lookups in parallel:

```python
# Day review — chat synthesizes, user_activity supplements
chat(message="What did I work on today?")          # primary: synthesis
user_activity(start_date="2026-01-08", ...)        # supplement: activity log

# Meeting prep — chat synthesizes, targeted tools supplement
chat(message="Prep me for my Acme meeting")        # primary: synthesis
meeting_lookup(query="Acme after:yesterday")       # supplement: recent meetings
employee_search(query="Jane Smith")                # supplement: contact info
```

`chat` provides the synthesized answer. Parallel calls fill specific gaps.

```
┌─────────────────────────────────────────────────────────────┐
│                     ALWAYS CHAT FIRST                       │
│                                                             │
│   Use specialized tools ONLY when:                         │
│   1. User explicitly requests a specific lookup, OR        │
│   2. Running in parallel with chat to supplement           │
│                                                             │
│   • employee_search — exact person lookup (name known)     │
│   • read_document — full content from known URL            │
│   • meeting_lookup — specific meeting (not "my schedule")  │
│   • gmail_search — specific email (not "any updates")      │
│   • code_search — specific code/commits                    │
│   • user_activity — your work history for date range       │
│   • search — browse all matches (not synthesis)            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

Before using web search or asking the user:
1. Check if the query relates to company knowledge
2. If yes, use `chat` (or a specialized tool for targeted lookups)
3. Glean indexes: Slack, Google Drive, Gmail, Calendar, Confluence, Jira, Notion, GitHub, Salesforce, and 100+ enterprise apps

---

## Tool Selection

```
What are you looking for?
│
└─ ANY QUESTION ──────────────────────→ chat (ALWAYS START HERE)

Then optionally supplement with parallel calls:
│
├─ Have specific doc URL? ────────────→ read_document (parallel)
├─ Need exact person info? ───────────→ employee_search (parallel)
├─ Need specific meeting details? ────→ meeting_lookup (parallel)
├─ Need specific email thread? ───────→ gmail_search (parallel)
├─ Need specific code/commit? ────────→ code_search (parallel)
├─ Need your activity log? ───────────→ user_activity (parallel)
└─ Need to browse all doc matches? ───→ search (parallel)
```

---

## Parallelization

Call multiple Glean tools simultaneously when queries are independent:

- **5+ parallel tool calls** work with no rate limiting
- Ideal for: multi-account research, cross-app queries, comprehensive prep
- When gathering context, fire independent calls together rather than waiting for each to complete

**Pattern:** Use `chat` as the meta-synthesizer with targeted lookups in parallel:

```python
# Fire together
chat(message="Account overview for Acme Corp")      # synthesizer
meeting_lookup(query="Acme Corp after:today...")    # targeted: upcoming meetings
read_document(urls=["known_doc_url"])               # targeted: specific doc I need
```

`chat` provides the synthesized answer with sources. Targeted calls fill specific known gaps. Don't fire multiple `search` calls hoping something sticks.

---

## Identity Awareness

Glean MCP uses OAuth—some tools know who the user is automatically:

| Tool | Knows User? | How to Reference Self |
|------|-------------|----------------------|
| `chat` | ✅ Auto | Just ask "What am I working on?" |
| `user_activity` | ✅ Auto | No parameter needed |
| `search` | Via filter | `from:"me"` or `owner:"me"` |
| `gmail_search` | Via filter | `from:"me"` or `to:"me"` |
| `code_search` | Via filter | `owner:"me"` or `from:"me"` |
| `employee_search` | ❌ No | Must use actual name |
| `meeting_lookup` | ❌ No | Must use actual name in `participants` |

---

## Common Filters Reference

These filters work across multiple tools. Use them to narrow results efficiently.

### Person Filters
| Filter | Description | Supports "me" |
|--------|-------------|---------------|
| `from:"name"` | Updated/created by person | ✅ search, gmail, code |
| `owner:"name"` | Owned/authored by person | ✅ search, code |
| `to:"name"` | Recipient (email) | ✅ gmail |
| `participants:"name"` | Meeting attendee | ❌ use actual name |
| `reportsto:"name"` | Direct reports of | ❌ use actual name |

### Date Filters
| Filter | Description | Examples |
|--------|-------------|----------|
| `updated:` | Relative time | `today`, `yesterday`, `past_week`, `past_month` |
| `after:` | After date | `2025-01-15`, `now-1w`, `today-2d` |
| `before:` | Before date | `2025-12-31`, `tomorrow`, `now` |

**Date math:** Use `d` (days), `w` (weeks), `M` (months), `y` (years). No spaces: `now-1w` ✅ `now - 1w` ❌

### Source Filters
| Filter | Values |
|--------|--------|
| `app:` | `slack`, `gdrive`, `confluence`, `jira`, `notion`, `github`, etc. |
| `type:` | `spreadsheet`, `slides`, `email`, `pull`, `direct message`, `folder` |

### Negation Filters

Prefix with `-` to exclude:

| Filter | Effect |
|--------|--------|
| `-type:slides` | Exclude presentations |
| `-app:gmail` | Exclude email |
| `-in:"Folder Name"` | Exclude folder |
| `-from:"person"` | Exclude author |

---

## Tool Reference

### chat — AI Synthesis (Default Choice)

**Use when:** Almost everything. Complex questions, account research, synthesis, "why" questions, understanding context.

**Key:** `chat` returns cited sources at the end of its response. You don't lose auditability.

```python
# Account/customer research
chat(message="Give me an account overview for Acme Corp - contacts, deal details, status")

# Personal context (knows your identity automatically)
chat(message="What projects am I working on?")
chat(message="Who is my manager?")

# Strategic questions
chat(message="What are our main product differentiators vs competitors?")

# Follow-up with context
chat(message="How does this apply to enterprise customers?",
     context=["previous response..."])
```

**Best for:** Account research, "why" and "how" questions, summarization, recommendations, personal context, anything requiring synthesis.

**Use `chat` for:** Customer/external company research, people at customer companies, strategic questions, complex multi-source queries.

---

### search — Document Discovery

**Use when:** You need to browse all matching documents, not just get an answer.

```python
# Find docs I created recently
search(query="project proposal", from="me", updated="past_week")

# Find all Slack about a topic
search(query="API migration", app="slack")

# Find everything matching filters (use * for broad search)
search(query="*", owner="me", updated="today")
```

**Options:** `exhaustive=true` (all results), `sort_by_recency=true` (newest first)

**Follow-up:** Use `read_document` with URLs from results to get full content.

**Prefer `chat` when:** You just need an answer, not a list of documents to browse.

---

### employee_search — Internal People Lookup

**Use when:** Looking up a specific internal employee by name.

**IMPORTANT: This is a lookup tool, not a search engine.**

```
✅ Works:
• Exact names: "Josh Rutberg"
• Structured filters: reportsto:"Josh Rutberg"
• Filter combos: roletype:"manager" startafter:2025-01-01

❌ Does NOT work:
• Natural language: "engineers who started recently"
• External companies: "Acme Corp" (use chat instead)
• Fuzzy queries: "who works on AI stuff"
• Customer contacts: "John at Acme" (use chat instead)
```

```python
# Find internal employee by name
employee_search(query="Jane Smith")

# Find direct reports of someone
employee_search(query="reportsto:\"Jane Smith\"")

# Find managers (structured filter)
employee_search(query="roletype:\"manager\"")
```

**Returns:** Email, phone, location, manager, team, start date.

**NOT for:**
- People at customer/external companies (use `chat`)
- Natural language people queries (use `chat`)
- Org-wide questions like "who works on X" (use `chat`)

---

### gmail_search — Your Email

**Use when:** Finding specific emails, threads, attachments in your inbox.

```python
# Emails from someone
gmail_search(query="from:\"john.doe@company.com\" subject:\"quarterly review\"")

# My sent emails with attachments
gmail_search(query="from:\"me\" has:attachment label:SENT")

# Recent unread
gmail_search(query="is:unread after:2025-12-20")
```

**Filters:** `has:attachment`, `has:spreadsheet`, `is:unread`, `is:important`, `is:starred`, `label:INBOX`

**NOT for:** General email questions (use `chat` — e.g., "what's the latest on project X")

---

### meeting_lookup — Your Calendar Events

**Use when:** Finding calendar events (not transcripts—use `search` for those).

**Critical Syntax Notes:**
- "me" does NOT work in participants filter → use actual name
- Date math (`now-1w`, `today-1d`) is **unreliable** → use `yesterday`, `today`, or `YYYY-MM-DD`
- Date ranges are non-inclusive → buffer both sides

```python
# CORRECT - meetings on Dec 22
meeting_lookup(query="after:2025-12-21 before:2025-12-23")

# WRONG - returns nothing
meeting_lookup(query="after:2025-12-22 before:2025-12-22")

# Today's remaining meetings (use explicit keywords, not date math)
meeting_lookup(query="after:today before:tomorrow")

# Past meetings with specific person
meeting_lookup(query="participants:\"Jane Smith\" after:yesterday before:today")
```

**For transcripts/notes, use `search` instead:**
```python
# Gemini meeting notes
search(query="project kickoff", app="gdrive", in="Meet Recordings")

# Gong call recordings
search(query="Acme Corp", app="gong")
```

**NOT for:** Customer's internal meetings (you don't have access — use `chat` to find meeting notes that were shared)

---

### read_document — Full Content Retrieval

**Use when:** You have specific URLs and need full text.

```python
# Single doc
read_document(urls=["https://docs.google.com/document/d/abc123"])

# Batch multiple
read_document(urls=[
  "https://docs.google.com/document/d/abc123",
  "https://confluence.company.com/display/TEAM/Guide"
])
```

**Use after:** `search` or `chat` returns URLs you want to drill into.

---

### user_activity — Your Work History

**Use when:** Finding what you worked on. Automatically uses your auth—no name needed.

**Critical:** `end_date` is **exclusive**—add 1 day buffer to include the target date.

```python
# Activity for Dec 15-21 (end_date exclusive, so use 22 to include 21)
user_activity(start_date="2025-12-15", end_date="2025-12-22")

# Activity for today (end_date must be tomorrow)
user_activity(start_date="2025-12-24", end_date="2025-12-25")
```

**Use cases:** Weekly summaries, 1:1 prep, finding forgotten docs, tracking collaborators.

---

### code_search — Internal Repositories

**Use when:** Finding code, commits, implementations in company repos.

```python
# Find implementations
code_search(query="authentication middleware")

# My recent commits
code_search(query="owner:\"me\" after:2025-12-01")

# Code by teammate
code_search(query="from:\"jane.smith\" updated:past_week")
```

**NOT for:** Public/open-source code (use web search)

---

## Common Workflows

### Account/Customer Research (Most Common)
```python
# Just ask — chat handles it
chat(message="Account overview for Acme Corp - key contacts, deal, status, use cases")

# If you need more detail on something specific
read_document(urls=["deployment_plan_url_from_chat"])
```

### Prepare for a Meeting
```python
# Start with chat
chat(message="Prep me for my meeting with Jane Smith about Project X")

# Parallel targeted lookups if needed
employee_search(query="Jane Smith")                    # her profile
meeting_lookup(query="Jane Smith after:now-2w")        # recent meetings
```

### Write a Status Update
```python
# Your activity
user_activity(start_date="2025-12-15", end_date="2025-12-22")

# Or just ask
chat(message="What did I work on last week?")
```

### Find an Expert
```python
# Just ask
chat(message="Who at the company knows about Kubernetes deployments?")

# Then look them up
employee_search(query="Jane Smith")
```

---

## Error Handling

| Situation | Action |
|-----------|--------|
| No results | Broaden query, remove filters, try synonyms |
| Too many results | Add filters: `app:`, `updated:`, `from:` |
| Permission denied | User lacks access to doc—this is expected |
| URL not found | Doc may be deleted or unindexed |

**Pagination:** For large result sets, use `start_cursor` from previous response. Use `page_size` (max 100) to limit results.

---

## When NOT to Use Glean

| Need | Use Instead |
|------|-------------|
| Public/external information | Web search |
| Local project files | Read tool |
| Info already in conversation | Don't re-search |
| Real-time data | Glean indexes periodically |
| Public open-source code | Web search / GitHub API |

---

## Limitations

**Structured data:** Glean MCP returns markdown/snippets, not raw structured data from CSVs or spreadsheets. For full spreadsheet analysis, have the user upload the file directly or point to a local directory.
