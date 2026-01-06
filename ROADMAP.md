# Fieldkit Roadmap

Strategic roadmap for expanding fieldkit into a comprehensive AIOM toolkit.

---

## Vision

Fieldkit provides the **knowledge layer** for Glean field teams - skills, commands, and reference material that make Claude an effective AIOM copilot. It complements:

- **gleanwork/claude-plugins** (Steve Calvert) - Operational layer (MCP setup, hooks, developer workflows)
- **Levi's Native Tools** - Real-time UX (QuestionMonitor, Glean Answers, Glean Central)

Together: the full AIOM toolkit.

---

## Strategic Lens

**What Glean handles natively:**
- Enterprise search, chat, document retrieval (via MCP or web)
- Agent Builder for no-code agent creation
- Autonomous agents (coming H1 2026) - plan, adapt, execute
- 100+ native actions (Salesforce, Jira, GitHub - coming)
- Meeting prep, account briefs, summaries (Glean Agents can do this)

**What Claude Code + Skills uniquely enable:**
- Local + enterprise fusion (your codebase + Glean knowledge)
- Structured data handling (CSVs, exports - Glean MCP returns markdown)
- Multi-harness orchestration (Notion + Glean + Browser together)
- Agent specification authoring (human-readable specs → Agent Builder)
- Browser automation for testing and verification
- Deep code generation with enterprise context

**Skill selection principle:** Build skills for what Glean *can't* do, or where Claude Code's local context provides unique value.

---

## Recommended External Plugins

Plugins that complement fieldkit. Install alongside for full AIOM toolkit.

| Plugin | Source | Purpose |
|--------|--------|---------|
| `dev-browser` | `sawyerhood/dev-browser` | Browser automation for testing, verification, debugging |

**Installation:**
```bash
/plugin marketplace add sawyerhood/dev-browser
/plugin install dev-browser@sawyerhood/dev-browser
```

---

## Current State

| Skill | Status | Description |
|-------|--------|-------------|
| `glean-mcp` | **Shipped** | MCP routing, tool selection, query optimization |
| `context-engineering` | **Shipped** | Agent design education (adapted from Muratcan Koylan) |

---

## Roadmap

### Phase 0: Core Capabilities

Skills that address gaps where Glean MCP falls short or Claude Code has unique advantages.

#### 0.1 `browser-automation` (Skill)
**Priority:** High | **Effort:** Low | **Status:** Not Started

Guidance for effective browser automation when `dev-browser` plugin is installed.

**Triggers:**
- "test this in the browser"
- "verify the UI"
- "check localhost"
- "debug the webpage"

**Behavior:**
- Provides patterns for persistent page sessions
- Guides LLM-friendly DOM inspection
- Suggests verification strategies
- Handles common browser automation pitfalls

**Implementation:**
- Skill file with best practices from dev-browser docs
- Complements dev-browser plugin (requires separate install)

---

#### 0.2 `agent-spec-generator` (Skill)
**Priority:** High | **Effort:** Medium | **Status:** Not Started

Generate human-readable agent specifications that can be imported into Glean Agent Builder.

**Triggers:**
- "create an agent spec"
- "design an agent for [use case]"
- "spec out an agent"
- "agent specification for [customer]"

**Workflow:**
1. Gather agent requirements through interview:
   - What question/task does it answer?
   - Who is the audience?
   - What data sources are needed?
   - What actions should it take?
2. Generate structured spec document:
   - Name, description, example queries
   - Knowledge sources (collections, apps, URLs)
   - Suggested prompt/instructions
   - Success criteria
3. Output: Markdown spec ready for Agent Builder import

**Why this is a skill (not Glean native):**
- Glean Agent Builder requires manual configuration
- No API to programmatically create agents
- Spec doc bridges Claude's reasoning → human copy/paste → Agent Builder

**Output Format:**
```markdown
# Agent Specification: [Name]

## Overview
- **Purpose:** [one-liner]
- **Audience:** [who uses this]
- **Example queries:** [3-5 examples]

## Knowledge Sources
- [ ] Collection: [name]
- [ ] App: [confluence/gdrive/etc]
- [ ] URL: [specific pages]

## Instructions
[System prompt for the agent]

## Success Criteria
- [metric 1]
- [metric 2]
```

---

#### 0.3 `structured-data-handler` (Skill)
**Priority:** High | **Effort:** Medium | **Status:** Not Started

Handle structured data exports that Glean MCP can't process (CSVs, spreadsheets, data tables).

**Triggers:**
- "analyze this CSV"
- "process this spreadsheet"
- "export to CSV"
- "structured data from [source]"

