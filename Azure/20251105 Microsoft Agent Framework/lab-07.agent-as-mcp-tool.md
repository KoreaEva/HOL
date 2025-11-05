# 에이전트를 MCP 도구로 노출

## 프로그래밍 언어 선택

이 자습서에서는 **MCP(Model Context Protocol)** 를 통해  
에이전트를 도구 형태로 노출하여, MCP 도구를 지원하는 다른 시스템에서  
해당 에이전트를 사용할 수 있도록 하는 방법을 설명합니다.

---

## 필수 조건

필수 구성 요소 및 Python 패키지 설치는  
이 자습서의 **간단한 에이전트 만들기 및 실행** 단계를 참조하세요.

---

## 에이전트를 MCP 서버로 노출

`as_mcp_server()` 메서드를 통해  
에이전트를 **MCP 서버**로 노출할 수 있습니다.

이렇게 하면 MCP 호환 클라이언트에서  
에이전트가 도구처럼 호출될 수 있습니다.

---

### 1) MCP 서버로 노출할 에이전트 생성

에이전트에 함수 도구를 등록할 수도 있습니다.

```python
from typing import Annotated
from agent_framework.openai import OpenAIResponsesClient

def get_specials() -> Annotated[str, "Returns the specials from the menu."]:
    return """
        Special Soup: Clam Chowder
        Special Salad: Cobb Salad
        Special Drink: Chai Tea
        """

def get_item_price(
    menu_item: Annotated[str, "The name of the menu item."],
) -> Annotated[str, "Returns the price of the menu item."]:
    return "$9.99"

# Create an agent with tools
agent = OpenAIResponsesClient().create_agent(
    name="RestaurantAgent",
    description="Answer questions about the menu.",
    tools=[get_specials, get_item_price],
)
````

---

### 2) MCP 서버 인스턴스 생성

`as_mcp_server()` 호출을 통해 MCP 서버 객체를 생성합니다.

```python
# Expose the agent as an MCP server
server = agent.as_mcp_server()
```

에이전트의 **name** 과 **description** 은
MCP 서버의 메타데이터로 활용됩니다.

---

### 3) 표준 입출력을 통해 요청 수신

MCP 서버를 실행하려면
표준 입력/출력 스트림을 통해 통신하도록 구성해야 합니다.

```python
import anyio
from mcp.server.stdio import stdio_server

async def run():
    async def handle_stdin():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    await handle_stdin()

if __name__ == "__main__":
    anyio.run(run)
```

---

## 결과

위 코드를 실행하면 MCP 프로토콜을 통해 에이전트를 노출하는
**MCP 서버**가 시작되며,

예:

* VS Code GitHub Copilot Agents
* 기타 MCP 호환 클라이언트

에서 tool 형태로 사용할 수 있게 됩니다.


