import os
import redis

#Also allows local deployment
Redis = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
    ssl=True
)

try:
    Redis.ping()
    print("Redis Connected")
except Exception as e:
    print("Redis Connection Failed:", e)
