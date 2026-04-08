# Kannada Government Scheme Assistant 🏛️

A full-stack, AI-powered application designed to help citizens naturally search and discover government schemes in Kannada. This project uses advanced Natural Language Processing (NLP) math to semantically understand queries rather than relying on exact keyword matches.

---

## 🛠️ Tech Stack
*   **Backend:** FastAPI (Python)
*   **Frontend:** React (Vite)
*   **Database:** MongoDB Atlas
*   **AI/NLP Model:** HuggingFace `sentence-transformers` (`paraphrase-multilingual-MiniLM-L12-v2`)

---

## 🚀 Features Implemented So Far

### 1. Database & Security Foundation
*   **MongoDB Atlas Connection:** Created a robust connection pool to the `authnlp` remote database using `motor` (Async MongoDB driver). 
*   **Environment Variables:** Refactored the architecture to use a hidden `.env` file to keep database passwords entirely secure.
*   **Git Security:** Deployed `.gitignore` files at the root level to strictly prevent any secret keys from leaking to GitHub.

### 2. AI & NLP Processing Module (`backend/utils/nlp.py`)
*   **Kannada Text Cleaning:** Uses Regex to strip standard English punctuation while safely preserving the official `\u0C80-\u0CFF` Unicode Kannada block and spaces.
*   **Tokenization:** Simple and fast space-based tokenizer built for academic performance.
*   **Semantic Embeddings:** Integrated a lightweight multilingual AI model that reads Kannada sentences and translates their "meaning" into a 384-dimensional mathematical Vector.

### 3. Database Seeding (`backend/seed.py`)
*   Created a script that actively processes and seeds 5 Sample Kannada Schemes (Gruha Lakshmi, Anna Bhagya, Gruha Jyothi, Shakti, Yuva Nidhi).
*   *Key Action:* It automatically generates the respective AI embeddings for all 5 schemes and pushes them directly into MongoDB as math arrays.

### 4. Search Algorithm (`backend/utils/search.py`)
*   **Cosine Similarity Engine:** Hand-built a lightweight Python mathematical algorithm spanning dot products and vector magnitudes.
*   It compares the angle of the user's Search Query vector against all the vectors of the schemes stored in the database.
*   Returns the scheme with the closest angle overlay and provides an exact "AI Confidence Match %".

### 5. API Routing (`backend/routes/search.py`)
*   Engineered a modular `POST /api/search` route that acts as the bridge connecting the math module and the database. 
*   Takes the frontend text, triggers the embedding generation, fetches DB schemes, performs the matching math, and perfectly formats the JSON response.

### 6. React Frontend (`frontend/`)
*   Built a dynamic and premium dark-mode interface using pure CSS (`App.css`).
*   **Features:**
    *   Responsive glassmorphism search bar.
    *   Animated loaders during ML API calls.
    *   `axios` service hook to ping the FastAPI backend seamlessly.
    *   Beautiful result cards rendering Scheme Titles, Descriptions, Hash-tags, and the AI Match %.

---

## 🚦 How to Run

### Run Backend
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt

# Start Server
uvicorn main:app --reload
```

### Run Frontend
```bash
cd frontend
npm install

# Start React View
npm run dev
```
