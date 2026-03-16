import json

with open("data/medical_drugs.json") as f:
    drugs = json.load(f)

processed = []

for i, drug in enumerate(drugs):

    text = f"""
Drug Name: {drug.get("drugName","")}
Description: {drug.get("description","")}
Side Effects: {drug.get("sideEffects","")}
Category: {drug.get("category","")}
"""

    processed.append({
        "id": f"drug_{i}",
        "text": text.strip(),
        "metadata": {
            "drugName": drug.get("drugName"),
            "category": drug.get("category"),
            "manufacturer": drug.get("manufacturer"),
            "consumeType": drug.get("consumeType")
        }
    })

with open("data/rag_ready_dataset.json","w") as f:
    json.dump(processed,f,indent=2)

print("RAG dataset ready")