from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import pool
from app.routes import accounts


# connection pool clean startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    pool.open()
    pool.wait(timeout=10)
    yield
    pool.close()

# instantiates actual server object and attaches account
# endpoints to it
app = FastAPI(title="Idempotent Event-Driven Ledger", lifespan=lifespan)
app.include_router(accounts.router)


# quick health check
@app.get("/health")
def health():
    return {"status": "ok"}



