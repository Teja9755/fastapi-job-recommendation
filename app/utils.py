from typing import List,Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# utils.py (temporarily skip hashing)
def hash_password(password: str) -> str:
    # Return password as-is (for testing only!)
    return password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Compare plain text (for testing only!)
    return plain_password == hashed_password

def preprocess_skills(skills: List[str] or str) -> List[str]:
    if not skills:
        return []
    if isinstance(skills, str):
        skills = skills.split(",")  # split comma-separated string
    return [s.strip().lower() for s in skills]
    
def preprocess_location(location:str):
    if not location:
        return "unknown"
    if isinstance(location,str):
        return location.lower().strip()
    
def preprocess_user_input(user_data: Dict) -> Dict:
    return {
        "skills": preprocess_skills(user_data.get("skills", [])),
        "current_location": preprocess_location(user_data.get("current_location", "")),
        "preferred_location": preprocess_location(user_data.get("preferred_location", "")),
    }

def preprocess_job(job_data: Dict) -> Dict:
    return {
        "id": job_data.get("id"),
        "title": job_data.get("title", "").lower(),
        "skills_required": preprocess_skills(job_data.get("skills_required", [])),
        "location": preprocess_location(job_data.get("location", "")),
        "description": job_data.get("description", "").lower(),
        "company": job_data.get("company", "unknown")  # <-- ADD THIS
    }  

def vectorize_and_rank(user_data: Dict, jobs: List[Dict]) -> List[Dict]:
    # Combine user skills and preferred location into a "text" string
    user_text = " ".join(user_data["skills"]) + " " + user_data["preferred_location"]

    # Prepare job texts
    job_texts = []
    for job in jobs:
        job_texts.append(" ".join(job["skills_required"]) + " " + job["location"])

    # Vectorize
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([user_text] + job_texts)
    user_vector = vectors[0]
    job_vectors = vectors[1:]

    # Compute cosine similarity
    similarities = cosine_similarity(user_vector, job_vectors).flatten()

    # Attach similarity score to jobs
    for job, score in zip(jobs, similarities):
        job["score"] = float(score)

    # Sort by similarity descending
    ranked_jobs = sorted(jobs, key=lambda x: x["score"], reverse=True)
    return ranked_jobs