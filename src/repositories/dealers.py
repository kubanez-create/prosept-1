from src.models.dealers import Dealer
from src.utils.repository import SQLAlchemyRepository


class DealerRepository(SQLAlchemyRepository):
    model = Dealer
