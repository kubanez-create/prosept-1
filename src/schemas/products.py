from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    id: int
    article: str
    ean_13: float | None = None
    name: str | None = None
    cost: float | None = None
    recommended_price: str | None = None
    category_id: float | None = None
    ozon_name: str | None = None
    name_1c: str | None = None
    wb_name: str | None = None
    ozon_article: float | None = None
    wb_article: float | None = None
    ym_article: str | None = None
    wb_article_td: str | None = None


class ProductDb(BaseModel):
    name_1c: str | None = None
    cost: float | None = None
    recommended_price: str | None = None


class RecommendedProduct(BaseModel):
    id: int
    name_1c: str


class ProductDS(BaseModel):
    id: int
