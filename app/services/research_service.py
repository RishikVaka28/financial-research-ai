from fastapi import HTTPException, status

from app.repositories import CompanyRepository, ResearchReportRepository, UserRepository
from app.schemas import ResearchCreate
from app.services.financial_data_service import FinancialDataService
from app.services.openai_research_service import ResearchSummaryProvider


class ResearchService:
    def __init__(
        self,
        company_repository: CompanyRepository,
        research_repository: ResearchReportRepository,
        user_repository: UserRepository,
        financial_data_service: FinancialDataService,
        summary_provider: ResearchSummaryProvider,
        model_name: str,
    ) -> None:
        self.company_repository = company_repository
        self.research_repository = research_repository
        self.user_repository = user_repository
        self.financial_data_service = financial_data_service
        self.summary_provider = summary_provider
        self.model_name = model_name

    def create_research_report(self, payload: ResearchCreate):
        company = self.company_repository.get_by_ticker(payload.ticker)
        if company is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company with ticker {payload.ticker} was not found.",
            )

        if payload.user_id is not None and self.user_repository.get(payload.user_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {payload.user_id} was not found.",
            )

        source_data = self.financial_data_service.build_company_snapshot(company)
        summary = self.summary_provider.generate_summary(source_data)
        return self.research_repository.create(
            company_id=company.id,
            user_id=payload.user_id,
            ticker=company.ticker,
            summary=summary,
            source_data=source_data,
            model=self.model_name,
        )

    def get_report(self, report_id: int):
        report = self.research_repository.get(report_id)
        if report is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Research report {report_id} was not found.",
            )
        return report
