from fastapi import APIRouter,UploadFile,File,BackgroundTasks
from fastapi.responses import FileResponse
from fastapi import HTTPException
import uuid
import time
import os
from services.otp_services import otpgenerate
from zipfile import ZipFile
from services.cleanup_services import delete_files
from typing import List,Annotated
import storage.metadata_service as metadata_service

router = APIRouter()

@router.post("/uploadfile")
async def up_file(uploaded_file: Annotated[List[UploadFile],File(...)]):

    chunk_size=2*1024*1024
    ls=[]
    file_path=""
    file_id=""
    total_size=0
    MAX_FILE_SIZE = 100*1024*1024 #100MB
    file_too_large = False

    for uploads in uploaded_file:
        file_too_large = False  
        file_id = f"{str(uuid.uuid4())}-{uploads.filename}"
        file_path = f"uploads/{file_id}"
        total_size=0

        with open(file_path,"wb") as file:
            while True:
                content = await uploads.read(chunk_size)
                
                if not content:
                    break

                total_size+=len(content)
                if total_size > MAX_FILE_SIZE:
                    file_too_large = True
                    break
                
                file.write(content)

        if file_too_large: 
            os.remove(file_path)
            delete_files(ls)
            raise HTTPException(status_code=400,detail="File size exceeds the 100MB limit")

        if total_size==0: 
            os.remove(file_path)
            delete_files(ls)
            raise HTTPException(status_code=400,detail="File is empty")
        ls.append(file_path)

    
    if len(ls)>1:
        file_id = f"Files{str(uuid.uuid4())}.zip"
        file_path=f"uploads/{file_id}"
        try:
            with ZipFile(file_path,"w") as zipf:
                for i in ls:
                    zipf.write(i)
        except Exception:
            delete_files(ls)
            raise HTTPException(
                status_code=500,
                detail="Failed to create ZIP"
            )

    # size = os.path.getsize(file_path)
    # if os.path.getsize(file_path) == 0: return {"error":"File is empty"}


    otp = otpgenerate()
    while(metadata_service.otp_exists(otp)):
        otp = otpgenerate()

    if len(ls)==1:
        metadata={
            "type": "file",
            "storage" : "file",
            "file_id" : file_id,
            "file_name" : uploaded_file[0].filename,
            "file_path" : file_path,
            "uploaded_time": int(time.time()),
            "used": False
        }
        metadata_service.save_metadata(otp,metadata)

    else:
        metadata={
            "type": "file",
            "storage" : "file",
            "file_id" : file_id,
            "file_name" : "Files.zip",
            "file_path" : file_path,
            "uploaded_time": int(time.time()),
            "used": False
        }
        metadata_service.save_metadata(otp,metadata)
        delete_files(ls)
    
    file_name= metadata["file_name"]

    return {
        "message" : "File Saved Successfully",
        "OTP" : otp,
        "filename" : file_name
    }
    
    # finally:
    #     await uploaded_file.close()



@router.get("/download")
async def down(otp:str):
    if len(otp) != 6 or not otp.isalnum(): 
        raise HTTPException(status_code=400,detail="Invalid OTP")
    
    if not metadata_service.otp_exists(otp): 
        raise HTTPException(status_code=404,detail="OTP not found")

    data = metadata_service.get_metadata(otp)

    if data is None:
        raise HTTPException(status_code=404,detail="OTP not found")
    
    if data["used"]:
        raise HTTPException(status_code=410,detail="OTP already used")

    if data["type"]=="file":
        file_path = data["file_path"]


        if os.path.exists(file_path) :
            # data["used"]=True
            metadata_service.mark_used(otp)
            # backgroundtask.add_task(rem_otp,otp)                not needed as we have used diff cleanup logic
            # backgroundtask.add_task(rem_file,file_path)
            
            return FileResponse(file_path, filename=data["file_name"])
        else:
            raise HTTPException(status_code=404,detail="File not found")
    

    if data["type"] == "text":
        if data["storage"]=="memory":
            metadata_service.mark_used(otp)
            return {"content" : data["content"]}
        else:
            file_path = data["file_path"]
            metadata_service.mark_used(otp)
            # metadata_service.delete_metadata(otp)

            return FileResponse(file_path, filename=data["file_name"])
