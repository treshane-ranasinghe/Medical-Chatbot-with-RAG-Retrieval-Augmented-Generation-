# app/main.py
from fastapi import FastAPI, HTTPException
from app.schemas import UserMessage
from app.config import DEEPSEEK_API_URL, API_KEY
from app.rag import retrieve_context
import requests
import faiss



app = FastAPI(title="Medical Chatbot API with RAG")

@app.get("/")
def root():
    return {"message": "Medical Chatbot API is running with RAG. Use /chat endpoint."}

@app.post("/chat")
def chat(user_message: UserMessage):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not found. Set it in .env file.")

    # 🔹 Retrieve relevant medical context
    context = retrieve_context(user_message.message)
    context_text = "\n".join(context)

    # 🔹 Inject context into prompt
    augmented_prompt = f"""
    You are a medical assistant. Use the following medical knowledge if helpful:
    {context_text}

    Patient query: {user_message.message}
    """

    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [{"role": "user", "content": augmented_prompt}],
        "stream": False
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        reply = data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        return {"reply": reply, "context_used": context}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
