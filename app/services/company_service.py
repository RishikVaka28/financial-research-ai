from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.repositories import CompanyRepository
from app.schemas import CompanyCreate


class CompanyService:
    def __init__(self, company_repository: CompanyRepository) -> None:
        self.company_repository = company_repository

    def create_company(self, payload: CompanyCreate):
        try:
            return self.company_repository.create(payload)
        except IntegrityError as exc:
            self.company_repository.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Company with ticker {payload.ticker} already exists.",
            ) from exc

    def list_companies(self):
        return self.company_repository.list()

    def get_company(self, ticker: str):
        company = self.company_repository.get_by_ticker(ticker)
        if company is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company with ticker {ticker.upper()} was not found.",
            )
        return company

    def search_companies(self, query: str, limit: int):
        return self.company_repository.search(query=query, limit=limit)
