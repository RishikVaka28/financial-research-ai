from typing import Annotated

import structlog
from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_company_service
from app.schemas import CompanyCreate, CompanyRead
from app.services import CompanyService

router = APIRouter(prefix="/companies", tags=["Companies"])
logger = structlog.get_logger()
CompanyServiceDep = Annotated[CompanyService, Depends(get_company_service)]


@router.post("", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
def create_company(
    payload: CompanyCreate,
    service: CompanyServiceDep,
):
    company = service.create_company(payload)
    logger.info("company_created", ticker=company.ticker, company_id=company.id)
    return company


@router.get("", response_model=list[CompanyRead])
def list_companies(service: CompanyServiceDep):
    return service.list_companies()


@router.get("/search", response_model=list[CompanyRead])
def search_companies(
    service: CompanyServiceDep,
    query: str = Query(min_length=1, max_length=120, examples=["apple"]),
    limit: int = Query(default=10, ge=1, le=50),
):
    return service.search_companies(query=query, limit=limit)


@router.get("/{ticker}", response_model=CompanyRead)
def get_company(ticker: str, service: CompanyServiceDep):
    return service.get_company(ticker)
