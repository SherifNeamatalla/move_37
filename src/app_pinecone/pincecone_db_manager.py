from typing import List

import pinecone

from src.config.env_loader import load_env

load_env()


class PineconeDBManager:

    def __init__(self, index_name: str, dimension: int):
        self.create_index_if_not_exists(index_name, dimension)
        self.index = pinecone.Index(index_name)

    def create_index_if_not_exists(self, index_name: str, dimension: int) -> None:
        indexes = pinecone.list_indexes()
        if index_name not in indexes:
            pinecone.create_index(index_name, dimension)

    def delete_index(self) -> None:
        self.index.delete()

    def list_indexes(self):
        return pinecone.list_indexes()

    def index_info(self):
        return self.index.describe_index_stats()

    def upsert_index(self, ids: [str], vectors: List[str], metadata) -> None:
        self.index.upsert(zip(
            ids,
            vectors,
            metadata
        ))

    def delete_index_by_id(self, ids: List[str]) -> None:
        self.index.delete(ids=ids)

    def query_index(self, query_vectors, top_k: int = 10, include_metadata=False, filter: dict[str, str] = None):
        return self.index.query(queries=query_vectors, top_k=top_k, include_metadata=include_metadata, filter=filter)
