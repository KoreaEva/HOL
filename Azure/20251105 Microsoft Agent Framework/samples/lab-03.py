import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
from agent_framework import ChatMessage, TextContent, UriContent, Role
import os   

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    name="VisionAgent",
    instructions="You are a helpful agent that find information"
)

# async def main():
#     thread = agent.get_new_thread()

#     result1 = await agent.run("Tell me a joke about a pirate.", thread=thread)
#     print(result1.text)

#     result2 = await agent.run("Now add some emojis to the joke and tell it in the voice of a pirate's parrot.", thread=thread)
#     print(result2.text)
    

async def main():
    thread1 = agent.get_new_thread()
    thread2 = agent.get_new_thread()

    result1 = await agent.run("Tell me a joke about a pirate.", thread=thread1)
    print(result1.text)

    result2 = await agent.run("Tell me a joke about a robot.", thread=thread2)
    print(result2.text)

    result3 = await agent.run("Now add some emojis to the joke and tell it in the voice of a pirate's parrot.", thread=thread1)
    print(result3.text)

    result4 = await agent.run("Now add some emojis to the joke and tell it in the voice of a robot.", thread=thread2)
    print(result4.text)

asyncio.run(main())