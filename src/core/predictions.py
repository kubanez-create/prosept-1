import csv
import pickle
from functools import lru_cache

import pandas as pd
import torch
from sentence_transformers import util

from src.core.DS.dsmodels.preprocess import clean_text_dealer


def get_model():
    file = open("src/core/DS/dsmodels/labse_model.pkl", "rb")
    model = pickle.load(file)
    yield model
    file.close()


def get_corpus():
    file = open("src/core/DS/dsmodels/corpus_embeddings.pkl", "rb")
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
    marketing_dealerprice: pd.DataFrame, model, corpus_embeddings
) -> None:
    marketing_dealerprice.drop_duplicates(
        subset=["product_key", "dealer_id"], inplace=True
    )
    with open("src/core/DS/predictions.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["prod"] + [str(i) for i in range(20)])
        for product in marketing_dealerprice.index:
            preds = get_recommendation(
                marketing_dealerprice,
                model=model,
                corpus_embeddings=corpus_embeddings,
                dealer_product_key=product,
                k=20,
            )
            writer.writerow([product] + preds)


@lru_cache()
def get_predictions(id: int) -> list[int]:
    preds = pd.read_csv("src/core/DS/predictions.csv", index_col="prod")
    return preds.loc[id, :].to_list()


if __name__ == "__main__":
    marketing_dealerprice = pd.read_csv(
        "src/data/marketing_dealerprice.csv", sep=";", index_col="id"
    )
    model = get_model()
    corpus = get_corpus()
    prepare_predictions_csv(
        marketing_dealerprice, model=next(model), corpus_embeddings=next(corpus)
    )
