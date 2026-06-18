from app.models import Company


class FinancialDataService:
    def build_company_snapshot(self, company: Company) -> dict:
        return {
            "ticker": company.ticker,
            "name": company.name,
            "sector": company.sector,
            "industry": company.industry,
            "description": company.description,
        }
