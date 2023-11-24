from datetime import date
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.db import Base
from src.schemas.dealerprices import DealerPrice


class DealerPrice(Base):
    __tablename__ = "dealerprice"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_key: Mapped[str] = mapped_column(unique=True)
    price: Mapped[float]
    product_url: Mapped[Optional[str]]
    product_name: Mapped[str]
    date: Mapped[date]
    dealer_id: Mapped[int] = mapped_column(ForeignKey("dealer.id"))
    dealer: Mapped["Dealer"] = relationship(back_populates="dealerprices")
    proddealer: Mapped["ProductDealer"] = relationship(back_populates="key_obj")

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