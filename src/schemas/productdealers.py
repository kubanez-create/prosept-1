from pydantic import BaseModel


class ProductDealer(BaseModel):
    id: int
    key: str
    dealer_id: int
    product_id: int


class ProductDealerCreate(BaseModel):
    key: str
    dealer_id: int
    product_id: int
