import datetime
from typing import Optional, Annotated
from annotation.objectIdAnnotated import ObjectIdPydanticAnnotation

from bson import ObjectId
from pydantic import BaseModel, Field


class LedgerEntry(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(default_factory=ObjectId, alias="_id")
    income: object = Field(...)
    expenditure: object = Field(...)
    currentBalance: float = Field(...)
    lastUpdated: object = Field(
        default_factory=datetime.datetime.today, alias="lastUpdated")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": ObjectId('64eb840060251801697d99bb'),
                "income": {
                    "fees": 10000,
                    "person1": 2000
                },
                "expenditure": {
                    "books": 4000,
                    "celebration": {
                        "food": 5000,
                        "decoration": 1000
                    },
                },
                "currentBalance": 1000,
                "lastUpdated": datetime.datetime.today
            }
        }


class LedgerEntryUpdate(BaseModel):
    income: Optional[object]
    expenditure: Optional[object]
    currentBalance: Optional[float]

    class Config:
        schema_extra = {
            "example": {
                "income": {
                    "fees": 10000,
                    "person1": 2000
                },
                "expenditure": {
                    "books": 4000,
                    "celebration": {
                        "food": 5000,
                        "decoration": 1000
                    },
                },
                "currentBalance": 1000,
            }
        }
