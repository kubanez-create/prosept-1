import logging

from httpx import AsyncClient


async def test_add_specific_operations(ac: AsyncClient):
    response = await ac.post("/api/products/add", json={
        "id": 2,
        "article": "257-34",
        "ean_13": 17462873,
        "name": "Something something",
        "cost": 230,
        "recommended_price": "540",
        "category_id": 20,
        "ozon_name": "string",
        "name_1c": "string",
        "wb_name": "string",
        "ozon_article": 76,
        "wb_article": 43,
        "ym_article": "string",
        "wb_article_td": "string"
    })

    assert response.status_code == 200
    assert response.json()["id"] == 2

async def test_get_specific_operations(ac: AsyncClient):
    response = await ac.get("/api/products")

    assert response.status_code == 200
    assert len(response.json()) == 1
