import sqlite3
import os

from config import DATABASE_PATH, ACCOUNT_DB_NAME, STORAGE_DB_NAME

account_commands = [
    """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS user_logins (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id INTEGER NOT NULL,
        login_time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        success BOOLEAN NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """
]

storage_commands = [
    """
    CREATE TABLE IF NOT EXISTS uploaded_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        storage_name VARCHAR(255) NOT NULL,
        original_path VARCHAR(255) NOT NULL,
        size INTEGER NOT NULL,
        hash VARCHAR(255) NOT NULL,
        uploader_id INTEGER NOT NULL,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        FOREIGN KEY (uploader_id) REFERENCES users(id)
    )
    """
]

if __name__ == '__main__':
    if not os.path.exists(DATABASE_PATH):
        os.makedirs(DATABASE_PATH)
        
        
    conn = sqlite3.connect(f"{DATABASE_PATH}/{ACCOUNT_DB_NAME}.db")
    cursor = conn.cursor()
    for command in account_commands:
        cursor.execute(command)
    conn.commit()
    conn.close()
    
    conn = sqlite3.connect(f"{DATABASE_PATH}/{STORAGE_DB_NAME}.db")
    cursor = conn.cursor()
    for command in storage_commands:
        cursor.execute(command)
    conn.commit()
    conn.close()

