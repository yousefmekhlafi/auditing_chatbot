import fitz 
import logging
from typing import Dict, List

from src.data_ingestion.data_source import DocumentSource

logger = logging.getLogger(__name__)

def extract_text_from_pdf(doc_source: DocumentSource) -> Dict[int, str]:
    """
    Extracts plain text from each page of a PDF document.

    Args:
        doc_source: The DocumentSource object containing the path to the PDF.

    Returns:
        A dictionary where keys are page numbers (0-indexed) and
        values are the extracted text content of that page.
        Returns an empty dictionary if extraction fails.
    """
    pages_text = {}
    try:
        logger.info(f"Opening PDF for text extraction: {doc_source.path}")
        document = fitz.open(doc_source.path)
        num_pages = document.page_count
        logger.info(f"Extracting text from {num_pages} pages for document ID: {doc_source.id}")

        for page_num in range(num_pages):
            page = document.load_page(page_num)
            text = page.get_text("text", sort=True) # Get text, try sorting blocks vertically
            if not text.strip():
                logger.warning(f"Page {page_num + 1} in {doc_source.filename} seems to have no extractable text.")
            pages_text[page_num] = text
            # Log progress periodically if needed for large documents
            # if (page_num + 1) % 50 == 0:
            #     logger.debug(f"Processed {page_num + 1}/{num_pages} pages...")

        document.close()
        logger.info(f"Finished text extraction for document ID: {doc_source.id}")
        return pages_text

    except FileNotFoundError:
        logger.error(f"PDF file not found at path: {doc_source.path}")
        return {}
    except fitz.FitzError as fe:
         logger.error(f"PyMuPDF (Fitz) error processing {doc_source.filename}: {fe}")
         return {}
    except Exception as e:
        logger.exception(f"An unexpected error occurred during text extraction for {doc_source.filename}: {e}")
        return {} # Return empty dict on unexpected failure