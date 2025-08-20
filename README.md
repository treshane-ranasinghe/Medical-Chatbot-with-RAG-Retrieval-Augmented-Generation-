Medical Chatbot with RAG (Retrieval-Augmented Generation)

Overview
This FastAPI project implements a medical question-answering chatbot using RAG (Retrieval-Augmented Generation).
It retrieves relevant medical knowledge from a CSV dataset of diseases and symptoms and injects it into the LLM prompt, improving accuracy and specificity.

Features
Receives patient queries via /chat POST endpoint.
Retrieves relevant disease/symptom context from a CSV-based knowledge base.
Augments the user prompt with retrieved context.
Sends the prompt to a language model API (DeepSeek) for response generation.
Returns both the chatbot response and the context used.

Folder Structure
chatbot_ds/
├─ app/
│  ├─ main.py          # FastAPI app with /chat endpoint
│  ├─ schemas.py       # Pydantic model for request payload
│  ├─ config.py        # API key and URL configuration
│  ├─ rag.py           # RAG logic: context retrieval
├─ medical_symptoms.csv # CSV dataset: diseases + binary symptom columns
├─ venv/               # Python virtual environment
├─ .env                # Store DEEPSEEK_API_KEY
└─ README.md

Setup Instructions
1. Clone the repo & activate venv
git clone <your_repo_url>
cd chatbot_ds
python3 -m venv venv
source venv/bin/activate
2. Install dependencies
pip install -r requirements.txt
# Must include:
# fastapi, uvicorn, requests, pandas, faiss-cpu, python-dotenv
3. Add API Key
Create a .env file in the root:
DEEPSEEK_API_KEY=your_api_key_here
4. Start the server
uvicorn app.main:app --reload
Server runs on: http://127.0.0.1:8000
Swagger docs: http://127.0.0.1:8000/docs
API Usage
Endpoint: /chat
Method: POST
Payload:
{
    "message": "What are the symptoms of diabetes?"
}
Response:
{
    "reply": "The primary symptoms of diabetes are weight gain and thirst...",
    "context_used": [
        "diabetes is associated with symptoms such as weight gain, thirst.",
        "diabetic retinopathy is associated with symptoms such as ... "
    ]
}

Notes:
context_used shows which knowledge chunks were retrieved by RAG.
The chatbot integrates retrieved context into its response.
RAG Implementation
rag.py handles context retrieval:
Converts the CSV into a list of sentences describing disease-symptom relationships.
Embeds sentences into a FAISS vector store.
Retrieves top-N relevant chunks given the user query.
Prompt augmentation: Injects retrieved context into the prompt for better LLM answers.
Example CSV Format (medical_symptoms.csv)
diseases	fever	cough	weight_gain	thirst	eye_pain	...
diabetes	0	0	1	1	0	...
diabetic retinopathy	0	0	0	0	1	...


Postman Setup
URL: POST http://127.0.0.1:8000/chat
Headers:
Content-Type: application/json
Body:
{
    "message": "What are the symptoms of diabetes?"
}
Send → Response should include reply + context_used.

Troubleshooting
RAG not working: Check that FAISS and sentence embeddings are loaded correctly.
Duplicates in context: Remove duplicates in retrieve_context() by converting retrieved chunks to set.
Internal Server Error (500): Make sure .env has a valid API key and server is running.
Postman cannot send request: Ensure you are using POST and correct JSON body.