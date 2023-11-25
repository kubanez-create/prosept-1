from fastapi import APIRouter

from src.api.dependencies import UOWDep
from src.schemas.dealerprices import DealerPrice
from src.services.dealerprices import DealerPriceService

router = APIRouter(
    prefix="/dealerprices",
)


@router.post("/add")
async def add_dealerprice(
    dealerprice: DealerPrice,
    uow: UOWDep,
):
    dealerprice = await DealerPriceService().add_dealerprice(uow, dealerprice)
    return
