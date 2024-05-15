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
    """
    Vector database class

    Attributes:
    ----------
    llm_type: str
        The type of the LLM model

    embedding_model_name: str
        The name of the embedding model

    api_key: str
        The API key for the LLM model

    index: faiss object
        The index object

    documents: List[str]
        The list of documents

    Examples:
    ---------
    >>> vector_db = VectorDB(llm_type="openai",
                             embedding_model_name="text-embedding",
                             api_key="api_key")
    >>> vector_db.load("vector_store/index.faiss")
    >>> vector_db.build_index(["doc1", "doc2"])
    >>> vector_db.search("query", k=1)
    """
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

        # Initialize the index
        self.index = None
        self.documents = None

    def get_embedding(self,
                       doc: str
                       ) -> np.array:
        """
        Get the embedding of the document

        Parameters:
        -----------
        doc: str
            The document text

        Returns:
        --------
        np.array
            The embedding of the document
        """

        return self.llm.embeddings.create(input = [doc],
                                        model=self.embedding_model_name).data[0].embedding

    def build_index(self,
                    docs: List[str]
                    ) -> None:
        """
        Build the index

        Parameters:
        -----------
        docs: List[str]
            The list of documents
        """
        # Get the embeddings
        embeddings = [self.get_embedding(doc) for doc in docs]
        embeddings = np.array(embeddings)

        if self.index is  None:
            # Build the index
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
            self.index.add(embeddings)

            # Save the documents
            self.documents = docs
        else:
            # Add the embeddings
            self.index.add(embeddings)

            # Update the documents
            self.documents += docs

    def search(self,
               query: str,
               k: int
               ) -> List[int]:
        """
        Search the index

        Parameters:
        -----------
        query: str
            The query text

        k: int
            The number of nearest neighbors to return

        Returns:
        --------
        List[int]
            The list of indices of the nearest neighbors
        """
        # Get the embedding of the query
        query_embedding = np.array(self.get_embedding(query))

        # Search the index
        query_embedding = query_embedding.reshape(1, -1)
        _, idx = self.index.search(query_embedding, k)

        return idx[0].tolist()

    def save(self,
             db_path: str
             ) -> None:
        """
        Save the index

        Parameters:
        -----------
        db_path: str
            The path to save the index
        """
        faiss.write_index(self.index, db_path)
        with open(Path(db_path).with_suffix(".pkl"), "wb") as f:
            pickle.dump(self.documents, f)

    def load(self,
            db_path: str
            ) -> None:
        """
        Load the index

        Parameters:
        -----------
        db_path: str
            The path to load the index
        """
        self.index = faiss.read_index(db_path)
        with open(Path(db_path).with_suffix(".pkl"), "rb") as f:
            self.documents = pickle.load(f)
