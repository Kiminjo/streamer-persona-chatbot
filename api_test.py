import os
from openai import OpenAI

API_KEY = "<YOUR API KEY>"
MODEL = "gpt-3.5-turbo"

client = OpenAI(api_key=API_KEY)

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


