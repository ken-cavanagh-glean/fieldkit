# Glean Agent Tools Catalog

Complete reference of tools and actions available in Glean Agent Builder.

---

## Core Tools

Built-in tools always available in Agent Builder.

### Glean Search

Enterprise search across all connected apps.

```json
{
  "id": "Glean Search",
  "inputTemplate": [
    { "template": "[[query]] app:gong" }
  ],
  "gleanSearchConfig": {
    "numResults": 30,
    "enableFullDocumentSnippets": true
  }
}
```

**Search Operators:**

| Operator | Example | Description |
|----------|---------|-------------|
| `app:` | `app:gong` | Filter by data source |
| `from:` | `from:me` | Filter by sender |
| `to:` | `to:me` | Filter by recipient |
| `mentions:` | `mentions:me` | Content mentioning user |
| `participants:` | `participants:me` | Meetings with user |
| `type:` | `type:ticket` | Filter by document type |
| `updated:` | `updated:past_day` | Filter by recency |
| `in:` | `in:"Meet Recordings"` | Filter by folder |

**App Names:**

```
gong, slack, gmail, googlecalendar, gdrive, salescloud,
confluence, jira, zendesk, notion, github, asana
```

---

### Glean Document Reader

Read full content of specific documents.

```json
{
  "id": "Glean Document Reader",
  "documentReaderConfig": {},
  "customisationData": {
    "skipUserInteraction": true
  }
}
```

Use when you have a specific document URL or need to read files referenced by search results.

---

### Respond

Generate the final response to the user.

```json
{
  "id": "Respond",
  "respondConfig": {
    "temperature": "FACTUAL"
  },
  "customisationData": {
    "skipUserInteraction": true
  }
}
```

**Temperature Values:**

| Value | Use Case |
|-------|----------|
| `FACTUAL` | Precise, source-based responses |
| `BALANCED` | General-purpose responses |
| `CREATIVE` | Open-ended, creative content |

---

### Think

Intermediate reasoning step (output not shown to user).

```json
{
  "id": "Think",
  "thinkConfig": {
    "temperature": "FACTUAL"
  },
  "customisationData": {
    "skipUserInteraction": true
  }
}
```

Use for:
- Intermediate analysis before final response
- Extracting/transforming data between steps
- Boolean evaluations for branching

---

### Data Analysis

Process structured data (CSVs, tables, JSON).

```json
{
  "name": "Data Analysis"
}
```

Best with `GEMINI_3_0` model for large datasets:

```json
{
  "modelOptions": {
    "llmConfig": {
      "provider": "VERTEX_AI",
      "model": "GEMINI_3_0"
    }
  }
}
```

---

### Internal Csv Splitter

Split CSV/list into array for looping.

```json
{
  "id": "Internal Csv Splitter",
  "name": "Internal Csv Splitter",
  "inputTemplate": [
    { "template": "[[previous-step-output]]" }
  ]
}
```

Used with `loopConfig` to iterate over items.

---

### User Activity Retrieve

Get user's recent activity.

```json
{
  "id": "User Activity Retrieve",
  "inputTemplate": [
    { "template": "duration_days: 14" }
  ],
  "customisationData": {
    "skipUserInteraction": true
  }
}
```

---

## Web Search

### Google Gemini Web Search

Search the public web.

```json
{
  "name": "googlegeminiwebsearch"
}
```

Use for:
- Company research
- Public information
- News and current events

---

## Google Workspace Actions

### Gmail

| Action | Name |
|--------|------|
| Draft Email | `googledraftemail` |
| Send Email | `googlesendmail` |
| Read Email | `googlereadmail` |

```json
{
  "instructionTemplate": "Draft an email to [[Contact]] about [[Topic]]",
  "toolConfig": [{ "name": "googledraftemail" }]
}
```

### Google Docs

| Action | Name |
|--------|------|
| Create Doc | `creategdoc` |
| Update Doc | `updategdoc` |
| Read Doc | `readgdoc` |

```json
{
  "instructionTemplate": "Create a Google Doc titled '[[Title]]' with the report content",
  "toolConfig": [{ "name": "creategdoc" }]
}
```

### Google Sheets

| Action | Name |
|--------|------|
| Create Sheet | `creategsheet` |
| Update Sheet | `updategsheet` |
| Read Sheet | `readgsheet` |

### Google Calendar

| Action | Name |
|--------|------|
| Create Event | `creategcalevent` |
| Update Event | `updategcalevent` |
| Read Events | `readgcalendar` |

### Google Drive

| Action | Name |
|--------|------|
| Create Folder | `creategdrivefolder` |
| Upload File | `uploadtogdrive` |
| Share File | `sharegdrivefile` |

