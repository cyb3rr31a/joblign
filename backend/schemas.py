from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    class Config:
        orm_mode = True

class JobCreate(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    job_description : Optional[str] = None
    application_link: Optional[str] = None
    notes: Optional[str] = None

class JobUpdate(BaseModel):
    status: Optional[str] = None
    resume_score: Optional[int] = None
    ai_feedback: Optional[str] = None
    notes: Optional[str] = None

class JobOut(BaseModel):
    id: int
    title: str
    company: str
    location: Optional[str]
    status: str = "pending"
    resume_score: Optional[int]
    ai_feedback: Optional[str]
    job_description: Optional[str]
    application_link: Optional[str]
    notes: Optional[str]
    created_at: datetime
    class Config:
        orm_mode = True