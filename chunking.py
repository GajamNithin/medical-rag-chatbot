def create_chunks(drug):

    chunks = []

    name = drug.get("drugName","")

    if drug.get("description"):
        chunks.append({
            "text": f"Drug: {name}. Description: {drug['description']}",
            "section": "description"
        })

    if drug.get("sideEffects"):
        chunks.append({
            "text": f"Drug: {name}. Side Effects: {drug['sideEffects']}",
            "section": "side_effects"
        })

    if drug.get("category"):
        chunks.append({
            "text": f"Drug: {name}. Category: {drug['category']}",
            "section": "category"
        })

    if drug.get("consumeType"):
        chunks.append({
            "text": f"Drug: {name}. Consume Type: {drug['consumeType']}",
            "section": "usage"
        })

    return chunks