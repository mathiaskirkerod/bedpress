import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional


def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect("leaderboard.db")
    cursor = conn.cursor()

    # Create scores table with tries field
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        score INTEGER NOT NULL,
        tmp_score INTEGER,
        solution TEXT,
        timestamp TEXT NOT NULL,
        tries INTEGER DEFAULT 0
    )
    """
    )

    conn.commit()
    conn.close()

    print("Database initialized successfully")


def save_submission(
    name: str,
    score: int,
    solution: Optional[str] = None,
    tmp_score: Optional[int] = None,
) -> int:
    """
    Save a user submission to the database

    Args:
        name: User's name
        score: The score achieved (1-5)
        solution: The user's solution text
        tmp_score: Temporary score for this submission

    Returns:
        The ID of the inserted record
    """
    conn = sqlite3.connect("leaderboard.db")
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()

    # Check the current number of tries
    cursor.execute(
        "SELECT tries FROM scores WHERE name = ? ORDER BY timestamp DESC LIMIT 1",
        (name,),
    )
    row = cursor.fetchone()
    tries = row[0] + 1 if row else 1

    cursor.execute(
        "INSERT INTO scores (name, score, tmp_score, solution, timestamp, tries) VALUES (?, ?, ?, ?, ?, ?)",
        (name, score, tmp_score, solution, timestamp, tries),
    )
    last_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return last_id


def get_leaderboard(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get the top scores from the leaderboard

    Args:
        limit: Maximum number of entries to return

    Returns:
        List of leaderboard entries
    """
    conn = sqlite3.connect("leaderboard.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name, score, timestamp 
        FROM scores 
        ORDER BY score DESC 
        LIMIT ?
    """,
        (limit,),
    )

    rows = cursor.fetchall()
    conn.close()

    return [{"name": row[0], "score": row[1], "timestamp": row[2]} for row in rows]


def get_top_three() -> List[Dict[str, Any]]:
    """
    Get the top three distinct users by score

    Returns:
        List of top three entries
    """
    conn = sqlite3.connect("leaderboard.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name, MAX(score) as max_score, timestamp
        FROM scores
        GROUP BY name
        ORDER BY max_score DESC
        LIMIT 3
    """
    )

    rows = cursor.fetchall()
    conn.close()

    return [{"name": row[0], "score": row[1], "timestamp": row[2]} for row in rows]
