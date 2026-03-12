"""MAX messenger webhook processing module."""

from __future__ import annotations

import re
from typing import Any

from domdohod.bot.adapters import calculate_via_api, format_report

NUMBER_PATTERN = re.compile(r"-?\d+(?:\.\d+)?")


def extract_numbers(text: str) -> list[float]:
    """Extract numeric values from free-form text."""

    return [float(match) for match in NUMBER_PATTERN.findall(text)]


def handle_max_message(payload: dict[str, Any]) -> dict[str, str]:
    """Process MAX webhook payload and return response text."""

    user_id = str(payload.get("user_id", "unknown"))
    text = str(payload.get("text", ""))

    numbers = extract_numbers(text)
    if len(numbers) < 3:
        return {
            "message": (
                "Please send 3 numbers: property price, monthly rent, monthly expenses. "
                "Example: 10000000 75000 15000"
            )
        }

    price, rent, expenses = numbers[:3]
    result = calculate_via_api(
        user_id=user_id,
        source="max",
        price=price,
        rent=rent,
        expenses=expenses,
    )

    return {"message": format_report(result["roi"], result["payback"], result["analysis"])}
