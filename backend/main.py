from fastapi import FastAPI, UploadFile, File
from utils import parser, scorer, scraper, feedback

app = FastAPI()

# Greeting message
@app.get("/")
def root():
    return {"message": "Welcome to Joblign API"}

# Upload resume
@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    extracted_data = parser.extract_resume_data(content, file.filename)
    return {"resume_data": extracted_data}

# Upload Job Description
@app.post("/upload_job_description/")
async def upload_job_description(description: str):
    return {"job_description": description}

# Get ATS Score
@app.post("/get_match_score/")
async def get_match_score(resume_data: dict, job_description: str):
    score, missing_skills = scorer.compute_score(resume_data, job_description)
    return {"score": score, "missing_skills": missing_skills}

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