---

## Slack Actions

| Action | Name | Description |
|--------|------|-------------|
| Send DM | `slackdirectmessageuser` | Direct message to user |
| Post to Channel | `slackpostmessage` | Message to channel |
| Create Channel | `slackcreatechannel` | Create new channel |
| Add Reaction | `slackaddreaction` | React to message |

```json
{
  "instructionTemplate": "Send me a Slack DM with [[report-content]]",
  "toolConfig": [
    {
      "name": "slackdirectmessageuser",
      "customisationData": { "skipUserInteraction": true }
    }
  ]
}
```

---

## Salesforce Actions

| Action | Name |
|--------|------|
| SOQL Query | Custom action ID |
| Create Record | `sfcreaterecord` |
| Update Record | `sfupdaterecord` |
| Create Task | `sfcreatetask` |
| Create Opportunity | `sfcreateopportunity` |

### SOQL Query Example

```json
{
  "id": "custom-soql-action-id",
  "instructionTemplate": "SELECT Id, Name FROM Account WHERE Name IN ([[accounts]])",
  "customisationData": {
    "skipUserInteraction": true
  }
}
```

---

## Jira Actions

| Action | Name |
|--------|------|
| Create Issue | `jiracreateissue` |
| Update Issue | `jiraupdateissue` |
| Assign Issue | `jiraassignissue` |
| Transition Issue | `jiratransitionissue` |
| JQL Query | Custom action ID |

```json
{
  "instructionTemplate": "Create a Jira ticket for [[Issue Summary]]",
  "toolConfig": [{ "name": "jiracreateissue" }]
}
```

---

## Confluence Actions

| Action | Name |
|--------|------|
| Create Page | `confluencecreatepage` |
| Update Page | `confluenceupdatepage` |
| Read Page | `confluencereadpage` |

---

## Zendesk Actions

| Action | Name |
|--------|------|
| Create Ticket | `zendeskcreatticket` |
| Update Ticket | `zendeskupdateticket` |
| Add Comment | `zendeskaddcomment` |

---

## Asana Actions

| Action | Name |
|--------|------|
| Create Task | `asanacreatetask` |
| Update Task | `asanaupdatetask` |
| Complete Task | `asanacompletetask` |

---

## Zoom Actions

| Action | Name |
|--------|------|
| Create Meeting | `zoomcreatemeeting` |
| Get Recording | `zoomgetrecording` |

---

## Custom Actions

Agents can include custom actions via:

1. **Composio Integration** — 85+ pre-built actions
2. **MCP Servers** — Custom tool integrations
3. **Webhooks** — HTTP-based actions

### Custom Action Config

```json
{
  "id": "custom-action-uuid",
  "customisationData": {
    "skipUserInteraction": true
  }
}
```

---

## Action Configuration Options

### skipUserInteraction

Run action without user confirmation:

```json
{
  "customisationData": {
    "skipUserInteraction": true
  }
}
```

Use for:
- Automated workflows
- Scheduled agents
- Actions that don't need approval

**Caution:** Only use for safe, reversible actions.

---

## Tool Selection Guide

| Need | Tool |
|------|------|
| Find documents across enterprise | `Glean Search` |
| Read a specific document | `Glean Document Reader` |
| Generate user-facing output | `Respond` |
| Intermediate reasoning | `Think` |
| Process CSVs/tables | `Data Analysis` |
| Iterate over list | `Internal Csv Splitter` + loop |
| User's recent work | `User Activity Retrieve` |
| Public web info | `googlegeminiwebsearch` |
| Send notification | `slackdirectmessageuser` |
| Create document | `creategdoc` |
| Send email | `googledraftemail` |
| Create ticket | `jiracreateissue` |
| Query Salesforce | SOQL custom action |

---

## Multi-Tool Steps

Execute multiple tools in parallel within one step:

```json
{
  "id": "parallel-search",
  "type": "TOOL",
  "toolConfig": [
    { "id": "Glean Search", "inputTemplate": [{ "template": "[[query]] app:gong" }] },
    { "id": "Glean Search", "inputTemplate": [{ "template": "[[query]] app:slack" }] },
    { "id": "Glean Search", "inputTemplate": [{ "template": "[[query]] app:gmail" }] },
    { "id": "Glean Search", "inputTemplate": [{ "template": "[[query]] app:salescloud" }] }
  ],
  "memoryConfig": "ALL_DEPENDENCIES"
}
```

All searches execute in parallel, results combined for next step.

---

*Catalog derived from Glean Agent Builder (January 2026). Actions may require connector setup.*
