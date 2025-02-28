import pytest
import os
import sqlite3
from datetime import datetime
from src.database import Database

@pytest.fixture
def test_db():
    test_dir = "test_db"
    os.makedirs(test_dir, exist_ok=True)
    
    original_init = Database.__init__
    def mock_init(self):
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.create_tables()
    
    Database.__init__ = mock_init
    
    db = Database()
    yield db
    
    db.conn.close()
    Database.__init__ = original_init
    
    if os.path.exists(test_dir):
        os.rmdir(test_dir)

def test_create_tables(test_db):
    cursor = test_db.conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    assert cursor.fetchone() is not None
    
    cursor.execute("PRAGMA table_info(users)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}
    
    expected_columns = {
        'user_id': 'INTEGER',
        'username': 'TEXT',
        'first_name': 'TEXT',
        'last_name': 'TEXT',
        'joined_at': 'TIMESTAMP'
    }
    
    assert columns == expected_columns

def test_add_user(test_db):
    user_data = {
        'user_id': 12345,
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    test_db.add_user(**user_data)
    
    cursor = test_db.conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_data['user_id'],))
    user = cursor.fetchone()
    
    assert user is not None
    assert user[0] == user_data['user_id']
    assert user[1] == user_data['username']
    assert user[2] == user_data['first_name']
    assert user[3] == user_data['last_name']
    assert user[4] is not None

def test_add_duplicate_user(test_db):
    user_data = {
        'user_id': 12345,
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    test_db.add_user(**user_data)
    test_db.add_user(**user_data)
    
    cursor = test_db.conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (user_data['user_id'],))
    count = cursor.fetchone()[0]
    
    assert count == 1

def test_get_all_users(test_db):
    test_users = [
        (1, 'user1', 'First1', 'Last1'),
        (2, 'user2', 'First2', 'Last2'),
        (3, 'user3', 'First3', 'Last3')
    ]
    
    for user_id, username, first_name, last_name in test_users:
        test_db.add_user(user_id, username, first_name, last_name)
    
    users = test_db.get_all_users()
    
    assert len(users) == 3
    assert sorted(users) == [1, 2, 3]

def test_get_all_users_data(test_db):
    test_users = [
        (1, 'user1', 'First1', 'Last1'),
        (2, 'user2', 'First2', 'Last2')
    ]
    
    for user_id, username, first_name, last_name in test_users:
        test_db.add_user(user_id, username, first_name, last_name)
    
    users_data = test_db.get_all_users_data()
    
    assert len(users_data) == 2
    
    for i, (user_id, username, first_name, last_name) in enumerate(test_users):
        assert users_data[i][0] == user_id
        assert users_data[i][1] == username
        assert users_data[i][2] == first_name
        assert users_data[i][3] == last_name

def test_empty_database(test_db):
    assert test_db.get_all_users() == []
    assert test_db.get_all_users_data() == []