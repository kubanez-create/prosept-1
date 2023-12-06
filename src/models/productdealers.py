from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.db import Base


class ProductDealer(Base):
    __tablename__ = "productdealer"
    __table_args__ = (UniqueConstraint("key", "dealer_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str]
    dealer_id: Mapped[int] = mapped_column(
        ForeignKey("dealer.id"), primary_key=True
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id"), primary_key=True
    )

    dealers: Mapped["Dealer"] = relationship(back_populates="productdealers")
    products: Mapped["Product"] = relationship(back_populates="proddealers")
