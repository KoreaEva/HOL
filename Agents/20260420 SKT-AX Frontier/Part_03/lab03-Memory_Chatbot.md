이 플로우는 **Basic Prompting** 템플릿에 **Message History** 컴포넌트를 추가하여 확장한 것으로, 현재 대화의 컨텍스트로 최대 100개의 이전 채팅 메시지를 가져올 수 있습니다.

## **빠른 시작**

1.  **Language Model** 컴포넌트에 OpenAI API 키를 추가하거나, 다른 제공업체 및 모델을 선택하세요.
2.  **Playground**를 열고 LLM에게 귀하의 이름을 말해 주세요.
3.  Playground에서 새 채팅 세션을 시작한 다음, `내 이름이 뭐야?`라고 물어보세요. LLM은 저장된 채팅 기록에서 귀하의 이름을 찾아낼 수 있습니다.

![image](https://github.com/KoreaEva/HOL/blob/master/Agents/20260420%20SKT-AX%20Frontier/Part_03/images/lab03-01.png?raw=true)

## **Message History 컴포넌트에 대하여**

**Language Model**과 **Agent** 컴포넌트에는 기본적으로 활성화되어 있는 내장 채팅 메모리가 있으며, 이는 기능적으로 **Message History** 컴포넌트와 동일합니다. 외부 채팅 메모리 데이터베이스에 채팅 메모리를 저장하거나 불러오고 싶을 때, 혹은 채팅이 아닌 플로우에서 사용하거나 다른 채팅의 기억을 다른 세션에 제공하는 경우와 같이 현재 세션 컨텍스트 외부의 채팅 메모리를 가져와야 할 때만 **Message History** 컴포넌트를 사용하세요. 자세한 내용은 **Store chat memory**를 참조하세요.

## Prompt 

### **[English Version]**

**Edit Prompt**

You are a helpful assistant that answer questions.

Use markdown to format your answer, properly embedding images and urls.

History:

{memory}

---

### **[한국어 번역본]**

**프롬프트 수정**

당신은 질문에 답변하는 도움이 되는 어시스턴트입니다.

마크다운을 사용하여 답변 서식을 지정하고, 이미지와 URL을 적절하게 포함하세요.

기록(History):

{memory}

---
