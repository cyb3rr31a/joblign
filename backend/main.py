from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from auth import get_current_user, create_access_token, hash_password, verify_password
from utils import parser, scorer, feedback
# , scraper
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas


app = FastAPI()

# Create tables on startup
models.Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# In-memory store
resume_store = {}
resume_score = 0
job_description_store = {}

# Greeting message
@app.get("/")
def root():
    return {"message": "Welcome to Joblign API"}

# User authentication
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        email = user.email,
        hashed_password = hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

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
    global resume_score
    resume_data = resume_store.get("data")
    job_data = job_description_store.get("data")

    if not resume_data or not job_data:
        return {"error": "Missing resume or job description data"}

    score, missing_skills = scorer.compute_score(resume_data, job_data["text"])
    resume_score = score
    resume_skills = set(parser.extract_skills_from_resume(resume_data["text"]))
    job_skills = set(parser.extract_skills_from_job_desc(job_data["text"]))
    matched_skills = sorted(resume_skills.intersection(job_skills))

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": sorted(missing_skills)
    }

# Get recommendations on improvements
@app.post("/get_improvement_suggestions/")
async def get_suggestions():
    resume_data = resume_store.get("data")
    job_data = job_description_store.get("data")

    if not resume_data or not job_data:
        return {"error": "Missing resume or job description data"}
    
    score, missing_skills = scorer.compute_score(resume_data, job_data["text"])
    resume_data["missing_skills"] = missing_skills
    suggestions = feedback.generate_feedback(resume_data, job_data)
    return {"suggestions": suggestions}

"""
# Web scraping for jobs
@app.get("/search_jobs/")
async def search_jobs(query: str, location: str = "remote"):
    jobs = scraper.fetch_jobs(query, location)
    return {"results": jobs}
"""

@app.post("/jobs/", response_model=schemas.JobOut)
def create_job(
    job: schemas.JobCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
    ):
    db_job = models.Job(**job.dict(), resume_score = resume_score, owner_id = current_user.id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.get("/jobs/", response_model=list[schemas.JobOut])
def get_all_jobs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
    ):
    return db.query(models.Job).filter(models.Job.owner_id == current_user.id).all()

@app.get("/jobs/{job_id}", response_model=schemas.JobOut)
def get_job(
    job_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
    ):
    job = db.query(models.Job).filter(models.Job.id == job_id, models.Job.owner_id == current_user.id). first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.put("/jobs/{job_id}", response_model=schemas.JobOut)
def update_job(
    job_id: int, 
    updates: schemas.JobUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
    ):
    job = db.query(models.Job).filter(models.Job.id == job_id, models.Job.owner_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return job

@app.delete("/jobs/{job_id}")
def delete_job(
    job_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
    ):
    job = db.query(models.Job).filter(models.Job.id == job_id, models.Job.owner_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"detail": "Job deleted"}