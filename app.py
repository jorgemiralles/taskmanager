import os
from flask import Flask, jsonify, request, render_template
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_NAME']
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
    tasks = cursor.fetchall()
    for t in tasks:
        t['completed'] = bool(t['completed'])
        t['due_date'] = t['due_date'].isoformat() if t['due_date'] else None
        t['created_at'] = t['created_at'].isoformat()
    cursor.close()
    conn.close()
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO tasks (title, priority, due_date) VALUES (%s, %s, %s)',
        (data['title'], data.get('priority', 'medium'),
         data.get('due_date') or None)
    )
    conn.commit()
    task_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({'id': task_id}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE tasks SET title=%s, priority=%s, due_date=%s WHERE id=%s',
        (data['title'], data.get('priority', 'medium'),
         data.get('due_date') or None, task_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'ok': True})

@app.route('/api/tasks/<int:task_id>/toggle', methods=['PATCH'])
def toggle_task(task_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET completed = NOT completed WHERE id=%s', (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'ok': True})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id=%s', (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
