from pinecone import Pinecone, ServerlessSpec
from config import PINECONE_API_KEY

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medical-chatbot"

# create index if it doesn't exist
if index_name not in [i["name"] for i in pc.list_indexes()]:

    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pc.Index(index_name)