from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def get_vector_store(db_path: str, 
                     api_key: str):
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    db = FAISS.load_local(db_path, 
                          embeddings,
                          allow_dangerous_deserialization=True)
    return db 