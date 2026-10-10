"""Owner: Person 1"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db import get_session
from app.models import Space
from app.schemas import SpaceCreate, TransferCreate

router = APIRouter(tags=["spaces"])


@router.get("/spaces", response_model=list[Space])
def list_spaces(account_id: str, session: Session = Depends(get_session)):
    # TODO(Person 1)
    raise HTTPException(501, "Not implemented yet")


@router.post("/spaces", response_model=Space, status_code=201)
def create_space(body: SpaceCreate, session: Session = Depends(get_session)):
    # TODO(Person 1): create with balance 0
    raise HTTPException(501, "Not implemented yet")


@router.post("/spaces/{space_id}/transfers", response_model=Space)
def transfer_into_space(space_id: str, body: TransferCreate, session: Session = Depends(get_session)):
    """Move money from the main account into the Space.

    Return 400 if the main account balance is too low.
    """
    # TODO(Person 1)
    raise HTTPException(501, "Not implemented yet")
