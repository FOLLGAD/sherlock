import openai

preprompts = [
    {"role": "user", "content": "You are a helpful assistant called Sherlock. Your personality is vaguely based off of Sherlock Holmes."},
]
messagehistory = []

def add_history(text, role="user"):
    global messagehistory
    messagehistory.append({"role": role, "content": text})
    if len(messagehistory) > 6:
        messagehistory = messagehistory[-6:]


async def chat(text):
    add_history(text)
    ans = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=preprompts + messagehistory,
    )
    m = ans.choices[0].message
    messagehistory.append(m)

    return m.content
