# PDF Review System (FastAPI) - Full Repo

This repo contains a production-ready skeleton of the PDF Review System using FastAPI,
n8n automation, Telegram integration stubs, and Docker Compose for local deployment.

See `.env.example` for required environment variables.

Run with Docker Compose (example):
1. Copy `.env.example` -> `.env` and fill secrets.
2. docker-compose up -d --build
3. Visit:
   - FastAPI docs: http://localhost:8000/docs
   - n8n UI:         http://localhost:5678
### 🧾 PDF Review Automation System

> 🚀 A production-ready FastAPI + n8n + Telegram-based PDF Review Automation system — designed for secure PDF handling, review workflows, and automated notifications.

---

##  Overview

This system automates document (PDF) review cycles between **FastAPI**, **n8n**, and **Telegram**.  
It supports:
- Upload and validation of PDFs (≤ 5MB)
- Automated processing and review actions
- Secure callback handling
- Telegram-based review loop
- Static hosting for overlays and generated reports

---

##  ---

##  Key Components

| Component | Tech Stack | Description |
|------------|-------------|--------------|
| **Backend** | FastAPI (Python 3.10+) | Handles API endpoints, validation, auth |
| **Automation** | n8n | Executes PDF review workflow and retries |
| **Database** | PostgreSQL | Used by n8n for persistence |
| **Proxy/Static** | Nginx | Serves static files and proxies API |
| **Messaging** | Telegram Bot | Sends overlay + Excel review links |
| **Containerization** | Docker + Docker Compose | Full system orchestration |

---

## Setup & Installation

###  Clone Repository
```bash
git clone https://github.com/pappubabu200-jpg/pdf-review-automation-system.git
cd pdf-review-automation-system

# Environment set up
X_SECRET=mystrongsecret
TELEGRAM_BOT_TOKEN=123456789:ABCDEF
N8N_WEBHOOK_URL=http://n8n:5678/webhook/analyze
BASE_URL=http://localhost

### work flow
Workflow (n8n)

1. FastAPI /analyze endpoint receives PDF metadata


2. n8n workflow triggers → validates → creates overlay/excel links


3. n8n calls back FastAPI /review/continue


4. Telegram bot sends the user a message with the generated links


5. FastAPI updates the job’s status.json and cleans logs


 ## Project Structure

pdf-review-automation-system/
│
├── src/
│   ├── main.py                # FastAPI entrypoint
│   ├── config.py              # Env and app settings
│   ├── api/                   # Routes (/analyze, /review/continue)
│   ├── services/              # Telegram, file ops, n8n helpers
│   └── models/                # Job schema & status models
│
├── static/files/              # Job artifacts (PDFs, status.json)
│
├── docker-compose.yml         # Full service orchestration
├── Dockerfile                 # FastAPI build
├── nginx.conf                 # Reverse proxy and static serving
├── requirements.txt           # Dependencies
├── .env.example               # Template for environment variables
└── README.md                  # Project documentation
 ### Logs & Security

All write actions require x-secret header

Logs capture: job_id, request duration, and counters

Static file serving is sandboxed (no directory traversal)

Secrets managed via .env or Docker secrets

Nginx disables caching for /files/*
Credits

 # credits
FastAPI — High-performance Python web framework

n8n — Open-source automation platform

Docker & Nginx — For production deployment

Telegram Bot API — For real-time review updates
Status

#Stable Build: Production-ready

Includes complete Docker stack, tested API, and modular structure ready for deployment on any VPS or cloud (AWS, Render, Railway, etc.)


