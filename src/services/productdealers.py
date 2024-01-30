from src.schemas.productdealers import ProductDealer, ProductDealerCreate
from src.utils.unitofwork import IUnitOfWork


class ProductDealerService:
    async def add_productdealer(
            self,
            uow: IUnitOfWork,
            productdealer: ProductDealer
    ) -> int:
        productdealer_dict = productdealer.model_dump()
        async with uow:
            productdealer = await uow.productdealers.add_one(productdealer_dict)
            await uow.commit()
            return productdealer.id

    async def create_productdealer(
            self,
            uow: IUnitOfWork,
            productdealer: ProductDealerCreate
    ) -> ProductDealer:
        productdealer_dict = productdealer.model_dump()
        async with uow:
            productdealer = await uow.productdealers.create_one(productdealer_dict)
            await uow.commit()
            return productdealer
