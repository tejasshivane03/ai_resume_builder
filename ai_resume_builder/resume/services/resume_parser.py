"""
Parser service for extracting plain text from uploaded PDF, DOCX, or TXT resumes.
"""
import io
import logging

logger = logging.getLogger(__name__)


def extract_text_from_file(uploaded_file):
    """
    Extract plain text from an uploaded file object (InMemoryUploadedFile or TemporaryUploadedFile).
    Supports .pdf, .docx, and plain text files.
    """
    if not uploaded_file:
        return ""

    filename = uploaded_file.name.lower()
    content_bytes = uploaded_file.read()
    uploaded_file.seek(0)  # Reset file pointer

    if filename.endswith('.pdf'):
        return _extract_from_pdf(content_bytes)
    elif filename.endswith('.docx'):
        return _extract_from_docx(content_bytes)
    elif filename.endswith('.txt'):
        try:
            return content_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return content_bytes.decode('latin-1', errors='ignore')
    else:
        # Best effort decode as text
        try:
            return content_bytes.decode('utf-8', errors='ignore')
        except Exception:
            return ""


def _extract_from_pdf(pdf_bytes):
    """Extract text from PDF using pypdf, pdfplumber, or fitz if available."""
    # Try PyPDF / pypdf
    try:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        text = [page.extract_text() for page in reader.pages if page.extract_text()]
        if text:
            return "\n".join(text)
    except Exception:
        pass

    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        text = [page.extract_text() for page in reader.pages if page.extract_text()]
        if text:
            return "\n".join(text)
    except Exception:
        pass

    try:
        import fitz  # PyMuPDF
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = [page.get_text() for page in doc]
        if text:
            return "\n".join(text)
    except Exception:
        pass

    # Basic fallback string parsing
    raw_str = pdf_bytes.decode('latin-1', errors='ignore')
    import re
    cleaned = re.sub(r'[^\w\s@\.\-\+\#]', ' ', raw_str)
    return " ".join(cleaned.split())


def _extract_from_docx(docx_bytes):
    """Extract text from DOCX using python-docx."""
    try:
        import docx
        doc = docx.Document(io.BytesIO(docx_bytes))
        full_text = []
        for para in doc.paragraphs:
            if para.text:
                full_text.append(para.text)
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text:
                        full_text.append(cell.text)
        return "\n".join(full_text)
    except Exception as e:
        logger.warning(f"DOCX extraction failed: {e}")
        return ""
