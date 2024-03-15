from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Custom functions
from preprocessing import get_api_key

def get_vector_store(db_path: str, 
                     api_key: str):
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    db = FAISS.load_local(db_path, 
                          embeddings,
                          allow_dangerous_deserialization=True)
    return db 

def main():
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

    # Chat with the chatbot
    test_prompt = "유퀴즈 출연 후 아쉬웠던 점?"
    result = chatbot(test_prompt)

    print(result["query"])
    print(result["result"])
    print(result['source_documents'])

if __name__ == '__main__':
    main()