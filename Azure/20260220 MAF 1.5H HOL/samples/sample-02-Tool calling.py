
import asyncio
import os
from random import randint
from typing import Annotated

from agent_framework import tool
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
from pydantic import Field

# 1. 환경 변수 로드 (첫 번째 소스 코드 스타일 적용)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")
project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")

credential = AzureCliCredential()

# 2. 클라이언트 및 에이전트 설정
client = AzureOpenAIResponsesClient(
    credential=AzureCliCredential(),
    deployment_name=deployment_name,
    project_endpoint=project_endpoint
)

# Use "always_require" in production for user confirmation before tool execution.
@tool(approval_mode="never_require")
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    print("weather tool calling..")
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."
# </define_tool>

# <define_tool>
@tool(approval_mode="never_require")
def get_exchange_rate(
    base_currency: Annotated[str, Field(description="기준 통화 코드 (예: USD, EUR)")],
    target_currency: Annotated[str, Field(description="대상 통화 코드 (예: KRW, JPY)")],
) -> str:
    """두 통화 간의 환율 정보를 가져옵니다."""
    print("exchange rate tool calling..")
    
    # randint를 사용하여 환율 생성 (예: 130000 ~ 145000 사이 정수 생성 후 100으로 나눔)
    # KRW(원화)일 경우와 그 외의 경우를 나누어 처리합니다.
    if target_currency == "KRW":
        rate = randint(130000, 145000) / 100  # 예: 1350.55
    else:
        rate = randint(80, 150) / 100         # 예: 1.25
        
    return f"현재 {base_currency} 대비 {target_currency}의 환율은 {rate}입니다."
# </define_tool>

agent = client.as_agent(
    instructions="""
    당신은 여행사 'MVPTour'의 상담원입니다. 
    고객에게 정중하게 인사하고, 여행 계획에 대해 도움을 줄 준비가 되었음을 알리세요.
    답변 끝에는 항상 '즐거운 여행의 시작, MVPTour입니다!'라는 문구를 붙여주세요.
    """,
    name="MVPTour-Assistant",

    tools=[get_weather,get_exchange_rate],
)



async def main():
    print(f"✅ 에이전트 '{agent.name}'가 준비되었습니다.")

    # 사용자 입력 및 메시지 구성
    #user_input = "안녕하세요! 시애틀의 날씨는 어떤가요?"
    user_input = "지금 원화 대비 달러의 환율은 어떤가요?"
    print(f"\n[나]: {user_input}")
    

    
    # 3. 스트리밍 응답 실행
    # Non-streaming: get the complete response at once
    result = await agent.run(user_input)
    print(f"Agent: {result}")

if __name__ == "__main__":
    asyncio.run(main())