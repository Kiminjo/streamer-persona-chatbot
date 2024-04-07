from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

import chainlit as cl 
from typing import Union

# Custom functions
from preprocessing import get_api_key

def get_vector_store(db_path: str, 
                     api_key: str):
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    db = FAISS.load_local(db_path, 
                          embeddings,
                          allow_dangerous_deserialization=True)
    return db 


db_path = "vector_store/"
api_src = "openai_api.txt"

# Get the API key for the OpenAI model
api_key = get_api_key(api_src)

# Load the vector store
db = get_vector_store(db_path, api_key)

# Create the chat model
chat_model = ChatOpenAI(openai_api_key=api_key)

# Create the retrieval model
retriever = db.as_retriever()

# Create the chatbot
chatbot = RetrievalQA.from_llm(
    llm=chat_model,
    retriever=retriever,
    return_source_documents=True
)

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="준비되었습니다. 메시지를 입력하세요.").send()

@cl.on_message
async def on_message(prompt: Union[str, cl.Message]):
    if isinstance(prompt, cl.Message):
        prompt = prompt.content
    print(f"입력된 메시지: {prompt}")
    result = chatbot(prompt)
    answer = result["result"]
    await cl.Message(content=answer).send()

    # # Chat with the chatbot
    # test_prompt = "유퀴즈 출연 후 아쉬웠던 점?"
    # result = chatbot(test_prompt)

    # print(result["query"])
    # print(result["result"])
    # print(result['source_documents'])
