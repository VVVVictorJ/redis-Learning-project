from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import redis
from contextlib import asynccontextmanager

from api.api import api_router
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = redis.Redis(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
    )
    yield
    app.state.redis.close()


app = FastAPI(title="Cat Expense Tracker API", version="0.1.0", lifespan=lifespan)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to the frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Cat Expense Tracker API"}
