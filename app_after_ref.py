from flask import Flask, request, redirect, render_template, url_for, abort
import sqlite3
from contextlib import closing

def create_app():
    app = Flask(__name__)
    app.config['DATABASE'] = 'tasks.db'

    def get_db():
        try:
            conn = sqlite3.connect(app.config['DATABASE'])
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"Ошибка БД: {e}")
            abort(500)

    def query_db(query, args=(), commit=False):
        with closing(get_db()) as conn:
            if commit:
                with conn:
                    return conn.execute(query, args).fetchall()
            else:
                return conn.execute(query, args).fetchall()

    @app.route('/')
    def index():
        tasks = query_db('SELECT * FROM tasks')
        return render_template('tasks.html', tasks=tasks)

    @app.route('/add', methods=['POST'])
    def add():
        task = request.form.get('task', '').strip()
        if task:
            query_db('INSERT INTO tasks (task) VALUES (?)', [task], commit=True)
        return redirect(url_for('index'))

    @app.route('/delete/<int:id>')
    def delete(id):
        if not isinstance(id, int):
            abort(400)
        query_db('DELETE FROM tasks WHERE id = ?', [id], commit=True)
        return redirect(url_for('index'))

    # Инициализация БД
    with app.app_context():
        query_db('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)', commit=True)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)