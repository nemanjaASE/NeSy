from typing import List, Protocol
from ..models.result import Result
from ..models.symptom import EmbeddingMatrix


class TextEmbedder(Protocol):
    """
    Interface defining the contract for generating vector embeddings from text.

    Any infrastructure implementation (SentenceTransformers, OpenAI, etc.) must
    fulfill this interface to be used within the semantic matching pipeline.
    """

    async def generate_embeddings(
        self, texts: List[str], prefix: str = "query: "
    ) -> Result[EmbeddingMatrix]:
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
            Result[EmbeddingMatrix]: A list of embedding vectors, one per input text.
        """

    async def generate_embeddings_split(
        self, present_terms: list[str], absent_terms: list[str], prefix: str = "query: "
    ) -> Result[tuple[EmbeddingMatrix, EmbeddingMatrix]]:
        """
        Generate embeddings for present and absent symptom terms in a single model call.

        Combines both lists into one encoding pass to avoid concurrent access
        issues with the underlying model, then splits the result back into
        separate present and absent embedding matrices.

        This method should be preferred over calling generate_embeddings twice
        in parallel when using thread-bound models such as SentenceTransformers.

        Args:
            present_terms: Symptom terms the patient reports having.
            absent_terms:  Symptom terms the patient explicitly denies.
            prefix:        Prefix prepended to each term before encoding.
                           Defaults to "query: " for patient input context.

        Returns:
            Result[tuple[EmbeddingMatrix, EmbeddingMatrix]]: Success with a tuple of
            (present_embeddings, absent_embeddings), or failure with an error message.
        """
