import os
from groq import Groq

api_key = os.environ["GROQ_API_KEY"]
MODEL = "llama3-70b-8192"

# Set LLM Client 
client = Groq(api_key=api_key)

# Set chatting 
chat_completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content" : "you are a helpful assistant."}, 
        {"role" : "user", "content" : "who is the president of South Korea?"},
    ],
    model=MODEL,
    # response_format={"type": "json_object"},
    temperature = 0.5, # 창의성 허락수준
    max_tokens = 1024, # 최대 토큰수
    top_p = 1, # 샘플링시 상위값 가져올 확률
    stop = None, # api 답변 중지 시점
    stream = False # 스트림 형식으로 response 전달
)

# Print response
print(chat_completion.choices[0].message.content)