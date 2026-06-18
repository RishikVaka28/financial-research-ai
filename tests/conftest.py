import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.dependencies import get_research_service
from app.database import Base, get_db
from app.main import app
from app.repositories import CompanyRepository, ResearchReportRepository, UserRepository
from app.services import ResearchService
from app.services.financial_data_service import FinancialDataService


class FakeSummaryProvider:
    def generate_summary(self, company_data: dict) -> str:
        return f"Research summary for {company_data['ticker']}: stable test outlook."


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    Base.metadata.create_all(bind=engine)

    def override_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    def override_research_service():
        db = TestingSessionLocal()
        return ResearchService(
            company_repository=CompanyRepository(db),
            research_repository=ResearchReportRepository(db),
            user_repository=UserRepository(db),
            financial_data_service=FinancialDataService(),
            summary_provider=FakeSummaryProvider(),
            model_name="fake-test-model",
        )

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_research_service] = override_research_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
