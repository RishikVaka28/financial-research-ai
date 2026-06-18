from sqlalchemy.orm import Session

from app.models import ResearchReport


class ResearchReportRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        company_id: int,
        user_id: int | None,
        ticker: str,
        summary: str,
        source_data: dict,
        model: str,
    ) -> ResearchReport:
        report = ResearchReport(
            company_id=company_id,
            user_id=user_id,
            ticker=ticker,
            summary=summary,
            source_data=source_data,
            model=model,
        )
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def get(self, report_id: int) -> ResearchReport | None:
        return self.db.get(ResearchReport, report_id)
