"""Local SQLite database for offline history and snippets."""
import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".lisan" / "lisan.db"


def get_conn() -> sqlite3.Connection:
    """Get a SQLite connection with row factory enabled."""
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create all tables if they don't exist."""
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                raw_transcript TEXT NOT NULL,
                cleaned_transcript TEXT NOT NULL,
                app_name TEXT,
                word_count INTEGER,
                duration_seconds INTEGER,
                language TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS snippets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trigger TEXT NOT NULL UNIQUE,
                expansion TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            );
        """)


def save_history(
    raw: str,
    cleaned: str,
    app_name: str | None = None,
    word_count: int | None = None,
    duration: int | None = None,
    language: str | None = None,
) -> int:
    """Save a transcription to history.

    Returns:
        The inserted row ID.
    """
    with get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO history
               (raw_transcript, cleaned_transcript, app_name,
                word_count, duration_seconds, language)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (raw, cleaned, app_name, word_count, duration, language),
        )
        return cur.lastrowid  # type: ignore


def get_history(limit: int = 50) -> list[dict]:
    """Fetch most recent transcriptions.

    Args:
        limit: Max number of records to return.

    Returns:
        List of history records as dicts.
    """
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM history ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]


def get_snippets() -> list[dict]:
    """Fetch all saved snippets."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM snippets ORDER BY created_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def save_snippet(trigger: str, expansion: str) -> None:
    """Save or update a snippet.

    Args:
        trigger: The short voice trigger word e.g. 'cal'.
        expansion: The full text to expand to.
    """
    with get_conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO snippets (trigger, expansion) VALUES (?, ?)",
            (trigger, expansion),
        )


def delete_snippet(snippet_id: int) -> None:
    """Delete a snippet by ID."""
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM snippets WHERE id = ?",
            (snippet_id,),
        )