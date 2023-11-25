from fastapi import APIRouter

from src.api.dependencies import UOWDep
from src.schemas.productdealers import ProductDealer
from src.services.productdealers import ProductDealerService

router = APIRouter(
    prefix="/productdealers",
)


@router.post("/add")
async def add_productdealer(
    productdealer: ProductDealer,
    uow: UOWDep,
):
    productdealer = await ProductDealerService().add_productdealer(
        uow, productdealer)
    return
