from typing import List

from openai.embeddings_utils import get_embeddings

from src.app_pinecone.pincecone_db_manager import PineconeDBManager
from src.config.env_loader import load_env

MODEL_NAME = "text-embedding-ada-002"
DIMENSIONS = 1536
INDEX_NAME = "history-index"

load_env()


class PineconeHistoryIndex:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.db_manager = PineconeDBManager(
                index_name=INDEX_NAME,
                dimension=DIMENSIONS
            )
        return cls._instance

    def get_embeddings(self, texts: List[str]):
        return get_embeddings(list_of_text=texts, engine=MODEL_NAME)

    def delete_index(self):
        self.db_manager.delete_index()

    def upsert_index(self, texts: List[str], metadata: List = None) -> None:
        # generate id for each text
        ids = [str(i) for i in range(len(texts))]
        vectors = self.get_embeddings(texts)

        if metadata is None:
            metadata = []

        for i, text in enumerate(texts):
            metadata[i]["text"] = text

        self.db_manager.upsert_index(ids=ids, vectors=vectors, metadata=metadata)

    def query(self, query_text: str, agent_id: str, top_k: int = 10) -> List[str]:
        query_vectors = self.get_embeddings([query_text])
        result = \
            self.db_manager.query_index(query_vectors=query_vectors, top_k=top_k, include_metadata=True,
                                        filter={
                                            "agent_id": agent_id
                                        })['results'][0][
                'matches']
        return [item["metadata"] for item in result]
