"""SQLite database utilities for DomDohod."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "domdohod.db"


class Database:
    """Simple SQLite wrapper for MVP persistence."""

    def __init__(self, db_path: Path = DB_PATH) -> None:
        self.db_path = db_path

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def init_db(self) -> None:
        with self.connection() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    external_id TEXT NOT NULL,
                    source TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(external_id, source)
                );

                CREATE TABLE IF NOT EXISTS properties (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    price REAL NOT NULL,
                    rent REAL NOT NULL,
                    expenses REAL NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                );

                CREATE TABLE IF NOT EXISTS calculations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    property_id INTEGER NOT NULL,
                    roi REAL NOT NULL,
                    payback REAL NOT NULL,
                    analysis TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(property_id) REFERENCES properties(id)
                );
                """
            )

    def upsert_user(self, external_id: str, source: str) -> int:
        with self.connection() as conn:
            conn.execute(
                """
                INSERT INTO users (external_id, source)
                VALUES (?, ?)
                ON CONFLICT(external_id, source) DO NOTHING
                """,
                (external_id, source),
            )
            row = conn.execute(
                "SELECT id FROM users WHERE external_id = ? AND source = ?",
                (external_id, source),
            ).fetchone()
            assert row is not None
            return int(row["id"])

    def insert_property(self, user_id: int, price: float, rent: float, expenses: float) -> int:
        with self.connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO properties (user_id, price, rent, expenses)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, price, rent, expenses),
            )
            return int(cursor.lastrowid)

    def insert_calculation(
        self,
        user_id: int,
        property_id: int,
        roi: float,
        payback: float,
        analysis: str,
    ) -> None:
        with self.connection() as conn:
            conn.execute(
                """
                INSERT INTO calculations (user_id, property_id, roi, payback, analysis)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, property_id, roi, payback, analysis),
            )
