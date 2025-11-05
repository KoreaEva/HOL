import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
import os   

from typing import Annotated
from pydantic import Field
from agent_framework import ai_function

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C."

# @ai_function(name="weather_tool", description="Retrieves weather information for any location")
# def get_weather(
#     location: Annotated[str, Field(description="The location to get the weather for.")],
# ) -> str:
#     return f"The weather in {location} is cloudy with a high of 15°C."


agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    instructions="You are a helpful assistant",
    tools=get_weather
)

async def main():
    result = await agent.run("What is the weather like in Amsterdam?")
    print(result.text)

asyncio.run(main())