import sqlite3


def init_db():

    conn = sqlite3.connect("database/attacks.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            username TEXT,
            password TEXT,
            user_agent TEXT,
            attack_type TEXT,
            severity TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def log_attack(
    ip_address,
    username,
    password,
    user_agent,
    attack_type,
    severity
):

    conn = sqlite3.connect("database/attacks.db")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO attacks (
            ip_address,
            username,
            password,
            user_agent,
            attack_type,
            severity
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        ip_address,
        username,
        password,
        user_agent,
        attack_type,
        severity
    ))

    conn.commit()
    conn.close()
