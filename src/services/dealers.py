from src.schemas.dealers import Dealer
from src.utils.unitofwork import IUnitOfWork


class DealerService:
    async def add_dealer(
            self,
            uow: IUnitOfWork,
            product: Dealer
    ):
        dealer_dict = product.model_dump()
        async with uow:
            dealer = await uow.dealers.add_one(dealer_dict)
            await uow.commit()
            return dealer.id