import sqlite3

DB_PATH = "data/chat.db"

MAX_HISTORY = 20


def init_db():

    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        role TEXT,
        content TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_message(session_id, role, content):

    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        """
        INSERT INTO messages(
            session_id,
            role,
            content
        )
        VALUES (?, ?, ?)
        """,
        (
            session_id,
            role,
            content
        )
    )

    conn.commit()
    conn.close()


def get_history(session_id):

    conn = sqlite3.connect(DB_PATH)

    rows = conn.execute(
        """
        SELECT role, content
        FROM messages
        WHERE session_id=?
        ORDER BY id DESC
        LIMIT ?
        """,
        (
            session_id,
            MAX_HISTORY
        )
    ).fetchall()

    conn.close()

    rows.reverse()

    return [
        {
            "role": r[0],
            "content": r[1]
        }
        for r in rows
    ]


init_db()