"""Core investment calculator business logic."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CalculationResult:
    """Structured result of ROI calculation."""

    roi: float
    payback: float


def calculate_roi(price: float, rent: float, expenses: float) -> CalculationResult:
    """Calculate yearly ROI (%) and payback period in years.

    Args:
        price: Property purchase price.
        rent: Monthly rental income.
        expenses: Monthly operating expenses.

    Returns:
        CalculationResult containing ROI and payback values rounded to 2 decimals.

    Raises:
        ValueError: If price is non-positive or annual profit is non-positive.
    """

    if price <= 0:
        raise ValueError("Property price must be greater than 0.")

    annual_profit = (rent - expenses) * 12
    if annual_profit <= 0:
        raise ValueError("Annual profit must be greater than 0 for ROI calculation.")

    roi = (annual_profit / price) * 100
    payback = price / annual_profit

    return CalculationResult(roi=round(roi, 2), payback=round(payback, 2))
