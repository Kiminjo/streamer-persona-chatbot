import os
from openai import OpenAI

# Read API Key 
with open("../openai_api.txt", "r") as f: 
    api_key = f.readline()
    f.close()

MODEL = "gpt-3.5-turbo"

client = OpenAI(api_key=api_key)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "안녕 만나서 반가워",
        }
    ],
    model=MODEL,
)

print(chat_completion.choices[0].message.content)


