import asyncio
import csv
import sys

import aiohttp

sys.path.append("")

from src.db.db import async_session_maker


class Loader:
    def __init__(self, model, file) -> None:
        self.model = model
        self.file = file
        self.session = async_session_maker()

    async def load_model(self):
        with open(self.file) as f:
            reader = csv.reader(f, delimiter=";")
            field_names, *objects = reader

            for row in objects:
                data_to_insert = dict(zip(field_names, row))

                if self.model == "products":
                    product_obj = {
                        "id": data_to_insert.get("id"),
                        "article": data_to_insert.get("article"),
                        "ean_13": data_to_insert.get("ean_13") if data_to_insert.get("ean_13") else 0,
                        "name": data_to_insert.get("name"),
                        "cost": data_to_insert.get("cost") if data_to_insert.get("cost") else 0,
                        "recommended_price": data_to_insert.get("recommended_price"),
                        "category_id": data_to_insert.get("category_id") if data_to_insert.get("category_id") else 0,
                        "ozon_name": data_to_insert.get("ozon_name"),
                        "name_1c": data_to_insert.get("name_1c"),
                        "wb_name": data_to_insert.get("wb_name"),
                        "ozon_article": data_to_insert.get("ozon_article") if data_to_insert.get("ozon_article") else 0,
                        "wb_article": data_to_insert.get("wb_article") if data_to_insert.get("wb_article") else 0,
                        "ym_article": data_to_insert.get("ym_article"),
                        "wb_article_td": data_to_insert.get("wb_article_td"),
                    }
                    url = "http://127.0.0.1:8000/api/products/add"
                    headers = {"Content-type": "application/json"}
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            url,
                            json=product_obj,
                            headers=headers,
                        ):
                            pass

                if self.model == "dealers":
                    dealer_obj = {
                        "id": data_to_insert.get("id"),
                        "name": data_to_insert.get("name"),
                    }
                    url = "http://127.0.0.1:8000/api/dealers/add"
                    headers = {"Content-type": "application/json"}
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            url,
                            json=dealer_obj,
                            headers=headers,
                        ):
                            pass

                if self.model == "dealerprices":
                    dealerprice_obj = {
                        "id": data_to_insert.get("id"),
                        "product_key": data_to_insert.get("product_key"),
                        "price": data_to_insert.get("price"),
                        "product_url": data_to_insert.get("product_url"),
                        "product_name": data_to_insert.get("product_name"),
                        "date": data_to_insert.get("date"),
                        "dealer_id": data_to_insert.get("dealer_id"),
                    }
                    url = "http://127.0.0.1:8000/api/dealerprices/add"
                    headers = {"Content-type": "application/json"}
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            url,
                            json=dealerprice_obj,
                            headers=headers,
                        ):
                            pass

                if self.model == "productdealers":
                    productdealer_obj = {
                        "id": data_to_insert.get("id"),
                        "key": data_to_insert.get("key"),
                        "dealer_id": data_to_insert.get("dealer_id"),
                        "product_id": data_to_insert.get("product_id"),
                    }
                    url = "http://127.0.0.1:8000/api/productdealers/add"
                    headers = {"Content-type": "application/json"}
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            url,
                            json=productdealer_obj,
                            headers=headers,
                        ):
                            pass


if __name__ == "__main__":
    model, file = sys.argv[1:]
    # Ensure correct usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python loader.py modelname file_address")
    loader = Loader(model=model, file=file)
    asyncio.run(loader.load_model())
