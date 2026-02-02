import sqlite3

def conectar():
    conn = sqlite3.connect("financeiro.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        tipo TEXT NOT NULL,
        categoria TEXT NOT NULL,
        valor REAL NOT NULL,
        comentario TEXT,
        data TEXT NOT NULL,
        hora TEXT NOT NULL
    )
    """)
    conn.commit()
    return conn, cursor
