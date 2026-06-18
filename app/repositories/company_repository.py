from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Company
from app.schemas import CompanyCreate


class CompanyRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, payload: CompanyCreate) -> Company:
        company = Company(**payload.model_dump())
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company

    def list(self) -> list[Company]:
        return list(self.db.scalars(select(Company).order_by(Company.ticker)).all())

    def get_by_ticker(self, ticker: str) -> Company | None:
        return self.db.scalar(select(Company).where(Company.ticker == ticker.upper()))
