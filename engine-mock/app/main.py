"""Mock Engine Core: a pretend version of Starling's Engine platform.

Owner: Person 1

Run:  uvicorn app.main:app --reload --port 8001
Docs: http://localhost:8001/docs
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Session, select

from app import db
from app.models import Account
from app.routes import accounts, admin, simulate, spaces, standing_orders, transactions
from seed.load import SEED_FILE, reset_and_load


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    # A brand-new database has no accounts: load the demo data so nobody has to remember /admin/reset
    with Session(db.engine) as session:
        empty = session.exec(select(Account)).first() is None
    if empty and SEED_FILE.exists():
        print("engine-mock: empty database, loading seed data:", reset_and_load())
    yield


app = FastAPI(
    title="Mock Engine Core",
    description="Accounts, transactions, Spaces and standing orders for the Meflation demo.",
    version="0.1.0",
    lifespan=lifespan,
)


#@app.get("/")
#def root():
#    return {"Hello" : "World"}


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok", "service": "engine-mock"}


for module in (accounts, transactions, spaces, standing_orders, simulate, admin):
    app.include_router(module.router)
