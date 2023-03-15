from langchain.agents import Tool, initialize_agent
from langchain.tools import BaseTool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAIChat, OpenAI
from langchain.memory import ConversationBufferMemory
import subprocess

from home import lights

llm = OpenAIChat(temperature=0)

c = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        template="{input}",
        input_variables=["input"]
    )
)

import json
def lampchange(injson):
    j = json.loads(injson)
    out = subprocess.check_output(["hass-cli", "--columns", "entity_id,name,area,platform", "entity", "list", "light|scene|script|input"])
    out = out.decode("utf-8")
    print(out)
    print("Searching for", j['entities'])
    res = c.run("Home Assistant entities available:\n"+out+ "\n\n" + f"Which ones best fit this description: {j['entities']}? Answer with a JSON array of entity_ids, or empty list [].")
    entities = json.loads(res)
    print(entities)
    for entity in entities:
        lights(entity, brightness_percent = j.get("brightness", None), brightness_step = j.get("brightness_step", None), rgbww = j.get("rgbww", None))

    return f"Successfully changed lights"


TOOLS = [
    Tool(
        name ="Change lamps",
        func=lampchange,
        description="""Change the light of a lamp. Use JSON format: `{{ "entities": *description of lights that should change*, "rgbww": [255, 0, 255, 50, 0] | null, "brightness": percent | null, "brightness_step": percent | null }}`""",
    ),
]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(TOOLS, llm, agent="conversational-react-description", verbose=True, memory=memory)

while True:
    i = input("ask smth:")
    res = agent.run(input=i)
    print(res)

