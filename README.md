# Financial Research AI

Financial Research AI is a FastAPI backend that lets users store companies by ticker
and generate AI-assisted research summaries from company information and financial data.

## Features

- Create and list companies with ticker, sector, industry, and description fields.
- Generate research reports with `POST /research`.
- Store companies, users, and research reports in PostgreSQL through SQLAlchemy.
- Isolated service and repository layers for clean architecture and dependency injection.
- Pydantic request and response validation.
- Structured JSON logging with `structlog`.
- Docker and Docker Compose support.
- Swagger documentation at `/docs` and ReDoc at `/redoc`.

## API Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/companies` | Create a company record. |
| `GET` | `/companies` | List all companies. |
| `POST` | `/research` | Generate and store an AI research report for a ticker. |
| `GET` | `/research/{id}` | Retrieve a stored research report. |
| `GET` | `/health` | Health check. |

See [docs/API.md](docs/API.md) for example payloads and response shapes.

## Project Structure

```text
app/
├── api/
├── services/
├── models/
├── repositories/
├── schemas/
├── database/
└── main.py
```

## Local Setup

1. Create an environment file:

   ```bash
   cp .env.example .env
   ```

2. Add your OpenAI API key when you are ready to generate live research:

   ```bash
   OPENAI_API_KEY=your_key_here
   ```

3. Run with Docker:

   ```bash
   docker compose up --build
   ```

4. Open the API docs:

   ```text
   http://localhost:8000/docs
   ```

## Development Without Docker

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

The default non-Docker database is SQLite for quick local development. Docker Compose
uses PostgreSQL with `DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/financial_research_ai`.

## Example Requests

Create a company:

```bash
curl -X POST http://localhost:8000/companies \
  -H "Content-Type: application/json" \
  -d '{"name":"Apple Inc.","ticker":"AAPL","sector":"Technology","industry":"Consumer Electronics","description":"Builds devices, software, and services."}'
```

Generate research:

```bash
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL"}'
```

## Testing

```bash
pytest
ruff check .
```

Tests use an in-memory SQLite database and a fake research summary provider, so they do
not require an OpenAI API key.

## Architecture Notes

- `api/` contains thin route handlers and dependency wiring.
- `services/` contains business workflows, including OpenAI research generation.
- `repositories/` owns database access.
- `models/` defines SQLAlchemy tables for users, companies, and research reports.
- `schemas/` defines Pydantic validation contracts.
- `database/` owns the SQLAlchemy engine, session, and metadata initialization.

The OpenAI integration is intentionally isolated in `OpenAIResearchService`; this keeps
the domain workflow testable and makes it easy to swap in another provider later.
