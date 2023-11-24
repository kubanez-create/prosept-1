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
            reader = csv.reader(f)
            field_names, *objects = reader

            for row in objects:
                data_to_insert = dict(zip(field_names, row))

                if self.model == "clients":
                    client_obj = {"name": data_to_insert.get("name")}
                    url = "http://localhost:8000/api/clients/add"
                    headers = {"Content-type": "application/json"}
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            url,
                            json=client_obj,
                            headers=headers,
                        ) as response:
                            pass

                if self.model == "products":
                    product_obj = {
                        "db_id": data_to_insert.get("db_id"),
                        "name": data_to_insert.get("name"),
                    }
                    url = "http://localhost:8000/api/products/add"
                    headers = {"Content-type": "application/json"}
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            url,
                            json=product_obj,
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
