from datetime import date

from sqlalchemy import select, and_, func

from src.models.dealers import Dealer
from src.models.dealerprices import DealerPrice
from src.models.products import Product
from src.models.productdealers import ProductDealer
from src.schemas.dealerprices import DealerPriceDb
from src.schemas.products import ProductDb
from src.utils.repository import SQLAlchemyRepository


class DealerPriceRepository(SQLAlchemyRepository):
    model = DealerPrice

    async def find_all(
            self,
            *,
            date_before: date | None = None,
            date_after: date | None = None,
            dealer: int | None = None,
            status: bool | None = False,
    ) -> list[DealerPriceDb]:
        # if there's no filters - apply none
        stmt = select(
            self.model.product_key,
            self.model.price,
            self.model.product_name,
            self.model.dealer_id,
            Product.article,
            Product.name,
            Product.cost,
            Product.recommended_price
        ).join(
            ProductDealer,
            onclause=ProductDealer.key==DealerPrice.product_key,
            isouter=True
        ).join(Product, isouter=True)
        # we will allow filter by both before and after dates for now
        if date_after is not None and date_before is not None:
            stmt = stmt.where(
                and_(
                    self.model.date >= date_after,
                    self.model.date <= date_before
                )
            )
        if dealer is not None:
            stmt = stmt.where(self.model.dealer_id == dealer)

        res = await self.session.execute(stmt)
        res_list = []
        results = res.all()
        for row in results:
            outer_dict = {
                "product_key": row[0],
                "price": row[1],
                "product_name": row[2],
                "dealer_id": row[3]
            }
            inner_dict = {
                "article": row[4],
                "name": row[5],
                "cost": row[6],
                "recommended_price": row[7]
            }
            outer_obj = DealerPriceDb.model_validate(outer_dict)
            if not status and inner_dict.get("name") is None:
                res_list.append(outer_obj)
                continue
            if status and inner_dict.get("name") is not None:
                inner_obj = ProductDb.model_validate(inner_dict)
                outer_obj.product = inner_obj
                outer_obj.status = True
            if status:
                res_list.append(outer_obj)
        return res_list

    async def get_statistics(self):
        subquery = select(
            self.model.dealer_id,
            self.model.product_key,
        ).select_from(
            self.model,
        ).distinct().alias(name="subq")

        joined = select(
            ProductDealer.product_id,
            subquery.c.dealer_id,
            subquery.c.product_key
        ).join(
            ProductDealer,
            onclause=(subquery.c.product_key==ProductDealer.key) &
                     (subquery.c.dealer_id==ProductDealer.dealer_id),
            isouter=True
        ).alias(name="joined")
        stmt = select(
            joined.c.dealer_id,
            func.count(joined.c.product_id).label("matched"),
            func.count(joined.c.product_id.is_(None)).label("unmatched"),
        ).select_from(
            joined
        ).group_by(joined.c.dealer_id)

        res = await self.session.execute(stmt)
        res = [(row[0].dealer_id, row.article) for row in res.all()]
        return res
