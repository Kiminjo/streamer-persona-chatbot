# IO
from typing import Optional
from pathlib import Path

# ETC
import warnings

# Custom imports
from .factory import ModelFactory
from .vector_db import VectorDB
from .configs import system_prompt_template

class PersonaLLM:
    def __init__(self,
                 llm_type: str,
                 model_name: str,
                 embedding_model_name: Optional[str] = None,
                 api_key: Optional[str] = None,
                 db_path: str | Path = "vector_store/index.faiss",
                 ):
        if llm_type == "openai" and api_key is None:
            raise ValueError("API key must be provided for OpenAI LLM")

        # Initialize the params
        self.model_name = model_name
        self.embedding_model_name = embedding_model_name
        self.input_prompt = []

        # Initialize the LLM model
        self.llm = ModelFactory().create_model(llm_type=llm_type,
                                               api_key=api_key)

        # Load the database
        self.vector_db = VectorDB(llm_type=llm_type,
                                    embedding_model_name=embedding_model_name,
                                    api_key=api_key)
        self.vector_db.load(db_path)
        self.documents = self.vector_db.documents

    def generate(self,
                 prompt: str,
                 ) -> str:
        # Print warning if the prompt is empty
        if self.input_prompt == []:
            warnings.warn("System is empty. Please run 'search' method first.")

        # Update the input prompt
        self.input_prompt.append({"role": "user", "content": prompt})

        # Generate the response
        ai_response = self.llm.chat.completions.create(
              model=self.model_name,
              messages=self.input_prompt,
              temperature=0.7,
              )

        return ai_response.choices[0].message.content

    def search(self,
               query: str
               ) -> None:
        # Search the index
        idx = self.vector_db.search(query, k=1)
        related_doc = self.documents[idx[0]]

        # Update the input prompt
        system_prompt = system_prompt_template.format(information=related_doc, streamer_name="침착맨")
        self.input_prompt.append({"role": "system", "content": system_prompt})
