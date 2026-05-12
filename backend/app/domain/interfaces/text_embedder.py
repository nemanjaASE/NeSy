from typing import List, Protocol
from ..models.symptom import EmbeddingMatrix

class TextEmbedder(Protocol):
    """
    Interface defining the contract for generating vector embeddings from text.

    Any infrastructure implementation (SentenceTransformers, OpenAI, etc.) must
    fulfill this interface to be used within the semantic matching pipeline.
    """

    async def generate_embeddings(
        self,
        texts: List[str],
        prefix: str = "query: "
    ) -> EmbeddingMatrix:
        """
        Asynchronously generate vector embeddings for a list of input texts.

        For E5-based models, a task-specific prefix should be provided to ensure
        optimal embedding quality:
            - "query: "   for patient-reported symptoms and search inputs
            - "passage: " for ontology terms stored in the knowledge graph

        Args:
            texts:  A list of plain-text strings to be embedded.
            prefix: A prefix prepended to each text before encoding.
                    Defaults to "query: " for patient input context.

        Returns:
            EmbeddingMatrix: A list of embedding vectors, one per input text.
        """