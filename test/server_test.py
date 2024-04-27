import requests
import os 

api_key = os.environ.get("OPENAI_API_KEY")
db_path = "vector_store/"
url = "http://127.0.0.1:8000/chat"

output = requests.post(url, json={"api_key": api_key, 
                                  "db_path": db_path,
                                  "prompt": "유퀴즈 출연 후 아쉬웠던 점?"})

print(output.json()["output"])