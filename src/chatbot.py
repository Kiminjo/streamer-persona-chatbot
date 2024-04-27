# Langchain Module 
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# Custom Module
from .utils.vector_db import get_vector_store

class PersonaChatbot:
    def __init__(self, 
                 api_key: str, 
                 db_path: str
                 ):
        self.api_key = api_key
        self.db_path = db_path
        self.chatbot = self._get_model_()

    def _get_model_(self):
        db = get_vector_store(self.db_path, self.api_key)
        chat_model = ChatOpenAI(openai_api_key=self.api_key)
        retriever = db.as_retriever()
        
        chatbot = RetrievalQA.from_llm(
            llm=chat_model,
            retriever=retriever,
            return_source_documents=True
        )
        return chatbot

    def chat(self, prompt: str):
        result = self.chatbot(prompt)
        return result["result"]


