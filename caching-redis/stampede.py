'''--stampede creation:
import concurrent.futures
import threading
import time
import redis
r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)
print("Redis connected:", r.ping())
KEY = "stampede:product:999"
# Make sure the cache starts empty
r.delete(KEY)
db_calls = 0
# Used only to safely update db_calls
counter_lock = threading.Lock()
# Make all 20 threads start their Redis check at roughly the same time
start_barrier = threading.Barrier(20)

def get_product():
    global db_calls
    # Wait until all 20 requests are ready
    start_barrier.wait()
    # Check Redis
    value = r.get(KEY)
    if value is not None:
        return "HIT"
    # Cache miss -> pretend to query database
    with counter_lock:
        db_calls += 1
    time.sleep(1)
    # Put result into Redis
    r.set(KEY, "Expensive Product", ex=60)
    return "MISS -> DB"
print("Starting 20 concurrent requests...")
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    futures = [
        executor.submit(get_product)
        for _ in range(20)
    ]
    results = [future.result() for future in futures]
print("Finished!")
print("Results:", results)
print("Database calls:", db_calls)'''

#cache stampede solving
import concurrent.futures
import threading
import time
import uuid
import redis

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)
print("Redis connected:", r.ping())

KEY = "stampede:product:999"
LOCK_KEY = "lock:stampede:product:999"

# Start clean
r.delete(KEY)
r.delete(LOCK_KEY)

db_calls = 0
counter_lock = threading.Lock()

# Make all requests check the cache at roughly the same time
start_barrier = threading.Barrier(20)

def release_lock(lock_key, lock_value):
    """
    Delete the lock only if it still belongs to us.
    """
    script = """
    if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
    else
        return 0
    end
    """
    r.eval(
        script,
        1,
        lock_key,
        lock_value,
    )

def get_product():
    global db_calls

    # Make all requests arrive together
    start_barrier.wait()

    # -------------------------
    # 1. Check cache
    # -------------------------

    value = r.get(KEY)

    if value is not None:
        return "HIT"

    # -------------------------
    # 2. Cache MISS
    # -------------------------

    # Give this request a unique lock value
    lock_value = str(uuid.uuid4())

    # Try to acquire the lock
    got_lock = r.set(
        LOCK_KEY,
        lock_value,
        nx=True,
        ex=10,
    )

    if got_lock:
        try:
            # -------------------------
            # 3. Double-check cache
            # -------------------------

            value = r.get(KEY)

            if value is not None:
                return "HIT-AFTER-LOCK"

            # -------------------------
            # 4. Simulate DB call
            # -------------------------

            with counter_lock:
                db_calls += 1

            print("DB CALL")

            time.sleep(1)

            # -------------------------
            # 5. Populate cache
            # -------------------------

            r.set(
                KEY,
                "Expensive Product",
                ex=60,
            )

            return "MISS -> DB"

        finally:
            # -------------------------
            # 6. Release lock
            # -------------------------

            release_lock(
                LOCK_KEY,
                lock_value,
            )

    else:
        # -------------------------
        # 7. Someone else has lock
        # -------------------------

        # Wait a little and check cache again
        for _ in range(20):
            time.sleep(0.1)

            value = r.get(KEY)

            if value is not None:
                return "HIT-AFTER-WAIT"

        return "FAILED"


# -------------------------
# Run 20 concurrent requests
# -------------------------

print("Starting 20 concurrent requests...")

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:

    futures = [
        executor.submit(get_product)
        for _ in range(20)
    ]

    results = [
        future.result()
        for future in futures
    ]


print("Finished!")
print("Results:", results)
print("Database calls:", db_calls)