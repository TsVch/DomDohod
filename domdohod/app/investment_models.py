"""Pydantic models used across API and bot integrations."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CalculationInput(BaseModel):
    """Input payload for ROI calculation."""

    user_id: str = Field(..., description="External user identifier from messenger")
    source: str = Field(..., description="Message source, e.g. telegram or max")
    price: float = Field(..., gt=0)
    rent: float = Field(..., ge=0)
    expenses: float = Field(..., ge=0)


class CalculationOutput(BaseModel):
    """Output payload for ROI calculation."""

    roi: float
    payback: float
    analysis: str
