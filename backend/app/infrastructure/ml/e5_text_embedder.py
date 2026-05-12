import asyncio
import logging
from typing import List
from sentence_transformers import SentenceTransformer
from app.domain import TextEmbedder, EmbeddingGenerationError, EmbeddingMatrix
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
    ) -> EmbeddingMatrix:
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
            EmbeddingMatrix: A list of embedding vectors, one per input text.

        Raises:
            EmbeddingGenerationError: If encoding fails for any reason.
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
            return embeddings_array.tolist()

        except Exception as e:
            logger.error(f"Failed to generate embeddings: {str(e)}", exc_info=True)
            raise EmbeddingGenerationError(f"Critical error in embedding generation: {str(e)}")