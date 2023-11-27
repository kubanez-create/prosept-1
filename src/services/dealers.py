from src.schemas.dealers import Dealer
from src.utils.unitofwork import IUnitOfWork


class DealerService:
    async def add_dealer(self, uow: IUnitOfWork, dealer: Dealer):
        dealer_dict = dealer.model_dump()
        async with uow:
            dealer = await uow.dealers.add_one(dealer_dict)
            await uow.commit()
            return dealer.id

    async def get_dealers(
            self,
            uow: IUnitOfWork,
            dealer: str | None = None
    ):
        async with uow:
            dealers = await uow.dealers.find_all(
                dealer=dealer,
            )
            return dealers
