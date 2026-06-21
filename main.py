from fastapi import FastAPI
import asyncio
from services.cleanup_services import cleanup_task
from routes.files import router as FileRouter
from routes.texts import router as TextRouter
import os

os.makedirs("uploads", exist_ok=True)
os.makedirs("texts", exist_ok=True)
app = FastAPI()

app.include_router(FileRouter)
app.include_router(TextRouter)

@app.get("/")
async def root():
    return {"message":"Hello World"}


#Cleanup
@app.on_event("startup")
async def start_cleanup():
    asyncio.create_task(cleanup_task())
