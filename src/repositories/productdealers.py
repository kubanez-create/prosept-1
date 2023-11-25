from src.models.productdealers import ProductDealer
from src.utils.repository import SQLAlchemyRepository


class ProductDealerRepository(SQLAlchemyRepository):
    model = ProductDealer
