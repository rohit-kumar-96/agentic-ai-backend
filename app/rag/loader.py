from docx import Document
from pypdf import PdfReader


def load_pdf(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text

def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
    


def load_docx(file_path):
    doc = Document(file_path)

    text = "\n".join(
        para.text
        for para in doc.paragraphs
    )

    return text