# LLM-based Mobile QA Automation workflow

An LLM-based mobile app test automation workflow that automatically performs everything from Maestro test file generation to execution and result reporting when a natural language test scenario is provided

[![Language](https://img.shields.io/badge/language-Korean-blue.svg)](./README.ko.md)

## 📌 Project Overview

- Implemented a workflow that combines Maestro, a mobile UI and End-to-End test automation tool, with an LLM so that test file generation → execution → result reporting can be performed with a single command
- The user only needs to provide the desired test scenario, and then delegates the tasks of automatically generating files and executing commands to an AI agent, enabling more accurate test file formatting and minimizing manual work

## 🛠 Tech Stack

| Category | Stack |
|-----------|--------|
| AI Agent | Codex CLI, Python |
| LLM Server | FastAPI, OpenAI GPT-4 |
| Mobile App | Flutter |
| Test Automation | Maestro |


## ✨ Key Features

### Input test scenarios

```bash
python3 cli.py \
  --intent "Start dashboard page test. Search text 'Search fruits...' and enter Durian. Click search button and verify Durian is visible." \
  --app-id "com.example.maestroTest" \
  --deep-link "myapp://dashboard" \ # screen route to be tested
  --test-name "dashboard_test" # test file name to use
```

### Maestro Test file Generation

- When the Planner Agent returns the JSON response received from the LLM server, the Generator Agent creates a Maestro test file based on that response data

```yaml
- tapOn: "Login"
- inputText: "user1234"
- assertVisible: "Dashboard"
```

### Test Execution

- Enter a specific screen based on Deep Link
- Automatically execute Maestro test commands

### Result

- Parse execution logs
- Extract and summarize failed steps

## Architecture
<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/e6fd25f5-c48f-4af3-a704-66d0d84e7fb6" />

```
automated_maestro_test_flutter/
├── flutter_app/ (Test app)
│   └── maestro/
│       └── test.yaml
├── llm_service/ (LLM server)
│   ├── planner_service.py (Returns a response based on the input test scenarios and prompt template)
│   └── prompts/
│       └── planner.md
└── orchestrator/ (Agent orchestrator)
    ├── cli.py
    └── agents/
        ├── planner_agent.py (Sends a request to LLM server, returns and validates a reponse)
        ├── plan_validator.py
        ├── generator_agent.py (Creates a test file and validates it)
        ├── generation_validator.py
        └── runner_agent.py (Execute test)
```


### Local LLM server - Planner Service
- Compose prompts based on prompt templates and user input
- Send prompts to the LLM and return results
- Previously, the Planner Agent handled this work directly, but due to sandbox-related issues in Codex CLI that prevented the workflow from running, a separate local LLM server was implemented (see troubleshooting section)


## Agent Orchestration

Code-based AI orchestration structure (Deterministic flows)

### Planner Agent + Plan Validator
- Send user input (natural language scenario, App ID, screen URL) to the LLM server
- Return a structured JSON response for the test scenario
- Validate whether the response structure is valid through the Plan Validator, and return an error if invalid

```json
// JSON response example
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

### Generator Agent + Generation Validator
- Parse the JSON response returned by the Planner Agent
- Generate a YAML file for Maestro test execution
- Validate whether the file structure is valid through the Generation Validator, and return an error if invalid

```yaml
# Example of generated test file

- tapOn: "Login"
- inputText: "user1234"
- assertVisible: "Dashboard"
```

### Runner Agent

- Execute the generated Maestro test file
- Output a console-based summary of test results

## 🔍 Troubleshooting

### Codex Sandbox Network Limitation

When the agent directly calls the OpenAI API, the following error occurs:

```text
APIConnectionError: Connection error
httpx.ConnectError:
nodename nor servname provided, or not known
```

### Cause

- Codex CLI runs in a Sandbox environment by default and restricts external network access

### Solution

- Since communication with itself via localhost does not require external network requests, this was implemented as a workaround by creating a separate FastAPI-based local LLM server and having the Planner Agent receive LLM responses through the local server
