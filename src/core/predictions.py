import csv
import pickle
import sys
from functools import lru_cache

import pandas as pd
import torch
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sentence_transformers import util
from sqlalchemy import create_engine

sys.path.append("")

from src.DS.dsmodels.preprocess import clean_text_dealer
from src.schemas.products import RecommendedProduct

NUMBER_OF_PREDICTED_ITEMS = 5

def get_model():
    file = open("src/DS/dsmodels/labse_model.pkl", "rb")
    model = pickle.load(file)
    yield model
    file.close()


def get_corpus():
    file = open("src/DS/dsmodels/corpus_embeddings.pkl", "rb")
    corpus_embeddings = pickle.load(file)
    yield corpus_embeddings
    file.close()


def get_recommendation(
    marketing_dealerprice: pd.DataFrame,
    model,
    corpus_embeddings,
    dealer_product_key: int,
    k: int = 3,
) -> list[int]:
    """
    Function that gives k-recommended names from Procept product base
    :param marketing_dealerprice: dataframe from dealerprice
    :param dealer_product_key: dealer product name to which match recommendations
    :param k: number of recommended items
    :return products_id: list of recommended products_id
    """
    query = marketing_dealerprice.loc[dealer_product_key][["product_name"]]
    query = clean_text_dealer(query)
    query_embedding = model.encode(query, convert_to_tensor=True)

    cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=k)

    best_idx = []

    for score, idx in zip(top_results[0], top_results[1]):
        score = score.cpu().data.numpy()
        idx = idx.item()
        best_idx.append(idx)

    return best_idx


def prepare_predictions_csv(
    marketing_dealerprice: pd.DataFrame,
    model,
    corpus_embeddings,
    k=3,
) -> None:
    # filter marketing_dealerprice table to get only unique
    # product_key-dealer_id rows
    marketing_dealerprice.drop_duplicates(
        subset=["product_key", "dealer_id"], inplace=True
    )
    with open("src/DS/predictions.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["prod"] + [str(i) for i in range(k)])
        for product in marketing_dealerprice.index:
            preds = get_recommendation(
                marketing_dealerprice,
                model=model,
                corpus_embeddings=corpus_embeddings,
                dealer_product_key=product,
                k=k,
            )
            writer.writerow([product] + preds)


@lru_cache()
def get_predictions_df() -> pd.DataFrame:
    return pd.read_csv("src/DS/predictions.csv", index_col="prod")


@lru_cache()
def get_products_df() -> pd.DataFrame:
    products = pd.read_csv("src/data/marketing_product.csv", sep=";", index_col=0)
    products.dropna(subset=["name"], inplace=True)
    products = products[products.name != "   "]
    products.fillna("unknown", inplace=True)
    return products


def row_to_product(row):
    return RecommendedProduct.model_validate(
        {
            "id": row["id"],
            "name_1c": row["name_1c"],
        }
    )


def main():
    marketing_dealerprice = pd.read_csv(
        "src/data/marketing_dealerprice.csv", sep=";", index_col="id"
    )
    model = get_model()
    corpus = get_corpus()
    prepare_predictions_csv(
        marketing_dealerprice,
        model=next(model),
        corpus_embeddings=next(corpus),
        k=NUMBER_OF_PREDICTED_ITEMS
    )


async def scheduler():
    scheduler = AsyncIOScheduler()
    engine = create_engine("sqlite:///scheduler.db")
    scheduler.add_jobstore(
        "sqlalchemy",
        engine=engine,
    )
    # it will fire every day at 6 AM
    scheduler.add_job(main, "cron", hour=6)

    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()

if __name__ == "__main__":
    main()