# src/embedding/embedder.py
import logging
from typing import List
from sentence_transformers import SentenceTransformer
import torch # sentence-transformers uses torch or tensorflow

from src.parsing.models import DocumentChunk
from src.utils.config_manager import get_config

logger = logging.getLogger(__name__)

class SentenceTransformerEmbedder:
    """Handles embedding creation using Sentence Transformers."""
    _model = None # Class variable to hold the loaded model (singleton-like)

    def __init__(self, model_name: str = None):
        if model_name is None:
            model_name = get_config("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
        self.model_name = model_name
        self._load_model() # Ensure model is loaded on instantiation

        # Detect device
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device} for embeddings")
        if SentenceTransformerEmbedder._model:
             SentenceTransformerEmbedder._model.to(self.device)


    def _load_model(self):
        """Loads the Sentence Transformer model (if not already loaded)."""
        if SentenceTransformerEmbedder._model is None:
            logger.info(f"Loading embedding model: {self.model_name}...")
            try:
                # Specify trust_remote_code=True if using newer SentenceTransformer versions and certain models
                SentenceTransformerEmbedder._model = SentenceTransformer(self.model_name)
                logger.info("Embedding model loaded successfully.")
            except Exception as e:
                logger.exception(f"Failed to load embedding model '{self.model_name}': {e}")
                # Optional: Raise the exception or handle appropriately
                raise
        else:
             logger.info("Embedding model already loaded.")


    def embed_chunks(self, chunks: List[DocumentChunk]) -> List[List[float]]:
        """Embeds the text content of document chunks."""
        if not chunks:
            return []
        if not SentenceTransformerEmbedder._model:
             logger.error("Embedding model is not loaded. Cannot embed chunks.")
             return [] # Or raise an error

        texts_to_embed = [chunk.text for chunk in chunks]
        logger.info(f"Embedding {len(texts_to_embed)} text chunks...")

        try:
            # The encode method handles batching internally
            embeddings = SentenceTransformerEmbedder._model.encode(
                texts_to_embed,
                show_progress_bar=True, # Nice for longer processes
                convert_to_numpy=False, # Get lists of floats
                device=self.device
            ).tolist() # Ensure it's a list of lists
            logger.info("Finished embedding chunks.")
            return embeddings
        except Exception as e:
            logger.exception(f"An error occurred during embedding: {e}")
            return [] # Return empty list on failure

    def embed_query(self, query: str) -> List[float]:
         """Embeds a single query string."""
         if not SentenceTransformerEmbedder._model:
             logger.error("Embedding model is not loaded. Cannot embed query.")
             return [] # Or raise

         logger.debug(f"Embedding query: '{query[:100]}...'") # Log snippet
         try:
             embedding = SentenceTransformerEmbedder._model.encode(
                 query,
                 convert_to_numpy=False,
                 device=self.device
             ).tolist() # Ensure it's a list of floats
             return embedding
         except Exception as e:
            logger.exception(f"An error occurred during query embedding: {e}")
            return []