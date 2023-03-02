import openai

messagehistory = [
    {"role": "user", "content": "You are a helpful assistant called Sherlock. Your personality is vaguely based off of Sherlock Holmes."},
]

def add_history(text, role="user"):
    messagehistory.append({"role": role, "content": text})


async def chat(text):
    add_history(text)
    ans = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=messagehistory,
    )
    m = ans.choices[0].message
    messagehistory.append(m)

    return m.content
