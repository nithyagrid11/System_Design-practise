import json
import redis
import psycopg

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)

db = psycopg.connect(
    "host=localhost "
    "port=5433 "
    "dbname=cache_lab "
    "user=cache_user "
    "password=cache_pass",
    autocommit=True,
)


def get_user(user_id):
    key = f"user:{user_id}"

    cached = redis_client.get(key)

    if cached:
        print("CACHE HIT")
        return json.loads(cached)

    print("CACHE MISS")

    with db.cursor() as cursor:
        cursor.execute(
            "SELECT id, name, email FROM users WHERE id = %s",
            (user_id,),
        )
        row = cursor.fetchone()

    user = {
        "id": row[0],
        "name": row[1],
        "email": row[2],
    }

    redis_client.set(key, json.dumps(user), ex=300)

    return user


# Start clean
redis_client.delete("user:3")

# 1. First request -> DB -> Redis
print("\nFIRST READ")
print(get_user(3))

# 2. Second request -> Redis
print("\nSECOND READ")
print(get_user(3))

# 3. Change PostgreSQL
print("\nUPDATE DATABASE")

with db.cursor() as cursor:
    cursor.execute(
        """
        UPDATE users
        SET name = 'Chitti Updated'
        WHERE id = 3
        """
    )

# 4. Read again WITHOUT invalidating Redis
print("\nREAD AFTER DB UPDATE")
print(get_user(3))

# 5. Invalidate cache
print("\nINVALIDATE CACHE")
redis_client.delete("user:3")

# 6. Read again
print("\nREAD AFTER INVALIDATION")
print(get_user(3))