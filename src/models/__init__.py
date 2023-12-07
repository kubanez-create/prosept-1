# trunk-ignore(ruff/F401)
from src.db.db import Base

# trunk-ignore(ruff/F401)
from .dealerprices import DealerPrice

# import here all other models for alembic revision
# trunk-ignore(ruff/F401)
from .dealers import Dealer

# trunk-ignore(ruff/F401)
from .productdealers import ProductDealer

# trunk-ignore(ruff/F401)
from .products import Product

# trunk-ignore(ruff/F401)
from .users import User
