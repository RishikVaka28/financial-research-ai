from typing import Annotated

import structlog
from fastapi import APIRouter, Depends, status

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
