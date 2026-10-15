import redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)

print("Redis connected:", redis_client.ping())

redis_client.set("user:1:name", "Nithya")

name = redis_client.get("user:1:name")

print("Name:", name)