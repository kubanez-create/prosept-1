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
    dealer: int | None = None,
    status: bool | None = False
):
    """Get all (possibly) filtered dealer's items.

    To get all objects use status=True, to get only unmatched objects -
    set status=False
    Args:
        uow (UOWDep): unit of work dependancy
        date_before (date): filter all goods before that date
        date_after (date): filter all goods after that date
        dealer (int): dealer's id
        status (bool): whether or not to include unmatched goods
    """
    dlp_objects = await DealerPriceService().get_dealerprices(
        date_before=date_before,
        date_after=date_after,
        dealer=dealer,
        status=status,
        uow=uow
    )
    return dlp_objects
