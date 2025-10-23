from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import router
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code: create tables
    await init_db()
    yield
    

app = FastAPI(lifespan=lifespan)
app.include_router(router)