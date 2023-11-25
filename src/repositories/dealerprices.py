from src.models.dealerprices import DealerPrice
from src.utils.repository import SQLAlchemyRepository


class DealerPriceRepository(SQLAlchemyRepository):
    model = DealerPrice