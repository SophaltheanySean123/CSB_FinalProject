from pdfminer.high_level import extract_text
from docx import Document

def extract_text_pdf(path: str) -> str:
    """Extract text from PDF file"""
    try:
        return extract_text(path)
    except Exception as e:
        raise ValueError(f"Failed to extract PDF text: {str(e)}")

def extract_text_docx(path: str) -> str:

    try:
        doc = Document(path)
        return "\\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        raise ValueError(f"Failed to extract DOCX text: {str(e)}")

def extract_text_from_file(path: str, filename: str) -> str:

    if filename.endswith(".pdf"):
        return extract_text_pdf(path)
    elif filename.endswith(".docx"):
        return extract_text_docx(path)
    elif filename.endswith(".txt"):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise ValueError(f"Failed to read text file: {str(e)}")
    else:
        raise ValueError("Unsupported file type")

def truncate_text(text: str, max_chars: int = 15000) -> str:
    """Truncate text to avoid token limits"""
    if len(text) > max_chars:
        return text[:max_chars]
    return text