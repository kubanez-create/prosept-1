from .endpoints.dealers import router as router_dealers
from .endpoints.dealerprices import router as router_dealerprices
from .endpoints.products import router as router_products
from .endpoints.users import router as router_users

all_routers = [
    router_users,
    router_products,
    router_dealers,
    router_dealerprices,
]
