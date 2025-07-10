import pdfplumber
import docx2txt
import io
import spacy
import re

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

skill_keywords = ["python", "java", "sql", "javascript", "html", "css", "git"]

education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college', 'school']

exp_keywords = ['experience', 'intern', 'managed', 'intern', 'developed', 'engineer', 'project', 'led']

def extract_text_from_pdf(file_bytes):
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    return text

def extract_text_from_docx(file_bytes):
    with open("temp_resume.docx", "wb") as f:
        f.write(file_bytes)
    text = docx2txt.process("temp_resume.docx")
    return text

def extract_skills(text):
    text_lower = text.lower()
    found = [skill for skill in skill_keywords if skill in text_lower]
    return list(set(found)) # remove dulpicates

def extract_education(text):
    return [line for line in text.splitlines() if any(kw in line.lower() for kw in education_keywords)]

def extract_experience(text):
    return [line for line in text.splitlines() if any (kw in line.lower() for kw in exp_keywords)]

def extract_resume_data(file_bytes, filename):
    # Extract text based on file type
    if filename.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_bytes)
    elif filename.endswith(".docx"):
        raw_text = extract_text_from_docx(file_bytes)
    else:
        raise ValueError("Unsupported file format. Please upload PDFor DOCX")
    
    # Clean spacing within lines but preserve newlines
    cleaned_text = '\n'.join(line.strip() for line in raw_text.splitlines() if line.strip())

    # Extract structured fields
    skills = extract_skills(cleaned_text)
    education = extract_education(cleaned_text)
    experience = extract_experience(cleaned_text)

    return {
        "text": raw_text,
        "skills": skills,
        "education": education,
        "experience": experience
    }
