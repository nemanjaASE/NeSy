from typing import List, Protocol

class TextEmbedder(Protocol):
    """
    Protocol for generating vector embeddings from text.
    """
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Takes a string and returns a dense vector representation.
        """