from sqlalchemy import insert

from src.core.predictions import get_products_df, row_to_product
from src.models.products import Product
from src.schemas.products import ProductDS, RecommendedProduct
from src.utils.repository import SQLAlchemyRepository


class ProductRepository(SQLAlchemyRepository):
    model = Product

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_preds(
        self,
        idxs: list[ProductDS],
        k: int,
    ) -> list[RecommendedProduct]:
        db_inds = [ind.id for ind in idxs]
        product_df = get_products_df()
        products = product_df.loc[db_inds, :].apply(
            row_to_product, axis=1
        ).tolist()
        # return first k predicted items only
        return products[:k]
