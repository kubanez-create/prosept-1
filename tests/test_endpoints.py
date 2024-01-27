import logging
from httpx import AsyncClient


async def test_add_product(ac: AsyncClient):
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

async def test_get_product(ac: AsyncClient):
    response = await ac.get("/api/products")

    assert response.status_code == 200
    assert len(response.json()) == 1

async def test_add_dealer(ac: AsyncClient):
    response = await ac.post("/api/dealers/add", json={"name": "Something"})

    assert response.status_code == 200


async def test_get_dealer(ac: AsyncClient):
    response = await ac.get("/api/dealers")

    assert response.status_code == 200
    assert len(response.json()) == 1

async def test_add_dealerprice(ac: AsyncClient, add_dealer):
    response = await ac.post("/api/dealerprices/add", json={
        "product_key": "546227",
        "price": 233.00,
        "product_url": "https://akson.ru//p/sredstvo_universalnoe_prosept_universal_spray_500ml/",
        "product_name": "Средство универсальное Prosept Universal Spray, 500мл",
        "date": "2023-07-11",
        "dealer_id": add_dealer
    })

    assert response.status_code == 200


async def test_get_dealerprice(ac: AsyncClient):
    response = await ac.get("/api/dealerprices")

    assert response.status_code == 200
    assert len(response.json()) == 1

async def test_get_statistics(ac: AsyncClient):
    response = await ac.get("/api/dealerprices/statistics")

    assert response.status_code == 200
    assert len(response.json()) == 1

async def test_get_predictions(ac: AsyncClient):
    response = await ac.get("/api/predictions?product_id=2&k=5")

    assert response.status_code == 200
    assert len(response.json()) == 5

async def test_add_productdealer(ac: AsyncClient, add_dealer, add_product):
    response = await ac.post("/api/productdealers/", json={
        "key": "546227",
        "dealer_id": add_dealer,
        "product_id": add_product
    })

    assert response.status_code == 200
