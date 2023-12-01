import requests
from typing import List
from fastapi import APIRouter

from pydantic import BaseModel

router = APIRouter()



base_url = "http://localhost:8080/predict"
data = {"data": {"key": "value"}}

class Product(BaseModel):
    id: int
    article: str
    name: str
    cost: float

class RecommendationResponse(BaseModel):
    data: List[Product]

@router.get("/predictions")
def predict():
    pass
    # response = requests.post(base_url, json=data)
    # if response.status_code == 200:
    #     response_json = response.json()
    #     return response_json
    # else:
    #     return f"Ошибка: {response.status_code}, {response.text}"