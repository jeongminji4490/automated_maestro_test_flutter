# LLM-based Mobile QA Automation workflow

An LLM-powered mobile QA automation workflow that generates, executes, and analyzes Maestro test scenarios from a single natural-language command.

[![Language](https://img.shields.io/badge/language-Korean-blue.svg)](./README.ko.md)

## 📌 Project Overview

This project combines Maestro and an LLM-based workflow to automate the entire mobile QA testing process:

- Generate test scripts
- Execute tests
- Analyze results

The goal is to reduce manual effort involved in writing Maestro YAML files, running CLI commands, and reviewing test results.

## 🛠 Tech Stack

| Category | Stack |
|-----------|--------|
| AI Agent | Codex CLI, Python |
| LLM Server | FastAPI, OpenAI GPT-4 |
| Mobile App | Flutter |
| Test Automation | Maestro |

## Architecture
<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/bd3cf4aa-0067-4fe2-a0e7-bfdcb5677104" />


## ✨ Key Features

### Input test scenarios

```bash
python3 cli.py \
  --intent "Start dashboard page test. Search text 'Search fruits...' and enter Durian. Click search button and verify Durian is visible." \
  --app-id "com.example.maestroTest" \
  --deep-link "myapp://dashboard" \
  --test-name "dashboard_test"
```

### Maestro Test file Generation

The Planner Agent converts user intent into structured JSON, and the Generator Agent transforms it into Maestro YAML.

```yaml
- tapOn: "Login"
- inputText: "user1234"
- assertVisible: "Dashboard"
```

### Automated Test Execution

- Navigate to a target screen using Deep Links
- Execute Maestro CLI automatically
- Collect test execution results

### Result Analysis

- Parse Maestro execution logs
- Extract failed steps
- Generate summarized test results

## Agent Orchestration

This project adopts a role-based multi-agent workflow architecture.

### Planner Agent

Responsibilities:

- Receive user input
- Send requests to the LLM server
- Return structured JSON responses

Example:

```json
{
  "appId": "com.example.maestroTest",
  "route": "myapp://dashboard",
  "steps": [
    { "action": "open" },
    { "action": "deeplink" },
    { "action": "assert_visible", "target": "Durian" }
  ]
}
```

The Planner Agent does not generate YAML directly.

Instead, the LLM only interprets intent and returns structured JSON, while YAML generation remains fully deterministic in code.

Benefits:

- Prevent invalid YAML generation
- Easier guardrail implementation
- Better control over test generation logic

### Generator Agent

Responsibilities:

- Parse JSON responses
- Generate Maestro YAML files

### Runner Agent

Responsibilities:

- Execute Maestro tests
- Collect logs
- Analyze and summarize results

## 🔍 Troubleshooting

### Codex Sandbox Network Limitation

Direct OpenAI API calls from the agent resulted in:

```text
APIConnectionError: Connection error
httpx.ConnectError:
nodename nor servname provided, or not known
```

### Cause

Codex CLI runs inside a sandboxed environment where outbound network access is restricted.

### Solution

- Built a separate FastAPI-based LLM server
- Routed agent requests through the local LLM server
