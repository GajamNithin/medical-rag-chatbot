import json
from chunking import create_chunks
from embeddings import create_embedding
from vector_store import index

with open("data/rag_ready_dataset.json") as f:
    drugs = json.load(f)

vectors = []
id_counter = 0

for drug in drugs:

    chunks = create_chunks(drug)

    for chunk in chunks:

        embedding = create_embedding(chunk["text"])

        vectors.append(
            {
                "id": f"id-{id_counter}",
                "values": embedding,
                "metadata": {
                    "text": chunk["text"],
                    "section": chunk["section"]
                }
            }
        )

        id_counter += 1

# batch upsert
batch_size = 100

for i in range(0, len(vectors), batch_size):
    batch = vectors[i:i+batch_size]
    index.upsert(vectors=batch)

print("Data stored in Pinecone")