import asyncio
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

async def main():
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(
            project_endpoint="https://winkey-openai-1029.services.ai.azure.com/api/projects/winkey-greatwall-project",
            model_deployment_name="gpt-4o-mini",
            async_credential=credential,
            agent_name="HelperAgent"
        ).create_agent(
            instructions="You are an assistant for the customers of the Chinese restaurant Greatwall."
        ) as agent,
    ):
        result = await agent.run("Hello!")
        print(result.text)

asyncio.run(main())