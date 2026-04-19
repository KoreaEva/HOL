# **문서 Q&A (Document Q&A)**

이 플로우는 파일을 로드하고 LLM을 사용하여 로드된 문서의 내용을 바탕으로 질문에 답변합니다.

## **사전 요구 사항**

* **OpenAI API 키**

## **빠른 시작**

1.  **OpenAI** 모델 컴포넌트에 사용자의 **OpenAI API 키**를 붙여넣으세요.
2.  **File** 컴포넌트에서 로드하려는 파일을 선택하세요.
3.  **Playground**를 열고 문서와 대화하세요.

![image](https://github.com/KoreaEva/HOL/blob/master/Agents/20260420%20SKT-AX%20Frontier/Part_03/images/lab04-01.png?raw=true)

## Prompt

이미지에서 추출한 내용을 **영어 전체**와 **한국어 전체** 섹션으로 나누어 정리해 드립니다.

---

### **[English Version]**

**Edit Prompt**

Answer user's questions based on the document below:

---

{Document}

---

Question:

---

### **[한국어 번역본]**

**프롬프트 수정**

아래 문서를 바탕으로 사용자의 질문에 답변해 주세요:

---

{Document}

---

질문:

---