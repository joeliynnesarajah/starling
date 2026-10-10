"""Categorised transactions and CSV statement upload.

Owner: Person 2
"""

from fastapi import APIRouter, HTTPException, UploadFile

from app.schemas import CategorisationSummary, CategorisedTransaction, StatementImportResponse

router = APIRouter(tags=["statements"])


@router.get("/categorised", response_model=list[CategorisedTransaction])
def categorised_transactions(account_id: str):
    """Useful for debugging the mapping, and for a "see your transactions" view."""
    # TODO(Person 2): engine_client.get_transactions -> categorise
    raise HTTPException(501, "Not implemented yet")


@router.get("/categorised/summary", response_model=CategorisationSummary)
def categorisation_summary(account_id: str):
    """Powers the "94% of your spending categorised" badge."""
    # TODO(Person 2)
    raise HTTPException(501, "Not implemented yet")


@router.post("/statements/upload", response_model=StatementImportResponse, status_code=201)
async def upload_statement(file: UploadFile, account_name: str = "My statement"):
    """Parse the CSV, create an account for it in Engine, bulk insert, return the summary.

    Creating the account needs an Engine endpoint: agree it with Person 1.
    """
    # TODO(Person 2)
    raise HTTPException(501, "Not implemented yet")
