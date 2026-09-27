KnowledgePulse AI

Enterprise Knowledge Health & Intelligence Platform

KnowledgePulse AI is an enterprise knowledge-management platform for uploading, processing, classifying, evaluating, searching, and interacting with organizational documents using Retrieval-Augmented Generation (RAG).

Features

JWT authentication

Role-based access control: Admin, Manager, Employee

PDF, DOCX, PPTX, and TXT document upload

File validation and SHA-256 duplicate detection

Text extraction and cleaning

Document classification and quality scoring

Section detection and semantic chunking

Embedding generation and ChromaDB vector storage

Semantic and hybrid search

RAG-based AI chat with conversation history

Source-aware answers and safe no-information fallback

Knowledge Health dashboard

Search/RAG analytics

Document analytics

Document Intelligence

Technology Stack

Backend

Python, FastAPI, SQLAlchemy, PostgreSQL, psycopg2, Pydantic, JWT

AI / Retrieval

ChromaDB, Sentence Transformers, embeddings, semantic search, hybrid search, RAG, Ollama/LLM integration

Frontend

React, TypeScript, Vite, React Router, Axios, Recharts, Tailwind CSS, React Hook Form, Zod

Architecture

React Frontend
|
| REST API
v
FastAPI Backend
|
+-------------------+
|                   |
v                   v
PostgreSQL            ChromaDB
|                   |
Users, Documents,     Chunks and
Conversations,        Embeddings
Messages, Analytics

Document Processing

Upload
-> Validation
-> Text Extraction
-> Cleaning
-> Duplicate Detection
-> Classification
-> Quality Scoring
-> Section Detection
-> Semantic Chunking
-> Embeddings
-> ChromaDB
-> Processed Document

RAG Pipeline

Question
-> Query Embedding
-> ChromaDB Retrieval
-> Hybrid Relevance Scoring
-> Relevance Filtering
-> Context
-> RAG Prompt
-> LLM
-> Answer + Sources

If relevant information cannot be found, the system returns:

I could not find enough information in the available documents.

Main API

Base prefix:

/api/v1

Important endpoints:

POST /api/v1/auth/login
GET  /api/v1/users/me

POST /api/v1/documents/upload
GET  /api/v1/documents

POST /api/v1/search/search
POST /api/v1/chat/

GET /api/v1/dashboard/summary

GET /api/v1/analytics/trends
GET /api/v1/analytics/dashboard
GET /api/v1/analytics/recent-searches

GET /api/v1/knowledge-health/summary

GET /api/v1/document-analytics/overview
GET /api/v1/document-analytics/quality-distribution
GET /api/v1/document-analytics/recent

GET /api/v1/document-quality/{document_id}
GET /api/v1/documents/intelligence/{document_id}

Frontend Routes

/login
/dashboard
/documents
/upload
/chat
/analytics
/documents/intelligence/:id

Project Structure

KnowledgePulse-AI/
├── backend/
├── frontend/
├── database/
├── docker/
├── docs/
├── scripts/
├── docker-compose.yml
└── README.md

Configuration

The backend uses environment variables such as:

PROJECT_NAME
VERSION
API_V1_STR
HOST
PORT
DEBUG
SECRET_KEY
ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
DATABASE_URL
OLLAMA_MODEL
OLLAMA_HOST
GEMINI_API_KEY

Never commit .env or production secrets to Git.

Running the Backend

cd backend
.\.venv\Scripts\Activate.ps1

Start the FastAPI application with the configured Uvicorn command.

Swagger:

http://127.0.0.1:8000/docs

Running the Frontend

cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173

Testing

The project has been verified for authentication, RBAC, document upload and validation, document processing, duplicate detection, classification, quality scoring, embeddings, ChromaDB, semantic/hybrid search, RAG, conversation follow-up, safe fallback behavior, analytics, Knowledge Health, Document Intelligence, and the main frontend workflows.

Security

JWT authentication

Password hashing

Role-based authorization

Protected API endpoints

Environment-based secrets

File validation

File-size restrictions

SHA-256 hashing

RAG relevance filtering

Current Status

The core KnowledgePulse AI application has been implemented and regression-tested across its major backend and frontend workflows.

Future Enhancements

Advanced search filters

Improved document classification

Automated document reprocessing

Scheduled knowledge-health reports

Cloud/container deployment

Monitoring and logging

Additional LLM providers

Knowledge graph integration

Conclusion

KnowledgePulse AI combines enterprise document management, document intelligence, vector search, and RAG-based AI assistance into a single
knowledge