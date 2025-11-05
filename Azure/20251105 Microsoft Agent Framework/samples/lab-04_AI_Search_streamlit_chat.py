import os
import asyncio
from typing import Annotated, Optional

import streamlit as st
from dotenv import load_dotenv
from pydantic import Field

from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import ai_function

from azure.identity import AzureCliCredential
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

# Load local .env next to this file (keeps secrets out of source)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
key = os.getenv("AZURE_SEARCH_KEY")
index = os.getenv("AZURE_SEARCH_INDEX")

client = SearchClient(endpoint, index, AzureKeyCredential(key))

agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    instructions="You are a helpful assistant",
    tools=get_weather
)


st.page_title="AI Search Chat"

# ---- Tools ---------------------------------------------------------------
@ai_function(name="weather_tool", description="Retrieves weather information for any location")
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location (demo tool)."""
    return f"The weather in {location} is cloudy with a high of 15°C."

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


# ---- UI: Chat -----------------------------------------------------------
st.title("AI Search Chat 🔎")
st.caption("Ask questions; the assistant can call tools (weather, tesla_docs) when helpful.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요?"}
    ]

# Render history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("메시지를 입력하세요…")
if prompt:
    # Show user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Run the agent for a reply
    assistant_text = ""
    try:
        # Agent uses asyncio; run synchronously in Streamlit
        result = asyncio.run(agent.run(prompt))
        assistant_text = getattr(result, "text", str(result))
    except Exception as e:
        assistant_text = f"응답 중 오류가 발생했습니다: {e}"

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(assistant_text)

    # Persist assistant reply
    st.session_state.messages.append({"role": "assistant", "content": assistant_text})
