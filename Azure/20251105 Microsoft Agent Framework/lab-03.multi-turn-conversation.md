# 에이전트와의 다중 턴 대화

## 프로그래밍 언어 선택

이 자습서 단계에서는 **에이전트와 다중 턴 대화**를 수행하는 방법을 설명합니다.  
여기서 사용하는 에이전트는 Azure OpenAI 채팅 완료 서비스 기반으로 빌드됩니다.

> **중요**
>
> 에이전트 프레임워크는 다양한 유형의 에이전트를 지원합니다.  
> 이 자습서에서는 채팅 완료 서비스 기반 에이전트를 사용하지만  
> **다른 모든 에이전트 유형도 동일한 방식으로 실행**됩니다.  
> 에이전트 유형 및 생성 방법은 *Agent Framework 사용자 가이드*를 참조하세요.

---

## 필수 조건

필수 구성 요소 및 에이전트 생성 과정은  
현재 자습서의 **간단한 에이전트 만들기 및 실행** 단계를 참조하세요.

---

## 다중 턴 대화를 사용하여 에이전트 실행

에이전트는 **상태를 내부적으로 유지하지 않는 stateless 구조**입니다.  
따라서 다중 턴 대화를 위해서는 **대화 상태를 유지하는 객체**를 직접 생성해야 합니다.

대화 상태 객체는 아래와 같이 생성합니다:

```python
thread = agent.get_new_thread()
````

생성된 thread 객체를 `run()` 또는 `run_stream()` 호출 시 함께 전달하면
해당 대화 컨텍스트를 유지한 채로 대화가 이어집니다.

```python
async def main():
    result1 = await agent.run("Tell me a joke about a pirate.", thread=thread)
    print(result1.text)

    result2 = await agent.run("Now add some emojis to the joke and tell it in the voice of a pirate's parrot.", thread=thread)
    print(result2.text)

asyncio.run(main())
```

이렇게 하면 호출 간의 대화 상태가 유지되며,
에이전트는 **이전 입력 및 응답을 참조한 답변**을 생성할 수 있습니다.

---

## 대화 기록 저장 방식 안내

> **중요**
>
> 에이전트가 사용하는 서비스 유형에 따라
> **대화 기록 저장 위치**가 달라집니다.

예시:

* **Azure OpenAI 채팅 완료 서비스 사용 시**

  * 대화 기록은 `AgentThread` 객체 내부에 저장
  * 호출마다 기록 전체가 서비스로 전송

* **Azure AI 에이전트 서비스 사용 시**

  * 대화 기록은 Azure AI Agent Service 측에 저장
  * 호출 시 대화 ID 참조만 전송

---

## 여러 대화를 처리하는 단일 에이전트

에이전트 하나로 여러 독립 대화를 운영하려면
`AgentThread` 객체를 여러 개 생성하면 됩니다.

* 각 스레드는 **완전히 독립적인 대화 상태**를 가짐
* 에이전트는 상태를 고정 보관하지 않으므로 간섭 없음

```python
async def main():
    thread1 = agent.get_new_thread()
    thread2 = agent.get_new_thread()

    result1 = await agent.run("Tell me a joke about a pirate.", thread=thread1)
    print(result1.text)

    result2 = await agent.run("Tell me a joke about a robot.", thread=thread2)
    print(result2.text)

    result3 = await agent.run("Now add some emojis to the joke and tell it in the voice of a pirate's parrot.", thread=thread1)
    print(result3.text)

    result4 = await agent.run("Now add some emojis to the joke and tell it in the voice of a robot.", thread=thread2)
    print(result4.text)

asyncio.run(main())
```

각각의 `thread1`, `thread2`는 완전히 분리된 대화 흐름을 유지할 수 있습니다.
