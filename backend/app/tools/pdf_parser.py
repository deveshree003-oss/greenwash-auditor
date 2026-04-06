"""PDF parsing utilities (lightweight placeholders).

Try to use PyPDF2 if available; otherwise return an empty string.
Replace with a more robust parser (pdfplumber, tika, or OCR) as needed.
"""
from typing import List
import fitz


def parse_pdf(path: str) -> str:
    """Extract text from a PDF file at `path`.

    Returns the concatenated page text or an empty string on failure.
    """
    try:
        import PyPDF2

        text_parts: List[str] = []
        with open(path, "rb") as fh:
            reader = PyPDF2.PdfReader(fh)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n".join(text_parts)
    except Exception:
        return ""


def parse_pdf_safe(path: str) -> str:
    """Wrapper that returns an empty string instead of raising.

    Kept separate so callers can choose to call the raw parser directly
    if they want exceptions propagated.
    """
    return parse_pdf(path)


def extract_text(file) -> str:
    """Extract text from a file-like object containing PDF bytes using PyMuPDF.

    The `file` argument should be a file-like object (e.g., an uploaded
    `UploadFile.file`) that supports `.read()`.
    """
    try:
        data = file.read()
        doc = fitz.open(stream=data, filetype="pdf")
        texts: List[str] = [page.get_text() for page in doc]
        return "\n".join(texts)
    except Exception as e:
        return f"ERROR: {str(e)}"
