from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ResearchCreate(BaseModel):
    ticker: str = Field(min_length=1, max_length=16, examples=["AAPL"])
    user_id: int | None = Field(default=None, examples=[1])

    @field_validator("ticker")
    @classmethod
    def normalize_ticker(cls, value: str) -> str:
        return value.strip().upper()


class ResearchReportRead(BaseModel):
    id: int
    company_id: int
    user_id: int | None
    ticker: str
    summary: str
    source_data: dict
    model: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
