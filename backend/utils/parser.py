import pdfplumber
import docx2txt
import io
import spacy
import re

# Load the spaCy model
nlp = spacy.load("en_core_web_trf")

SKILL_KEYWORDS = [
    "python", "java", "sql", "javascript", "html", "css", "git"
]

def extract_text_from_pdf(file_bytes):
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    return text

def extract_text_from_docx(file_bytes):
    with open("temp_resume.docx", "wb") as f:
        f.write(file_bytes)
    text = docx2txt.process("temp_resume.docx")
    return text