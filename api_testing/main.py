import client

user_id = 923310495560

hotnets_paper_path = "./testing_documents/hotnets21.pdf"
pgvector_readme_path = "./testing_documents/pgvector_README.md"

def test_RAG():
    client.upload(user_id, [hotnets_paper_path, pgvector_readme_path])
    client.search(user_id, "What is pgvector?", 2)
    client.search(user_id, "Who are the authors of the paper rethinking web affordability?", 2)
    client.clear_docs(user_id)

test_RAG()