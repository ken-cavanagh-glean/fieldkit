---
name: browser-automation
description: Guidance for effective browser automation with dev-browser plugin. Use for testing local development, verifying UI changes, debugging visual issues, and automating browser tasks.
---

# Browser Automation Skill

Guidance for effective browser automation in Claude Code. Complements the `dev-browser` plugin.

## Prerequisites

This skill provides guidance for using browser automation. Requires the `dev-browser` plugin to be installed:

```bash
/plugin marketplace add sawyerhood/dev-browser
/plugin install dev-browser@sawyerhood/dev-browser
```

## When to Use Browser Automation

**Good use cases:**
- Testing local development (localhost, staging)
- Verifying UI changes after code modifications
- Debugging visual issues or user flows
- Extracting data from web pages
- Automating repetitive browser tasks

**Poor use cases:**
- Tasks that require authenticated sessions you can't access
- High-frequency scraping (use APIs instead)
- Actions on production systems without explicit approval

## Core Patterns

### 1. Persistent Page Sessions

Dev-browser maintains page state across interactions. Use this for multi-step workflows:

```
1. Navigate once to the page
2. Inspect → identify elements
3. Interact → click, type, verify
4. Don't reload unless necessary
```

### 2. LLM-Friendly DOM Inspection

Use DOM snapshots over screenshots when possible:
- Snapshots are structured and searchable
- Screenshots require visual interpretation
- Combine both for complex debugging

**Pattern:**
```
snapshot → identify element refs → interact with refs
```

### 3. Step-by-Step for Exploration

When exploring unknown pages:
```
1. Take snapshot to understand structure
2. Identify interactive elements
3. Take one action
4. Verify result with new snapshot
5. Repeat
```

### 4. Full Scripts for Known Flows

When you know the exact flow:
```
1. Write complete interaction sequence
2. Execute in one script
3. Verify final state
```

## Common Operations

### Navigation
- `browser_navigate` - Go to URL
- `browser_navigate_back` - Go back
- `browser_snapshot` - Get page structure (preferred)
- `browser_take_screenshot` - Visual capture

### Interaction
- `browser_click` - Click element by ref
- `browser_type` - Type into element
- `browser_fill_form` - Fill multiple fields
- `browser_select_option` - Select from dropdown
- `browser_press_key` - Keyboard input

### Waiting
- `browser_wait_for` - Wait for text/element/time
- Always wait after navigation or actions that trigger loading

### Debugging
- `browser_console_messages` - Check for errors
- `browser_network_requests` - Inspect API calls

## Best Practices

### 1. Reference-Based Interaction
Always use element refs from snapshots, not CSS selectors:
```
snapshot → find ref="btn-42" → click ref="btn-42"
```

### 2. Explicit Waits
After actions that cause page changes:
```
click → wait_for text="Success" → continue
```

### 3. Error Recovery
If an action fails:
1. Take new snapshot
2. Verify page state
3. Adjust approach

### 4. Form Filling
Use `browser_fill_form` for multiple fields:
```
fill_form([
  {name: "email", type: "textbox", ref: "...", value: "..."},
  {name: "password", type: "textbox", ref: "...", value: "..."}
])
```

### 5. Verification Pattern
After completing a flow:
```
1. Take final snapshot or screenshot
2. Verify expected elements present
3. Check console for errors
4. Report success/failure with evidence
```

## Integration with Glean Workflows

### Testing Agent-Generated Content
1. Build agent in Glean
2. Navigate to Glean in browser
3. Test agent responses
4. Verify output format and accuracy

### Verifying Customer Deployments
1. Navigate to customer's Glean instance (if accessible)
2. Test specific agent or search functionality
3. Document results with screenshots

### Local Development Testing
1. Start local dev server
2. Navigate to localhost
3. Test changes iteratively
4. Verify before committing

## Example Workflow

**Testing a login flow:**

```
1. browser_navigate("http://localhost:3000/login")
2. browser_snapshot() → identify form elements
3. browser_fill_form([
     {name: "email", ref: "input-1", value: "test@example.com"},
     {name: "password", ref: "input-2", value: "testpass"}
   ])
4. browser_click(ref: "submit-btn")
5. browser_wait_for(text: "Dashboard")
6. browser_snapshot() → verify logged in state
7. Report: "Login successful - dashboard loaded"
```

---

*Skill version: 1.0.0*
*Requires: dev-browser plugin*
-- Axon | 2026-01-01
