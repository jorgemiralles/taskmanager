import os
import sys
import mysql.connector

TEST_DB = 'taskmanager_test'

def run_sql(statements):
    conn = mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )
    cursor = conn.cursor()
    for stmt in statements:
        if stmt.strip():
            cursor.execute(stmt)
    conn.commit()
    cursor.close()
    conn.close()

def before_all(context):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(root, '.env')
    if os.path.exists(env_path):
        for line in open(env_path):
            line = line.strip()
            if line and not line.startswith('#'):
                k, _, v = line.partition('=')
                if k:
                    os.environ.setdefault(k.strip(), v.strip())
    os.environ['DB_NAME'] = TEST_DB

    sys.path.insert(0, root)
    from app import app as flask_app

    run_sql([
        'CREATE DATABASE IF NOT EXISTS ' + TEST_DB,
        'USE ' + TEST_DB,
        '''CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
            due_date DATE,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    ])

    flask_app.config['TESTING'] = True
    context.client = flask_app.test_client()

def after_all(context):
    run_sql(['DROP DATABASE IF EXISTS ' + TEST_DB])

def before_scenario(context, scenario):
    run_sql([
        'USE ' + TEST_DB,
        'TRUNCATE TABLE tasks'
    ])
