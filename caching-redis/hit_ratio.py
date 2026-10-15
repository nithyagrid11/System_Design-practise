import redis

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)

# Create 8 cached users
for i in range(1, 20):
    r.set(f"user:{i}", f"User {i}")


hits = 0
misses = 0

# 10 requests
requested_ids = [
    1, 2, 3, 4, 5,
    6, 12, 77,67,49
]

for user_id in requested_ids:
    value = r.get(f"user:{user_id}")

    if value is not None:
        hits += 1
    else:
        misses += 1

total = hits + misses
hit_ratio = hits / total

print("Hits:", hits)
print("Misses:", misses)
print("Hit ratio:", hit_ratio)
print("Hit ratio %:", hit_ratio * 100)