import requests
import os

api_key = os.environ.get("OPENAI_API_KEY")
db_path = "vector_store/"
url = "http://127.0.0.1:8000/chat"

prompt = input()

output = requests.post(url, json={"api_key": api_key,
                                  "db_path": db_path,
                                  "prompt": prompt})

print(output.json()["output"])
