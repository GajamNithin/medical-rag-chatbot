import requests
from embeddings import create_embedding
from vector_store import index
import numpy as np

import json

with open("data/medical_drugs.json") as f:
    DRUG_DATA = json.load(f)

DRUG_NAMES = set(drug["drugName"].strip().lower() for drug in DRUG_DATA)

MEDICAL_KEYWORDS = [
    "drug", "medicine", "tablet", "capsule",
    "treatment", "side effect", "dosage",
    "disease", "pain", "fever",
    "diabetes", "blood pressure",
    "antibiotic", "infection",
    "used for", "symptoms", "cure"
]


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def is_medical_query(query):

    q = query.lower()

    # keyword-based detection
    if any(word in q for word in MEDICAL_KEYWORDS):
        return True

    return False

def keyword_search(query, drugs):
    q = query.lower()
    matched = []

    for drug in drugs:
        name = drug.get("drugName", "").lower()

        if name and name in q:
            # create simple text chunk
            text = f"Drug: {drug['drugName']}. Description: {drug.get('description', '')}. Side Effects: {drug.get('sideEffects', '')}"
            matched.append(text)

    return matched

def generate_answer(query):

    if not is_medical_query(query):
        return "I can only answer medical drug related questions."

    # create embedding
    query_embedding = create_embedding(query)

    # search pinecone
    results = index.query(
    vector=query_embedding,
    top_k=5,   # fetch more results
    include_metadata=True
    )
    vector_chunks = [match["metadata"]["text"] for match in results["matches"]]

    # 🔹 Keyword search
    keyword_chunks = keyword_search(query, DRUG_DATA)

    # 🔹 Combine both
    all_chunks = vector_chunks + keyword_chunks

    scored_chunks = []
    
    for chunk_text in all_chunks:
    
        chunk_embedding = create_embedding(chunk_text)
    
        score = cosine_similarity(query_embedding, chunk_embedding)
    
        scored_chunks.append((score, chunk_text))
    
    # sort and pick best
    scored_chunks.sort(reverse=True)
    
    top_chunks = [chunk for _, chunk in scored_chunks[:3]]
    
    context = "\n".join(top_chunks)
    
    prompt = f"""
You are a medical assistant chatbot.

Instructions:
- If the context contains relevant information, use it to answer.
- If the context is empty or not relevant, answer using your general medical knowledge.
- Do NOT say "information not in context".
- Always give a clear and helpful answer.

Context:
{context}

Question:
{query}

Answer:
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