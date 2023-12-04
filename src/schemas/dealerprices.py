from datetime import date
from typing import Optional

from pydantic import BaseModel

from src.schemas.products import ProductDb


class DealerPrice(BaseModel):
    product_key: str
    price: float
    product_url: Optional[str]
    product_name: str
    date: date
    dealer_id: int


class DealerPriceDb(BaseModel):
    id: str
    price: float
    product_name: str
    date: date
    status: bool | None = False
    dealer_id: int
    product: ProductDb | None = None
