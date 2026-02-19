import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv, dotenv_values
from azure.identity import AzureCliCredential
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import ChatAgent, ChatMessage, TextContent, Role

# 1. 환경 변수 로드
load_dotenv(dotenv_path="./.env")

# .env 파일에서 필요한 정보들
env_path = Path(__file__).parent / ".env"
env_vars = dotenv_values(env_path)

deployment_name = env_vars.get("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4.1-mini")

# 클라이언트 설정 - Azure CLI 자격증명 사용
client = AzureOpenAIChatClient(
    credential=AzureCliCredential(),
    deployment_name=deployment_name
)

# 에이전트 생성
agent = client.create_agent(
    name="MVPTour-Assistant",
    instructions="""
    당신은 여행사 'MVPTour'의 상담원입니다. 
    고객에게 정중하게 인사하고, 여행 계획에 대해 도움을 줄 준비가 되었음을 알리세요.
    답변 끝에는 항상 '즐거운 여행의 시작, MVPTour입니다!'라는 문구를 붙여주세요.
    """
)

async def main():
    print(f"✅ 에이전트 '{agent.name}'가 준비되었습니다.")

    # 대화 실행
    user_input = "안녕하세요! 도쿄 여행 패키지 추천해 주세요."
    print(f"\n[나]: {user_input}")
    
    # 메시지 생성
    message = ChatMessage(
        role=Role.USER,
        contents=[TextContent(text=user_input)]
    )
    
    # 스트리밍으로 응답 받기
    print("[상담원]: ", end="", flush=True)
    async for update in agent.run_stream(message):
        if update.text:
            print(update.text, end="", flush=True)
    print()  # 줄바꿈

if __name__ == "__main__":
    asyncio.run(main())