from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.db import Base
from src.schemas.dealers import Dealer


class Dealer(Base):
    __tablename__ = "dealer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    dealerprices: Mapped[
        List["DealerPrice"]] = relationship(back_populates="dealer")
    productdealers: Mapped[
        List["ProductDealer"]] = relationship(back_populates="dealer_obj")

    def to_read_model(self) -> Dealer:
        return Dealer(
            id=self.id,
            name=self.name,
        )