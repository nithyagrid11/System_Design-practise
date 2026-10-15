import json
import statistics
import time

import psycopg
import redis


# -------------------------
# Connect to Redis
# -------------------------

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)


# -------------------------
# Connect to PostgreSQL
# -------------------------

db = psycopg.connect(
    "host=localhost "
    "port=5433 "
    "dbname=cache_lab "
    "user=cache_user "
    "password=cache_pass",
    autocommit=True,
)


# -------------------------
# Put the same user in Redis
# -------------------------

user = {
    "id": 3,
    "name": "Nithya",
    "email": "nithya@example.com",
}

redis_client.set(
    "user:3",
    json.dumps(user),
)


# -------------------------
# Functions to benchmark
# -------------------------

def read_from_redis():
    return redis_client.get("user:3")


def read_from_postgres():
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, name, email
            FROM users
            WHERE id = %s
            """,
            (3,),
        )

        return cursor.fetchone()


# -------------------------
# Benchmark helper
# -------------------------

def benchmark(function, iterations=1000):
    times = []

    for _ in range(iterations):
        start = time.perf_counter_ns()

        function()

        end = time.perf_counter_ns()

        elapsed_us = (end - start) / 1_000

        times.append(elapsed_us)

    return {
        "average": statistics.mean(times),
        "median": statistics.median(times),
        "p95": statistics.quantiles(times, n=100)[94],
        "total": sum(times),
    }


# -------------------------
# Warm-up
# -------------------------

for _ in range(100):
    read_from_redis()
    read_from_postgres()


# -------------------------
# Run benchmark
# -------------------------

redis_results = benchmark(read_from_redis)
postgres_results = benchmark(read_from_postgres)


# -------------------------
# Print results
# -------------------------

print("\nRedis")
print("-----")
print(f"Average : {redis_results['average']:.2f} µs")
print(f"Median  : {redis_results['median']:.2f} µs")
print(f"P95     : {redis_results['p95']:.2f} µs")
print(f"Total   : {redis_results['total'] / 1000:.2f} ms")


print("\nPostgreSQL")
print("----------")
print(f"Average : {postgres_results['average']:.2f} µs")
print(f"Median  : {postgres_results['median']:.2f} µs")
print(f"P95     : {postgres_results['p95']:.2f} µs")
print(f"Total   : {postgres_results['total'] / 1000:.2f} ms")