import streamlit as st
import asyncio
import os
from random import randint
from typing import Annotated

import chromadb
from agent_framework import tool
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
from pydantic import Field

# 1. 환경 변수 및 설정
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# 페이지 설정
st.set_page_config(page_title="MVPTour AI 상담원", page_icon="✈️")
st.title("✈️ MVPTour 여행 상담 서비스")
st.markdown("시애틀 날씨, 실시간 환율, 여행 상품 정보를 문의해보세요!")

# --- 세션 상태 초기화 (에이전트 및 DB가 한 번만 생성되도록 설정) ---
if "agent_initialized" not in st.session_state:
    # ChromaDB 설정
    chroma_client = chromadb.Client()
    collection = chroma_client.get_or_create_collection(name="mvp_tour_info")
    collection.add(
        documents=[
            "시애틀 투어 패키지: 3박 4일 일정으로 스페이스 니들 입장권이 포함되어 있습니다.",
            "MVPTour 특별 환전 서비스: 본사 1층에서 오전 9시부터 오후 4시까지 우대 환율을 제공합니다.",
            "예약 취소 규정: 여행 7일 전까지는 100% 환불 가능하며, 이후에는 50% 수수료가 발생합니다."
        ],
        ids=["doc1", "doc2", "doc3"]
    )
    st.session_state.collection = collection

    # 툴 정의
    @tool(approval_mode="never_require")
    def get_weather(location: Annotated[str, Field(description="날씨를 조회할 지역")]) -> str:
        """지정된 위치의 날씨 정보를 가져옵니다."""
        conditions = ["맑음", "흐림", "비", "폭풍우"]
        return f"{location}의 날씨는 {conditions[randint(0, 3)]}이며, 최고 기온은 {randint(10, 30)}°C입니다."

    @tool(approval_mode="never_require")
    def get_exchange_rate(
        base_currency: Annotated[str, Field(description="기준 통화 (예: USD)")],
        target_currency: Annotated[str, Field(description="대상 통화 (예: KRW)")]
    ) -> str:
        """두 통화 간의 환율 정보를 가져옵니다."""
        if target_currency == "KRW":
            rate = randint(130000, 145000) / 100
        else:
            rate = randint(80, 150) / 100
        return f"현재 {base_currency} 대비 {target_currency}의 환율은 {rate}입니다."

    @tool(approval_mode="never_require")
    def search_travel_docs(query: Annotated[str, Field(description="검색 키워드")]) -> str:
        """사내 지식베이스에서 여행 정보를 검색합니다."""
        results = st.session_state.collection.query(query_texts=[query], n_results=1)
        if results['documents'][0]:
            return f"관련 정보: {results['documents'][0][0]}"
        return "관련 정보를 찾을 수 없습니다."

    # 클라이언트 및 에이전트 설정
    deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")
    project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    client = AzureOpenAIResponsesClient(
        credential=AzureCliCredential(),
        deployment_name=deployment_name,
        project_endpoint=project_endpoint
    )

    agent = client.as_agent(
        instructions="""
        당신은 여행사 'MVPTour'의 상담원입니다. 정중하게 인사하고 여행 계획을 도와주세요.
        답변 끝에는 항상 '즐거운 여행의 시작, MVPTour입니다!'라는 문구를 붙여주세요.
        """,
        name="MVPTour-Assistant",
        tools=[get_weather, get_exchange_rate, search_travel_docs],
    )

    st.session_state.agent = agent
    st.session_state.chat_session = agent.create_session()
    st.session_state.messages = []
    st.session_state.agent_initialized = True

# --- 채팅 인터페이스 구현 ---

# 기존 대화 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("무엇을 도와드릴까요?"):
    # 1. 사용자 메시지 표시 및 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. 에이전트 응답 생성 (비동기 함수 실행)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("💡 생각 중...")
        
        async def get_agent_response():
            return await st.session_state.agent.run(prompt, session=st.session_state.chat_session)

        # Streamlit 내에서 비동기 코드 실행
        full_response = asyncio.run(get_agent_response())
        message_placeholder.markdown(full_response)
    
    # 3. 에이전트 메시지 저장
    st.session_state.messages.append({"role": "assistant", "content": full_response})