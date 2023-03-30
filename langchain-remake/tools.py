from langchain.agents import tool
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage, ChatMessage
import requests
from ha import ha_entities
import shell


@tool("Play Music", return_direct=True)
def music_tool(query: str) -> str:
    """Useful for playing music. The input to this command should be a string containing a JSON object with at least one of the following keys: 'artist', 'album', 'song', 'playlist'."""
    print(query)
    return "OK!"


@tool("Play Music", return_direct=True)
def music_tool(query: str) -> str:
    """Useful for playing music. The input to this command should be a string containing a JSON object with at least one of the following keys: 'artist', 'album', 'song', 'playlist'."""
    print(query)
    return "OK!"

def parse_code(code: str) -> str:
    if "```python" in code:
        code = code[code.index("```python") + 9 :]
        code = code[: code.index("```")]
    elif "```" in code:
        code = code[code.index("```") + 3 :]
        code = code[: code.index("```")]
    return code

class HomeAssistantTool:
    description = "The user has a Home Assistant setup. This starts the process for changing things like lights, cameras etc. Use this tool whenever the user needs that sort of thing. Has modes and alerts."
    llm: ChatOpenAI = None

    def __init__(self, llm):
        self.llm = llm

    async def arun(self, query: str) -> str:
        entities = ""

        if "ENTITY(" in query:
            entity_keyword = query[query.index("ENTITY(") + 7 : query.index(")")]
            query = query.replace(f"ENTITY({entity_keyword})", "")
            all_entities = ha_entities()
            entities = [e for e in all_entities if entity_keyword.lower() in e.lower()]

        res = self.llm.generate(
            [
                [
                    SystemMessage(
                        content=f"""
The user has a Home Assistant setup. This starts the process for changing things like lights, cameras etc. Use this tool whenever the user needs that sort of thing. Has modes and alerts.
Write a python script that performs the action using the Home Assistant REST API using python's requests library. Environment variables are defined as HASS_SERVER and HASS_TOKEN.

Respond with only python code inside one unique code block, and nothing else. do not write explanations. do not type commands unless I instruct you to do so

Entities available:
{entities}
"""
                    ),
                    HumanMessage(content=query),
                ]
            ]
        )

        code = res.generations[0][0].text
        code = parse_code(code)
        print("CODEEEE", code)
        out = await shell.run(code)
        print(out)
        return "OK!"
