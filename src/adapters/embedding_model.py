from langchain_huggingface import HuggingFaceEmbeddings

# RAG에서 사용할 모델

def get_embedder():
    return HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-base",
        encode_kwargs={"normalize_embeddings": True}
    )


# from langchain_huggingface import HuggingFaceEmbeddings

# def get_embedder():
#     return HuggingFaceEmbeddings(
#         model_name="Qwen/Qwen3-Embedding-0.6B",
#         model_kwargs={"device": "cpu"},  # 추후 논의 필요
#         encode_kwargs={
#             "normalize_embeddings": True,
#             "instruction": "Represent this algorithm explanation for retrieval:"
#         }
#     )