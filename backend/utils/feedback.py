from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Generate feedback function
def generate_feedback(resume_data: dict, job_description:str):
    skills = ", ".join(resume_data.get("skills", []))
    education = ", ".join(resume_data.get("education", []))
    experience = ", ".join(resume_data.get("education", []))
    missing_skills = resume_data.get("missing_skills", [])

    prompt = f"""
    You are an expert career coach and resume reviewer.
    A candidate has uploaded the following resume:
    Skills: {skills}
    Education: {education}
    Experience: {experience}

    They are applying for the following job:
    {job_description}

    The following skills are missing or weak in their resume: {', '.join(missing_skills)}

    Please provide detailed, actionable suggestions to improve their resume for this specific job.
    Include:
    - Bulet points they could add
    - Keywords they should include
    - Any soft/hard skills to highlight
    - Suggestions on phrasing or formatting

    Respond clearly and professionally
    """

    try:
        response = client.chat.completions.create(
            model = "gpt-4.1",
            messages=[
                {"role": "system", "content": "You are an expert resume coach."},
                {"role": "user", "content": prompt}
            ],
            temperature = 0.7,
            max_tokens = 600
        )

        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating feedback: {str(e)}" 