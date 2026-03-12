# DomDohod MVP

DomDohod is a real estate investment assistant with a **shared FastAPI backend** and bot integrations for **Telegram** and **MAX messenger**.

## Features

- ROI and payback calculator for rental properties.
- AI-style investment assessment (high/stable/low yield).
- Shared `/calculate` API used by all channels.
- Telegram conversational bot (aiogram).
- MAX webhook processor with numeric text parsing.
- SQLite persistence with calculation history.

## Project structure

```text
domdohod/
  app/
    calculator.py
    ai_analysis.py
    investment_models.py
  bot/
    telegram_bot.py
    max_bot.py
    adapters.py
  core/
    config.py
    database.py
  main.py
  requirements.txt
  .env.example
```

## Setup

1. Create virtual environment and install dependencies:

```bash
cd domdohod
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure environment:

```bash
cp .env.example .env
```

Fill in tokens and host/port values.

## Run FastAPI backend

```bash
cd domdohod
uvicorn domdohod.main:app --reload --host 0.0.0.0 --port 8000
```

Available endpoints:

- `POST /calculate`
- `POST /telegram_webhook`
- `POST /max_webhook`

## Run Telegram bot

```bash
cd domdohod
python -m domdohod.bot.telegram_bot
```

Bot flow:
1. Property price
2. Monthly rent
3. Monthly expenses
4. Bot sends ROI/payback/analysis report

## Configure MAX webhook

1. Deploy backend and expose `/max_webhook` publicly.
2. Configure MAX callback URL in MAX developer console:
   `https://<your-domain>/max_webhook`
3. Send text with numbers, for example:
   `10000000 75000 15000`

## Example API request

```bash
curl -X POST http://127.0.0.1:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "12345",
    "source": "telegram",
    "price": 10000000,
    "rent": 75000,
    "expenses": 15000
  }'
```

Example response:

```json
{
  "roi": 7.2,
  "payback": 13.89,
  "analysis": "Stable investment: ROI is between 6% and 10%, suggesting balanced risk and return."
}
```
