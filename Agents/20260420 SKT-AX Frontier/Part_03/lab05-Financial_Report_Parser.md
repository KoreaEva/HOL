이 템플릿은 주어진 재무 보고서 텍스트에서 주요 재무 지표를 추출합니다. 추출된 데이터는 채팅에서 확인하기 적합하도록 구조화되고 포맷팅됩니다.

## 빠른 시작

1.  Language Model 컴포넌트에 사용자의 OpenAI API 키를 추가하거나, 다른 제공업체 및 모델을 선택하세요.
2.  Playground를 열어 채팅을 시작하고 플로우를 실행하세요. 이 예시에서는 Chat Input 컴포넌트에 샘플 재무 보고서가 미리 로드되어 있습니다. Language Model 컴포넌트는 재무 보고서에서 매출 총이익(Gross Profit), EBITDA, 당기순이익(Net Income), 영업 비용(Operating Expenses) 정보를 식별하고 추출합니다. 그 후, Structured Output 컴포넌트가 추출된 데이터를 가독성과 후속 처리를 위해 구조화된 형식으로 변환합니다. 마지막으로, Parser 컴포넌트가 추출된 데이터를 사용자에게 반환할 메시지 형태로 변환합니다.

---

![image](https://github.com/KoreaEva/HOL/blob/master/Agents/20260420%20SKT-AX%20Frontier/Part_03/images/lab05-01.png?raw=true) <br>
![image](https://github.com/KoreaEva/HOL/blob/master/Agents/20260420%20SKT-AX%20Frontier/Part_03/images/lab05-02.png?raw=true) <br>
![image](https://github.com/KoreaEva/HOL/blob/master/Agents/20260420%20SKT-AX%20Frontier/Part_03/images/lab05-03.png?raw=true)

