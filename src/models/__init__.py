from src.db.db import Base

from .dealerprices import DealerPrice

# import here all other models for alembic revision
from .dealers import Dealer
from .productdealers import ProductDealer
from .products import Product
from .users import User
