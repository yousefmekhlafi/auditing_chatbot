# src/vector_store/vector_store_manager.py
import logging
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Tuple

from src.parsing.models import DocumentChunk
from src.utils.config_manager import get_config, PROJECT_ROOT
import os

logger = logging.getLogger(__name__)

class VectorStoreManager:
    """Manages interactions with the ChromaDB vector store."""

    def __init__(self, path: str = None, collection_name: str = None):
        if path is None:
            path = get_config("VECTOR_STORE_PATH", "vector_store/chroma_db")
        if collection_name is None:
            collection_name = get_config("VECTOR_STORE_COLLECTION_NAME", "audit_documents")

        # Ensure path is absolute or relative to project root
        if not os.path.isabs(path):
             self.path = os.path.join(PROJECT_ROOT, path)
        else:
             self.path = path

        self.collection_name = collection_name
        self.client = None
        self.collection = None

        logger.info(f"Initializing ChromaDB client with persistence directory: {self.path}")
        os.makedirs(self.path, exist_ok=True) # Ensure directory exists

        try:
            self.client = chromadb.PersistentClient(path=self.path)
            logger.info(f"Getting or creating collection: {self.collection_name}")
            # Note: You might need to specify the embedding function expected by the collection
            # if you want Chroma to handle embedding for queries. For now, we embed externally.
            # embedding_function = chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(model_name=get_config("EMBEDDING_MODEL_NAME"))
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                # embedding_function=embedding_function # Optional: Let Chroma handle query embedding
                metadata={"hnsw:space": "cosine"} # Use cosine distance - common for sentence transformers
            )
            logger.info(f"Vector store initialized. Collection '{self.collection_name}' ready.")
            logger.info(f"Current collection count: {self.collection.count()}")

        except Exception as e:
            logger.exception(f"Failed to initialize ChromaDB client or collection: {e}")
            # Optional: Raise the exception or handle appropriately
            raise

    def add_documents(self, chunks: List[DocumentChunk], embeddings: List[List[float]]):
        """Adds document chunks and their embeddings to the collection."""
        if not chunks or not embeddings or len(chunks) != len(embeddings):
            logger.warning("Invalid input for adding documents. Chunks or embeddings empty or mismatched length.")
            return

        if not self.collection:
             logger.error("Vector store collection is not available.")
             return

        chunk_ids = [chunk.chunk_id for chunk in chunks]
        texts = [chunk.text for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]

        logger.info(f"Adding/updating {len(chunk_ids)} documents in collection '{self.collection_name}'...")
        try:
            # Use upsert to add new or update existing documents by ID
            self.collection.upsert(
                ids=chunk_ids,
                embeddings=embeddings,
                documents=texts, # Storing the text itself is useful for context retrieval
                metadatas=metadatas
            )
            logger.info(f"Successfully added/updated {len(chunk_ids)} documents.")
            logger.info(f"New collection count: {self.collection.count()}")
        except Exception as e:
            logger.exception(f"Failed to add documents to ChromaDB collection: {e}")

    def query(self, query_embedding: List[float], n_results: int = 5) -> List[Tuple[DocumentChunk, float]]:
        """Queries the collection for similar documents."""
        if not self.collection:
             logger.error("Vector store collection is not available.")
             return []
        if not query_embedding:
             logger.error("Query embedding is empty.")
             return []

        logger.debug(f"Querying collection '{self.collection_name}' for {n_results} results.")
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding], # Query expects a list of embeddings
                n_results=n_results,
                include=['documents', 'metadatas', 'distances'] # Request needed info
            )

            # Process results into a more usable format
            processed_results = []
            if results and results.get('ids') and results['ids'][0]:
                for i, chunk_id in enumerate(results['ids'][0]):
                    doc_id = "_".join(chunk_id.split("_")[:-2]) # Infer doc_id from chunk_id format
                    text = results['documents'][0][i]
                    metadata = results['metadatas'][0][i]
                    distance = results['distances'][0][i]

                    chunk = DocumentChunk(
                         doc_id=doc_id,
                         chunk_id=chunk_id,
                         text=text,
                         metadata=metadata
                    )
                    processed_results.append((chunk, distance)) # Return chunk and its distance

            logger.debug(f"Query returned {len(processed_results)} results.")
            return processed_results

        except Exception as e:
            logger.exception(f"Failed to query ChromaDB collection: {e}")
            return []