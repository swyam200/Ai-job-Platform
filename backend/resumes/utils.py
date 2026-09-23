import fitz
def extract_text_from_pdf(file):
    text=""
    pdf_document=fitz.open(stream=file.read(),filetype="pdf")
    for page in pdf_document:
        text+=page.get_text()
    pdf_document.close()
    return text.strip()