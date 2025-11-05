
# 에이전트와 함께 이미지 사용

## 프로그래밍 언어 선택

이 자습서에서는 **에이전트와 함께 이미지를 사용**하여  
에이전트가 이미지 콘텐츠를 분석하고 응답할 수 있도록 하는 방법을 보여줍니다.

---

## 필수 조건

필수 구성 요소 및 NuGet 패키지 설치는  
이 자습서의 **간단한 에이전트 만들기 및 실행** 단계를 참조하세요.

---

## 에이전트에 이미지 전달

텍스트 및 이미지 콘텐츠를 모두 포함하는 `ChatMessage` 객체를 만들어  
에이전트에 이미지를 보낼 수 있습니다.  

그러면 에이전트는 이미지를 분석하고 그에 맞는 응답을 반환합니다.

먼저, 이미지를 분석할 수 있는 에이전트를 생성합니다.

```python
import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    name="VisionAgent",
    instructions="You are a helpful agent that can analyze images"
)
````

---

다음으로, **텍스트 프롬프트 + 이미지 URL**을 모두 포함하는 `ChatMessage`를 생성합니다.

* 텍스트에는 `TextContent`
* 이미지에는 `UriContent` 를 사용합니다.

```python
from agent_framework import ChatMessage, TextContent, UriContent, Role

message = ChatMessage(
    role=Role.USER,
    contents=[
        TextContent(text="What do you see in this image?"),
        UriContent(
            uri="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
            media_type="image/jpeg"
        )
    ]
)
```

---

## 로컬 파일 시스템의 이미지 사용

`DataContent` 를 사용하여 로컬 파일을 에이전트에 전달할 수도 있습니다.

```python
from agent_framework import ChatMessage, TextContent, DataContent, Role

# Load image from local file
with open("path/to/your/image.jpg", "rb") as f:
    image_bytes = f.read()

message = ChatMessage(
    role=Role.USER,
    contents=[
        TextContent(text="What do you see in this image?"),
        DataContent(
            data=image_bytes,
            media_type="image/jpeg"
        )
    ]
)
```

---

## 에이전트 실행

생성한 메시지를 에이전트에 전달하여 실행합니다.
스트리밍을 통해 생성 즉시 응답을 받을 수 있습니다.

```python
async def main():
    result = await agent.run(message)
    print(result.text)

asyncio.run(main())
```

