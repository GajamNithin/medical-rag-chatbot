import requests
from embeddings import create_embedding
from vector_store import index

def generate_answer(query):

    # if not is_medical_query(query):
    #     return "I can only answer medical drug related questions."

    # create embedding
    query_embedding = create_embedding(query)

    # search pinecone
    results = index.query(
        vector=query_embedding,
        top_k=2,
        include_metadata=True
    )

    context = ""

    for match in results["matches"]:
        context += match["metadata"]["text"] + "\n"

    prompt = f"""
You are a medical assistant.

Answer the question using the provided context.

Context:
{context}

Question:
{query}
"""

    response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "phi3",
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 120
        }
    }
)

    return response.json()["response"]