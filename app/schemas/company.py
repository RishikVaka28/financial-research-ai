from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CompanyBase(BaseModel):
    name: str = Field(min_length=1, max_length=255, examples=["Apple Inc."])
    ticker: str = Field(min_length=1, max_length=16, examples=["AAPL"])
    sector: str | None = Field(default=None, max_length=120, examples=["Technology"])
    industry: str | None = Field(default=None, max_length=120, examples=["Consumer Electronics"])
    description: str | None = Field(
        default=None,
        max_length=4000,
        examples=["Designs, manufactures, and sells consumer electronics and services."],
    )

    @field_validator("ticker")
    @classmethod
    def normalize_ticker(cls, value: str) -> str:
        normalized = value.strip().upper()
        if not normalized:
            raise ValueError("Ticker must contain at least one non-whitespace character.")
        return normalized


class CompanyCreate(CompanyBase):
    pass


class CompanyRead(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
