# app/rag.py
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


# Load dataset
df = pd.read_csv("app/data/medical_symptoms.csv")

# Convert rows into text docs
docs = []
for _, row in df.iterrows():
    disease = row["diseases"]
    symptoms = [col for col in df.columns if col != "diseases" and row[col] == 1]
    
    if symptoms:
        text = f"{disease} is associated with symptoms such as {', '.join(symptoms)}."
    else:
        text = f"{disease} has no listed symptoms in this dataset."
    
    docs.append(text)

# Build embeddings + FAISS index
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(docs, convert_to_numpy=True)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

def retrieve_context(query: str, top_k: int = 3):
    """Retrieve top relevant medical info for a query"""
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)
    results = [docs[i] for i in indices[0]]
    return results
