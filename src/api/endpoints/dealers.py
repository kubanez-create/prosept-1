from fastapi import APIRouter

from src.api.dependencies import UOWDep
from src.schemas.dealers import Dealer
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
