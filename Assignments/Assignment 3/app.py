# app.py
from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row  # Allows access to rows by column name
    return conn

# Home Page: List all tasks
@app.route('/')
def home():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('home.html', tasks=tasks)

# Create Task: Add a new task
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        description = request.form['description']
        conn = get_db_connection()
        conn.execute('INSERT INTO tasks (description) VALUES (?)', (description,))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('create.html')

# Update Task: Modify an existing task
@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update(task_id):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()

    if request.method == 'POST':
        description = request.form['description']
        status = request.form.get('status', 0)
        conn.execute('UPDATE tasks SET description = ?, status = ? WHERE id = ?', (description, status, task_id))
        conn.commit()
        conn.close()
        return redirect('/')

    conn.close()
    return render_template('update.html', task=task)

# Delete Task: Remove a task
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
