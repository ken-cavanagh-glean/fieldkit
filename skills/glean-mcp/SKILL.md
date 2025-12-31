---
name: glean-mcp
description: Use Glean MCP as the primary search tool for enterprise context. Favor Glean over web search for company docs, people, meetings, emails, and internal knowledge.
---

## Setup

**Prerequisites:** Glean MCP server must be configured and authenticated. Tools will appear with `mcp__glean_*` prefix.

**Required tools:** `search`, `chat`, `employee_search`, `gmail_search`, `meeting_lookup`, `read_document`, `user_activity`, `code_search`

---

## Core Principle

**Glean MCP is the primary search tool for enterprise/company context.**

Before using web search or asking the user:
1. Check if the query relates to company knowledge
2. If yes, use the appropriate Glean tool
3. Glean indexes: Slack, Google Drive, Gmail, Calendar, Confluence, Jira, Notion, GitHub, and 100+ enterprise apps

---

## Tool Selection

```
What are you looking for?
│
├─ DOCUMENTS/CONTENT
│   ├─ Have URL? → read_document
│   ├─ Need analysis/synthesis? → chat
│   └─ Need to find docs? → search
│
├─ PEOPLE/ORG → employee_search
├─ MEETINGS/CALENDAR → meeting_lookup
├─ EMAIL → gmail_search
├─ CODE/REPOS → code_search
├─ MY RECENT WORK → user_activity
└─ COMPLEX QUESTION → chat
```

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

---

## Tool Reference

### search — Document Discovery

**Use when:** Finding documents, files, wikis, Slack messages by keywords.

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

---

### chat — AI Synthesis

**Use when:** Complex questions requiring analysis across multiple sources.

**Note:** Chat knows who you are automatically via auth. You can ask personal questions.

```python
# Personal context (knows your identity)
chat(message="What projects am I working on?")
chat(message="Who is my manager?")

# Strategic questions
chat(message="What are our main product differentiators vs competitors?")

# Follow-up with context
chat(message="How does this apply to enterprise customers?",
     context=["previous response..."])
```

**Best for:** "Why" and "how" questions, summarization, recommendations, personal context.

---

### employee_search — People Lookup

**Use when:** Finding people, org structure, contact info, team composition.

**Note:** "me" does NOT work here. Use actual names.

```python
# Find someone
employee_search(query="Jane Smith")

# Find direct reports
employee_search(query="reportsto:\"Jane Smith\"")

# Find new hires in a role
employee_search(query="engineer startafter:2025-01-01")

# Find managers
employee_search(query="roletype:\"manager\"")
```

**Returns:** Email, phone, location, manager, team, start date.

---

### gmail_search — Email Discovery

**Use when:** Finding emails, threads, attachments.

```python
# Emails from someone
gmail_search(query="from:\"john.doe@company.com\" subject:\"quarterly review\"")

# My sent emails with attachments
gmail_search(query="from:\"me\" has:attachment label:SENT")

# Recent unread
gmail_search(query="is:unread after:2025-12-20")
```

**Filters:** `has:attachment`, `has:spreadsheet`, `is:unread`, `is:important`, `is:starred`, `label:INBOX`

---

### meeting_lookup — Calendar & Transcripts

**Use when:** Finding meetings, getting transcripts, reviewing discussions.

**Note:** "me" does NOT work in participants filter. Use actual name.

**Important:** Date ranges are non-inclusive. Buffer both sides:

```python
# CORRECT - meetings on Dec 22
meeting_lookup(query="after:2025-12-21 before:2025-12-23")

# WRONG - returns nothing
meeting_lookup(query="after:2025-12-22 before:2025-12-22")
```

```python
# Today's remaining meetings
meeting_lookup(query="after:now before:tomorrow")

# Past meetings with transcripts
meeting_lookup(query="participants:\"Jane Smith\" extract_transcript:\"true\" after:now-2w")

# Topic search
meeting_lookup(query="topic:\"standup\" after:now-1w before:now")
```

---

### read_document — Full Content Retrieval

**Use when:** You have URLs from search and need full text.

```python
# Single doc
read_document(urls=["https://docs.google.com/document/d/abc123"])

# Batch multiple
read_document(urls=[
  "https://docs.google.com/document/d/abc123",
  "https://confluence.company.com/display/TEAM/Guide"
])
```

**Always use after search** to get complete content. Returns success/failure status per URL.

---

### user_activity — Your Work History

**Use when:** Finding what you worked on. Automatically uses your auth—no name needed.

```python
# Last week's activity
user_activity(start_date="2025-12-15", end_date="2025-12-22")

# This month
user_activity(start_date="2025-12-01", end_date="2025-12-24")
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

---

## Common Workflows

### Research a Topic
```
1. search(query="topic") → find docs
2. read_document(urls=[...]) → get full content
3. chat(message="Summarize...") → synthesize if needed
```

### Prepare for a Meeting
```
1. employee_search(query="attendee name") → understand who
2. search(query="topic", from="attendee") → their recent work
3. meeting_lookup(query="participants:\"attendee\"") → past meetings
```

### Write a Status Update
```
1. user_activity(start_date, end_date) → your work
2. meeting_lookup(query="after:X before:Y") → meetings attended
3. search(query="*", from="me", updated="past_week") → docs touched
```

### Find an Expert
```
1. search(query="topic") → find relevant docs
2. Note the owners/authors
3. employee_search(query="author name") → get their info
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
