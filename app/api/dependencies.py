from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.database import get_db
from app.repositories import CompanyRepository, ResearchReportRepository, UserRepository
from app.services import CompanyService, OpenAIResearchService, ResearchService
from app.services.financial_data_service import FinancialDataService

DbSession = Annotated[Session, Depends(get_db)]
AppSettings = Annotated[Settings, Depends(get_settings)]


def get_company_service(db: DbSession) -> CompanyService:
    return CompanyService(CompanyRepository(db))


def get_research_service(db: DbSession, settings: AppSettings) -> ResearchService:
    return ResearchService(
        company_repository=CompanyRepository(db),
        research_repository=ResearchReportRepository(db),
        user_repository=UserRepository(db),
        financial_data_service=FinancialDataService(),
        summary_provider=OpenAIResearchService(settings),
        model_name=settings.openai_model,
    )
