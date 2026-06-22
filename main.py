from fastapi import FastAPI
import asyncio
from services.cleanup_services import cleanup_task
from routes.files import router as FileRouter
from routes.texts import router as TextRouter
from fastapi.middleware.cors import CORSMiddleware
import os

os.makedirs("uploads", exist_ok=True)
os.makedirs("texts", exist_ok=True)
app = FastAPI(title="OTP File Sharing API",version="1.0.0",description="Secure file and text sharing using OTP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(FileRouter)
app.include_router(TextRouter)

@app.get("/")
async def root():
    return {"message":"Hello World"}


#Cleanup
@app.on_event("startup")
async def start_cleanup():
    asyncio.create_task(cleanup_task())
