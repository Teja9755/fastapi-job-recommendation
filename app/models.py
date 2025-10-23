from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    skills=Column(JSONB,default=list)

class Userprofile(Base):
    __tablename__="userprofile"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String(50),nullable=False)
    skills=Column(JSONB,default=list)
    current_location=Column(String(50))
    preferred_location=Column(String(50)) 

class Job(Base):
    __tablename__ = "Jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    description = Column(Text)
    company = Column(String(20), nullable=False)
    locations = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    skills_required=Column(JSONB,default=list)
