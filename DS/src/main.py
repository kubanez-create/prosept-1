import pickle
from typing import Annotated

import pandas as pd
import torch
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import util

from dsmodels.preprocess import clean_text_dealer

origins = [
    "http://localhost",
    "http://localhost:8000",
]

class Product(BaseModel):
    id: int


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_dealer_prices():
    marketing_dealerprice = pd.read_csv(
        "DS/data/marketing_dealerprice.csv", sep=";", index_col="id"
    )
    return marketing_dealerprice


def get_model_file():
    model_file = open("dsmodels/labse_model.pkl", "rb")
    model = pickle.load(model_file)
    yield model
    model_file.close()


def get_corpus_file():
    corpus_file = open("dsmodels/corpus_embeddings.pkl", "rb")
    corpus_embeddings = pickle.load(corpus_file)
    yield corpus_embeddings
    corpus_file.close()


@app.get("/predictions", response_model=list[Product])
def get_recommendations(
    marketing_dealerprice: Annotated[dict, Depends(get_dealer_prices)],
    model: Annotated[dict, Depends(get_model_file)],
    corpus_embeddings: Annotated[dict, Depends(get_corpus_file)],
    dealer_product_key: int,
    k: int = 3,
):
    """
    Function that gives k-recommended names from Procept product base
    :param marketing_dealerprice: dataframe from dealerprice
    :param dealer_product_key: dealer product id to which match recommendations
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
        best_idx.append(Product.model_validate({"id": idx}))

    return best_idx
