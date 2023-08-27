from typing import List

from fastapi import APIRouter, Body, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from models.ledgerEntryModel import LedgerEntry, LedgerEntryUpdate

router = APIRouter()


@router.post("/", response_description="Create a new entry in the ledger", status_code=status.HTTP_201_CREATED, response_model=LedgerEntry)
def create_ledger_entry(request: Request, ledger_entry: LedgerEntry = Body(...)):
    ledger_entry = jsonable_encoder(ledger_entry)
    new_ledger_entry = request.app.database["ledger"].insert_one(ledger_entry)
    created_ledger_entry = request.app.database["ledger"].find_one(
        {"_id": new_ledger_entry.inserted_id}
    )
    return created_ledger_entry


@router.get("/", response_description="Display full ledger", response_model=List[LedgerEntry])
def show_ledger(request: Request):
    ledger = list(request.app.database["ledger"].find(limit=100))
    return ledger


@router.get("/{id}", response_description="Get a single ledger entry by id", response_model=LedgerEntry)
def find_ledger_entry(id: str, request: Request):
    if (ledger_entry := request.app.database["ledger"].find_one({"_id": id})) is not None:
        return ledger_entry
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Ledger Entry with ID {id} not found")


@router.put("/{id}", response_description="Update a ledger entry", response_model=LedgerEntry)
def update_ledger_entry(id: str, request: Request, ledger_entry: LedgerEntryUpdate = Body(...)):
    ledger_entry = {k: v for k, v in ledger_entry.dict().items()
                    if v is not None}
    if len(ledger_entry) >= 1:
        update_ledger_entry = request.app.database["ledger"].update_one(
            {"_id": id}, {"$set": ledger_entry}
        )

        if update_ledger_entry.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Ledger Entry with ID {id} not found")

    if (
        existing_book := request.app.database["ledger"].find_one({"_id": id})
    ) is not None:
        return existing_book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Ledger Entry with ID {id} not found")


@router.delete("/{id}", response_description="Delete a ledger entry")
def delete_ledger_entry(id: str, request: Request, response: Response):
    delete_ledger_entry = request.app.database["ledger"].delete_one({
                                                                    "_id": id})

    if delete_ledger_entry.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Ledger Entry with ID {id} not found")
