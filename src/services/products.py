from src.schemas.products import Product, ProductDb
from src.utils.unitofwork import IUnitOfWork


class ProductService:
    async def add_product(self, uow: IUnitOfWork, product: Product) -> ProductDb:
        product_dict = product.model_dump()
        async with uow:
            product = await uow.products.add_one(product_dict)
            await uow.commit()
            return product.id
