import os, sqlite3
from typing import Optional

DB_PATH = os.environ.get("DB_PATH", "auth.db")

def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = connect()
    con.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    con.commit()
    con.close()

def create_user(username: str, password_hash: str) -> None:
    con = connect()
    con.execute("INSERT INTO users(username, password_hash) VALUES(?, ?)", (username, password_hash))
    con.commit()
    con.close()

def get_user_by_username(username: str) -> Optional[sqlite3.Row]:
    con = connect()
    cur = con.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    con.close()
    return row

def update_user_password(username: str, new_hash: str) -> None:
    con = connect()
    con.execute("UPDATE users SET password_hash = ? WHERE username = ?", (new_hash, username))
    con.commit()
    con.close()
