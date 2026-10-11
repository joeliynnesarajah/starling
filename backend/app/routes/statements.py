"""Categorised transactions and CSV statement upload."""

from fastapi import APIRouter, HTTPException, UploadFile

from app import engine_client
from app.categorise.categorise import categorise
from app.categorise.csv_import import parse_statement
from app.schemas import CategorisationSummary, CategorisedTransaction, StatementImportResponse

router = APIRouter(tags=["statements"])

# The only fields the Engine mock stores for a transaction
ENGINE_FIELDS = ("date", "merchant", "mcc", "amount_pence")


def _get_transactions(account_id: str) -> list[dict]:
    # Ask the Engine mock for this account's transactions
    try:
        return engine_client.get_transactions(account_id)
    except engine_client.EngineError as e:
        raise HTTPException(502, str(e)) from e


@router.get("/categorised", response_model=list[CategorisedTransaction])
def categorised_transactions(account_id: str):
    """Useful for debugging the mapping, and for a "see your transactions" view."""
    results, _ = categorise(_get_transactions(account_id))
    return results


@router.get("/categorised/summary", response_model=CategorisationSummary)
def categorisation_summary(account_id: str):
    """Powers the "94% of your spending categorised" badge."""
    _, summary = categorise(_get_transactions(account_id))
    return summary


@router.post("/statements/upload", response_model=StatementImportResponse, status_code=201)
async def upload_statement(file: UploadFile, account_name: str = "My statement"):
    """Parse the CSV, create an account for it in Engine, bulk insert, return the summary."""

    # 1. Read the CSV with our parser
    try:
        rows = parse_statement(await file.read())
    except (ValueError, UnicodeDecodeError) as e:
        raise HTTPException(400, f"Couldn't read that file: {e}") from e
    if not rows:
        raise HTTPException(400, "No transactions found in that file")

    # 2. Label every row (uses the bank's own category column too)
    for i, row in enumerate(rows, start=1):
        row["id"] = i
    _, summary = categorise(rows)

    # 3. Create a new account in the Engine mock and save the transactions there
    try:
        account = engine_client.create_account(account_name)
        account_id = str(account["id"])
        to_save = [{key: row[key] for key in ENGINE_FIELDS} for row in rows]
        inserted = engine_client.bulk_create_transactions(account_id, to_save)
    except engine_client.EngineError as e:
        raise HTTPException(502, str(e)) from e

    # 4. Tell the frontend the new account id and how well we categorised it
    return StatementImportResponse(account_id=account_id, inserted=inserted, summary=summary)