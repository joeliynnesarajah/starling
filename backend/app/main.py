"""Meflation API: the app the frontend talks to.

Shared file: set up by Person 3. Add your router to the list at the bottom.

Run:  uvicorn app.main:app --reload --port 8000
Docs: http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import bank, inflation, inflation_proof, personal, statements

app = FastAPI(
    title="Meflation API",
    description="Your personal inflation rate, from Engine transactions and ONS price data.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok", "service": "meflation-api"}


# bank:            Person 1  (passes Engine data through to the frontend)
# statements:      Person 2  (CSV upload, categorised transactions)
# inflation:       Person 3  (ONS rates)
# personal:        Person 4  (personal rate and history)
# inflation_proof: Person 4  (the toggle)
for module in (bank, statements, inflation, personal, inflation_proof):
    app.include_router(module.router)
