# app/schemas.py
from pydantic import BaseModel, EmailStr, field_validator
from typing import List

# ---------- User Schemas ----------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    skills:str

    # Pydantic v2 replacement for @validator
    @field_validator("password")
    def password_length(cls, v):
        if not (6 <= len(v) <= 72):
            raise ValueError("Password must be between 6 and 72 characters")
        return v

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = {"from_attributes": True}  # Pydantic v2 uses model_config instead of Config

class UserProfileCreate(BaseModel):
    username: str
    skills: List[str]
    current_location: str
    preferred_location: str

class UserProfileOut(BaseModel):
    id: int
    username: str
    skills: List[str]
    current_location: str
    preferred_location: str

    model_config = {"from_attributes": True}    



# ---------- Job Schemas ----------
class JobCreate(BaseModel):
    title: str
    description: str
    company: str
    location: str
    skills_required:str

class JobOut(BaseModel):
    id: int
    title: str
    description: str
    company: str
    location: str
    skills_required: List[str]  # <-- change to List[str]
    score: float  # optional if you want similarity score

    model_config = {"from_attributes": True}
