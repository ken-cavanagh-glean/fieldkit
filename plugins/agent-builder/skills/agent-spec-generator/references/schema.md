# Glean Agent JSON Schema

Complete schema reference for Glean Agent Builder export/import format.

---

## Root Structure

```json
{
  "rootWorkflow": {
    "name": "string",
    "description": "string",
    "icon": { ... },
    "schema": { ... }
  },
  "serverVersion": "string"
}
```

---

## rootWorkflow

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Agent name (displayed in UI) |
| `description` | string | No | Agent description (shown in agent picker) |
| `icon` | object | Yes | Icon configuration |
| `schema` | object | Yes | Agent workflow definition |

### icon

```json
{
  "backgroundColor": "var(--theme-brand-light-blue-50)",
  "color": "#333",
  "iconType": "GLYPH",
  "name": "rocket-2"
}
```

| Field | Type | Values |
|-------|------|--------|
| `backgroundColor` | string | CSS variable (see Icon Colors below) |
| `color` | string | Hex color code |
| `iconType` | string | `"GLYPH"` |
| `name` | string | Icon name (see Icon Names below) |

#### Icon Colors

```
var(--theme-brand-light-blue-50)
var(--theme-brand-apple-green-50)
var(--theme-secondary-orange)
var(--theme-selected)
```

#### Icon Names

```
rocket-2, feather, bar-chart, calendar, briefcase,
file-text, users, search, settings, mail,
message-circle, check-circle, alert-circle, star
```

---

## schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `goal` | string | No | High-level agent objective |
| `steps` | array | Yes | Workflow steps |
| `fields` | array | Yes | Input form fields |
| `tags` | array | No | Collection tags |
| `notes` | array | No | Canvas annotations |
| `modelOptions` | object | No | Global LLM settings |
| `trigger` | object | Yes | Trigger configuration |

---

## steps[]

Each step in the workflow.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique step identifier (UUID or custom) |
| `type` | string | Yes | `TOOL`, `AGENT`, `BRANCH`, `LOOP` |
| `instructionTemplate` | string | No | Prompt with `[[variable]]` references |
| `stepDependencies` | array | No | IDs of steps this depends on |
| `toolConfig` | array | Yes* | Tool configurations (*required for TOOL type) |
| `branchConfig` | object | Yes* | Branch configuration (*required for BRANCH type) |
| `modelOptions` | object | No | Per-step LLM override |
| `memoryConfig` | string | No | `ALL_DEPENDENCIES` or `NO_MEMORY` |

### Step Type: TOOL

Execute one or more tools.

```json
{
  "id": "search-step",
  "type": "TOOL",
  "instructionTemplate": "Search for [[Account Name]] in Gong",
  "toolConfig": [
    {
      "id": "Glean Search",
      "inputTemplate": [{ "template": "[[Account Name]] app:gong" }],
      "gleanSearchConfig": { "numResults": 30 }
    }
  ],
  "memoryConfig": "ALL_DEPENDENCIES"
}
```

### Step Type: AGENT

Call another agent as a sub-workflow.

```json
{
  "id": "run-research-agent",
  "type": "AGENT",
  "toolConfig": [
    {
      "id": "agent-uuid-here",
      "name": "agent-uuid-here",
      "inputTemplate": [
        { "template": "[[Prospect]]", "name": "Prospect" }
      ],
      "runAgentConfig": {}
    }
  ],
  "memoryConfig": "ALL_DEPENDENCIES"
}
```

### Step Type: BRANCH

Conditional execution paths.

```json
{
  "id": "branch-step",
  "type": "BRANCH",
  "branchConfig": {
    "branches": [
      {
        "condition": {
          "boolFunction": {
            "id": "Think",
            "inputTemplate": [
              { "template": "[[field_name]] is \"yes\"", "name": "ExecutionConditionBoolPrompt" }
            ]
          }
        },
        "stepId": "step-if-true"
      }
    ],
    "default": {
      "stepId": "step-if-false"
    }
  },
  "memoryConfig": "ALL_DEPENDENCIES"
}
```

### Step Type: LOOP

Iterate over a collection (from CSV splitter or array output).

```json
{
  "id": "loop-over-items",
  "type": "AGENT",
  "toolConfig": [
    {
      "id": "agent-uuid",
      "name": "agent-uuid",
      "inputTemplate": [
        { "template": "[[csv-splitter-step]]", "name": "Item" }
      ],
      "runAgentConfig": {},
      "loopConfig": {
        "inputStepDependency": "csv-splitter-step"
      }
    }
  ]
}
```

---

## toolConfig[]

Configuration for tools within a step. Multiple tools = parallel execution.

### Common Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Tool ID (e.g., `Glean Search`, `Respond`) |
| `name` | string | Action name (for actions, e.g., `slackdirectmessageuser`) |
| `inputTemplate` | array | Input templates with `[[variable]]` references |
| `customisationData` | object | Custom settings (e.g., `skipUserInteraction`) |

### Tool-Specific Configs

#### Glean Search

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

#### Glean Document Reader

```json
{
  "id": "Glean Document Reader",
  "documentReaderConfig": {},
  "customisationData": {
    "skipUserInteraction": true
  }
}
```

#### Respond

```json
{
  "id": "Respond",
  "respondConfig": {
    "temperature": "FACTUAL"
  }
}
```

Temperature values: `FACTUAL`, `BALANCED`, `CREATIVE`

#### Think

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

#### Data Analysis

```json
{
  "name": "Data Analysis"
}
```

#### Actions (by name)

