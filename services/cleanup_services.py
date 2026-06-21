import asyncio
import time
import os
# from storage.metadata import otp_store
import storage.metadata_service as metadata_service


# 🔥 Cleanup function (runs forever)
async def cleanup_task():
    while True:
        current_time = int(time.time())
        to_delete = [] 

        otps = metadata_service.get_all_otps()

        for otp in otps:
            data = metadata_service.get_metadata(otp)
            if data is None: continue
            # print(data)
            if current_time - data["uploaded_time"]>600 or data["used"]:
                if data["storage"]=="file":
                    file_path = data["file_path"]
                    # print("Trying to delete:", file_path)
                    # print("Exists?", os.path.exists(file_path))

                    if os.path.exists(file_path):
                        os.remove(file_path)
                        # print("Deleted successfully")
                    # else:
                        # print("File not found")   

                to_delete.append(otp)


        for otp in to_delete:
            metadata_service.delete_metadata(otp)

        print("Cleanup done")
    

        await asyncio.sleep(30)  # ⏳ run every 30 seconds

def delete_files(file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)


