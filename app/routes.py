from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User, Job,Userprofile
from app.schemas import UserCreate, UserOut, JobCreate, JobOut,UserProfileOut,UserProfileCreate
from app.database import get_db
from app.utils import hash_password, verify_password
from typing import List
from app.utils import preprocess_job,preprocess_user_input,vectorize_and_rank

router = APIRouter()

# ------------ User ----------------
@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login")
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalars().first()
    if not existing_user or not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}

# ------------ Job ----------------
@router.post("/jobs", response_model=JobOut)
async def create_job(job: JobCreate, db: AsyncSession = Depends(get_db)):
    # Use model_dump() instead of dict() for Pydantic v2
    new_job = Job(**job.model_dump())
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    return new_job

@router.get("/jobs/{id}",response_model=JobOut)
async def get_job_id(id:int,db:AsyncSession=Depends(get_db)):
    result=await db.execute(select(Job).where(Job.id==id))
    job=result.scalars().first()
    if not job:
        raise HTTPException(status_code=404,detail="not found")
    else:
        return job


@router.post("/user_profile", response_model=UserProfileOut)
async def create_user_profile(profile: UserProfileCreate, db: AsyncSession = Depends(get_db)):
    # Check if username already exists
    result = await db.execute(select(Userprofile).where(Userprofile.username == profile.username))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_profile = Userprofile(
        username=profile.username,
        skills=profile.skills,
        current_location=profile.current_location,
        preferred_location=profile.preferred_location
    )
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile

# ------------ Get all user profiles ------------
@router.get("/user_profiles", response_model=List[UserProfileOut])
async def get_user_profiles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Userprofile))
    profiles = result.scalars().all()
    return profiles

# ------------ Get single user profile by ID ------------
@router.get("/user_profile/{id}", response_model=UserProfileOut)
async def get_user_profile(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Userprofile).where(Userprofile.id == id))
    profile = result.scalars().first()
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile


@router.get("/recommendations/{user_id}", response_model=List[JobOut])
async def get_recommendations(user_id: int, db: AsyncSession = Depends(get_db), top_n: int = 10):
    # 1️⃣ Fetch user profile
    result = await db.execute(select(Userprofile).where(Userprofile.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User profile not found")

    # 2️⃣ Preprocess user input
    user_processed = preprocess_user_input(user.__dict__)

    # 3️⃣ Fetch all jobs
    result = await db.execute(select(Job))
    jobs = result.scalars().all()

    # 4️⃣ Preprocess jobs
    processed_jobs = [preprocess_job(job.__dict__) for job in jobs]

    # 5️⃣ Rank jobs using vectorization
    ranked_jobs = vectorize_and_rank(user_processed, processed_jobs)

    # 6️⃣ Return top N
    return ranked_jobs[:top_n]