import uuid
from typing import Optional

from pydantic import BaseModel, Field


class LedgerEntry(BaseModel):
    id: object = Field(default_factory=uuid.uuid4, alias="_id")
    currentBalance: float = Field(...)
    dateOfEntry: object = Field(...)
    expenditure: object = Field(...)
    income: object = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "currentBalance": 1000,
                "dateOfEntry": "21-08-2023",
                "expenditure": {
                    "books": 4000,
                    "celebration": {
                        "food": 5000,
                        "decoration": 1000
                    },
                },
                "income": {
                    "fees": 10000,
                    "person1": 2000
                }
            }
        }


class LedgerEntryUpdate(BaseModel):
    currentBalance: Optional[float]
    dateOfEntry: Optional[object]
    expenditure: Optional[object]
    income: Optional[object]

    class Config:
        schema_extra = {
            "example": {
                "currentBalance": 1000,
                "dateOfEntry": "21-08-2023",
                "expenditure": {
                    "books": 4000,
                    "celebration": {
                        "food": 5000,
                        "decoration": 1000
                    },
                },
                "income": {
                    "fees": 10000,
                    "person1": 2000
                }
            }
        }
