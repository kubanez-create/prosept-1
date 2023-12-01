from sqlalchemy import insert

from src.models.products import Product
from src.utils.repository import SQLAlchemyRepository

# from sqlalchemy.exc import NoResultFound
# from sqlalchemy.orm import selectinload


class ProductRepository(SQLAlchemyRepository):
    model = Product

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()
