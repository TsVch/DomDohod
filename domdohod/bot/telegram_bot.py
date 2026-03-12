"""Telegram bot implementation using aiogram."""

from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from domdohod.bot.adapters import calculate_via_api, format_report
from domdohod.core.config import get_settings


class InvestmentForm(StatesGroup):
    price = State()
    rent = State()
    expenses = State()


dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.set_state(InvestmentForm.price)
    await message.answer("Welcome to DomDohod! Enter property price:")


@dp.message(InvestmentForm.price)
async def process_price(message: Message, state: FSMContext) -> None:
    if not _is_number(message.text):
        await message.answer("Please enter a valid number for property price.")
        return
    await state.update_data(price=float(message.text))
    await state.set_state(InvestmentForm.rent)
    await message.answer("Enter monthly rent:")


@dp.message(InvestmentForm.rent)
async def process_rent(message: Message, state: FSMContext) -> None:
    if not _is_number(message.text):
        await message.answer("Please enter a valid number for monthly rent.")
        return
    await state.update_data(rent=float(message.text))
    await state.set_state(InvestmentForm.expenses)
    await message.answer("Enter monthly expenses:")


@dp.message(InvestmentForm.expenses)
async def process_expenses(message: Message, state: FSMContext) -> None:
    if not _is_number(message.text):
        await message.answer("Please enter a valid number for monthly expenses.")
        return

    data = await state.get_data()
    try:
        result = calculate_via_api(
            user_id=str(message.from_user.id),
            source="telegram",
            price=data["price"],
            rent=data["rent"],
            expenses=float(message.text),
        )
    except Exception as exc:  # noqa: BLE001
        logging.exception("Failed to calculate via API: %s", exc)
        await message.answer("Could not process the request. Please try again later.")
        await state.clear()
        return

    report = format_report(result["roi"], result["payback"], result["analysis"])
    await message.answer(report, parse_mode="Markdown")
    await state.clear()


@dp.message(F.text)
async def fallback(message: Message) -> None:
    await message.answer("Send /start to begin a new investment calculation.")


def _is_number(value: str | None) -> bool:
    if value is None:
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False


async def run_bot() -> None:
    settings = get_settings()
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured.")

    bot = Bot(token=settings.telegram_bot_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_bot())
