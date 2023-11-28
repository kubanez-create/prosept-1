from sqlalchemy import insert, select
from src.models.productdealers import ProductDealer
from src.utils.repository import SQLAlchemyRepository


class ProductDealerRepository(SQLAlchemyRepository):
    model = ProductDealer

    async def create_one(self, data: dict) -> int:
        id = await self.session.execute(
            select(self.model.id).order_by(self.model.id))
        stmt = insert(self.model).values(**data, id=(id.all()[-1][0] + 1)).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()
