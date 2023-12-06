import os
from langchain.embeddings import HuggingFaceEmbeddings

model_name = "intfloat/multilingual-e5-small"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True, "batch_size": 32}

embeddings_model = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
