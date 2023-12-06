from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)
import embeddings

class milvus():
    def __init__(self):
        connections.connect("default", host="localhost", port="19530")

        if utility.has_collection("documents", using='default'):
            self.collection = Collection("documents")

        else:
            fields = [
                FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=100),
                FieldSchema(name="user_id", dtype=DataType.INT64),
                FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=384)
            ]
            schema = CollectionSchema(fields, "Document based Retrieval Augmented Generation (RAG)")
            self.collection = Collection("documents", schema)

            index = {
                "index_type": "HNSW",
                "metric_type": "IP",
                "params": {"M": 32, "efConstruction": 128},
            }
            self.collection.create_index("vector", index)
        
        self.collection.load()

    def index(self, docs):
        texts = [f"passage: {doc.page_content}" for doc in docs]
        vectors = embeddings.embeddings_model.embed_documents(texts)
        sources = [doc.metadata["source"] for doc in docs]
        user_ids = [doc.metadata["user_id"] for doc in docs]
        entities = [sources, user_ids, texts, vectors]
        self.collection.insert(entities)
        self.collection.flush()

    def search(self, user_id, query, top_k):
        vectors_to_search = [embeddings.embeddings_model.embed_query(f"query: {query}")]
        search_params = {
            "metric_type": "IP",
            "params": {"ef": 64},
        }
        result = self.collection.search(
            vectors_to_search,
            "vector",
            search_params,
            expr=f"user_id=={user_id}",
            limit=top_k,
            output_fields=["text"]
        )
        hits = result[0]
        texts = [hit.entity.get('text') for hit in hits]
        context = "\n".join(texts)
        return context
    
    def clear_docs(self, user_id):
        ids = self.collection.query(f'user_id=={user_id}', output_fields=["pk"])
        pk = [id["pk"] for id in ids]
        expr = f'pk in {pk}'
        self.collection.delete(expr=expr)
        self.collection.flush()
