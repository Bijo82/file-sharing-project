from storage.redis_client import Redis
import json

def save_metadata(otp,metadata):
    # metadata={
    #         "type": t,
    #         "storage" : storage,
    #         "file_id" : file_id,
    #         "file_name" : filename,
    #         "file_path" : file_path,
    #         # "expiry" : current_sec+600,
    #         "used": used
    #     }
    Redis.set(otp,json.dumps(metadata),ex=600)

def get_all_otps():
    return Redis.keys("*")
    
def get_metadata(otp):
    metadata = Redis.get(otp)

    print("Redis returned:", repr(metadata))

    if metadata is None:
        return None
    else:
        return json.loads(metadata)

def delete_metadata(otp):
    Redis.delete(otp)

def otp_exists(otp):
    return Redis.exists(otp)

def mark_used(otp):
    data = get_metadata(otp)
    if data == "None" : pass
    else: 
        data["used"]=True
        save_metadata(otp,data)
