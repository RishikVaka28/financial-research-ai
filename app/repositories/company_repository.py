from __future__ import annotations

from sqlalchemy import or_, select
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

    def search(self, query: str, limit: int) -> list[Company]:
        pattern = f"%{query.strip()}%"
        statement = (
            select(Company)
            .where(
                or_(
                    Company.ticker.ilike(pattern),
                    Company.name.ilike(pattern),
                    Company.sector.ilike(pattern),
                    Company.industry.ilike(pattern),
                )
            )
            .order_by(Company.ticker)
            .limit(limit)
        )
        return list(self.db.scalars(statement).all())
