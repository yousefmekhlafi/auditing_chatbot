# src/data_ingestion/data_source.py
from dataclasses import dataclass
import os

@dataclass
class DocumentSource:
    """Represents a source document."""
    path: str
    id: str 

    @property
    def filename(self) -> str:
        return os.path.basename(self.path)

    def __str__(self) -> str:
        return f"DocumentSource(id='{self.id}', path='{self.path}')"