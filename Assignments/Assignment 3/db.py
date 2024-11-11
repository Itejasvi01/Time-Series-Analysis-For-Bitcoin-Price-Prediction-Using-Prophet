# db.py
import sqlite3

def init_db():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    
    # Create the tasks table if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            status INTEGER NOT NULL DEFAULT 0
        )
    ''')
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Initialize the database
if __name__ == '__main__':
    init_db()
