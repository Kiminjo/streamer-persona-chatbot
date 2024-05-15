# IO
import pickle
import numpy as np
from pathlib import Path
from typing import List

# Faiss
import faiss

# Custom imports
from .factory import ModelFactory

class VectorDB:
    def __init__(self,
                 llm_type: str,
                 embedding_model_name: str,
                 api_key: str,
                 ):
        # Initialize the params
        self.embedding_model_name = embedding_model_name

        # Initialize the LLM model
        self.llm = ModelFactory().create_model(llm_type=llm_type,
                                               api_key=api_key)

    def get_embedding(self,
                       doc: str
                       ) -> np.array:

        return self.llm.embeddings.create(input = [doc],
                                        model=self.embedding_model_name).data[0].embedding

    def build_index(self,
                    docs: List[str]
                    ) -> None:
        # Get the embeddings
        embeddings = [self.get_embedding(doc) for doc in docs]
        embeddings = np.array(embeddings)

        # Build the index
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

        # Save the documents
        self.documents = docs

    def search(self,
               query: str,
               k: int
               ) -> List[int]:
        # Get the embedding of the query
        query_embedding = np.array(self.get_embedding(query))

        # Search the index
        query_embedding = query_embedding.reshape(1, -1)
        _, idx = self.index.search(query_embedding, k)

        return idx[0].tolist()

    def save(self,
             db_path: str
             ) -> None:
        faiss.write_index(self.index, db_path)
        with open(Path(db_path).with_suffix(".pkl"), "wb") as f:
            pickle.dump(self.documents, f)

    def load(self,
            db_path: str
            ) -> None:
        self.index = faiss.read_index(db_path)
        with open(Path(db_path).with_suffix(".pkl"), "rb") as f:
            self.documents = pickle.load(f)
