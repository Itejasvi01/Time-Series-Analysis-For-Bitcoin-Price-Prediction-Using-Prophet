# tasks.py
import sqlite3

DATABASE = 'tasks.db'

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows access to rows by column name
    return conn

def get_all_tasks():
    """Fetches all tasks from the database."""
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return tasks

def create_task(description):
    """Inserts a new task into the database."""
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (description) VALUES (?)', (description,))
    conn.commit()
    conn.close()

def get_task_by_id(task_id):
    """Fetches a task by its ID."""
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    return task

def update_task(task_id, description, status):
    """Updates an existing task in the database."""
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET description = ?, status = ? WHERE id = ?', (description, status, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    """Deletes a task from the database."""
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
