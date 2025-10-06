import sqlite3
from contextlib import contextmanager

conn = sqlite3.connect("data.db")

def init_db():
    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL, 
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

@contextmanager
def get_db_connection(): # контекстный менедж
    conn = sqlite3.connect("data.db")
    try:
        yield conn
    finally:
        conn.close()