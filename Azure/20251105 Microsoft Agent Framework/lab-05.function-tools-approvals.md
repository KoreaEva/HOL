
# 사람이 개입하는 승인 프로세스에서 기능 도구 사용

## 프로그래밍 언어 선택

이 자습서 단계에서는 에이전트에 대한 사용자 승인이 필요한 함수 도구를 사용하는 방법을 보여 있습니다.

예를 들어 에이전트가 함수 호출을 승인하기 위해 사용자 입력이 필요한 경우 이를 **휴먼 인 더 루프(Human-in-the-loop)** 패턴이라고 합니다. 사용자 입력이 필요한 에이전트 실행은 최종 답변을 완료하는 대신 사용자에게 필요한 입력을 나타내는 응답으로 완료됩니다. 그런 다음 에이전트의 호출자는 사용자로부터 필요한 입력을 가져오고 새 에이전트 실행의 일부로 에이전트에 다시 전달하는 역할을 담당합니다.

---

## 필수 조건

필수 구성 요소 및 Python 패키지 설치는 이 자습서의 **간단한 에이전트 만들기 및 실행** 단계를 참조하세요.

---

## 승인이 필요한 함수 도구를 사용하여 에이전트 만들기

함수를 사용하는 경우, **실행되기 전에 사람의 승인이 필요한지 여부**를 각 함수에 대해 나타낼 수 있습니다.  
이는 `@ai_function` 데코레이터를 사용할 때 `approval_mode` 매개 변수를 `"always_require"` 로 설정하여 수행됩니다.

다음은 지정된 위치에 대한 날씨를 가짜로 만드는 간단한 함수 도구의 예입니다.

```python
from typing import Annotated
from agent_framework import ai_function

@ai_function
def get_weather(location: Annotated[str, "The city and state, e.g. San Francisco, CA"]) -> str:
    """Get the current weather for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C."
````

승인이 필요한 함수를 만들려면 `approval_mode` 매개 변수를 사용할 수 있습니다.

```python
@ai_function(approval_mode="always_require")
def get_weather_detail(location: Annotated[str, "The city and state, e.g. San Francisco, CA"]) -> str:
    """Get detailed weather information for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C, humidity 88%."
```

이제 에이전트를 만들 때 함수 도구 목록을 `ChatAgent` 생성자에 전달하여 에이전트에 함수 도구가 필요한 승인을 제공할 수 있습니다.

```python
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIResponsesClient

async with ChatAgent(
    chat_client=OpenAIResponsesClient(),
    name="WeatherAgent",
    instructions="You are a helpful weather assistant.",
    tools=[get_weather, get_weather_detail],
) as agent:
    # Agent is ready to use
```

---

이제 **승인이 필요한 함수**가 있으므로, 에이전트는 함수를 직접 실행하고 결과를 반환하는 대신 **승인 요청**으로 응답할 수 있습니다.
에이전트에 함수에 대한 사용자 승인이 필요했음을 나타내는 사용자 입력 요청에 대한 응답을 확인할 수 있습니다.

```python
result = await agent.run("What is the detailed weather like in Amsterdam?")

if result.user_input_requests:
    for user_input_needed in result.user_input_requests:
        print(f"Function: {user_input_needed.function_call.name}")
        print(f"Arguments: {user_input_needed.function_call.arguments}")
```

함수 승인 요청이 있는 경우, 이름 및 인수를 포함한 함수 호출의 세부 정보는 `user_input_requests` 의 `function_call` 속성에서 찾을 수 있습니다.
사용자가 함수 호출을 승인할지 거부할지를 결정할 수 있도록 사용자에게 표시할 수 있습니다.

사용자가 입력을 제공하면 `user_input_needed.create_response()` 메서드를 사용하여 응답을 만들 수 있습니다.
`True`를 전달하면 **승인**, `False`를 전달하면 **거부**입니다.

그런 다음 새 에이전트 `ChatMessage`에 응답을 전달하여 에이전트에서 결과를 다시 가져올 수 있습니다.

```python
from agent_framework import ChatMessage, Role

# Get user approval (in a real application, this would be interactive)
user_approval = True  # or False to reject

# Create the approval response
approval_message = ChatMessage(
    role=Role.USER, 
    contents=[user_input_needed.create_response(user_approval)]
)

# Continue the conversation with the approval
final_result = await agent.run([
    "What is the detailed weather like in Amsterdam?",
    ChatMessage(role=Role.ASSISTANT, contents=[user_input_needed]),
    approval_message
])
print(final_result.text)
```

---

## 루프 내에서 승인 처리

승인이 필요한 여러 함수 호출을 사용하는 경우
**모든 함수가 승인되거나 거부될 때까지** 루프에서 승인을 처리해야 할 수 있습니다.

```python
async def handle_approvals(query: str, agent) -> str:
    """Handle function call approvals in a loop."""
    current_input = query

    while True:
        result = await agent.run(current_input)

        if not result.user_input_requests:
            # No more approvals needed, return the final result
            return result.text

        # Build new input with all context
        new_inputs = [query]

        for user_input_needed in result.user_input_requests:
            print(f"Approval needed for: {user_input_needed.function_call.name}")
            print(f"Arguments: {user_input_needed.function_call.arguments}")

            # Add the assistant message with the approval request
            new_inputs.append(ChatMessage(role=Role.ASSISTANT, contents=[user_input_needed]))

            # Get user approval (in practice, this would be interactive)
            user_approval = True  # Replace with actual user input

            # Add the user's approval response
            new_inputs.append(
                ChatMessage(role=Role.USER, contents=[user_input_needed.create_response(user_approval)])
            )

        # Continue with all the context
        current_input = new_inputs

# Usage
result_text = await handle_approvals("Get detailed weather for Seattle and Portland", agent)
print(result_text)
```

---

## 정리

사람과 함께 협업하는 루프 승인 기능 도구를 사용할 때마다:

* 각 에이전트 실행 응답에서 **user_input_requests** 를 확인한다.
* 필요하면 사용자 승인/거부를 입력받는다.
* 해당 승인 메시지를 **새로운 메시지로 다시 전달**한다.
* **모든 함수 호출이 승인·거부될 때까지 반복**한다.

