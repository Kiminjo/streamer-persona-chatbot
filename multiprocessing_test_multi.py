from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import time
from multiprocessing import Process
import chainlit as cl 

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


queries = ["유퀴즈하고 아쉬웠던 점은 무엇인가요?", 
           "유퀴즈 할때 아쉬운점",
           "유퀴즈 찍을때 아쉬웠던 점",
           "유퀴즈하고 아쉬웠던 점", 
            ]

def quesition(query):
    start_time = time.time()
    docs = db.similarity_search(query)
    end_time = time.time()
    print(f"Query: {query}")
    print(f"Matched doc: {docs[0].page_content}")
    print(f"Time: {end_time - start_time}")
    print("----------------------------------")
    return True


if __name__ == '__main__':

    start=time.time()
    p1=Process(target=quesition, args=(queries[0],))
    p2=Process(target=quesition, args=(queries[1],))
    p3=Process(target=quesition, args=(queries[2],))
    p4=Process(target=quesition, args=(queries[3],))

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    end=time.time()

    print("MultiProcessing : ", end-start)
    print("\n")
    print("----------------------------------")