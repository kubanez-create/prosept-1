from fastapi import APIRouter

from src.api.dependencies import UOWDep
from src.schemas.products import Product
from src.services.products import ProductService

router = APIRouter(
    prefix="/products",
)


@router.post("/add")
async def add_product(
    product: Product,
    uow: UOWDep,
):
    product = await ProductService().add_product(uow, product)
    return