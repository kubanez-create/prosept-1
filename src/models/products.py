from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.db import Base
from src.schemas.products import Product


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    article: Mapped[str]
    ean_13: Mapped[Optional[float]]
    name: Mapped[Optional[str]]
    cost: Mapped[Optional[float]]
    recommended_price: Mapped[Optional[str]]
    category_id: Mapped[Optional[float]]
    ozon_name: Mapped[Optional[str]]
    name_1c: Mapped[Optional[str]]
    wb_name: Mapped[Optional[str]]
    ozon_article: Mapped[Optional[float]]
    wb_article: Mapped[Optional[float]]
    ym_article: Mapped[Optional[str]]
    wb_article_td: Mapped[Optional[str]]
    proddealers: Mapped[List["ProductDealer"]] = relationship(
        back_populates="products"
    )

    def to_read_model(self) -> Product:
        return Product(
            id=self.id,
            name=self.name,
        )
