from datetime import date
from fastapi import APIRouter

from src.api.dependencies import UOWDep
from src.schemas.dealerprices import DealerPrice, DealerPriceDb
from src.services.dealerprices import DealerPriceService

router = APIRouter(
    prefix="/dealerprices",
)


@router.post("/add", tags=["AdminZone"])
async def add_dealerprice(
    dealerprice: DealerPrice,
    uow: UOWDep,
):
    dealerprice = await DealerPriceService().add_dealerprice(uow, dealerprice)
    return

@router.get("/", response_model=list[DealerPriceDb])
async def get_dealerprices(
    uow: UOWDep,
    date_before: date | None = None,
    date_after: date | None = None,
    dealer: int | None = None
):
    """Get all (possibly) filtered dealer's items.

    Args:
        uow (UOWDep): unit of work dependancy
        status (bool): status query parameter
        date_before (date): filter all goods before that date
        date_after (date): filter all goods after that date
        dealer (int): dealer's id
    """
    dlp_objects = await DealerPriceService().get_dealerprices(
        date_before=date_before,
        date_after=date_after,
        dealer=dealer,
        uow=uow
    )
    return dlp_objects
