import asyncio
import logging
from typing import List
from sentence_transformers import SentenceTransformer
from app.domain import Result, TextEmbedder, EmbeddingMatrix
from app.core import timed

logger = logging.getLogger(__name__)

class E5Embedder(TextEmbedder):
    """
    TextEmbedder implementation using the multilingual-e5-large model
    via the SentenceTransformers library.

    The model is loaded into memory once at initialization and reused
    across all embedding requests. Encoding is offloaded to a thread
    executor to avoid blocking the async event loop.
    """

    def __init__(self, model_name: str):
        """
        Load the SentenceTransformer model into memory.

        Args:
            model_name: The HuggingFace model identifier or local path
                        (e.g. 'intfloat/multilingual-e5-large').
        """
        logger.info(f"Initializing E5Embedder with model: {model_name}")
        self.model = SentenceTransformer(model_name)
        logger.info("Embedding model loaded successfully into memory.")

    @timed("Embedding Generation")
    async def generate_embeddings(
        self,
        texts: List[str],
        prefix: str = "query: "
    ) -> Result[EmbeddingMatrix]:
        """
        Asynchronously generate vector embeddings for a list of input texts.

        Each text is prefixed before encoding to align with the E5 model's
        training objective. Encoding runs in a thread executor to prevent
        blocking the async event loop during CPU-intensive inference.

        Args:
            texts:  A list of plain-text strings to be embedded.
            prefix: A prefix prepended to each text before encoding.
                    Use "query: " for patient symptoms and "passage: "
                    for ontology terms. Defaults to "query: ".

        Returns:
            Result[EmbeddingMatrix]: Success with a list of embedding vectors,
            one per input text, or failure with an error message.
        """
        try:
            prefixed = [f"{prefix}{text}" for text in texts]
            logger.debug(f"Generating embeddings for {len(prefixed)} texts with prefix '{prefix}'.")

            loop = asyncio.get_running_loop()
            embeddings_array = await loop.run_in_executor(
                None,
                lambda: self.model.encode(prefixed)
            )

            logger.info(f"Successfully generated {len(embeddings_array)} embeddings.")
            return Result.success(embeddings_array.tolist())

        except Exception as e:
            logger.error(f"Failed to generate embeddings: {str(e)}", exc_info=True)
            return Result.failure(f"Embedding generation failed: {str(e)}")
    
    @timed("Embedding Generation Split")
    async def generate_embeddings_split(
        self,
        present_terms: list[str],
        absent_terms:  list[str],
        prefix: str = "query: "
    ) -> Result[tuple[EmbeddingMatrix, EmbeddingMatrix]]:
        """
        Generate embeddings for present and absent terms in a single model call.

        Combines both lists into one encoding pass to avoid concurrent access
        issues with the underlying SentenceTransformer model, then splits
        the result back into present and absent embedding matrices.

        Args:
            present_terms: Symptom terms the patient reports having.
            absent_terms:  Symptom terms the patient explicitly denies.
            prefix:        Prefix prepended to each term before encoding.

        Returns:
            Result[tuple[EmbeddingMatrix, EmbeddingMatrix]]: Success with
            (present_embeddings, absent_embeddings), or failure with an error message.
        """
        all_terms = present_terms + absent_terms

        result = await self.generate_embeddings(all_terms, prefix=prefix)
        if result.is_failure:
            return Result.failure(result.error)

        all_embeddings = result.value
        split = len(present_terms)

        return Result.success((
            all_embeddings[:split],
            all_embeddings[split:]
        ))