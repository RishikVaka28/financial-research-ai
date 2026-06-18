# API Documentation

Base URL for local development:

```text
http://localhost:8000
```

Interactive documentation is available at:

- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Health Check

### `GET /health`

Returns service status.

Response:

```json
{
  "status": "ok",
  "service": "Financial Research AI"
}
```

## Companies

### `POST /companies`

Creates a company record.

Request:

```json
{
  "name": "Apple Inc.",
  "ticker": "AAPL",
  "sector": "Technology",
  "industry": "Consumer Electronics",
  "description": "Builds devices, software, and services."
}
```

Response `201 Created`:

```json
{
  "id": 1,
  "name": "Apple Inc.",
  "ticker": "AAPL",
  "sector": "Technology",
  "industry": "Consumer Electronics",
  "description": "Builds devices, software, and services.",
  "created_at": "2026-06-18T00:00:00Z",
  "updated_at": "2026-06-18T00:00:00Z"
}
```

### `GET /companies`

Lists company records ordered by ticker.

Response `200 OK`:

```json
[
  {
    "id": 1,
    "name": "Apple Inc.",
    "ticker": "AAPL",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "description": "Builds devices, software, and services.",
    "created_at": "2026-06-18T00:00:00Z",
    "updated_at": "2026-06-18T00:00:00Z"
  }
]
```

## Research

### `POST /research`

Generates and stores an AI research report for a known company ticker.

Request:

```json
{
  "ticker": "AAPL",
  "user_id": null
}
```

Response `201 Created`:

```json
{
  "id": 1,
  "company_id": 1,
  "user_id": null,
  "ticker": "AAPL",
  "summary": "AI-generated company research summary...",
  "source_data": {
    "ticker": "AAPL",
    "name": "Apple Inc.",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "description": "Builds devices, software, and services."
  },
  "model": "gpt-5.5",
  "created_at": "2026-06-18T00:00:00Z"
}
```

### `GET /research/{id}`

Retrieves a stored research report.

Response `200 OK`:

```json
{
  "id": 1,
  "company_id": 1,
  "user_id": null,
  "ticker": "AAPL",
  "summary": "AI-generated company research summary...",
  "source_data": {
    "ticker": "AAPL",
    "name": "Apple Inc."
  },
  "model": "gpt-5.5",
  "created_at": "2026-06-18T00:00:00Z"
}
```

## Error Responses

- `404 Not Found`: company, user, or report does not exist.
- `409 Conflict`: duplicate company ticker.
- `422 Unprocessable Entity`: request validation failed.
- `503 Service Unavailable`: `OPENAI_API_KEY` is not configured for live research generation.
