from .parser import extract_skills_from_resume, extract_skills_from_job_desc

def compute_score(resume_data: dict, job_description: str):
    resume_skills = set(extract_skills_from_resume(resume_data["text"]))
    
    # Find required skills from job description
    required_skills = set(extract_skills_from_job_desc(job_description))

    matched_skills = resume_skills.intersection(required_skills)
    missing_skills = required_skills - resume_skills

    if required_skills:
        score = int((len(matched_skills) / len(required_skills)) * 100)
    else:
        score = 0

    return score, list(missing_skills)
