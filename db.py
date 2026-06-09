import sqlite3

DB_NAME = "database.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password BLOB NOT NULL,
        role TEXT DEFAULT 'USER'
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS museums (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        price INTEGER NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        museum_id INTEGER NOT NULL,
        visit_date TEXT NOT NULL,
        adults INTEGER NOT NULL,
        children INTEGER NOT NULL,
        total_amount INTEGER NOT NULL,
        status TEXT DEFAULT 'ACTIVE'
    )
    """)

    # Insert museum automatically
    cur.execute("SELECT COUNT(*) FROM museums")

    if cur.fetchone()[0] == 0:

        cur.execute("""
        INSERT INTO museums(
            name,
            description,
            price
        )
        VALUES (?, ?, ?)
        """,
        (
            "Government Museum Chennai",
            "Historic Museum",
            50
        ))

    conn.commit()
    conn.close()
