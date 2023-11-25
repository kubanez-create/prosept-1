from .endpoints.users import router as router_users
from .endpoints.products import router as router_products
from .endpoints.dealers import router as router_dealers

all_routers = [
    router_users,
    router_products,
    router_dealers,
]