```json
{ "name": "slackdirectmessageuser" }
{ "name": "creategdoc" }
{ "name": "googledraftemail" }
{ "name": "googlegeminiwebsearch" }
```

---

## fields[]

Input form fields.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Internal field name (used in `[[name]]`) |
| `displayName` | string | Yes | Label shown to user |
| `description` | string | No | Help text |
| `defaultValue` | string | No | Pre-filled value |
| `type` | object | Yes | Field type configuration |
| `options` | array | No | Options for SELECT/MULTI_SELECT |

### Field Types

```json
// Text
{ "type": { "type": "TEXT" } }

// Select (dropdown)
{
  "type": { "type": "SELECT" },
  "options": [
    { "value": "option1", "label": "Option 1" },
    { "value": "option2", "label": "Option 2" }
  ]
}

// Multi-Select
{ "type": { "type": "MULTI_SELECT" } }

// Number
{ "type": { "type": "NUMBER" } }

// Date
{ "type": { "type": "DATE" } }

// Boolean
{ "type": { "type": "BOOLEAN" } }

// File Upload
{ "type": { "type": "FILE" } }

// Entity Reference (Person/Team)
{ "type": { "type": "ENTITY" } }
```

---

## tags[]

Collection tags for organizing agents.

```json
{
  "tags": [
    {
      "category": "WORKFLOW_COLLECTION",
      "collectionTagValue": 4128
    }
  ]
}
```

---

## notes[]

Canvas annotations (visual notes in Agent Builder UI).

```json
{
  "notes": [
    {
      "backgroundColor": "var(--theme-selected)",
      "content": "Note text here",
      "boundingBox": {
        "x": 300,
        "y": 20,
        "width": 270,
        "height": 166
      }
    }
  ]
}
```

---

## modelOptions

LLM configuration (global or per-step).

```json
{
  "modelOptions": {
    "llmConfig": {
      "provider": "OPEN_AI",
      "model": "GPT41_20250414"
    }
  }
}
```

### Providers and Models

| Provider | Models |
|----------|--------|
| `OPEN_AI` | `GPT41_20250414`, `GPT5_2` |
| `VERTEX_AI` | `GEMINI_3_0` |

---

## trigger

How the agent is activated.

### INPUT_FORM (Manual)

```json
{
  "trigger": {
    "type": "INPUT_FORM",
    "config": {
      "inputForm": {
        "scheduleConfig": {}
      }
    }
  }
}
```

### INPUT_FORM (Scheduled)

```json
{
  "trigger": {
    "type": "INPUT_FORM",
    "config": {
      "inputForm": {
        "scheduleConfig": {
          "enabled": true
        }
      }
    }
  }
}
```

### WEBHOOK

```json
{
  "trigger": {
    "type": "WEBHOOK",
    "config": {
      "webhook": {
        "url": "https://..."
      }
    }
  }
}
```

### SLACK_COMMAND

```json
{
  "trigger": {
    "type": "SLACK_COMMAND",
    "config": {
      "slackCommand": {
        "command": "/agent-name"
      }
    }
  }
}
```

### CONTENT_TRIGGER

```json
{
  "trigger": {
    "type": "CONTENT_TRIGGER",
    "config": {
      "contentTrigger": {
        "filters": { ... }
      }
    }
  }
}
```

---

## Variable References

Use `[[variable]]` syntax:

| Syntax | References |
|--------|------------|
| `[[field_name]]` | Input field value |
| `[[step-id]]` | Output from previous step |
| `[[step-id.property]]` | Specific property from step output |

---

## Complete Example

```json
{
  "rootWorkflow": {
    "name": "Sales: Account Snapshot",
    "description": "Help AEs understand the status of an account",
    "icon": {
      "backgroundColor": "var(--theme-brand-light-blue-50)",
      "color": "#333",
      "iconType": "GLYPH",
      "name": "rocket-2"
    },
    "schema": {
      "goal": "Help AEs and sales managers understand the status of an account.",
      "steps": [
        {
          "id": "0",
          "type": "TOOL",
          "toolConfig": [
            {
              "id": "Glean Search",
              "inputTemplate": [{ "template": "[[prospect]] app:gong" }],
              "gleanSearchConfig": { "numResults": 30, "enableFullDocumentSnippets": true }
            },
            {
              "id": "Glean Search",
              "inputTemplate": [{ "template": "[[prospect]] app:slack" }]
            },
            {
              "id": "Glean Search",
              "inputTemplate": [{ "template": "[[prospect]] app:salescloud type:opportunity" }]
            }
          ],
          "memoryConfig": "ALL_DEPENDENCIES"
        },
        {
          "id": "1",
          "instructionTemplate": "Based on the context, summarize the account status...",
          "type": "TOOL",
          "stepDependencies": ["0"],
          "toolConfig": [
            {
              "id": "Respond",
              "respondConfig": { "temperature": "FACTUAL" }
            }
          ],
          "memoryConfig": "ALL_DEPENDENCIES"
        }
      ],
      "fields": [
        {
          "name": "prospect",
          "displayName": "prospect",
          "defaultValue": "Acme Corp",
          "type": { "type": "TEXT" }
        }
      ],
      "modelOptions": {
        "llmConfig": { "provider": "OPEN_AI", "model": "GPT41_20250414" }
      },
      "trigger": {
        "type": "INPUT_FORM",
        "config": { "inputForm": { "scheduleConfig": {} } }
      }
    }
  }
}
```

---

*Schema derived from Glean Agent Builder exports (January 2026)*
