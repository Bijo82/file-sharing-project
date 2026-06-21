from fastapi import APIRouter, HTTPException
from models.schemas import TextData
from services.otp_services import otpgenerate
import uuid
import time
import storage.metadata_service as metadata_service

router = APIRouter()

@router.post("/uploadtext")
async def uploadText(data:TextData):

    text = data.text

    if text.strip() == "":
        raise HTTPException(status_code=400,detail="Text cannot be empty")

    MAX_INLINE_TEXT_SIZE = 10*1024
    MAX_TEXT_SIZE = 1*1024*1024

    if len(text.encode("utf-8")) > MAX_TEXT_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Text size exceeds 1MB limit"
        )
    otp = otpgenerate()
    while(metadata_service.otp_exists(otp)):
        otp = otpgenerate()
    
    if len(text.encode("utf-8")) <= MAX_INLINE_TEXT_SIZE:
        metadata={
            "type" : "text",
            "storage" : "memory",
            "content" : text,
            "uploaded_time": int(time.time()),
            "used" : False
        }
        metadata_service.save_metadata(otp,metadata)
    else:
        text_id = f"{str(uuid.uuid4())}.txt"
        text_path = f"texts/{text_id}"

        with open(text_path,"w",encoding="utf-8") as t:
            try:
                t.write(text)
            except Exception:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to save text")

        metadata={
            "type" : "text",
            "storage" : "file",
            "file_path" : text_path,
            "file_name" : text_id,
            "uploaded_time": int(time.time()),
            "used" : False
        }
        metadata_service.save_metadata(otp,metadata)
    return {
        "message" : "Text saved successfully",
        "Otp": otp,
        # "storage" : otp_store[otp]["storage"]
        }

    