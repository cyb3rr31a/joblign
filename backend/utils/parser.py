import pdfplumber
import docx2txt
import io
import spacy
import re

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Keywords
skill_keywords = ["python", "java", "javascript", "typescript", "c", "c++", "c#", "go", "ruby", "php", "swift", "kotlin", "r", "scala", "matlab", "sql", "bash", "shell", "html", "css", "rust", "dart", "django", "flask", "fastapi", "spring", "express", "next.js", "react", "angular", "vue.js", "svelte", "nestjs", "tailwind css", "bootstrap", "jquery", "redux", "pytorch", "tensorflow", "scikit-learn", "keras", "xgboost", "pandas", "numpy", "matplotlib", "seaborn", "opencv", "git", "github", "gitlab", "docker", "kubernetes", "jenkins", "terraform", "ansible", "prometheus", "grafana", "airflow", "mlflow", "streamlit", "tableau", "power bi", "superset", "postman", "jupyter", "notebooks", "huggingface", "openai", "firebase", "sentry", "nginx", "aws", "azure", "gcp", "google cloud", "amazon web services", "microsoft azure", "cloudflare", "heroku", "digitalocean", "cloud functions", "lambda", "cloudformation", "s3", "ec2", "rds", "cloudwatch", "bigquery", "mysql", "postgresql", "mongodb", "redis", "cassandra", "sqlite", "firebase", "dynamodb", "oracle", "elasticsearch", "neo4j", "snowflake", "clickhouse", "duckdb", "influxdb", "ci/cd", "github actions", "circleci", "travisci", "buildkite", "argo", "helm", "vagrant", "infrastructure as code", "monitoring", "observability", "log aggregation", "data analysis", "data visualization", "data engineering", "machine learning", "deep learning", "nlp", "computer vision", "llms", "model training", "feature engineering", "model deployment", "recommender systems", "ai ethics", "drift detection", "automated retraining", "unit testing", "integration testing", "e2e testing", "playwright", "cypress", "selenium", "pytest", "unittest", "test automation", "tdd", "bdd", "agile", "scrum", "kanban", "jira", "confluence", "project management", "product ownership", "sdlc", "devops lifecycle", "version control", "code reviews", "cybersecurity", "penetration testing", "vulnerability assessment", "firewalls", "intrusion detection", "network security", "endpoint protection", "encryption", "threat modeling", "soc", "siem", "incident response", "tcp/ip", "dns", "http", "https", "ftp", "ssh", "vpn", "load balancing", "subnetting", "firewall configuration", "communication", "problem solving", "critical thinking", "teamwork", "adaptability", "time management", "leadership", "collaboration", "attention to detail", "creativity", "self-motivation", "api development", "rest api", "graphql", "microservices", "design patterns", "oop", "mvc", "functional programming", "low-level programming", "data structures", "algorithms", "big o notation", "cloud native", "multi-threading", "distributed systems", "system design"]

education_keywords = ["diploma", "bachelor", "master", "phd"]
exp_keywords = ["intern", "attache"]

# Extract text from pdf
def extract_text_from_pdf(file_bytes):
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    return text

# Extract text from docx
def extract_text_from_docx(file_bytes):
    with open("temp_resume.docx", "wb") as f:
        f.write(file_bytes)
    text = docx2txt.process("temp_resume.docx")
    return text

def extract_named_entities(text):
    doc = nlp(text)
    name = None

    for ent in doc.ents:
        if ent.label_ == "PERSON" and name is None:
            name = ent.text

    return {
        "name": name,
    }

def extract_skills_from_resume(text):
    text_lower = text.lower()
    found = [skill for skill in skill_keywords if skill in text_lower]
    return set(found) # remove dulpicates

def extract_skills_from_job_desc(text):
    text = text.lower()
    found_skills = set()

    for skill in skill_keywords:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found_skills.add(skill)

    return sorted(found_skills)

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
    named_entities = extract_named_entities(raw_text)
    skills = extract_skills_from_resume(cleaned_text)
    education = extract_education(cleaned_text)
    experience = extract_experience(cleaned_text)

    return {
        "text": raw_text,
        "name": named_entities["name"],
        "skills": skills,
        "education": education,
        "experience": experience
    }
