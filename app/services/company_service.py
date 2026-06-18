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
