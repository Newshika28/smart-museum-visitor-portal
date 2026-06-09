from db import get_db_connection

conn = get_db_connection()
cur = conn.cursor()

cur.execute(
    "SELECT * FROM museums WHERE name=?",
    ("Government Museum Chennai",)
)

existing = cur.fetchone()

if not existing:

    cur.execute("""
    INSERT INTO museums(name, description, price)
    VALUES (?, ?, ?)
    """, (
        "Government Museum Chennai",
        "One of the oldest museums in India with historical collections.",
        50
    ))

    print("Museum inserted")

else:
    print("Museum already exists")

conn.commit()
conn.close()