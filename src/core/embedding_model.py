import torch
from langchain_community.embeddings import HuggingFaceEmbeddings


# RAG에서 사용할 모델

def get_embedder():
    return HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-base",
        encode_kwargs={"normalize_embeddings": True}
    )