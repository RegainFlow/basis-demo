from __future__ import annotations

import json
import os
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / ".data" / "invoices.sqlite3"


def database_path() -> Path:
    configured = os.environ.get("BASIS_DB_PATH")
    if configured:
        return Path(configured)
    return DEFAULT_DB_PATH


def initialize_database(path: Path | None = None) -> None:
    db_path = path or database_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as connection:
        connection.execute(
            """
            create table if not exists invoices (
                id integer primary key autoincrement,
                submitted_at text not null,
                request_json text not null,
                totals_json text not null
            )
            """
        )


def save_invoice_submission(
    request_payload: dict[str, Any],
    totals_payload: dict[str, Any],
) -> int:
    db_path = database_path()
    initialize_database(db_path)

    with sqlite3.connect(db_path) as connection:
        cursor = connection.execute(
            """
            insert into invoices (submitted_at, request_json, totals_json)
            values (?, ?, ?)
            """,
            (
                datetime.now(UTC).isoformat(),
                json.dumps(request_payload, sort_keys=True),
                json.dumps(totals_payload, sort_keys=True),
            ),
        )
        return int(cursor.lastrowid)
