# 에이전트에 미들웨어 추가

## 프로그래밍 언어 선택

몇 가지 간단한 단계로 에이전트에 **미들웨어(Middleware)** 를 추가하는 방법을 알아봅니다.  
미들웨어를 사용하면 로깅, 보안 및 기타 교차 관심사를 위해  
에이전트 상호작용을 **가로채고 수정**할 수 있습니다.

---

## 1단계: 간단한 에이전트 만들기

```python
import asyncio
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

async def main():
    credential = AzureCliCredential()

    async with AzureAIAgentClient(async_credential=credential).create_agent(
        name="GreetingAgent",
        instructions="You are a friendly greeting assistant.",
    ) as agent:
        result = await agent.run("Hello!")
        print(result.text)

if __name__ == "__main__":
    asyncio.run(main())
````

---

## 2단계: 미들웨어 만들기

에이전트가 실행되는 시점을 감지하기 위한 간단한 **로깅 미들웨어** 예제입니다.

```python
from agent_framework import AgentRunContext
from typing import Callable, Awaitable

async def logging_agent_middleware(
    context: AgentRunContext,
    next: Callable[[AgentRunContext], Awaitable[None]],
) -> None:
    """Simple middleware that logs agent execution."""
    print("Agent starting...")

    # Continue to agent execution
    await next(context)

    print("Agent finished!")
```

---

## 3단계: 에이전트에 미들웨어 추가

```python
async def main():
    credential = AzureCliCredential()

    async with AzureAIAgentClient(async_credential=credential).create_agent(
        name="GreetingAgent",
        instructions="You are a friendly greeting assistant.",
        middleware=logging_agent_middleware,  # Add your middleware here
    ) as agent:
        result = await agent.run("Hello!")
        print(result.text)
```

---

## 4단계: 함수 미들웨어 만들기

에이전트에서 **함수 도구**를 사용하는 경우
해당 함수 호출도 가로챌 수 있습니다.

```python
from agent_framework import FunctionInvocationContext

def get_time():
    """Get the current time."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

async def logging_function_middleware(
    context: FunctionInvocationContext,
    next: Callable[[FunctionInvocationContext], Awaitable[None]],
) -> None:
    """Middleware that logs function calls."""
    print(f"Calling function: {context.function.name}")

    await next(context)

    print(f"Function result: {context.result}")
```

에이전트에 함수 및 미들웨어 모두 추가:

```python
async with AzureAIAgentClient(async_credential=credential).create_agent(
    name="TimeAgent",
    instructions="You can tell the current time.",
    tools=[get_time],
    middleware=[logging_function_middleware],
) as agent:
    result = await agent.run("What time is it?")
```

---

## 5단계: Run-Level 미들웨어 사용

특정 요청 실행에 대해서만 미들웨어를 적용할 수 있습니다.

```python
# Use middleware for this specific run only
result = await agent.run(
    "This is important!",
    middleware=[logging_function_middleware]
)
```

---

## 다음 단계는 무엇인가요?

아래 주제를 다루는 **에이전트 미들웨어 사용자 가이드**를 참고하세요:

* 다양한 미들웨어 유형 (에이전트, 함수, 채팅)
* 복잡한 시나리오용 **클래스 기반 미들웨어**
* 미들웨어 종료 및 결과 덮어쓰기
* 고급 미들웨어 패턴 및 모범 사례