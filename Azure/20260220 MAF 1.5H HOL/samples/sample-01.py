import asyncio
import os
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

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

agent = client.as_agent(
    instructions="""
    당신은 여행사 'MVPTour'의 상담원입니다. 
    고객에게 정중하게 인사하고, 여행 계획에 대해 도움을 줄 준비가 되었음을 알리세요.
    답변 끝에는 항상 '즐거운 여행의 시작, MVPTour입니다!'라는 문구를 붙여주세요.
    """,
    name="MVPTour-Assistant"
)

async def main():
    print(f"✅ 에이전트 '{agent.name}'가 준비되었습니다.")

    # 사용자 입력 및 메시지 구성
    user_input = "안녕하세요! 도쿄 여행 패키지 추천해 주세요."
    print(f"\n[나]: {user_input}")
    

    
    # 3. 스트리밍 응답 실행
    # Non-streaming: get the complete response at once
    result = await agent.run(user_input)
    print(f"Agent: {result}")

if __name__ == "__main__":
    asyncio.run(main())