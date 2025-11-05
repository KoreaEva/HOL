
# 에이전트와 함께 함수 도구 사용

## 프로그래밍 언어 선택

이 자습서 단계에서는 에이전트와 함께 **함수 도구(Function Tools)** 를 사용하는 방법을 보여줍니다.  
여기서 에이전트는 Azure OpenAI **채팅 완료 서비스**를 기반으로 합니다.

> **중요**
>
> 모든 에이전트 형식이 함수 도구를 지원하는 것은 아닙니다.  
> 일부는 호출자가 자체 함수를 제공할 수 없고, **사용자 지정 기본 제공 도구만** 지원할 수 있습니다.  
> 본 단계에서는 함수 도구를 지원하는 **채팅 클라이언트 기반 에이전트**를 사용합니다.

---

## 필수 조건

필수 구성 요소 및 Python 패키지 설치는  
이 자습서의 **간단한 에이전트 만들기 및 실행** 단계를 참조하세요.

---

## 함수 도구를 사용하여 에이전트 만들기

함수 도구는 필요할 때 에이전트가 호출할 수 있도록 하는 **사용자 지정 코드**입니다.  
에이전트 생성 시 `tools` 매개변수에 Python 함수를 전달하면 됩니다.

함수 또는 매개변수에 대해 더 정확한 설명을 제공하려면 다음을 사용할 수 있습니다:

- Python **type annotation**
- `Annotated`
- Pydantic `Field`

아래 예제는 지리적 위치 기반의 간단한 날씨 정보를 반환합니다:

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

## ai_function 데코레이터 사용

`@ai_function` 데코레이터를 사용하여:

* 함수 이름 지정
* 설명 지정

이 가능합니다.

```python
from typing import Annotated
from pydantic import Field
from agent_framework import ai_function

@ai_function(name="weather_tool", description="Retrieves weather information for any location")
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    return f"The weather in {location} is cloudy with a high of 15°C."
```

> name / description 를 지정하지 않으면
> 프레임워크는 기본적으로 **함수명 및 docstring**을 사용합니다.

---

## 에이전트 생성 시 함수 도구 등록

```python
import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    instructions="You are a helpful assistant",
    tools=get_weather
)
```

이제 에이전트를 실행하면 필요한 경우 `get_weather` 함수가 호출됩니다.

```python
async def main():
    result = await agent.run("What is the weather like in Amsterdam?")
    print(result.text)

asyncio.run(main())
```

---

## 여러 함수 도구를 사용하여 클래스 만들기

여러 함수 도구를 클래스 내부 메서드로 구성할 수 있습니다:

* 관련 함수 묶기
* 함수 사이에서 상태 공유 가능

```python
class WeatherTools:
    def __init__(self):
        self.last_location = None

    def get_weather(
        self,
        location: Annotated[str, Field(description="The location to get the weather for.")],
    ) -> str:
        """Get the weather for a given location."""
        return f"The weather in {location} is cloudy with a high of 15°C."

    def get_weather_details(self) -> int:
        """Get the detailed weather for the last requested location."""
        if self.last_location is None:
            return "No location specified yet."
        return f"The detailed weather in {self.last_location} is cloudy with a high of 15°C, low of 7°C, and 60% humidity."
```

클래스의 메서드들을 함수 도구로 제공할 수 있습니다:

```python
tools = WeatherTools()
agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    instructions="You are a helpful assistant",
    tools=[tools.get_weather, tools.get_weather_details]
)
```

또한 클래스 메서드도 `@ai_function`으로 데코레이팅할 수 있습니다.

