from datetime import date

from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.db import Base


class ProductDealer(Base):
    __tablename__ = "productdealer"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str]
    date: Mapped[date]
    dealer_id: Mapped[int] = mapped_column(
        ForeignKey("dealer.id"), primary_key=True
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id"), primary_key=True
    )
    keys: Mapped["DealerPrice"] = relationship(
        primaryjoin="ProductDealer.key==DealerPrice.product_key",
        # primaryjoin="and_(DealerPrice.dealer_id == ProductDealer.dealer_id, "
        # "ProductDealer.key==DealerPrice.product_key)"
    )

    dealers: Mapped["Dealer"] = relationship(back_populates="productdealers")
    products: Mapped["Product"] = relationship(back_populates="proddealers")
    __table_args__ = (
        ForeignKeyConstraint(
            ['key', "date", 'dealer_id'],
            ['dealerprice.product_key', 'dealerprice.date', 'dealerprice.dealer_id']
        ),
    )
