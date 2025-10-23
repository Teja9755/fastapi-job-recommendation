import asyncio
from app.models import Job
from app.database import AsyncSessionLocal

companies = ["TechCorp", "DataCorp", "MLCorp", "AIHub", "CloudSolutions"]
titles = ["Python Backend Developer", "Data Analyst", "ML Engineer", "Frontend Developer", "DevOps Engineer"]
locations = ["Bangalore", "Hyderabad", "Chennai", "Pune", "Mumbai"]
skills_list = [
    ["Python", "FastAPI", "PostgreSQL"],
    ["Python", "Pandas", "SQL"],
    ["Python", "scikit-learn", "FastAPI"],
    ["JavaScript", "React", "CSS"],
    ["AWS", "Docker", "Kubernetes"]
]

async def seed_job():
    async with AsyncSessionLocal() as session:
        for i in range(50):
            job=Job(
                title=titles[i % len(titles)],
                description=f"job description is {titles[i % len(titles)]}",
                company=companies[i % len(companies)],
                locations=locations[i % len(locations)],
                is_active=True,
                skills_required=skills_list[i % len(skills_list)]
            )
            session.add(job)
        await session.commit()
        print("50 jobs inserted!")

asyncio.run(seed_job())