**Workflow:**
1. Identify data source (local file, URL, Glean doc)
2. For Glean sources:
   - Use `search` to find the doc
   - Use `read_document` to get content
   - Parse markdown tables → structured format
3. For local files:
   - Read CSV/Excel directly
   - Parse into analyzable format
4. Enable operations:
   - Filtering, sorting, aggregation
   - Statistical analysis
   - Format conversion (CSV ↔ JSON ↔ markdown)
   - Export to files

**Why this is a skill (not Glean native):**
- Glean MCP returns markdown snippets, not raw data
- Can't extract CSVs from Google Sheets via MCP
- Claude Code has local file access for exports

**Glean Workaround Patterns:**
- Search for spreadsheet → get URL → user downloads → Claude processes local file
- Search for data → extract tables from markdown → reconstruct structure

---

### Phase 1: Daily Workflow Tools

Skills and commands for everyday AIOM work.

#### 1.1 `/fieldkit:prep-call` (Command)
**Priority:** High | **Effort:** Medium | **Status:** Not Started

Pre-call briefing generator. Run before any customer meeting.

```bash
/fieldkit:prep-call [customer] [meeting-topic]
```

**Outputs:**
- Attendee context (titles, tenure, relationships)
- Recent activity from customer (docs, Slack, emails)
- Past meeting summaries with this customer
- Open issues/risks from success plan
- Suggested talking points based on context

**Implementation:**
- Parallel calls: `employee_search`, `search`, `meeting_lookup`
- Template: structured briefing format
- Trigger: explicit command only (not auto-invoked)

**Glean Tools Used:**
- `employee_search` - Attendee lookup
- `search` - Recent docs/Slack from customer
- `meeting_lookup` - Past meetings with transcripts
- `chat` - Synthesize into talking points

---

#### 1.2 `account-context` (Skill)
**Priority:** High | **Effort:** Low | **Status:** Not Started

Auto-invoked skill that helps Claude understand account context when discussing customers.

**Triggers:**
- "what's going on with [customer]"
- "status of [customer]"
- "brief me on [customer]"
- "[customer] health"

**Behavior:**
- Pull recent activity, open opportunities, key contacts
- Summarize adoption metrics if available
- Flag any risks or open issues

**Implementation:**
- Skill file with trigger patterns
- References `glean-mcp` for tool routing

---

#### 1.3 `/fieldkit:weekly-summary` (Command)
**Priority:** Medium | **Effort:** Medium | **Status:** Not Started

Generate weekly status update for manager sync or personal tracking.

```bash
/fieldkit:weekly-summary
```

**Outputs:**
- Accounts touched this week
- Meetings attended
- Key decisions/outcomes
- Documents created/updated
- Blockers and next steps

**Glean Tools Used:**
- `user_activity` - Your work history
- `meeting_lookup` - Meetings attended
- `search` - Docs you touched

---

### Phase 2: Customer Success Frameworks

Skills that encode AIOM best practices.

#### 2.1 `blueprint-consultation` (Skill)
**Priority:** High | **Effort:** Medium | **Status:** Not Started

Guides Claude through the blueprint consultation process for agent prioritization.

**Triggers:**
- "help me prioritize agents for [customer]"
- "which agents should we build first"
- "use case prioritization"
- "impact effort matrix"

**Workflow:**
1. Gather inputs:
   - Department/team
   - Pain points
   - Frequency of task
   - Time spent per occurrence
   - % of team performing task
2. Score: Impact (H/M/L) x Effort (H/M/L)
3. Output: Prioritized matrix with rationale

**References:**
- Katya Alfaro's blueprint playbook framework
- GTM enablement materials

**Implementation:**
- Skill with structured interview flow
- Can output markdown table or structured format

---

#### 2.2 `agent-roi-calculator` (Skill)
**Priority:** High | **Effort:** Medium | **Status:** Not Started

Quantify agent value for business reviews.

**Triggers:**
- "quantify agent value"
- "ROI for [agent-name]"
- "prepare business review"
- "value of agents for [customer]"

**Workflow:**
1. Identify agent(s) to analyze
2. Gather metrics: WAU, queries/week, avg response time
3. Estimate time saved per interaction
4. Calculate: `users x frequency x time_saved x hourly_rate`
5. Output: ROI narrative with methodology

**Assumptions to Document:**
- Default hourly rate (or ask user)
- Time saved per query type
- Baseline (what they did before)

---

#### 2.3 `adoption-intervention` (Skill)
**Priority:** Medium | **Effort:** Medium | **Status:** Not Started

For low-adoption accounts - diagnose and recommend interventions.

**Triggers:**
- "adoption is low for [customer]"
- "how do I increase usage"
- "intervention plan"
- "[customer] isn't using Glean"

