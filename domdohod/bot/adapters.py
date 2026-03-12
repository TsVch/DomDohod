"""Shared helpers used by Telegram and MAX bot integrations."""

from __future__ import annotations

import requests

from domdohod.core.config import get_settings


def format_report(roi: float, payback: float, analysis: str) -> str:
    """Format calculation output for messenger delivery."""

    return (
        "🏠 *DomDohod Investment Report*\n"
        f"ROI: *{roi}%*\n"
        f"Payback period: *{payback} years*\n"
        f"Analysis: {analysis}"
    )


def calculate_via_api(user_id: str, source: str, price: float, rent: float, expenses: float) -> dict:
    """Call shared FastAPI backend calculation endpoint."""

    settings = get_settings()
    response = requests.post(
        f"{settings.api_base_url}/calculate",
        json={
            "user_id": user_id,
            "source": source,
            "price": price,
            "rent": rent,
            "expenses": expenses,
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
