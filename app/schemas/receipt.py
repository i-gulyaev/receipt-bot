import datetime
from typing import List

from pydantic import BaseModel


class ReceiptItem(BaseModel):
    name: str
    price: float
    total_sum: float
    quantity: float


class Receipt(BaseModel):
    seller: str
    total_sum: float
    date: datetime.datetime
    items: List[ReceiptItem] = []
