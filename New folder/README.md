# 🧾 LedgerAI — AI-Powered Bookkeeping Platform

<div align="center">

**Automate your bookkeeping with AI-powered transaction categorization, smart dashboards, and beautiful reports.**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![Tailwind](https://img.shields.io/badge/Tailwind_CSS-3.4+-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI Categorization** | Automatically categorize transactions using rule-based engine + optional LLM |
| 📊 **Smart Dashboard** | Real-time financial overview with interactive charts |
| 📥 **CSV/Excel Import** | Bulk import transactions with duplicate detection |
| 📄 **Report Generation** | P&L, expense reports, tax summaries with PDF/CSV export |
| 👥 **Multi-tenant** | Organizations with role-based access (Owner, Accountant, Employee) |
| 🔐 **Secure** | JWT auth, field-level encryption, audit logging |
| 🌙 **Dark Mode** | Premium dark-themed UI with glassmorphism effects |
| 💬 **AI Assistant** | Chat with your financial data using natural language |

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   React +   │────▶│    Nginx     │────▶│   FastAPI    │
│  TypeScript  │     │  (Reverse    │     │   Backend    │
│  + Tailwind  │     │   Proxy)     │     │              │
└─────────────┘     └──────────────┘     └──────┬───────┘
                                                │
                    ┌───────────────────────────┼───────────────┐
                    │                           │               │
              ┌─────▼─────┐            ┌────────▼──┐    ┌──────▼──────┐
              │ PostgreSQL │            │   Redis   │    │   MinIO     │
              │ + pgvector │            │ Cache/Queue│    │ (S3 storage)│
              └───────────┘            └───────────┘    └─────────────┘
```

## 🚀 Quick Start

### Prerequisites

- [Docker](https://www.docker.com/get-started) & Docker Compose
- [Node.js 18+](https://nodejs.org/) (for frontend development)
- [Python 3.12+](https://www.python.org/) (for backend development)

### 1. Clone & Configure

```bash
git clone <your-repo-url> ledgerai
cd ledgerai

# Create environment file
cp .env.example .env
# Edit .env with your settings (defaults work for local development)
```

### 2. Start with Docker (Recommended)

```bash
# Start all services
docker compose up -d

# Run database migrations
docker compose exec backend alembic upgrade head

# Seed default categories
docker compose exec backend python -m scripts.seed_categories

# Open the app
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/docs
```

### 3. Development Mode (Without Docker)

```bash
# Start infrastructure services
docker compose up -d postgres redis minio

# Backend
cd backend
pip install -e ".[dev]"
alembic upgrade head
python -m scripts.seed_categories
uvicorn app.main:app --reload --port 8000

# Frontend (in new terminal)
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
ledgerai/
├── backend/                 # FastAPI Python backend
│   ├── app/
│   │   ├── api/v1/         # REST API routes
│   │   ├── ai/             # AI categorization engine
│   │   ├── core/           # Auth, security, middleware
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── schemas/        # Pydantic DTOs
│   │   ├── services/       # Business logic
│   │   ├── repositories/   # Data access layer
│   │   ├── workers/        # Celery background tasks
│   │   └── utils/          # Shared utilities
│   └── tests/              # Backend tests
│
├── frontend/                # React + TypeScript frontend
│   └── src/
│       ├── api/            # API client layer
│       ├── components/     # UI components
│       ├── pages/          # Page components
│       ├── stores/         # Zustand state
│       ├── hooks/          # Custom hooks
│       └── types/          # TypeScript types
│
├── infra/                   # Infrastructure configs
│   ├── nginx/              # Reverse proxy
│   └── scripts/            # Database init scripts
│
├── docker-compose.yml       # Local development stack
├── Makefile                 # Development commands
└── .env.example             # Environment template
```

## 🔧 Available Commands

```bash
make help          # Show all commands
make dev           # Start development servers
make up            # Start Docker stack
make down          # Stop Docker stack
make migrate       # Run database migrations
make seed          # Seed default categories
make test          # Run all tests
make lint          # Lint all code
make clean         # Clean everything
```

## 📊 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 Default Plans

| Plan | Price | Transactions/mo | Users | Features |
|------|-------|-----------------|-------|----------|
| **Free** | $0 | 100 | 1 | Basic categorization, dashboard |
| **Starter** | $19/mo | 1,000 | 3 | CSV import, reports, email support |
| **Professional** | $49/mo | 10,000 | 10 | AI assistant, automations, bank sync |
| **Enterprise** | Custom | Unlimited | Unlimited | Priority support, custom integrations |

## 🛡️ Security

- JWT-based authentication with refresh tokens
- Bcrypt password hashing
- Fernet encryption for sensitive data (bank tokens)
- Row-level tenant isolation
- Rate limiting on auth endpoints
- Audit logging for all mutations
- CORS configuration
- Security headers via Nginx

## 📝 License

MIT License — see [LICENSE](LICENSE) for details.
