from src.schemas.products import Product
from src.utils.unitofwork import IUnitOfWork


class ProductService:
    async def add_product(
            self,
            uow: IUnitOfWork,
            product: Product
    ) -> Product:
        product_dict = product.model_dump()
        async with uow:
            product = await uow.products.add_one(product_dict)
            await uow.commit()
            return product

    async def get_products(self, uow: IUnitOfWork) -> list[Product]:
        async with uow:
            products = await uow.products.find_all()
            return products

    async def get_predicted_products(
        self,
        uow: IUnitOfWork,
        idxs: list[dict[str, int]],
        k: int,
    ):
        async with uow:
            products = await uow.products.get_preds(idxs, k)
            return products
