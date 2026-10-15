# System Design Practice

A hands-on learning repository for exploring system design concepts through practical experiments, coding, benchmarking, and failure testing.

The goal is to understand how real-world systems work, why particular architectural decisions are made, and what trade-offs arise when systems scale.

## Labs

### 1. Redis Caching

**Folder:** `caching-redis/`

Practical experiments with Redis caching and PostgreSQL.

Topics covered:
- Redis basics and key-value operations
- Cache-aside pattern
- Cache hits, misses, and TTL
- Cache hit ratio
- Cache invalidation
- Cache stampede and concurrent requests
- Redis versus PostgreSQL performance benchmarking
- Docker Compose for local development

**Tech stack:** Python, Redis, PostgreSQL, Docker Compose

### 2. Cloudflare and CDN

**Folder:** `cloudflare-lab/`

Experiments exploring content delivery networks and HTTP caching behaviour.

Topics explored:
- CDN fundamentals
- Static asset delivery
- HTTP caching headers
- ETags and conditional requests
- Cache validation and origin requests
- Cloudflare caching concepts

**Tech stack:** HTML, CSS, Cloudflare

### 3. RabbitMQ and Asynchronous Processing

**Folder:** `rabbitmq-lab/`

A local learning lab for understanding message brokers and asynchronous job processing.

Planned experiments:
- Producers, consumers, and queues
- Exchanges, routing keys, and bindings
- Multiple competing consumers
- Acknowledgements and message durability
- Retries and dead-letter queues
- Prefetch and backpressure
- Worker failures and message redelivery
- Queue throughput and processing latency

**Tech stack:** Python, RabbitMQ, Pika, Docker

## Repository Structure

```text
System_Design-practise/
├── .gitignore
├── README.md
├── caching-redis/
│   ├── basic_redis.py
│   ├── benchmark.py
│   ├── cache_demo.py
│   ├── compose.yaml
│   ├── hit_ratio.py
│   ├── invalidation_demo.py
│   ├── requirements.txt
│   └── stampede.py
├── cloudflare-lab/
│   ├── index.html
│   └── styles.css
└── rabbitmq-lab/
    └── requirements.txt
```

Each Python lab maintains its own virtual environment locally. Virtual environments are excluded from version control; dependency manifests are committed so environments can be recreated.

## Getting Started

### Prerequisites

- Python 3
- Docker Desktop
- Git
- A local Redis and PostgreSQL setup for the caching experiments
- RabbitMQ for the messaging experiments

### Redis Lab

```bash
cd caching-redis

python3 -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt
docker compose up -d
```

Run an individual experiment, for example:

```bash
python basic_redis.py
```

Check each script's configuration before running it. Some experiments may require PostgreSQL or Redis to be available and correctly configured.

### RabbitMQ Lab

Start a local RabbitMQ instance with the management interface:

```bash
docker run -d \
  --name rabbitmq-lab \
  --hostname rabbitmq-lab \
  -p 5672:5672 \
  -p 15672:15672 \
  rabbitmq:4-management
```

Create and activate the Python environment:

```bash
cd rabbitmq-lab

python3 -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt
```

The RabbitMQ management interface is available at `http://localhost:15672`.

For local learning, the default credentials are:

- Username: `guest`
- Password: `guest`

These credentials are intended for local development, not production deployments.

### Cloudflare Lab

Open `cloudflare-lab/index.html` in a browser to inspect the static page and its styling. Cloudflare-specific experiments may require a configured domain and access to Cloudflare.

## Learning Approach

Each lab follows a practical approach:

1. Understand the underlying concept.
2. Read the relevant official documentation.
3. Implement a small experiment.
4. Observe the system's behaviour.
5. Measure performance where appropriate.
6. Introduce failures and investigate the results.
7. Document findings, limitations, and trade-offs.

## Future Topics

- Asynchronous programming and background workers
- Message queues and event-driven architecture
- Reverse proxies and load balancing
- Database replication and replication lag
- Database sharding and partitioning
- Reliability, retries, and idempotency
- Monitoring, latency, throughput, and bottlenecks
- Integrating multiple components into a mini-project

## Resources

- [RabbitMQ Documentation](https://www.rabbitmq.com/docs)
- [RabbitMQ Python Tutorials](https://www.rabbitmq.com/tutorials)
- [Redis Documentation](https://redis.io/docs/latest/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Cloudflare Learning Center](https://www.cloudflare.com/learning/)
- [Docker Documentation](https://docs.docker.com/)

---

**Purpose:** Learn system design by building, testing, measuring, and understanding systems rather than memorizing concepts.