from sqlalchemy import insert
# from sqlalchemy.exc import NoResultFound
# from sqlalchemy.orm import selectinload

from src.models.products import Product
from src.utils.repository import SQLAlchemyRepository


class ProductRepository(SQLAlchemyRepository):
    model = Product

    async def add_one(self, data: dict) -> int:
        stmt = (
            insert(self.model)
            .values(**data)
            .returning(self.model)
            # .options(selectinload(self.model.items))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()