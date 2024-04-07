from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

from typing import Union
from pathlib import Path

def get_txt_file(src: str):
    loader = TextLoader(src, 
                        encoding='utf-8')
    return loader.load()

def text_split(text: list[str],
               chunk_size: int = 30,
               separator: str = '\n\n',
               chunk_overlap: int = 0):
    splitter = CharacterTextSplitter(chunk_size=chunk_size,
                                     separator=separator,
                                     chunk_overlap=chunk_overlap)
    return splitter.split_documents(text)

def get_api_key(src: Union[str, Path]):
    with open(src, 'r') as f:
        return f.read()