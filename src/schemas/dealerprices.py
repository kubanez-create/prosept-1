from datetime import date
from typing import Optional
from pydantic import BaseModel


class DealerPrice(BaseModel):
    product_key: str
    price: float
    product_url: Optional[str]
    product_name: str
    date: date
    dealer_id: int
