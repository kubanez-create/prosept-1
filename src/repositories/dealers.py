from sqlalchemy import select
from src.models.dealers import Dealer
from src.schemas.dealers import DealerDb
from src.utils.repository import SQLAlchemyRepository


class DealerRepository(SQLAlchemyRepository):
    model = Dealer

    async def find_all(
            self,
            *,
            dealer: str | None = None
    ) -> list[DealerDb]:
        # if there's no filters - apply none
        stmt = select(self.model)

        if dealer is not None:
            stmt = stmt.where(self.model.name == dealer)

        res = await self.session.execute(stmt)
        res = [
            DealerDb(
                **{"id": row[0].id, "name": row[0].name}
            ) for row in res.all()
        ]

        return res