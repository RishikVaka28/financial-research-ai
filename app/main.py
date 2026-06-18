from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.companies import router as companies_router
from app.api.research import router as research_router
from app.config import get_settings
from app.database import init_db
from app.logging import configure_logging

settings = get_settings()
configure_logging(settings.log_level)


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    summary="AI-generated company research summaries from company and financial data.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Companies", "description": "Create and list company records by ticker."},
        {"name": "Research", "description": "Generate and retrieve AI research reports."},
    ],
)

app.include_router(companies_router)
app.include_router(research_router)


@app.get("/health", tags=["System"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}
