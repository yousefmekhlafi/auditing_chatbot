# src/data_ingestion/loaders/pdf_loader.py
import os
import logging
from pathlib import Path
from typing import List, Iterator

from src.data_ingestion.data_source import DocumentSource
from src.utils.config_manager import get_config, PROJECT_ROOT

logger = logging.getLogger(__name__)

def list_pdfs(directory: str) -> List[Path]:
    """Lists all PDF files in a given directory."""
    dir_path = Path(directory)
    if not dir_path.is_absolute():
        # Assume relative to project root if not absolute
        dir_path = Path(PROJECT_ROOT) / directory

    if not dir_path.is_dir():
        logger.error(f"PDF source directory not found or not a directory: {dir_path}")
        return []

    pdf_files = list(dir_path.rglob("*.pdf")) # Use rglob for recursive search
    logger.info(f"Found {len(pdf_files)} PDF(s) in {dir_path}")
    return pdf_files

def load_documents(pdf_dir: str = None) -> Iterator[DocumentSource]:
    """Loads document sources from the configured PDF directory."""
    if pdf_dir is None:
        pdf_dir = get_config("PDF_SOURCE_DIR", "data/raw") # Get path from config
        logger.info(f"Using PDF source directory from config: {pdf_dir}")

    pdf_paths = list_pdfs(pdf_dir)

    for pdf_path in pdf_paths:
        try:
            doc_id = pdf_path.stem # Use filename without extension as ID
            yield DocumentSource(path=str(pdf_path), id=doc_id)
        except Exception as e:
            logger.error(f"Error creating DocumentSource for {pdf_path}: {e}")
            continue # Skip this file and continue with others