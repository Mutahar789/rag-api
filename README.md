# rag-api

## Introduction
This repository hosts a FastAPI-based API for Retrieval-Augmented Generation (RAG), a cutting-edge technique in Natural Language Processing that enhances response quality by retrieving relevant information during the generation process. Our implementation focuses on speed, scalability, and ease of integration utilizes [Milvus](https://milvus.io/) for efficient vector storage.

## Features
- Fast response times suitable for real-time applications.
- Scalable architecture, handling concurrent requests efficiently.
- Customizable retrieval component for domain-specific applications.

## Default Configuration
- Embedding Model: intfloat/multilingual-e5-small (Embedding dimensions: 384)
- Indexing algorithm: HNSW (maxConnections: 32, efConstruction: 128, ef: 64)
- Similarity metric: Cosine distance

Note: The API design is highly flexible, allowing for straightforward substitutions of the embedding model and indexing algorithm. Users can easily replace 'intfloat/multilingual-e5-small' with their preferred model and switch out the HNSW indexing algorithm in Milvus, adapting the system to diverse requirements and use cases.

## Install
```
bash setup.sh
```

## Run
```
bash setup.sh
```
