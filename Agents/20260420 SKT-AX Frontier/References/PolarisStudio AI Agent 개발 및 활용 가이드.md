## 0. 소개 영상

![PolarisStudio소개영상](https://raw.githubusercontent.com/joonlab/md-share-db/main/videos/PolarisStudio%EC%86%8C%EA%B0%9C%EC%98%81%EC%83%81_8d94c1.mp4)

---

안녕하세요, 여러분.
Polaris.Studio 교육에 앞서, 플랫폼의 핵심 기능을 이해하고 원활하게 실습에 참여하실 수 있도록 가이드 문서를 공유해 드립니다.

본 문서는 Polaris.Studio를 활용하여 어떻게 아이디어를 실제 동작하는 AI Agent로 구현하고, 사내 시스템과 연동하여 업무에 활용할 수 있는지 전체적인 흐름을 다룹니다.

---

## 1. Polaris.Studio란 무엇인가?

Polaris.Studio는 코딩 지식이 없어도, 누구나 MNO 비즈니스 목적에 맞는 AI Agent를 만들고 실행할 수 있는 SKT의 사내 AI Agent 개발 플랫폼입니다. 데이터 분석, 리포트 생성, 업무 자동화 등 다양한 작업을 AI Agent를 통해 해결할 수 있습니다.

![Polaris.Studio 메인 화면](https://raw.githubusercontent.com/joonlab/md-share-db/main/images/01_main_screen_8a7047.jpg)


## 2. 워크플로우 템플릿으로 빠르게 시작하기

Polaris.Studio는 LTV 데이터 분석, 온라인 마케팅 지원금 조회 등 현업에서 자주 사용하는 기능들을 미리 만들어 둔 '템플릿' 형태로 제공합니다. 이를 통해 처음부터 만들 필요 없이, 필요한 템플릿을 선택하여 즉시 업무에 활용하거나 필요에 맞게 수정하여 사용할 수 있습니다.

![워크플로우 템플릿 목록](https://raw.githubusercontent.com/joonlab/md-share-db/main/images/02_template_list_65b969.jpg)

![새로운 워크플로우 생성 팝업](https://raw.githubusercontent.com/joonlab/md-share-db/main/images/03_new_workflow_popup_c54a61.jpg)


## 3. 나만의 AI Agent 만들기 (Step-by-Step)

템플릿 외에도, 특정 업무에 최적화된 Agent를 직접 만들 수 있습니다. 영상의 'LTV 데이터 분석 Agent' 생성 과정을 따라가며 핵심 단계를 알아보겠습니다.

#### Step 1: 새 워크플로우 생성

가장 먼저 Agent가 동작할 작업 공간인 '워크플로우'를 생성합니다.

![워크플로우 생성 팝업](https://raw.githubusercontent.com/joonlab/md-share-db/main/images/04_create_workflow_007cdd.jpg)


#### Step 2: 핵심 컴포넌트 배치 및 연결

워크플로우 캔버스에 필요한 기능 단위인 '컴포넌트'들을 드래그 앤 드롭으로 배치하고, 데이터 흐름에 맞게 연결합니다.

- **채팅 입력**: 사용자의 질문을 받는 시작점
- **Polaris 에이전트**: 사용자의 질문을 이해하고, 도구를 사용해 작업을 수행하는 AI의 두뇌
- **채팅 출력**: Agent의 답변을 사용자에게 보여주는 종착점

![컴포넌트 연결 화면](https://raw.githubusercontent.com/joonlab/md-share-db/main/images/05_component_flow_7b3457.jpg)


#### Step 3: Agent 능력 강화하기 (프롬프트와 도구 추가)

Agent가 구체적인 작업을 수행하도록 상세한 지시사항('프롬프트')을 입력하고, 데이터 분석 및 시각화를 위한 '도구(Tool)'를 추가합니다.

![프롬프트 템플릿 목록 팝업](https://raw.githubusercontent.com/joonlab/md-share-db/main/images/06_prompt_template_52d267.jpg)

![전체 워크플로우 다이어그램](https://raw.githubusercontent.com/joonlab/md-share-db/main/images/07_full_workflow_0d230b.jpg)


#### Step 4: Playground에서 Agent 테스트하기

완성된 Agent가 의도대로 동작하는지 'Playground'에서 테스트합니다. 자연어 질문을 입력하고 Agent의 답변과 작업 수행 과정을 실시간으로 확인할 수 있습니다.

![Playground 테스트 화면](https://raw.githubusercontent.com/joonlab/md-share-db/main/images/08_playground_test_1cc4e5.jpg)


#### Step 5: 분석 결과 확인 및 보고서 생성

Agent는 코드 실행, 데이터 분석, 시각화 등 복잡한 작업을 자율적으로 수행하고 그 결과를 그래프와 같은 형태로 제공합니다. 더 나아가, 분석 결과를 바탕으로 정형화된 보고서 작성을 요청할 수도 있습니다.

![LTV 시뮬레이션 결과 그래프](https://raw.githubusercontent.com/joonlab/md-share-db/main/images/09_simulation_graph_6b9ab2.jpg)

![보고서 작성 결과](https://raw.githubusercontent.com/joonlab/md-share-db/main/images/10_report_writing_500dea.jpg)


## 4. Agent 공유 및 사내 시스템 연동

개발이 완료된 Agent는 다른 구성원이나 사내 시스템과 연동하여 실제 업무에 바로 적용할 수 있습니다.

![Confluence 보고서 게시 화면](https://raw.githubusercontent.com/joonlab/md-share-db/main/images/11_confluence_2175de.jpg)


#### MAMF 및 Polaris Catalog 연동

'워크플로우 연동' 메뉴를 통해 클릭 몇 번으로 Agent를 MAMF나 Polaris Catalog에 손쉽게 배포할 수 있습니다. 배포된 Agent는 해당 시스템 내에서 즉시 사용 가능합니다.

![워크플로우 연동하기 팝업](https://raw.githubusercontent.com/joonlab/md-share-db/main/images/12_workflow_connect_429c9b.jpg)

![MAMF Agent 목록](https://raw.githubusercontent.com/joonlab/md-share-db/main/images/13_mamf_agent_519671.jpg)

![Polaris.AI 포털 화면](https://raw.githubusercontent.com/joonlab/md-share-db/main/images/14_polaris_ai_44f2ac.jpg)


---

## 마치며

지금까지 Polaris.Studio를 활용한 AI Agent 개발부터 테스트, 그리고 실제 업무 시스템에 적용하는 전체 과정을 살펴보았습니다. 본 가이드와 영상을 통해 플랫폼의 강력한 기능들을 미리 숙지하시고, 다가오는 교육에서 더욱 유익한 시간을 보내시면 좋겠습니다.

궁금한 점은 교육 시간에 편하게 질문해 주세요. 감사합니다.


## 참고 자료

1. [SKT Polaris Studio 소개 페이지](https://md-share-cf.pages.dev/view/docs/SKT%20Polaris%20Studio%20%EC%86%8C%EA%B0%9C%20%ED%8E%98%EC%9D%B4%EC%A7%80_78d514.md)