**Workflow:**
1. Assess current state:
   - WAU, Power Users, Agent WAU
   - Deployment method (web, Slack, extension)
   - Content coverage
2. Compare to benchmarks
3. Identify gaps:
   - Deployment gaps (not where users work)
   - Training gaps (don't know how to use)
   - Content gaps (answers aren't good)
4. Recommend specific interventions by persona

**Output:** Prioritized action plan with owners

---

### Phase 3: Customer Intelligence

Skills for understanding patterns across customers.

#### 3.1 `customer-question-patterns` (Skill)
**Priority:** Medium | **Effort:** High | **Status:** Not Started

Analyze what customers ask most frequently - find documentation gaps.

**Triggers:**
- "what questions does [customer] ask"
- "common questions across my accounts"
- "reduce question volume"
- "documentation gaps"

**Workflow:**
1. Search: Gong transcripts, Slack threads, support tickets
2. Cluster questions by topic
3. Classify:
   - Already answered (link to existing docs)
   - Needs new content (gap)
   - Needs agent (automate)
4. Output: Top 10 questions + recommended actions

**Use Cases:**
- Pre-create knowledge collections
- Identify agent opportunities
- Reduce support burden

---

#### 3.2 `competitive-context` (Skill)
**Priority:** Low | **Effort:** Low | **Status:** Not Started

Quick competitive intelligence when customer mentions alternatives.

**Triggers:**
- "customer asked about [competitor]"
- "how do we compare to [competitor]"
- "[competitor] vs Glean"

**Behavior:**
- Pull internal competitive docs
- Summarize key differentiators
- Provide talk track

---

### Phase 4: Integration with Native Tools

Fieldkit skills that feed into or receive from Levi's tools.

#### 4.1 QuestionMonitor Integration
**Priority:** Low | **Effort:** Medium | **Status:** Not Started

- QuestionMonitor detects question during call
- Routes to fieldkit skill for specialized handling
- Example: "What's our pricing?" triggers internal pricing skill

#### 4.2 Glean Central Data Skills
**Priority:** Low | **Effort:** Medium | **Status:** Not Started

- Skills that output structured data for Glean Central
- Account health scores, risk indicators, success metrics
- Glean Central displays, fieldkit computes

---

## Implementation Notes

### Skill vs Command Decision

| Use... | When... |
|--------|---------|
| **Skill** | Claude should auto-invoke based on conversation patterns |
| **Command** | User explicitly requests a workflow with `/` prefix |

### File Structure

```
fieldkit/
├── skills/
│   ├── glean-mcp/
│   │   └── SKILL.md
│   ├── context-engineering/
│   │   └── SKILL.md
│   ├── browser-automation/          # Phase 0 - NEW
│   │   └── SKILL.md
│   ├── agent-spec-generator/        # Phase 0 - NEW
│   │   └── SKILL.md
│   ├── structured-data-handler/     # Phase 0 - NEW
│   │   └── SKILL.md
│   ├── blueprint-consultation/      # Phase 2
│   │   └── SKILL.md
│   ├── agent-roi-calculator/        # Phase 2
│   │   └── SKILL.md
│   ├── adoption-intervention/       # Phase 2
│   │   └── SKILL.md
│   └── account-context/             # Phase 1
│       └── SKILL.md
├── commands/                         # New directory
│   ├── prep-call/
│   │   └── COMMAND.md
│   └── weekly-summary/
│       └── COMMAND.md
├── .claude-plugin/
│   └── marketplace.json
├── README.md
└── ROADMAP.md                        # This file
```

### Contribution Workflow

1. Pick an item from roadmap
2. Create skill/command in appropriate directory
3. Update `marketplace.json`
4. Test with real account scenarios
5. Submit PR with example outputs

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Skills shipped | 6+ by Q1 |
| AIOMs using fieldkit | 50%+ of team |
| Time saved per call prep | 10+ min |
| Business reviews with ROI data | 80%+ |

---

## Ideas Backlog

Raw ideas not yet prioritized or specced. Add ideas here first.

| Idea | Category | Notes |
|------|----------|-------|
| `glean-sdk` | Development | Teach Claude to use Glean SDK for building integrations, API calls, agent programmatic control |
| `mcp-server-builder` | Development | Guide for building custom MCP servers |
| `agent-debugger` | Development | Diagnose why agents aren't returning expected results |

### Adding Ideas

Just add a row to the table above. When ready to build:
1. Move to appropriate Phase section
2. Spec out triggers, workflow, implementation
3. Assign priority and effort

---

## Contributors

- Kenneth Cavanagh - fieldkit maintainer
- Levi DeHaan - Native tools, QuestionMonitor
- Glean Field Engineering - glean-mcp skill

---

*Last updated: 2026-01-05*
-- Axon
