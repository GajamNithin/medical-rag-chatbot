# from openai import OpenAI
# from config import OPENAI_API_KEY

# client = OpenAI(api_key=OPENAI_API_KEY)

# def create_embedding(text):

#     response = client.embeddings.create(
#         model="text-embedding-3-small",
#         input=text
#     )

#     return response.data[0].embedding

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embedding(text):

    embedding = model.encode(text)

    return embedding.tolist()