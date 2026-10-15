import json
import time

import redis
import psycopg


# -------------------------
# Redis connection
# -------------------------

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)


# -------------------------
# PostgreSQL connection
# -------------------------

db = psycopg.connect(
    "host=localhost "
    "port=5433 "
    "dbname=cache_lab "
    "user=cache_user "
    "password=cache_pass",
    autocommit=True,
)


def get_user(user_id):
    cache_key = f"user:{user_id}"

    # 1. Check Redis first
    cached = redis_client.get(cache_key)

    if cached is not None:
        print("CACHE HIT")
        return json.loads(cached)

    # 2. Redis did not have the user
    print("CACHE MISS")

    # 3. Ask PostgreSQL
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, name, email
            FROM users
            WHERE id = %s
            """,
            (user_id,),
        )

        row = cursor.fetchone()

    if row is None:
        return None

    # 4. Convert DB row to Python object
    user = {
        "id": row[0],
        "name": row[1],
        "email": row[2],
    }

    # 5. Put the result into Redis
    redis_client.set(
        cache_key,
        json.dumps(user),
        ex=60,
    )

    return user
# -------------------------
# Direct PostgreSQL read
# -------------------------

def direct_db_read(user_id):
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, name, email
            FROM users
            WHERE id = %s
            """,
            (user_id,),
        )

        return cursor.fetchone()


# -------------------------
# 1. Direct DB
# -------------------------

start = time.perf_counter_ns()

user = direct_db_read(3)

end = time.perf_counter_ns()

print("\nDIRECT POSTGRES")
print("User:", user)
print("Time:", (end - start) / 1_000_000, "ms")


# -------------------------
# 2. Force cache MISS
# -------------------------

redis_client.delete("user:3")

start = time.perf_counter_ns()

user = get_user(3)

end = time.perf_counter_ns()

print("\nCACHE MISS")
print("User:", user)
print("Time:", (end - start) / 1_000_000, "ms")


# -------------------------
# 3. Cache HIT
# -------------------------

start = time.perf_counter_ns()

user = get_user(3)

end = time.perf_counter_ns()

print("\nCACHE HIT")
print("User:", user)
print("Time:", (end - start) / 1_000_000, "ms")

'''
# -------------------------1st usecase - hit/miss/ttl
# Clear old cache
# -------------------------

redis_client.delete("user:3")


# -------------------------
# First request
# -------------------------

start = time.perf_counter_ns()

user = get_user(3)

end = time.perf_counter_ns()

print("User:", user)
print("Time:", (end - start) / 1_000_000, "ms")


# -------------------------
# Second request
# -------------------------

start = time.perf_counter_ns()

user = get_user(3)

end = time.perf_counter_ns()

print("User:", user)
print("Time:", (end - start) / 1_000_000, "ms")'''