import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
import os   

from typing import Annotated
from pydantic import Field
from agent_framework import ai_function

from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import streamlit as st

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
key = os.getenv("AZURE_SEARCH_KEY")
index = os.getenv("AZURE_SEARCH_INDEX")

client = SearchClient(endpoint, index, AzureKeyCredential(key))

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

@ai_function(name="tesla_docs", description="Search tesla documents from Azure AI Search")
def search_docs(
    query: Annotated[str, Field(description="Keyword to search documents")]
) -> str:
    results = client.search(search_text=query, top=5)
    compiled = []
    for item in results:
        compiled.append(f"- {item['title']}: {item['content'][:120]}...")
    return "\n".join(compiled)

agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    instructions="You are a helpful assistant",
    tools=[get_weather, search_docs]
)

async def main():
    question = st.text_input("Ask a question:")
    button_click = st.button("Ask")

    if button_click:
        result = await agent.run(question)
        #result = await agent.run("How is Tesla’s low-voltage battery charged?")
        st.write(result.text)

asyncio.run(main())