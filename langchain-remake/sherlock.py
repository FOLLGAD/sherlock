import os
os.environ["LANGCHAIN_HANDLER"] = "langchain"

from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper, BashProcess
from langchain.agents import initialize_agent
from langchain.agents.tools import Tool
from tools import music_tool, HomeAssistantTool

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2, verbose=True)

search = SerpAPIWrapper()
bash = BashProcess()
ha_tool = HomeAssistantTool(llm)

tools = [
    Tool(
        name = "Google Search",
        func=search.run,
        description="Useful for when you need to answer questions about current events or the current state of the world. the input to this should be a single search term."
    ),
    Tool(
        name = "Terminal",
        func=bash.run,
        description="Useful for typing bash commands for the terminal."
    ),
    Tool(
        name = "Home Assistant Control",
        func=ha_tool.arun,
        coroutine=ha_tool.arun,
        description="The user has a Home Assistant setup. This starts the process for changing things like lights, cameras etc. Use this tool whenever the user needs that sort of thing. Has modes and alerts. The input should be a standalone query containing all context necessary. The command should follow this format: `ENTITY(entity_keyword) Full user command with context`, example: `ENTITY(light) Turn off all lights`"
    ),
    music_tool,
    # Tool(
    #     name = "Play Music",
    #     func=music_tool,
    #     description="Useful for playing music. The input to this command should be a JSON object with at least one of the following keys: 'artist', 'album', 'song', 'playlist'."
    # ),
]
agent_chain = initialize_agent(tools, llm, agent="chat-conversational-react-description", verbose=True, memory=memory)

async def main():
    while True:
        res = await agent_chain.arun(input=input("sven:"))
        print(res)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())