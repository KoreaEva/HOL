# 이미지 감성 분석 (Image Sentiment Analysis)

플레이그라운드(Playground)에 업로드된 이미지를 감성에 따라 분류합니다.

## 사전 요구 사항

* OpenAI API 키

## 빠른 시작

1. Language Model 컴포넌트에 사용자의 OpenAI API 키를 추가하세요.
2. Playground를 열고 채팅창에 이미지를 제출하세요.

LLM이 이미지를 분석합니다. 감성 분석 결과는 Structured Output 컴포넌트의 출력 스키마(Output Schema)에 따라 구조화된 테이블 형태로 출력되며, 이후 플레이그라운드에 표시될 메시지로 파싱됩니다.

![image](https://github.com/KoreaEva/HOL/blob/master/Agents/20260420%20SKT-AX%20Frontier/Part_03/images/lab06-01.png?raw=true)

## Prompt

이미지에서 추출한 내용을 영어 전체와 한국어 전체 섹션으로 나누어 정리해 드립니다.

---

### [English Version]

Edit Prompt

Classify the image into neutral, negative or positive.

---

### [한국어 번역본]

프롬프트 수정

이미지를 중립, 부정, 또는 긍정으로 분류하세요.

---