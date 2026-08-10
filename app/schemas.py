from decimal import Decimal
from datetime import datetime
from uuid import UUID
from typing import Literal
from pydantic import BaseModel, Field

class AccountCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    type: Literal["asset", "liability", "equity"] = "liability"

class AccountOut(BaseModel):
    id: UUID
    name: str
    type: str
    balance: Decimal
    created_at: datetime