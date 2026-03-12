"""FastAPI entrypoint for DomDohod shared backend."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException

from domdohod.app.ai_analysis import analyze_investment
from domdohod.app.calculator import calculate_roi
from domdohod.app.investment_models import CalculationInput, CalculationOutput
from domdohod.bot.max_bot import handle_max_message
from domdohod.core.database import Database

app = FastAPI(title="DomDohod API", version="0.1.0")
db = Database()


@app.on_event("startup")
def on_startup() -> None:
    """Initialize database schema on service startup."""

    db.init_db()


@app.post("/calculate", response_model=CalculationOutput)
def calculate(payload: CalculationInput) -> CalculationOutput:
    """Perform ROI calculation, AI analysis and persist history."""

    try:
        result = calculate_roi(price=payload.price, rent=payload.rent, expenses=payload.expenses)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    analysis = analyze_investment(result.roi)

    user_id = db.upsert_user(external_id=payload.user_id, source=payload.source)
    property_id = db.insert_property(
        user_id=user_id,
        price=payload.price,
        rent=payload.rent,
        expenses=payload.expenses,
    )
    db.insert_calculation(
        user_id=user_id,
        property_id=property_id,
        roi=result.roi,
        payback=result.payback,
        analysis=analysis,
    )

    return CalculationOutput(roi=result.roi, payback=result.payback, analysis=analysis)


@app.post("/telegram_webhook")
def telegram_webhook(update: dict[str, Any]) -> dict[str, Any]:
    """Minimal Telegram webhook endpoint placeholder for shared backend deployments."""

    message = update.get("message", {})
    return {
        "status": "received",
        "chat_id": message.get("chat", {}).get("id"),
        "note": "Use domdohod/bot/telegram_bot.py for the full conversational flow.",
    }


@app.post("/max_webhook")
def max_webhook(payload: dict[str, Any]) -> dict[str, str]:
    """Receive MAX webhook payload and return ready-to-send response text."""

    try:
        return handle_max_message(payload)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"Failed to process MAX payload: {exc}") from exc
