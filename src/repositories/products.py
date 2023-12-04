from sqlalchemy import insert, select

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
        idxs: list[ProductDS]
    ) -> list[RecommendedProduct]:
        db_inds = [ind.id for ind in idxs]
        stmt = select(self.model).where(self.model.id.in_(db_inds))
        res = await self.session.execute(stmt)
        products = [
            RecommendedProduct.model_validate(
                prod[0], from_attributes=True
            ) for prod in res.all()
        ]
        # return first 5 predicted items only
        return products[:4]
