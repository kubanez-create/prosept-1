from src.schemas.productdealers import ProductDealer
from src.utils.unitofwork import IUnitOfWork


class ProductDealerService:
    async def add_productdealer(
            self,
            uow: IUnitOfWork,
            productdealer: ProductDealer
    ):
        productdealer_dict = productdealer.model_dump()
        async with uow:
            productdealer = await uow.productdealers.add_one(productdealer_dict)
            await uow.commit()
            return productdealer.id
