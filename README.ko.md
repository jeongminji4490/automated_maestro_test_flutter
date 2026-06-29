# LLM-based Mobile QA Automation workflow

자연어 기반 테스트 시나리오를 입력하면 Maestro 테스트 파일 생성부터 실행 및 결과 도출까지 자동으로 수행하는 LLM 기반 모바일 앱 테스트 자동화 워크플로우

[![Language](https://img.shields.io/badge/language-English-green.svg)](./README.md)


## 📌 프로젝트 개요

- 모바일 UI 및 End-to-End 테스트 자동화 도구 Maestro와 LLM을 결합하여, 테스트 파일 생성 → 실행 → 결과 도출까지 하나의 명령어로 수행할 수 있는 워크플로우 구현
- 사용자가 원하는 테스트 시나리오를 제시만 하고, 이후 자동으로 파일을 생성하고 명령어를 실행하는 역할을 AI 에이전트에게 위임하여 더 정확한 양식의 테스트 파일을 생성하고, 수동 작업 최소화

## 🛠 기술 스택

| Category | Stack |
|-----------|--------|
| AI Agent | Codex CLI, Python |
| LLM Server | FastAPI, OpenAI GPT-4 |
| Mobile App | Flutter |
| Test Automation | Maestro |





## ✨ 주요 기능

### 테스트 시나리오 입력

```bash
python3 cli.py \
  --intent "Start dashboard page test. Search text 'Search fruits...' and enter Durian. Click search button and verify Durian is visible." \
  --app-id "com.example.maestroTest" \ 
  --deep-link "myapp://dashboard" \ # 테스트 하고자 하는 화면 주소
  --test-name "dashboard_test" # 사용하고자 하는 테스트 파일명
```


### Maestro 테스트 파일 생성

- Planner Agent가 LLM 서버로부터 받은 JSON 응답을 반환하면 Generator Agent가 해당 응답 데이터를 기반으로 Maestro 테스트 파일 생성

```yaml
- tapOn: "Login"
- inputText: "user1234"
- assertVisible: "Dashboard"
```



### 테스트 실행

- Deep Link 기반 특정 화면 진입
- Maestro 테스트 명령어 자동 실행

### 결과 분석

- 실행 로그 파싱
- 실패 Step 추출 및 요약

## 프로젝트 구조

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/bcd3029f-fc94-406f-b660-da41b19961de" />


```
automated_maestro_test_flutter/
├── flutter_app/ (테스트용 앱)
│   └── maestro/
│       └── test.yaml
├── llm_service/ (LLM 서버)
│   ├── planner_service.py (테스트 시나리오/프롬프트 템플릿 기반 응답 반환)
│   └── prompts/
│       └── planner.md
└── orchestrator/ (에이전트 오케스트레이터)
    ├── cli.py
    └── agents/
        ├── planner_agent.py (LLM 서버 요청 + 응답 검증 및 반환)
        ├── plan_validator.py
        ├── generator_agent.py (테스트 파일 생성 + 검증)
        ├── generation_validator.py
        └── runner_agent.py (테스트 실행)
```

### Local LLM server - Planner Service

- 프롬프트 템플릿과 사용자 입력에 기반하여 프롬프트 구성
- LLM에 프롬프트 전달 및 결과 반환
- 기존에는 위 작업을 Planner Agent가 담당했으나, Codex CLI에서 sandbox 관련 문제로 워크플로우가 실행되지 않는 문제가 있어서 별도의 로컬 LLM 서버 구현 (트러블슈팅 항목 참고)

## 에이전트 구성 및 동작 흐름

코드기반 AI 오케스트레이션 구조 (Deterministic flows)

### Planner Agent + Plan Validator

- 사용자 입력(자연어 시나리오, App ID, 화면 URL)을 LLM 서버에 전달
- 테스트 시나리오에 대한 구조화된 JSON 응답 반환
- Plan validator를 통해 응답 구조가 유효한지 검증하고, 유효하지 않을 시 에러 반환
    
```json
    // JSON 응답 예시
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

- LLM이 YAML 파일을 직접 생성할수도 있지만, 잘못된 형식의 파일이 생성될 확률 존재 → 따라서 LLM은 프롬프트만 해석해서 구조화된 JSON 응답만을 반환하고, YAML 생성은 코드(Generator Agent)에서 완전히 결정론적으로 처리하도록 설계

### Generator Agent + Generation Validator

- Planner Agent가 반환한 JSON 응답을 파싱
- Maestro 테스트 실행을 위한 YAML 파일 생성
- Generation Validator를 통해 파일 구조가 유효한지 검증하고, 유효하지 않을 시 에러 반환
    
```yaml
    # 생성된 테스트 파일 예시
    
    - tapOn: "Login"
    - inputText: "user1234"
    - assertVisible: "Dashboard"
```

#### 3. Runner Agent

- 생성된 Maestro 테스트 파일 실행
- 콘솔 기반 테스트 결과 요약 출력


## 🔍 Troubleshooting

### Codex Sandbox Network Limitation

에이전트가 OpenAI API를 직접 호출할 경우 다음 오류가 발생:

```text
APIConnectionError: Connection error
httpx.ConnectError:
nodename nor servname provided, or not known
```

### Cause

- Codex CLI는 기본적으로 Sandbox 환경에서 실행되며 외부 네트워크 접근을 제한

### Solution
- localhost를 통한 자기 자신과의 통신은 외부 네트워크 요청이 필요하지 않기 때문에, FastAPI 기반 별도 로컬 LLM 서버를 만들고 Planner Agent가 로컬 서버를 통해 LLM 응답을 수신하는 방식으로 우회해서 구현
