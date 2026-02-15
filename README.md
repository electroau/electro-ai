# Electro AI - Document Intelligence Backend

FastAPI backend implementing upload, parsing, vectorization, and RBAC-aware access for business documents.

## Features
- `POST /api/documents/upload` for `.xlsx`, `.csv`, `.pdf` uploads (50MB max).
- Local file storage under `data/uploads/{user_id}/{year}/{month}`.
- PostgreSQL metadata persistence using SQLAlchemy `Document` model.
- Background parsing and embedding pipeline:
  - CSV/Excel parsed with pandas.
  - PDF parsed with pdfplumber.
  - Text normalization and ~800-token chunking.
  - OpenAI embeddings persisted in Qdrant with metadata payload.
- RBAC:
  - Authenticated users required via headers.
  - Employees only see their own docs.
  - Admin can access all docs.
- Audit logging for upload + processing lifecycle.

## Auth headers
Use these headers on API requests:
- `X-User-Id`: UUID for authenticated user.
- `X-User-Role`: `employee` or `admin`.

## Quickstart
1. Add environment variables (optional `.env`):
   - `OPENAI_API_KEY`
2. Start services:
   ```bash
   docker compose up --build
   ```
3. API is available at `http://localhost:8000`.

## Endpoints
- `POST /api/documents/upload`
- `GET /api/documents`
- `GET /api/documents/{document_id}`
- `GET /health`

## Upload example
```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -H "X-User-Id: 11111111-1111-1111-1111-111111111111" \
  -H "X-User-Role: employee" \
  -F "file=@sample.csv"
```

## Notes
- If `OPENAI_API_KEY` is missing, background processing marks documents as `failed`.
- Tables are created automatically on startup for local development.
