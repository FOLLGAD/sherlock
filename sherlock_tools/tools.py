from multiprocessing.process import BaseProcess
from langchain import GoogleSerperAPIWrapper
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage, ChatMessage
from sherlock_tools.home_assistant import ha_entities, play_music
import sherlock_tools.shell as shell
import sherlock_tools.spotify_search as spotify_search
import json


def remove_backticks(query):
    # query can have 0, 1 or 3 backticks surrounding the command. remove them if they exist
    if query.startswith("```") and query.endswith("```"):
        query = query[3:-3]
    elif query.startswith("`") and query.endswith("`"):
        query = query[1:-1]
    return query


search = GoogleSerperAPIWrapper()
bash = BaseProcess()


async def bash_tool(query):
    return bash.run(remove_backticks(query))


async def search_tool(query):
    return (
        search.run(query)
        + "\n\nImportant note: If none of the above results were helpful, feel free to ignore it"
    )


async def music_tool(query: str) -> str:
    """Useful for playing music. The input to this command should be a string containing a JSON object with at least one of the following keys: 'artist', 'album', 'song', 'playlist'."""
    artist, album, song, playlist, enqueue = None, None, None, None, "play"
    # parse query as json object
    print(query)
    try:
        query = json.loads(remove_backticks(query))
        artist = query.get("artist")
        album = query.get("album")
        song = query.get("song")
        playlist = query.get("playlist")
        enqueue = query.get("enqueue")
    except:
        pass

    if not any([artist, album, song, playlist]):
        return "Error: No music specified"

    result, music_type = spotify_search.search(
        artist=artist, album=album, song=song, playlist=playlist
    )

    res = play_music(result["uri"], enqueue=enqueue)
    if res != 200:
        print(res)
        return "Failed"

    return f"Now playing {music_type} {result['name']}"


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
            header = all_entities[0]
            entities = [header] + [
                e for e in all_entities[1:] if entity_keyword.lower() in e.lower()
            ]

        res = self.llm.generate(
            [
                [
                    SystemMessage(
                        content=f"""
The user has a Home Assistant setup. This starts the process for changing things like lights, cameras etc. Use this tool whenever the user needs that sort of thing. Has modes and alerts.
Write a python script that performs the action using the Home Assistant REST API using python's requests library. Environment variables are defined as HASS_SERVER and HASS_TOKEN.

Respond with only python code inside one unique code block, and nothing else. do not write explanations. do not type commands unless I instruct you to do so
Whatever is printed to the console will be sent to the user. If you want to send a message to the user, use the print function.
"""
                    ),
                    HumanMessage(content=query),
                    SystemMessage(
                        content=f"""
Available Home Assistant entities:
```
{entities}
```
Based on the query, select an entity that best fits the query and write the code. Assume HASS_SERVER, HASS_TOKEN are already defined.
"""
                    ),
                ]
            ]
        )

        print(res.generations[0][0].text)

        code = res.generations[0][0].text
        code = parse_code(code)
        out = await shell.run(code)
        return out
