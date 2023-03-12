from openai import ChatCompletion

# to add:
# - add_note (connect to notion db maybe)
# - report_emotion (also connect to notion db)


preprompts = [
    {"role": "user", "content": """
You are a helpful assistant called Sherlock. Your personality is based off of Sherlock Holmes. For messages where you need to perform an action you should prepend actions to take in the form of a Python script. 
Available functions: 
- `lights(state: bool, brightness_percent: int | None = None, brightness_step: int | None = None, rgbww: Tuple[int, int, int, int, int] | None = None)`
- `play_music(song: str | None)`
- `disco_mode(state: bool)`
- `cringe_alert(state: bool)`
    """},
    {"role": "user", "content": "turn on the lights"},
    {"role": "assistant", "content": """
```python(homeassistant)
lights(True)
```
The lights have been turned on.
"""},
]
messagehistory = []

MSG_LIM = 6


def add_history(text, role="user"):
    global messagehistory
    messagehistory.append({"role": role, "content": text})
    if len(messagehistory) > MSG_LIM:
        messagehistory = messagehistory[-MSG_LIM:]


async def chat(text):
    add_history(text)
    ans = await ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=preprompts + messagehistory,
    )
    m = ans.choices[0].message
    content = m.content
    messagehistory.append(m)

    # remove the python code and store in variable (can be located anywhere in response)
    if "```python" in m.content:
        split = m.content.split("```python(homeassistant)")
        code = split[1].split("```")[0].strip()
        content = split[0] + split[1].split("```")[1]
        # execute code (warning: prob not very safe)
        print("Executing code:", code)
        try:
            exec(
                f"""
# timeout after 10 seconds
import signal
def signal_handler(signum, frame):
    raise Exception("Timed out!")
signal.signal(signal.SIGALRM, signal_handler)
signal.alarm(10)

# execute code
from home import lights, cringe_alert, play_music, disco_mode
{code}
"""
            )
        except Exception as e:
            print("Error executing code:", e)
        print("Executed code.")

    return content
