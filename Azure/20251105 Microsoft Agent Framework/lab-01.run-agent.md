# 에이전트 프레임워크를 사용하여 에이전트 만들기 및 실행

## 프로그래밍 언어 선택

이 자습서에서는 **Azure OpenAI 채팅 완료 서비스**를 기반으로 에이전트 프레임워크를 사용하여 에이전트를 만들고 실행하는 방법을 보여 줍니다.

> **중요**
>
> 에이전트 프레임워크는 다양한 유형의 에이전트를 지원합니다.  
> 이 자습서에서는 채팅 완료 서비스를 기반으로 하는 에이전트를 사용하지만 **다른 모든 에이전트 유형도 동일한 방식으로 실행**됩니다.  
> 다른 에이전트 유형 및 생성 방법에 대한 자세한 내용은 **Agent Framework 사용자 가이드**를 참조하세요.

---

## 필수 조건

시작하기 전에 다음 구성 요소가 준비되어 있어야 합니다:

- Python 3.10 이상
- 구성된 Azure OpenAI 서비스 엔드포인트 및 배포
- Azure CLI 설치 및 인증 (Azure 자격증명 인증용)
- 사용자에게 다음 역할 중 하나 부여됨:
  - Cognitive Services OpenAI User
  - Cognitive Services OpenAI Contributor

> **중요**
>
> 이 자습서에서는 채팅 완료 서비스에 Azure OpenAI를 사용하지만,  
> 에이전트 프레임워크의 **채팅 클라이언트 프로토콜과 호환되는 모든 유추(Inference) 서비스**를 사용할 수 있습니다.

---

## Python 패키지 설치

Azure OpenAI에서 Microsoft 에이전트 프레임워크 사용을 위해 다음 패키지를 설치합니다:

```bash
pip install agent-framework
````

---

## 에이전트 만들기

먼저 Azure OpenAI와 통신하기 위한 채팅 클라이언트를 생성하고,
필수 구성 요소 단계에서 Azure CLI로 인증했던 동일한 로그인 정보를 사용합니다.

그런 다음 에이전트에 대한 **지침(instructions)** 과 **이름(name)** 을 제공하여 에이전트를 생성합니다.

```python
import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    instructions="You are good at telling jokes.",
    name="Joker"
)
```

---

## 에이전트 실행

에이전트를 실행하려면 에이전트 인스턴스에서 `.run()` 메서드를 호출하여 사용자 입력을 제공합니다.

에이전트는 `응답(Response)` 객체를 반환하고,
`.text` 속성을 통해 텍스트 결과에 접근할 수 있습니다.

```python
async def main():
    result = await agent.run("Tell me a joke about a pirate.")
    print(result.text)

asyncio.run(main())
```

---

## 스트리밍을 사용하여 에이전트 실행

스트리밍 실행을 위해서는 `.run_stream()` 메서드를 사용합니다.

이 메서드는 업데이트 객체를 순차적으로 스트리밍하며,
각 업데이트의 `.text` 속성을 통해 **부분 출력**을 받을 수 있습니다.

```python
async def main():
    async for update in agent.run_stream("Tell me a joke about a pirate."):
        if update.text:
            print(update.text, end="", flush=True)
    print()  # New line after streaming is complete

asyncio.run(main())
```

---

## ChatMessage를 사용하여 에이전트 실행

간단한 문자열 대신,
`run` 및 `run_stream` 메서드에 **하나 이상의 ChatMessage 객체**를 전달할 수 있습니다.

```python
from agent_framework import ChatMessage, TextContent, UriContent, Role

message = ChatMessage(
    role=Role.USER,
    contents=[
        TextContent(text="Tell me a joke about this image?"),
        UriContent(uri="https://samplesite.org/clown.jpg", media_type="image/jpeg")
    ]
)

async def main():
    result = await agent.run(message)
    print(result.text)

asyncio.run(main())
```


