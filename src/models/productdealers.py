from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.db import Base

# to run migrations comment out next line and put DealerPriceDb.product_key
# as well as DealerPriceDb.date and DealerPriceDb.dealer_id
# in quotes but to run program you'll need to return everything as it is now
# from src.models.dealerprices import DealerPrice as DealerPriceDb


class ProductDealer(Base):
    __tablename__ = "productdealer"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str]
    dealer_id: Mapped[int] = mapped_column(ForeignKey("dealer.id"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), primary_key=True)
    keys: Mapped["DealerPrice"] = relationship(
        primaryjoin="ProductDealer.key==DealerPrice.product_key",
        foreign_keys=[
            "DealerPriceDb.product_key",
            "DealerPriceDb.date",
            "DealerPriceDb.dealer_id",
        ],
    )
    dealers: Mapped["Dealer"] = relationship(back_populates="productdealers")
    products: Mapped["Product"] = relationship(back_populates="proddealers")


#     def to_read_model(self) -> DealerPrice:
#         return DealerPrice(
#             id=self.id,
#             product_key=self.product_key,
#             price=self.price,
#             product_url=self.product_url,
#             product_name=self.product_name,
#             date=self.date,
#             dealer_id=self.dealer_id,
#         )
