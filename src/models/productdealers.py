from datetime import date
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.db import Base
from src.schemas.dealerprices import DealerPrice


class ProductDealer(Base):
    __tablename__ = "productdealer"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(ForeignKey("dealerprice.product_key"))
    key_obj: Mapped["DealerPrice"] = relationship(back_populates="proddealer")
    dealer_id: Mapped[int] = mapped_column(ForeignKey("dealer.id"))
    dealer_obj: Mapped[
        "Dealer"] = relationship(back_populates="productdealers")
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    product_obj: Mapped["Product"] = relationship(back_populates="proddealers")

    def to_read_model(self) -> DealerPrice:
        return DealerPrice(
            id=self.id,
            product_key=self.product_key,
            price=self.price,
            product_url=self.product_url,
            product_name=self.product_name,
            date=self.date,
            dealer_id=self.dealer_id
        )