from fastapi import APIRouter

from src.api.dependencies import UOWDep
from src.schemas.dealers import Dealer, DealerDb
from src.services.dealers import DealerService

router = APIRouter(
    prefix="/dealers",
)


@router.post("/add", tags=["AdminZone"])
async def add_dealer(
    dealer: Dealer,
    uow: UOWDep,
):
    dealer = await DealerService().add_dealer(uow, dealer)
    return


@router.get("/", response_model=list[DealerDb], tags=["Main"])
async def get_dealers(uow: UOWDep, dealer: str | None = None):
    """Get (possibly) filtered dealer's items.

    Args:
        uow (UOWDep): unit of work dependency
        dealer (str): dealer's name
    """
    dl_objects = await DealerService().get_dealers(dealer=dealer, uow=uow)
    return dl_objects
