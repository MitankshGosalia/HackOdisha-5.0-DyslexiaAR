import sqlite3
from pathlib import Path
from typing import Dict, Any


DB_PATH = Path(__file__).resolve().parent.parent / "database" / "app.db"


class Database:
    def __init__(self) -> None:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rating INTEGER NOT NULL,
                    comments TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS usage_stats (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    analyses INTEGER NOT NULL
                );
                """
            )
            # Ensure a single row exists
            cur.execute("INSERT OR IGNORE INTO usage_stats (id, analyses) VALUES (1, 0);")
            conn.commit()

    def add_feedback(self, rating: int, comments: str | None) -> None:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO feedback (rating, comments) VALUES (?, ?)", (rating, comments))
            conn.commit()

    def increment_usage(self) -> None:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("UPDATE usage_stats SET analyses = analyses + 1 WHERE id = 1;")
            conn.commit()

    def get_stats(self) -> Dict[str, Any]:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT analyses FROM usage_stats WHERE id = 1;")
            analyses = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM feedback;")
            feedback_count = cur.fetchone()[0]
            return {"analyses": analyses, "feedback_count": feedback_count}


