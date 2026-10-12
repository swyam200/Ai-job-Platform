
import fitz


def extract_text_from_pdf(file):
    """Extract text from a PDF without leaving the uploaded file at EOF."""
    file.seek(0)
    pdf_bytes = file.read()
    file.seek(0)

    text_parts = []

    try:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as pdf_document:
            for page in pdf_document:
                text_parts.append(page.get_text())
    except Exception as exc:
        raise ValueError("Could not read this PDF file.") from exc
    finally:
        file.seek(0)

    return "\n".join(text_parts).strip()
