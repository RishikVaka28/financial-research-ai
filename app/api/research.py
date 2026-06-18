from typing import Annotated

import structlog
from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_research_service
from app.schemas import ResearchCreate, ResearchReportRead
from app.services import ResearchService

router = APIRouter(prefix="/research", tags=["Research"])
logger = structlog.get_logger()
ResearchServiceDep = Annotated[ResearchService, Depends(get_research_service)]


@router.post("", response_model=ResearchReportRead, status_code=status.HTTP_201_CREATED)
def create_research(
    payload: ResearchCreate,
    service: ResearchServiceDep,
):
    report = service.create_research_report(payload)
    logger.info("research_report_created", ticker=report.ticker, report_id=report.id)
    return report


@router.get("/{report_id}", response_model=ResearchReportRead)
def get_research(report_id: int, service: ResearchServiceDep):
    return service.get_report(report_id)
