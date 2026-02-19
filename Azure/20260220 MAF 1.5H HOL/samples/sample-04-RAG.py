import asyncio
import os
from random import randint
from typing import Annotated

import chromadb # ChromaDB 라이브러리 추가
from agent_framework import tool
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
from pydantic import Field

# 1. 환경 변수 로드
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")
project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")

credential = AzureCliCredential()

# --- ChromaDB 설정 (RAG 준비) ---
# 메모리 기반의 간단한 ChromaDB 클라이언트를 생성합니다.
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="mvp_tour_info")

# 테스트용 여행 정보 데이터 추가 (실제 운영 시에는 PDF나 DB에서 로드)
collection.add(
    documents=[
        "시애틀 투어 패키지: 3박 4일 일정으로 스페이스 니들 입장권이 포함되어 있습니다.",
        "MVPTour 특별 환전 서비스: 본사 1층에서 오전 9시부터 오후 4시까지 우대 환율을 제공합니다.",
        "예약 취소 규정: 여행 7일 전까지는 100% 환불 가능하며, 이후에는 50% 수수료가 발생합니다."
    ],
    ids=["doc1", "doc2", "doc3"]
)

# 2. 클라이언트 및 에이전트 설정
client = AzureOpenAIResponsesClient(
    credential=AzureCliCredential(),
    deployment_name=deployment_name,
    project_endpoint=project_endpoint
)

# <define_tools>
@tool(approval_mode="never_require")
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    print(f"weather tool calling for {location}..")
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."

@tool(approval_mode="never_require")
def get_exchange_rate(
    base_currency: Annotated[str, Field(description="기준 통화 코드 (예: USD, EUR)")],
    target_currency: Annotated[str, Field(description="대상 통화 코드 (예: KRW, JPY)")],
) -> str:
    """두 통화 간의 환율 정보를 가져옵니다."""
    print(f"exchange rate tool calling for {base_currency} to {target_currency}..")
    if target_currency == "KRW":
        rate = randint(130000, 145000) / 100
    else:
        rate = randint(80, 150) / 100
    return f"현재 {base_currency} 대비 {target_currency}의 환율은 {rate}입니다."

@tool(approval_mode="never_require")
def search_travel_docs(
    query: Annotated[str, Field(description="여행 상품이나 회사 규정에 대해 검색할 키워드")],
) -> str:
    """사내 지식베이스(ChromaDB)에서 여행 상품 및 정책 정보를 검색합니다."""
    print(f"RAG tool calling: searching for '{query}'..")
    # ChromaDB에서 유사도 검색 수행
    results = collection.query(query_texts=[query], n_results=1)
    
    if results['documents'][0]:
        return f"관련 정보 검색 결과: {results['documents'][0][0]}"
    else:
        return "관련된 정보를 찾을 수 없습니다. 상담원에게 직접 문의해주세요."
# </define_tools>

agent = client.as_agent(
    instructions="""
    당신은 여행사 'MVPTour'의 상담원입니다. 
    고객에게 정중하게 인사하고, 여행 계획에 대해 도움을 줄 준비가 되었음을 알리세요.
    날씨, 환율 정보뿐만 아니라 사내 여행 상품이나 규정에 대해서도 'search_travel_docs'를 통해 답변할 수 있습니다.
    답변 끝에는 항상 '즐거운 여행의 시작, MVPTour입니다!'라는 문구를 붙여주세요.
    """,
    name="MVPTour-Assistant",
    tools=[get_weather, get_exchange_rate, search_travel_docs], # RAG 툴 추가
)

async def main():
    print(f"✅ 에이전트 '{agent.name}'가 준비되었습니다.")
    session = agent.create_session()

    # 1. 일반 날씨 질문
    user_input = "안녕하세요! 시애틀 날씨 알려주세요."
    result = await agent.run(user_input, session=session)
    print(f"Agent: {result}\n")
    
    # 2. RAG 기반 질문 (상품 정보 검색)
    user_input = "시애틀 투어 패키지 구성은 어떻게 되나요?"
    result = await agent.run(user_input, session=session)
    print(f"Agent: {result}\n")

    # 3. RAG 기반 질문 (취소 규정 검색)
    user_input = "여행을 취소하면 환불을 얼마나 받을 수 있나요?"
    result = await agent.run(user_input, session=session)
    print(f"Agent: {result}\n")

if __name__ == "__main__":
    asyncio.run(main())