import os
import sys
import pytest
import mysql.connector

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if os.path.exists('.env'):
    for line in open('.env'):
        line = line.strip()
        if line and not line.startswith('#'):
            k, _, v = line.partition('=')
            if k:
                os.environ.setdefault(k.strip(), v.strip())

os.environ['DB_NAME'] = 'taskmanager_test'

from app import app as flask_app

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


@pytest.fixture(scope='session')
def app():
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
    yield flask_app
    run_sql(['DROP DATABASE IF EXISTS ' + TEST_DB])


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clean_tasks():
    run_sql([
        'USE ' + TEST_DB,
        'TRUNCATE TABLE tasks'
    ])
