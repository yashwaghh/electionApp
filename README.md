# Election Education Assistant

A premium, interactive AI-powered web application designed to educate citizens about the election process, voting procedures, and democracy. Built with React, FastAPI, Google Gemini 2.5 Flash, and Cloud Translation.

## ✨ Features

- **🧠 Multi-Agent AI System:** Intelligent routing directs questions to specialized agents (e.g., Timeline Specialist for deadline questions).
- **🌐 Multilingual Support:** Real-time translation to multiple languages (English, Spanish, Hindi, Chinese) using Google Cloud Translation v3.
- **📷 Multimodal Analysis:** Upload election documents or ballots for instant AI analysis and explanation.
- **🎨 Premium UI/UX:** Responsive, dark-themed glassmorphism design with micro-animations, animated typing indicators, and markdown rendering.
- **⚡ High Performance:** Serverless architecture deployed on Google Cloud Run with a highly optimized multi-stage Docker build.

## 🏗️ Architecture

- **Frontend:** React, Vite, Tailwind CSS, Axios, React-Markdown.
- **Backend:** FastAPI, Pydantic, Uvicorn.
- **AI/Cloud Services:** Google Vertex AI (Gemini 2.5 Flash), Google Cloud Translation API, Google Cloud Run.

## 🚀 Running Locally

### Prerequisites
- Node.js (v20+)
- Python (3.11+)
- Google Cloud Project with Vertex AI and Translation APIs enabled.

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

The application will be available at `http://localhost:5173`.

## 🐳 Deployment (Google Cloud Run)

The application is containerized using a multi-stage Docker build. The FastAPI backend serves the compiled React static files, ensuring a single, efficient deployment artifact.

```bash
gcloud run deploy election-assistant --source . --region us-central1 --allow-unauthenticated
```
