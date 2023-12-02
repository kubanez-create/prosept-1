import aiohttp
from fastapi import APIRouter

from pydantic import BaseModel

from src.api.dependencies import UOWDep
from src.schemas.products import ProductDS, RecommendedProduct
from src.services.products import ProductService

router = APIRouter()


@router.get("/predictions", response_model=list[RecommendedProduct])
async def predict(product_id: int, k: int, uow: UOWDep):
    # url = (
    #     "http://172.17.0.1:8080/predictions/"
    #     f"?dealer_product_key={product_id}&k={k}"
    # )
    url = (
        "http://localhost:8080/predictions/?dealer_product_key="
        f"{product_id}&k={k}"
    )
    async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    response_json = await response.json()
                    predictions = await ProductService().get_predicted_products(
                            uow,
                            [ProductDS.model_validate(it) for it in response_json],
                    )
                    return predictions
                else:
                    return f"Ошибка: {response.status}, {response.text}"
