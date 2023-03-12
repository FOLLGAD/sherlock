import shell
from openai import ChatCompletion

# to add:
# - add_note (connect to notion db maybe)
# - report_emotion (also connect to notion db)

python_code_symbol = "python(homeassistant)"

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
    {"role": "assistant", "content": f"""
```{python_code_symbol}
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
    if f"```{python_code_symbol}" in m.content:
        split = m.content.split(f"```{python_code_symbol}")
        code = split[1].split("```")[0].strip()
        content = split[0] + split[1].split("```")[1]
        # execute code (warning: prob not very safe)
        print("Executing code:", code)
        shell.run(code)
        print("Executed code.")

    return content
