from fastapi import FastAPI
from rag_pipeline import generate_answer

app = FastAPI()


@app.post("/ask")
def ask_question(query: str):

    answer = generate_answer(query)

    return {
        "query": query,
        "answer": answer
    }