from fastapi import APIRouter

from src.api.dependencies import UOWDep
from src.schemas.productdealers import ProductDealer, ProductDealerCreate
from src.services.productdealers import ProductDealerService

router = APIRouter(
    prefix="/productdealers",
)


@router.post("/add", tags=["AdminZone"])
async def add_productdealer(
    productdealer: ProductDealer,
    uow: UOWDep,
):
    productdealer = await ProductDealerService().add_productdealer(
        uow, productdealer
    )
    return


@router.post("/", tags=["Main"])
async def create_productdealer(
    productdealer: ProductDealerCreate,
    uow: UOWDep,
) -> ProductDealer:
    """Create new match object.

    Args:
        productdealer (ProductDealer): operators choice object
        uow (UOWDep): unit of work dependency
    """
    productdealer = await ProductDealerService().create_productdealer(
        uow, productdealer
    )
    return productdealer
