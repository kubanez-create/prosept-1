from src.db.db import Base


# import here all other models for alembic revision
from .dealers import Dealer
from .dealerprices import DealerPrice
from .products import Product
from .productdealers import ProductDealer
from .users import User
