# Electro AI Monorepo

Production-ready starter monorepo for Electro AI with modular backend, enterprise frontend, and container-first deployment.

## Structure

- `backend/`: FastAPI async service (RBAC auth, audit logs, file ingestion, OpenAI integration)
- `frontend/`: Next.js 14 dark enterprise dashboard
- `infra/`: Kubernetes deployment baseline
- `docker-compose.yml`: local platform stack with health checks

## Quickstart

1. Copy env file:
   ```bash
   cp .env.example .env
   ```
2. Start stack:
   ```bash
   make up
   ```
3. Access:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs

## Core Backend Modules

- `app/auth`: JWT auth and role enforcement (Admin / Employee)
- `app/services/audit.py`: immutable audit event logger
- `app/ingestion/parsers.py`: PDF + Excel extraction
- `app/ai/openai_service.py`: async OpenAI responses API integration

## Notes

- Set `OPENAI_API_KEY` in `.env` for live AI responses.
- Add Alembic migrations before production data rollout.
