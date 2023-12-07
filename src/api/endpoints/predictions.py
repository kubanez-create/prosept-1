from fastapi import APIRouter

from src.api.dependencies import UOWDep
from src.core.predictions import get_predictions_df
from src.schemas.products import ProductDS, RecommendedProduct
from src.services.products import ProductService

router = APIRouter()


@router.get(
    "/predictions",
    response_model=list[RecommendedProduct],
    tags=["Main"]
)
async def predict(uow: UOWDep, product_id: int, k: int = 5):
    """Get k predicted products for a given dealer product's id.

    Args:
       - **uow** (UOWDep): unit of work dependency
       - **product_id** (int): id from dealerprice table
       - **k** (int, optional): how many predicted items to return. Defaults to 5.

    Returns:
        list[RecommendedProduct]: predicted items
    """
    pred_df: list[int] = get_predictions_df().loc[product_id, :].to_list()
    predictions = await ProductService().get_predicted_products(
        uow,
        [ProductDS.model_validate({"id": it}) for it in pred_df],
        k
    )
    return predictions
