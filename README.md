# 🩺 Medical Chatbot with RAG (Retrieval-Augmented Generation)



## 📖 Overview

This **FastAPI** project implements a **medical question-answering chatbot** using **RAG (Retrieval-Augmented Generation)**.
The chatbot retrieves relevant medical knowledge from a CSV dataset of diseases and symptoms, injecting it into the LLM prompt for more accurate and context-aware responses.

---

## ⚡ Features

* Receives patient queries via `/chat` POST endpoint.
* Retrieves relevant disease/symptom context from a CSV knowledge base.
* Augments user queries with retrieved context for precise answers.
* Generates responses via the **DeepSeek API**.
* Returns both the chatbot response and the context used.

---

## 📁 Folder Structure

```plaintext
chatbot_ds/
├─ app/
│  ├─ main.py          # FastAPI app with /chat endpoint
│  ├─ schemas.py       # Pydantic models for request payloads
│  ├─ config.py        # API key and URL configuration
│  ├─ rag.py           # RAG logic: context retrieval
├─ app/data/
│  └─ medical_symptoms.csv # CSV dataset: diseases + binary symptom columns
├─ venv/               # Python virtual environment
├─ .env                # Stores DEEPSEEK_API_KEY (ignored by git)
└─ README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository & Activate Virtual Environment

```bash
git clone <your_repo_url>
cd chatbot_ds
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
`fastapi`, `uvicorn`, `requests`, `pandas`, `faiss-cpu`, `python-dotenv`

### 3. Add API Key

Create a `.env` file in the root:

```dotenv
DEEPSEEK_API_KEY=your_api_key_here
```

### 4. Start the Server

```bash
uvicorn app.main:app --reload
```

* **Server URL:** `http://127.0.0.1:8000`
* **Swagger docs:** `http://127.0.0.1:8000/docs`

---

## 🧩 API Usage

### Endpoint: `/chat`

* **Method:** `POST`
* **Payload Example:**

```json
{
  "message": "What are the symptoms of diabetes?"
}
```

* **Response Example:**

```json
{
  "reply": "The primary symptoms of diabetes are weight gain and thirst...",
  "context_used": [
    "diabetes is associated with symptoms such as weight gain, thirst.",
    "diabetic retinopathy is associated with symptoms such as eye pain, vision issues..."
  ]
}
```

> `context_used` shows which knowledge chunks were retrieved by RAG.

---

## 🧠 RAG Implementation

* **`rag.py`** handles context retrieval:

  1. Converts CSV rows into sentences describing disease-symptom relationships.
  2. Embeds sentences into a **FAISS vector store**.
  3. Retrieves top-N relevant chunks for each query.
  4. Augments user prompt with retrieved context before sending to LLM.

### Example CSV Format (`medical_symptoms.csv`)

| diseases             | fever | cough | weight\_gain | thirst | eye\_pain | ... |
| -------------------- | ----- | ----- | ------------ | ------ | --------- | --- |
| diabetes             | 0     | 0     | 1            | 1      | 0         | ... |
| diabetic retinopathy | 0     | 0     | 0            | 0      | 1         | ... |

---

## 🧪 Postman Setup

* **URL:** `POST http://127.0.0.1:8000/chat`
* **Headers:** `Content-Type: application/json`
* **Body Example:**

```json
{
  "message": "What are the symptoms of diabetes?"
}
```

* **Send → Response** will include `reply` + `context_used`.

---

## ⚠️ Troubleshooting

* **RAG not working:** Ensure FAISS and sentence embeddings are loaded correctly.
* **Duplicates in context:** Convert retrieved chunks to `set()` in `retrieve_context()`.
* **Internal Server Error (500):** Verify `.env` has a valid API key and server is running.
* **Postman request errors:** Make sure POST method is used with valid JSON payload.

---

## 📦 GitHub Large File Warning

The dataset `medical_symptoms.csv` exceeds GitHub's 100MB file size limit.

* **Do not commit large CSV files directly.**
* Use **Git LFS** if storing large datasets: [https://git-lfs.github.com](https://git-lfs.github.com)

Add `.env` and large datasets to `.gitignore`:

```gitignore
.env
app/data/medical_symptoms.csv
```

