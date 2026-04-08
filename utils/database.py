import sqlite3
import datetime

DB_PATH = "data/bot_database.db"

def init_db():
    """Creates the tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Table for active shifts - added issue_key
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS active_shifts (
            user_id INTEGER PRIMARY KEY,
            start_time TEXT,
            status TEXT,
            break_start TEXT,
            total_break_seconds REAL DEFAULT 0,
            issue_key TEXT
        )
    ''')
    # Table for completed shift history - added issue_key
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shift_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            start_time TEXT,
            end_time TEXT,
            total_hours REAL,
            issue_key TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_PATH)
