from typing import Protocol

from fastapi import HTTPException, status
from openai import OpenAI

from app.config import Settings


class ResearchSummaryProvider(Protocol):
    def generate_summary(self, company_data: dict) -> str:
        ...


class OpenAIResearchService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def generate_summary(self, company_data: dict) -> str:
        if self.client is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=(
                    "OPENAI_API_KEY is not configured. "
                    "Add it to your environment to generate research."
                ),
            )

        response = self.client.responses.create(
            model=self.settings.openai_model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a financial research analyst. Produce balanced, concise "
                        "company research using only the supplied company data. Include "
                        "business overview, financial context, risks, and watch items."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Create a research summary for this company data: {company_data}",
                },
            ],
        )
        return response.output_text
