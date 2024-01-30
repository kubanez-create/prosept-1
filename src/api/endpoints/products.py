from fastapi import APIRouter

from src.api.dependencies import UOWDep
from src.schemas.products import Product, ProductShort
from src.services.products import ProductService

router = APIRouter(
    prefix="/products",
)


@router.post("/add", tags=["AdminZone"])
async def add_product(
    product: Product,
    uow: UOWDep,
) -> Product:
    product = await ProductService().add_product(uow, product)
    return product


@router.get("/", tags=["Main"])
async def get_products(
    uow: UOWDep,
) -> list[ProductShort]:
    """Get all manufacture's products.

    Args:
        uow (UOWDep): unit of work dependency
    """
    products = await ProductService().get_products(uow)
    return products
