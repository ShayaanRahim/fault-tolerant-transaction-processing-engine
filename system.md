Client (curl / Swagger UI)
        │
        ▼
main.py          — FastAPI app exists, router is wired up, pool is open
        │
        ▼
routes/accounts.py — the endpoint function receives the request
        │
        ▼
schemas.py (AccountCreate) — validates/shapes the incoming JSON
        │
        ▼
db.py (get_conn())  — hands out a connection with transaction guarantees
        │
        ▼
Postgres            — the actual SQL runs
        │
        ▼
schemas.py (AccountOut) — shapes the outgoing response
        │
        ▼
Client receives validated, typed JSON back