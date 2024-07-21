import sqlite3
import os

from config import DATABASE_PATH, DB_NAME, DB_NAME, DB_NAME

commands = [
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
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
""",
"""
CREATE TABLE IF NOT EXISTS uploaded_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    storage_name VARCHAR(255) NOT NULL,
    original_path VARCHAR(255) NOT NULL,
    size INTEGER NOT NULL,
    hash VARCHAR(255) NOT NULL,
    uploader_id INTEGER NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (uploader_id) REFERENCES users(id) ON DELETE CASCADE
)
""",
"""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    owner_id INTEGER NOT NULL,
    task_name VARCHAR(255) NOT NULL,
    type INTEGER NOT NULL,
    main_file_id INTEGER,
    file_count INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (main_file_id) REFERENCES uploaded_files(id) ON DELETE CASCADE
);
""",
"""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    owner_id INTEGER NOT NULL,
    file_id_1 INTEGER NOT NULL,
    file_id_2 INTEGER NOT NULL,
    similarity FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (file_id_1) REFERENCES uploaded_files(id) ON DELETE CASCADE,
    FOREIGN KEY (file_id_2) REFERENCES uploaded_files(id) ON DELETE CASCADE

); 
"""
]

if __name__ == '__main__':
    if not os.path.exists(DATABASE_PATH):
        os.makedirs(DATABASE_PATH)
        
        
    conn = sqlite3.connect(f"{DATABASE_PATH}/{DB_NAME}.db")
    cursor = conn.cursor()
    for command in commands:
        cursor.execute(command)
    conn.commit()
    conn.close()
    

