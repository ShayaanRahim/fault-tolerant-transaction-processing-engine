# Idempotent Event-Driven Ledger

A fault-tolerant transaction processing service that demonstrates production-grade backend systems concepts including idempotency, double-entry accounting, concurrency control, and event-driven architecture. The service guarantees that duplicate requests never result in duplicate transactions, maintains ledger consistency under concurrent workloads, and publishes durable events using the transactional outbox pattern.

### Features

* **Idempotent transaction processing** using idempotency keys to guarantee exactly-once execution across client retries.
* **Double-entry ledger** ensuring every transaction is balanced and fully auditable.
* **Concurrent transfer safety** using PostgreSQL transactions and row-level locking (or optimistic concurrency control) to prevent lost updates and double-spends.
* **Transactional outbox pattern** for reliable event publishing to downstream consumers.
* **Event-driven architecture** with ledger events streamed to external services via Kafka or Redis.
* **Fault tolerance** validated through crash recovery and chaos testing to ensure ledger consistency after unexpected failures.
* **Comprehensive concurrency testing** simulating high-volume parallel transfers and duplicate request retries to verify system correctness under load.

### Tech Stack

* **Backend:** FastAPI
* **Database:** PostgreSQL
* **Messaging:** Kafka (or Redis Streams)
* **Testing:** pytest
* **Infrastructure:** Docker & Docker Compose
