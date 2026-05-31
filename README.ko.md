# LLM-based Mobile QA Automation workflow

자연어 기반 QA 시나리오를 입력하면 Maestro 테스트 파일 생성부터 실행 및 결과 분석까지 자동 수행하는 LLM 기반 모바일 QA 자동화 워크플로우

[![Language](https://img.shields.io/badge/language-English-green.svg)](./README.md)


## 📌 프로젝트 개요

모바일 앱 QA 자동화 도구 Maestro와 LLM을 결합하여, 테스트 파일 생성 → 실행 → 결과 분석까지 하나의 명령어로 수행할 수 있는 워크플로우 구현

기존의 수동 작업:

- Maestro YAML 작성
- 테스트 실행 명령어 입력
- 결과 확인

과정을 자동화하여 모바일 QA 테스트 생산성 향상 목표


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

LLM이 테스트 의도를 구조화된 JSON으로 반환하면 Generator Agent가 Maestro YAML 파일 생성

```yaml
- tapOn: "Login"
- inputText: "user1234"
- assertVisible: "Dashboard"
```



### 테스트 실행

- Deep Link 기반 특정 화면 진입
- Maestro CLI 자동 실행
- 테스트 결과 수집

### 결과 분석

- Maestro 실행 로그 파싱
- 실패 Step 추출
- 테스트 결과 요약

## 프로젝트 구조

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/bcd3029f-fc94-406f-b660-da41b19961de" />


## Agent Orchestration

코드기반 AI 오케스트레이션 구조 (Deterministic flows)

### Planner Agent

- 사용자 입력 수집
- LLM 서버 요청
- 구조화된 JSON 응답 반환

예시:

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

### Generator Agent

- JSON 응답 파싱
- Maestro YAML 생성

### Runner Agent

- Maestro 실행
- 로그 수집
- 결과 분석 및 요약



## 🔍 Troubleshooting

### Codex Sandbox Network Limitation

에이전트가 OpenAI API를 직접 호출할 경우 다음 오류가 발생:

```text
APIConnectionError: Connection error
httpx.ConnectError:
nodename nor servname provided, or not known
```

### Cause

Codex CLI는 기본적으로 Sandbox 환경에서 실행되며 외부 네트워크 접근을 제한

### Solution

- FastAPI 기반 별도 LLM 서버 구축
- Agent는 로컬 서버를 통해 LLM 응답 수신
