from fastapi import FastAPI, UploadFile, File
from utils import parser, scorer
# , scraper, feedback

app = FastAPI()

# In-memory store
resume_store = {}
job_description_store = {}

# Greeting message
@app.get("/")
def root():
    return {"message": "Welcome to Joblign API"}

# Upload resume
@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    resume_data = parser.extract_resume_data(content, file.filename)
    global resume_store
    resume_store["data"] = resume_data
    return {"parsed_resume": resume_data}

# Upload Job Description
@app.post("/upload_job_description/")
async def upload_job_description(description: str):
    global job_description_store
    extracted = parser.extract_skills_from_job_desc(description)
    job_description_store["data"] = {
        "text": description,
        "skills": extracted
    }
    return {"extracted_skills": extracted}

# Get match Score
@app.post("/get_match_score/")
async def get_match_score():
    resume_data = resume_store.get("data")
    job_data = job_description_store.get("data")

    if not resume_data or not job_data:
        return {"error": "Missing resume or job description data"}

    score, missing_skills = scorer.compute_score(resume_data, job_data["text"])

    resume_skills = set(parser.extract_skills_from_resume(resume_data["text"]))
    job_skills = set(parser.extract_skills_from_job_desc(job_data["text"]))
    matched_skills = sorted(resume_skills.intersection(job_skills))

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": sorted(missing_skills)
    }
"""
# Get recommendations on improvements
@app.post("/improvement_suggestions/")
async def get_suggestions(resume_data: dict, job_description: str):
    suggestions = feedback.generate_feedback(resume_data, job_description)
    return {"suggestions": suggestions}

# Web scraping for jobs
@app.get("/search_jobs/")
async def search_jobs(query: str, location: str = "remote"):
    jobs = scraper.fetch_jobs(query, location)
    return {"results": jobs}
"""