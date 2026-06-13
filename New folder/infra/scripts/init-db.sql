-- ─── LedgerAI Database Initialization ─────────────────────
-- This script runs on first PostgreSQL startup

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable pgvector for AI embeddings
CREATE EXTENSION IF NOT EXISTS "vector";

-- Enable pg_trgm for fuzzy text search
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create indexes schema for future partitioning
-- (tables created by Alembic migrations)
