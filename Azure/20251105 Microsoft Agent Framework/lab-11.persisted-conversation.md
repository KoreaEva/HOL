# 에이전트 대화 유지 및 다시 시작

## 프로그래밍 언어 선택

이 자습서에서는 에이전트 대화(`AgentThread`)를 저장하고  
나중에 다시 로드하는 방법을 보여줍니다.

서비스 또는 클라이언트 애플리케이션에서 에이전트를 호스팅할 경우,  
여러 요청 또는 세션 사이에서 대화 상태를 **유지**해야 하는 시나리오가 많습니다.

`AgentThread` 를 사용하면 대화 컨텍스트를 저장하고  
이후 재개할 수 있습니다.

---

## 필수 조건

필수 구성 요소 및 Python 패키지 설치는  
이 자습서의 **간단한 에이전트 만들기 및 실행** 단계를 참조하세요.

---

## 대화 유지 및 다시 열기

먼저 에이전트를 생성하고  
대화 상태를 보유할 스레드를 생성합니다.

```python
from azure.identity import AzureCliCredential
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient

agent = ChatAgent(
    chat_client=AzureOpenAIChatClient(
        endpoint="https://<myresource>.openai.azure.com",
        credential=AzureCliCredential(),
        ai_model_id="gpt-4o-mini"
    ),
    name="Assistant",
    instructions="You are a helpful assistant."
)

thread = agent.get_new_thread()
````

---

## 대화 실행 및 스레드에 기록

`thread` 를 `run()` 호출에 전달하면
모든 발화가 스레드 내부에 기록됩니다.

```python
# Run the agent and append the exchange to the thread
response = await agent.run("Tell me a short pirate joke.", thread=thread)
print(response.text)
```

---

## 스레드 직렬화(Serialize)

`serialize()` 메서드를 사용하면
스레드를 사전(dict) 형태로 직렬화할 수 있습니다.

그 후 JSON 저장소(DB, Blob, 파일)에 저장할 수 있습니다.

```python
import json
import tempfile
import os

# Serialize the thread state
serialized_thread = await thread.serialize()
serialized_json = json.dumps(serialized_thread)

# Example: save to a local file (replace with DB or blob storage in production)
temp_dir = tempfile.gettempdir()
file_path = os.path.join(temp_dir, "agent_thread.json")
with open(file_path, "w") as f:
    f.write(serialized_json)
```

---

## 스레드 역직렬화(Deserialize)

저장된 JSON을 다시 로딩하고
동일한 **에이전트 타입**을 사용하여 스레드를 복원합니다.

> ⚠️ 주의
> 원래 스레드를 생성한 것과 동일한 **에이전트 타입/형식**을 사용해야 합니다.

```python
# Read persisted JSON
with open(file_path, "r") as f:
    loaded_json = f.read()

reloaded_data = json.loads(loaded_json)

# Deserialize the thread into an AgentThread tied to the same agent type
resumed_thread = await agent.deserialize_thread(reloaded_data)
```

---

## 다시 시작된 스레드로 대화 계속

이제 기존 대화를 이어서 진행할 수 있습니다.

```python
# Continue the conversation with resumed thread
response = await agent.run("Now tell that joke in the voice of a pirate.", thread=resumed_thread)
print(response.text)
```
