from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('tasks.db')
    return conn

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('tasks.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)')
    conn.close()
    app.run(debug=True)