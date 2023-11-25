from src.schemas.dealerprices import DealerPrice
from src.utils.unitofwork import IUnitOfWork


class DealerPriceService:
    async def add_dealerprice(
            self,
            uow: IUnitOfWork,
            dealerprice: DealerPrice
    ):
        dealerprice_dict = dealerprice.model_dump()
        async with uow:
            dealerprice = await uow.dealerprices.add_one(dealerprice_dict)
            await uow.commit()
            return dealerprice.id
