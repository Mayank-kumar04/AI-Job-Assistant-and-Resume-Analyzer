# AI Job Assistant and Resume Analyzer

An AI-powered resume analysis and job preparation platform that helps users analyze their resumes, compare them with job descriptions, identify skill gaps, and prepare for interviews.

## Features

- Resume upload and management
- Job description analysis
- ATS score and resume evaluation
- Resume and job description matching
- AI Resume Assistant with RAG
- Context-aware answers based on resume and job description
- AI-generated interview questions
- Resume-based and project-based interview preparation
- Dashboard for resume and job analysis
- Dark and light theme support
- JWT-based authentication

## Screenshots

### Dashboard

![Dashboard](AI%20Resume%20Analysis/Dashboard.png)

### Job Description

![Job Description](AI%20Resume%20Analysis/JD.png)

### ATS Analysis

![ATS Analysis](AI%20Resume%20Analysis/ATS%20Analysis.png)

### Resume vs Job Description Matching

![JD Matching](AI%20Resume%20Analysis/JD%20Matching.png)

### AI Resume Assistant

![AI Resume Assistant](AI%20Resume%20Analysis/AI%20Chatbot.png)

### Interview Questions

![Interview Questions](AI%20Resume%20Analysis/Interview%20Qns.png) 


## Tech Stack

### Frontend
- React.js
- JavaScript
- Tailwind CSS
- Vite

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite

### AI & RAG
- Google Gemini API
- LangChain
- Retrieval-Augmented Generation (RAG)
- Vector Search
- Gemini Embeddings

### Tools & Services
- Git
- GitHub
- Supabase
- Docker

## Project Structure

AI-Resume-Analyzer-RAG/
├── backend/
│   ├── app/
│   ├── scripts/
│   ├── src/
│   ├── uploads/
│   ├── vectorstore/
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── app/
│   ├── components/
│   ├── hooks/
│   ├── lib/
│   ├── public/
│   ├── src/
│   └── package.json
├── docs/
├── scripts/
├── docker-compose.yml
├── package.json
└── README.md

## Getting Started

### Prerequisites

Make sure the following are installed:

- Python 3.10+
- Node.js 20+
- npm
- Git
- Google Gemini API key

### Clone the Repository
git clone https://github.com/Mayank-kumar04/AI-Job-Assistant-and-Resume-Analyzer.git

cd AI-Job-Assistant-and-Resume-Analyzer

### Backend Setup

Navigate to the backend directory:

cd backend

Create a virtual environment:

python -m venv venv

Activate the virtual environment on Windows:

.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Create a .env file inside the backend directory.

Example configuration:

APP_NAME=AI Resume Analyzer
APP_ENV=development
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

DATABASE_URL=sqlite+aiosqlite:///./resume_analyzer.db

GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
EMBEDDING_MODEL=models/embedding-001

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
SUPABASE_TABLE_NAME=documents
SUPABASE_QUERY_NAME=match_documents

CHUNK_SIZE=500
CHUNK_OVERLAP=50

CORS_ORIGINS=http://localhost:5173;http://localhost:3000

UPLOAD_DIR=uploads

Start the backend:

python run.py

Backend URL:

http://localhost:8000

### Frontend Setup

Open another terminal and navigate to the frontend directory:

cd frontend

Install dependencies:

npm install

Start the frontend:

npm run dev

Frontend URL:

http://localhost:5173

## Application Workflow

Resume Upload
↓
Resume Processing
↓
Job Description
↓
ATS Analysis
↓
Resume-JD Matching
↓
RAG Context Retrieval
↓
Gemini AI
↓
AI Resume Assistant
↓
Interview Preparation

## AI Resume Assistant

The AI Resume Assistant uses Retrieval-Augmented Generation (RAG) to provide context-aware responses based on the user's resume and job description.

It can help with:

- Resume improvement
- Identifying missing skills
- Job suitability analysis
- Technical preparation
- Interview preparation
- Project-related questions
- Backend development guidance
- Resume and job description comparison

## Interview Preparation

The application generates interview questions based on:

- Resume
- Job description
- Technical skills
- Projects
- Academic background

Questions are organized into:

- HR Questions
- Technical Questions
- Resume-Based Questions
- Project-Based Questions

## ATS Analysis

The ATS analysis evaluates the resume and provides insights into areas such as:

- Skills
- Experience
- Projects
- Education
- Keywords
- Resume quality

## Resume and Job Matching

The application compares the uploaded resume with a job description to identify:

- Matching skills
- Missing skills
- Relevant experience
- Keyword alignment
- Areas for improvement

## RAG Pipeline

Documents
↓
Text Extraction
↓
Document Chunking
↓
Embeddings
↓
Vector Storage
↓
Similarity Search
↓
Relevant Context
↓
Gemini
↓
Generated Response

## Screenshots

Application screenshots and documentation are available in the docs directory.

## Environment Variables

The project requires environment variables for Gemini API access and application configuration.

Use backend/.env.example as a reference when creating your environment file.

Do not commit your actual .env file or API keys to GitHub.

## Running the Application

### Backend

cd backend
.\venv\Scripts\Activate.ps1
python run.py

### Frontend

cd frontend
npm run dev

Open the application at:

http://localhost:5173

## Author

Mayank Kumar

B.Tech Computer Science & Engineering
Lovely Professional University, Punjab

GitHub: https://github.com/Mayank-kumar04

