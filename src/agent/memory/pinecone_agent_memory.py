from typing import List

from src.app_pinecone.pinecone_history_index import PineconeHistoryIndex


class PineconeAgentMemory:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    # TODO add option for agent to fetch by key
    def add_to_memory(self, entries: List[dict] = None):
        """This method will add a key value pair to the agent's memory"""

        if not entries:
            return

        PineconeHistoryIndex().upsert_index(
            texts=list(map(lambda entry: entry["value"], entries)),
            metadata=list(map(lambda entry: {
                "agent_id": self.agent_id,
                "key": entry["key"],
            }, entries))

        )

    def get_relevant_memory(self, query: str, top_k: int = 5) -> List[str]:
        """This method will return a list of relevant memories"""

        results = PineconeHistoryIndex().query(
            query_text=query,
            agent_id=self.agent_id,
            top_k=top_k
        )
        return list(map(lambda result: f"{result['key']}: {result['text']}", results))
