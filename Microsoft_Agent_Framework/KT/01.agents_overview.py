from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import DefaultAzureCredential

from dotenv import load_dotenv
load_dotenv(".env")

async def main():
    async with (
        DefaultAzureCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            instructions="You are an assistant for the customers of the Chinese restaurant Greatwall."
        ) as agent
    ):

        response = await agent.run("Hello!")
        print(response.text)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())