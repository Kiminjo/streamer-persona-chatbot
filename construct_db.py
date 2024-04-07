from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from typing import Union
from pathlib import Path 
import warnings

# Custom functions
from preprocessing import get_txt_file, text_split, get_api_key

warnings.filterwarnings("ignore")

def preprocessing(doc_src: Union[str, Path],
                  api_src: Union[str, Path],
                  chunk_size: int = 30,
                  separator: str = '\n\n',
                  chunk_overlap: int = 0):
    if isinstance(doc_src, Path):
        doc_src = str(doc_src)
    
    # Get the text from the document and split it into chunks
    text = get_txt_file(doc_src)
    document = text_split(text,
                          chunk_size=chunk_size,
                          separator=separator,
                          chunk_overlap=chunk_overlap)

    # Get the API key for the OpenAI model
    api_key = get_api_key(api_src)

    return document, api_key

def main():
    data_src = "data/data.txt"
    api_src = "openai_api.txt"
    db_path = "vector_store/"
    
    # Preprocess the document
    document, api_key = preprocessing(data_src, api_src)
    
    # Load the OpenAI embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)

    # Create the vector store
    db = FAISS.from_documents(document, embeddings)

    # Save the vector store
    db.save_local(db_path)
    print(f"Database saved to {db_path}")

if __name__ == '__main__':
    main()