from contextlib import asynccontextmanager
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from app.api.api_v1.router import router
from app.core.config import settings
from app.models.user_model import User
from bson import ObjectId

from pydantic.v1.json import ENCODERS_BY_TYPE

ENCODERS_BY_TYPE[ObjectId] = str


@asynccontextmanager
async def lifespan(application: FastAPI):
    
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    
    db = db_client[settings.MONGO_DB_NAME]
    await init_beanie(
        database=db,
        document_models=[
            User,
        ]
    )
    yield
    
    db_client.close()

app = FastAPI(
    title= settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openai.json",
    lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins= settings.BACKEND_CORS_ORIGINS,
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers= ["*"],
    
)

app.include_router(router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Backend with Mongo"}



if __name__ == "__main__": 
    import uvicorn 
  
    uvicorn.run("__main__:app",reload=True, host="127.0.0.1", port=8000)
    