.PHONY: help dev up down build migrate seed test lint clean

# ─── Help ────────────────────────────────────────────────
help: ## Show this help
	@echo "LedgerAI - AI-Powered Bookkeeping Platform"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ─── Development ─────────────────────────────────────────
dev: ## Start all services for development
	docker compose up -d postgres redis minio
	@echo "Waiting for services to be ready..."
	@sleep 3
	@echo "Starting backend..."
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
	@echo "Starting frontend..."
	cd frontend && npm run dev &
	@echo ""
	@echo "🚀 LedgerAI is running!"
	@echo "   Frontend: http://localhost:5173"
	@echo "   Backend:  http://localhost:8000"
	@echo "   API Docs: http://localhost:8000/docs"
	@echo "   MinIO:    http://localhost:9001"

up: ## Start all services with Docker
	docker compose up -d
	@echo "🚀 LedgerAI is running at http://localhost:80"

down: ## Stop all services
	docker compose down

build: ## Build all Docker images
	docker compose build

# ─── Database ────────────────────────────────────────────
migrate: ## Run database migrations
	cd backend && alembic upgrade head

migrate-create: ## Create a new migration (usage: make migrate-create MSG="description")
	cd backend && alembic revision --autogenerate -m "$(MSG)"

seed: ## Seed default categories
	cd backend && python -m scripts.seed_categories

# ─── Testing ─────────────────────────────────────────────
test: ## Run all tests
	cd backend && pytest -v --cov=app
	cd frontend && npm test

test-backend: ## Run backend tests only
	cd backend && pytest -v --cov=app

test-frontend: ## Run frontend tests only
	cd frontend && npm test

# ─── Code Quality ────────────────────────────────────────
lint: ## Lint all code
	cd backend && ruff check app/
	cd frontend && npx eslint src/

format: ## Format all code
	cd backend && ruff format app/
	cd frontend && npx prettier --write src/

# ─── Utilities ───────────────────────────────────────────
clean: ## Remove all containers, volumes, and build artifacts
	docker compose down -v --remove-orphans
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf backend/.pytest_cache frontend/dist frontend/node_modules

logs: ## Show logs for all services
	docker compose logs -f

shell-db: ## Open PostgreSQL shell
	docker compose exec postgres psql -U ledgerai

shell-redis: ## Open Redis CLI
	docker compose exec redis redis-cli

env: ## Copy .env.example to .env
	cp .env.example .env
	@echo "✅ Created .env file. Edit it with your settings."
