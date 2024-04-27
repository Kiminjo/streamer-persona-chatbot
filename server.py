# Custom Module
from src import PersonaChatbot

# API
from fastapi import FastAPI
from pydantic import BaseModel

# Create the FastAPI app
app = FastAPI()

class APIKey(BaseModel):
    api_key: str

class ChatComponent(BaseModel):
    prompt: str
    api_key: str
    db_path: str

@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/chat/")
def chat_with_bot(chat_component: ChatComponent) -> dict:
    model = PersonaChatbot(api_key=chat_component.api_key,
                           db_path=chat_component.db_path)
    result = model.chat(chat_component.prompt)
    return {"output": result}

# @app.post("/get_model")
# def get_chatbot(api_key: APIKey) -> PersonaChatbot:
#     chatbot = PersonaChatbot(api_key.api_key)
#     return {"model": chatbot}

# @app.post("/chat/")
# def chat_with_bot(model_prompt: ChatPrompt=Depends(get_chatbot)) -> dict:
#     model = model_prompt.chatbot
#     result = model.chat(model_prompt.prompt)
#     return {"response": result}

