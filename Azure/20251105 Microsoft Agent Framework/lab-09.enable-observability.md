
# 에이전트에서 OpenTelemetry 사용

이 자습서에서는 에이전트와의 상호 작용이 자동으로 기록되고 내보내지도록  
**OpenTelemetry**를 활성화하는 방법을 보여줍니다.

예제에서는 **OpenTelemetry 콘솔 Exporter**를 사용하여  
출력이 콘솔에 표시됩니다.

---

## 필수 조건

필수 구성 요소는 다음 단계를 참조하세요:

- 이 자습서의 **간단한 에이전트 만들기 및 실행**

---

## 패키지 설치

Azure OpenAI와 함께 Agent Framework를 사용하려면 다음을 설치합니다:

```bash
pip install agent-framework
````

Agent Framework는 필요한 모든 OpenTelemetry 종속성을 자동으로 포함합니다.

### 기본 포함 OpenTelemetry 패키지:

```
opentelemetry-api
opentelemetry-sdk
opentelemetry-exporter-otlp-proto-grpc
opentelemetry-semantic-conventions-ai
```

### Azure Monitor(애플리케이션 인사이트)로 내보내기

```bash
pip install azure-monitor-opentelemetry
```

---

## 앱에서 OpenTelemetry 사용

Agent Framework는 기본 관찰성을 구성하는 헬퍼 함수
`setup_observability` 를 제공합니다.
기본적으로 **콘솔**로 내보냅니다.

```python
import asyncio
from agent_framework.observability import setup_observability

# Enable Agent Framework telemetry with console output (default behavior)
setup_observability(enable_sensitive_data=True)
```

---

## `setup_observability` 매개 변수

| 매개변수                                  | 설명                             |
| ------------------------------------- | ------------------------------ |
| enable_otel                           | OpenTelemetry 추적/메트릭 활성화       |
| enable_sensitive_data                 | prompt/response 등 민감 데이터 포함 여부 |
| otlp_endpoint                         | 원격 OTLP Exporter URL           |
| applicationinsights_connection_string | Azure Monitor Export 연결 문자열    |
| vs_code_extension_port                | VS Code/AI Toolkit 연동 포트       |
| exporters                             | 사용자 정의 exporter 리스트            |

### 환경 변수 사용 가능

예:

```bash
export ENABLE_OTEL=true
export ENABLE_SENSITIVE_DATA=true
export OTLP_ENDPOINT=http://localhost:4317
```

> 내보내기 구성이 없을 경우
> **기본적으로 콘솔 exporter**가 활성화됩니다.

---

## 옵션 설정 방식

### 1) 환경 변수 방식 (추천)

```bash
export ENABLE_OTEL=true
export ENABLE_SENSITIVE_DATA=true
export OTLP_ENDPOINT=http://localhost:4317
```

```python
from agent_framework.observability import setup_observability

setup_observability()  # Reads from environment variables
```

---

### 2) 코드 기반 구성

```python
from agent_framework.observability import setup_observability

setup_observability(
    enable_sensitive_data=True,
    otlp_endpoint="http://localhost:4317",
    applicationinsights_connection_string="InstrumentationKey=your_key"
)
```

---

### 3) 사용자 정의 Exporter (고급)

```python
from agent_framework.observability import setup_observability
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter

custom_exporters = [
    OTLPSpanExporter(endpoint="http://localhost:4317"),
    ConsoleSpanExporter()
]

setup_observability(exporters=custom_exporters, enable_sensitive_data=True)
```

---

## 사용자 정의 Span/Metric 생성

```python
from agent_framework.observability import get_tracer, get_meter

tracer = get_tracer()
meter = get_meter()

with tracer.start_as_current_span("my_custom_span"):
    pass

counter = meter.create_counter("my_custom_counter")
counter.add(1, {"key": "value"})
```

---

## 에이전트 만들기 및 실행

```python
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

# Create the agent - telemetry is automatically enabled
agent = ChatAgent(
    chat_client=AzureOpenAIChatClient(
        credential=AzureCliCredential(),
        model="gpt-4o-mini"
    ),
    name="Joker",
    instructions="You are good at telling jokes."
)

# Run the agent
result = await agent.run("Tell me a joke about a pirate.")
print(result.text)
```

---

## 예시 콘솔 출력 (추적 데이터)

```
{
    "name": "invoke_agent Joker",
    "context": {
        "trace_id": "...",
        "span_id": "...",
        "trace_state": "[]"
    },
    "kind": "SpanKind.CLIENT",
    ...
}
```

### 에이전트 응답

```
Why did the pirate go to school?

Because he wanted to improve his "arrr-ticulation"! ⛵
```

---

## 원격 분석 출력 이해

Agent Framework는 자동으로 다음 범위를 생성합니다:

| Span 이름                 | 설명        |
| ----------------------- | --------- |
| invoke_agent <name>     | 최상위 호출 단위 |
| chat <model>            | 모델 호출     |
| execute_tool <function> | 함수 도구 실행  |

또한 다음 메트릭을 생성합니다:

### 채팅 작업

* `gen_ai.client.operation.duration`
* `gen_ai.client.token.usage`

### 함수 호출

* `agent_framework.function.invocation.duration`

---

## Azure AI Foundry 통합

```python
from agent_framework.azure import AzureAIAgentClient
from azure.identity import AzureCliCredential

agent_client = AzureAIAgentClient(
    credential=AzureCliCredential(),
)

await agent_client.setup_azure_ai_observability()
```

또는

```python
from agent_framework.observability import setup_observability
from azure.ai.projects import AIProjectClient
from azure.identity import AzureCliCredential

project_client = AIProjectClient(endpoint, credential=AzureCliCredential())
conn_string = project_client.telemetry.get_application_insights_connection_string()

setup_observability(applicationinsights_connection_string=conn_string)
```

> 참고
> Azure Monitor 사용 시 `azure-monitor-opentelemetry` 패키지를 별도 설치해야 합니다.

