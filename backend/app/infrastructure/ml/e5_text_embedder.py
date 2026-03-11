import asyncio
from typing import List
from sentence_transformers import SentenceTransformer
from app.domain import TextEmbedder
from app.core import logger
from app.domain import EmbeddingGenerationError

class E5Embedder(TextEmbedder):
    """
    Infrastructure implementation of TextEmbedder using the multilingual-e5-large model.
    """

    def __init__(self, model_name: str):
        """
        Initialize the embedding model.
        """
        logger.info(f"Initializing Embedder with model: {model_name}")
        self.model = SentenceTransformer(model_name)
        logger.info("Embedding model loaded successfully into memory.")

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts asynchronously.
        """
        try:
            logger.debug(f"Generating embeddings for {len(texts)} items.")
            
            loop = asyncio.get_running_loop()

            embeddings_array = await loop.run_in_executor(
                None, 
                lambda: self.model.encode(texts)
            )
            
            logger.info("Successfully generated vector embeddings.")
            return embeddings_array.tolist()

        except Exception as e:
            logger.error(f"Failed to generate embeddings: {str(e)}", exc_info=True)
            raise EmbeddingGenerationError(f"Critical error in embedding generation: {str(e)}")