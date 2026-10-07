"""
Database Management Module.

Manages SQLite storage for user search history.
Uses parameterized queries to prevent SQL injection and
includes fail-safe error handling for ephemeral hosting environments.
"""

from pathlib import Path
import sqlite3
from typing import List, Dict, Any


def get_db_path() -> Path:
    """Return the cross-platform path to the SQLite database file."""
    base_dir = Path(__file__).resolve().parent
    return base_dir / "movies.db"


def get_connection() -> sqlite3.Connection:
    """
    Establish and return a connection to the SQLite database.
    Sets row_factory to sqlite3.Row for dict-like row access.
    """
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """
    Initialize SQLite database and create the search_history table if it does not exist.
    Safe to call repeatedly at startup.
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS search_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    movie_title TEXT NOT NULL,
                    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            conn.commit()
    except Exception as e:
        # Non-fatal error log; ensures app startup is never blocked by database glitches
        print(f"[Database Warning] Failed to initialize SQLite table: {e}")


def add_search(movie_title: str) -> bool:
    """
    Insert a recorded movie search into the search_history table.
    Uses parameterized query to prevent SQL injection.

    Parameters:
        movie_title (str): Title of the searched movie.

    Returns:
        bool: True if inserted successfully, False otherwise.
    """
    if not movie_title or not isinstance(movie_title, str):
        return False

    clean_title = movie_title.strip()
    if not clean_title:
        return False

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO search_history (movie_title) VALUES (?);",
                (clean_title,)
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"[Database Warning] Failed to log search '{clean_title}': {e}")
        return False


def get_search_history(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Retrieve recent search history ordered by most recent first.

    Parameters:
        limit (int): Maximum number of records to return (default: 50).

    Returns:
        List[Dict[str, Any]]: List of dictionary records with 'id', 'movie_title', 'searched_at'.
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, movie_title, searched_at
                FROM search_history
                ORDER BY id DESC
                LIMIT ?;
                """,
                (limit,)
            )
            rows = cursor.fetchall()
            return [
                {
                    "id": row["id"],
                    "movie_title": row["movie_title"],
                    "searched_at": str(row["searched_at"])
                }
                for row in rows
            ]
    except Exception as e:
        print(f"[Database Warning] Failed to fetch search history: {e}")
        return []


if __name__ == "__main__":
    print("Testing SQLite database initialization...")
    init_db()
    add_search("The Dark Knight")
    add_search("Inception")
    history = get_search_history()
    print("Recent history entries:")
    for item in history:
        print(f"- {item['movie_title']} at {item['searched_at']}")
