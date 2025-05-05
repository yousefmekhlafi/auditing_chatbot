# src/chunking/chunker.py
import logging
from typing import List, Dict, Iterator

# Using Langchain's splitter as it's quite effective
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.parsing.models import DocumentChunk
from src.utils.config_manager import get_config

logger = logging.getLogger(__name__)

def chunk_text_by_page(
    pages_text: Dict[int, str],
    doc_id: str,
    chunk_size: int = None,
    chunk_overlap: int = None,
) -> List[DocumentChunk]:
    """
    Chunks text from document pages using a recursive character splitter.

    Args:
        pages_text: Dictionary mapping page number (0-indexed) to page text.
        doc_id: The identifier for the source document.
        chunk_size: Target size of chunks in characters. Reads from config if None.
        chunk_overlap: Overlap between chunks in characters. Reads from config if None.

    Returns:
        A list of DocumentChunk objects.
    """
    if chunk_size is None:
        chunk_size = int(get_config("CHUNK_SIZE", 1000))
    if chunk_overlap is None:
        chunk_overlap = int(get_config("CHUNK_OVERLAP", 200))

    logger.info(f"Chunking document '{doc_id}' with size={chunk_size}, overlap={chunk_overlap}")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False, # Use default separators like "\n\n", "\n", " ", ""
    )

    all_chunks: List[DocumentChunk] = []
    chunk_index = 0

    for page_num, text in pages_text.items():
        if not text.strip():
            logger.debug(f"Skipping empty page {page_num + 1} for document '{doc_id}'")
            continue

        # Split the text of the current page
        page_chunks = text_splitter.split_text(text)

        for page_chunk_text in page_chunks:
            chunk_id = f"{doc_id}_chunk_{chunk_index}"
            metadata = {"page_number": page_num + 1} # Store 1-based page number
            chunk = DocumentChunk(
                doc_id=doc_id,
                chunk_id=chunk_id,
                text=page_chunk_text,
                metadata=metadata,
            )
            all_chunks.append(chunk)
            chunk_index += 1

        # logger.debug(f"Page {page_num + 1}: Created {len(page_chunks)} chunks.")

    logger.info(f"Finished chunking document '{doc_id}'. Total chunks: {len(all_chunks)}")
    return all_chunks

# Example usage (can be tested in a notebook)
# if __name__ == "__main__":
#     from src.utils.logging_config import setup_logging
#     setup_logging()
#     sample_pages = {0: "This is the first page.\nIt has two sentences.", 1: "This is the second page. It's a bit longer and might be split."}
#     chunks = chunk_text_by_page(sample_pages, "sample_doc")
#     for chunk in chunks:
#         print(chunk)
#         print("-" * 20)