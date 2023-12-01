from datetime import date

from src.schemas.dealerprices import DealerPrice
from src.utils.unitofwork import IUnitOfWork


class DealerPriceService:
    async def add_dealerprice(self, uow: IUnitOfWork, dealerprice: DealerPrice):
        dealerprice_dict = dealerprice.model_dump()
        async with uow:
            dealerprice = await uow.dealerprices.add_one(dealerprice_dict)
            await uow.commit()
            return dealerprice.id

    async def get_dealerprices(
        self,
        uow: IUnitOfWork,
        date_before: date | None = None,
        date_after: date | None = None,
        dealer: int | None = None,
        status: bool | None = False,
    ):
        async with uow:
            products = await uow.dealerprices.find_all(
                date_before=date_before,
                date_after=date_after,
                dealer=dealer,
                status=status,
            )
            return products

    async def get_statistics(self, uow: IUnitOfWork):
        async with uow:
            dealers = await uow.dealerprices.get_statistics()
            return dealers
