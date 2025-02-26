from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="pcsk_36hKfz_6GL8ztjrsZZicZyCdeUZkEV1D3fBAcooULof9ZZ8zSq9wjjTA6BNKoE1en36KRU")
index_name = "maxent"

pc.create_index(
    name=index_name,
    dimension=1536, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)
