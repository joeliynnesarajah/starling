"""Mock Engine Core: a pretend version of Starling's Engine platform.

Owner: Person 1

Run:  uvicorn app.main:app --reload --port 8001
Docs: http://localhost:8001/docs
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import init_db
from app.routes import accounts, admin, simulate, spaces, standing_orders, transactions


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Mock Engine Core",
    description="Accounts, transactions, Spaces and standing orders for the Meflation demo.",
    version="0.1.0",
    lifespan=lifespan,
)

@app.get("/")
def root():
    return {"Hello" : "World"}


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok", "service": "engine-mock"}


for module in (accounts, transactions, spaces, standing_orders, simulate, admin):
    app.include_router(module.router)
