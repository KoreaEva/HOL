# 에이전트를 함수 도구로 사용

## 프로그래밍 언어 선택

이 자습서에서는 **한 에이전트가 다른 에이전트를 도구로 호출**할 수 있도록  
에이전트를 함수 도구(Function Tool)로 사용하는 방법을 다룹니다.

---

## 필수 조건

필수 구성 요소 및 패키지 설치는  
이 자습서의 **간단한 에이전트 만들기 및 실행** 단계를 참조하세요.

---

## 함수 도구로 에이전트 만들기 및 사용

에이전트는 `ChatAgent.as_tool()`를 호출하여  
다른 에이전트에 **함수 도구 형태로 제공**할 수 있습니다.

이를 통해 에이전트를 **조합**하고 **고급 워크플로우**를 구성할 수 있습니다.

---

### 1) 먼저 에이전트에서 사용할 함수 도구 생성

```python
from typing import Annotated
from pydantic import Field

def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C."
````

---

### 2) 함수 도구를 가진 WeatherAgent 생성

```python
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

weather_agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    name="WeatherAgent",
    description="An agent that answers questions about the weather.",
    instructions="You answer questions about the weather.",
    tools=get_weather
)
```

---

### 3) WeatherAgent를 함수 도구로 변환하여 MainAgent에 제공

```python
main_agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    instructions="You are a helpful assistant who responds in French.",
    tools=weather_agent.as_tool()
)
```

---

### 4) 메인 에이전트 실행

이제 MainAgent는 WeatherAgent를 도구로 호출하고
**프랑스어로 응답**해야 합니다.

```python
result = await main_agent.run("What is the weather like in Amsterdam?")
print(result.text)
```

---

## 에이전트 도구 변환 시 사용자 지정 옵션

`as_tool()` 호출 시 아래를 커스터마이징할 수 있습니다:

* 도구 이름 (`name`)
* 도구 설명 (`description`)
* 인수 이름 (`arg_name`)
* 인수 설명 (`arg_description`)

```python
# Convert agent to tool with custom parameters
weather_tool = weather_agent.as_tool(
    name="WeatherLookup",
    description="Look up weather information for any location",
    arg_name="query",
    arg_description="The weather query or location"
)

main_agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    instructions="You are a helpful assistant who responds in French.",
    tools=weather_tool
)
```
