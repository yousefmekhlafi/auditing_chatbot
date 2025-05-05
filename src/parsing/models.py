# src/parsing/models.py
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class DocumentChunk:
    """Represents a chunk of text from a document."""
    doc_id: str         # Identifier of the source document (e.g., filename)
    chunk_id: str       # Unique identifier for this chunk (e.g., doc_id_chunk_0)
    text: str           # The actual text content of the chunk
    metadata: Dict[str, Any] = field(default_factory=dict) # Page num, etc.

    def __str__(self) -> str:
        return f"Chunk(id={self.chunk_id}, source={self.doc_id}, page={self.metadata.get('page_number', 'N/A')}, len={len(self.text)})"
