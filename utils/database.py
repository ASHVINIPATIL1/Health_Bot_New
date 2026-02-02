"""
Database Management
Handles user authentication and chat history storage using SQLite
"""

import sqlite3
import bcrypt
import json
from datetime import datetime
from pathlib import Path
from config.settings import Config


class Database:
    """Database operations manager"""
    
    def __init__(self):
        """Initialize database connection"""
        self.db_path = Config.DATABASE_PATH
        self._create_tables()
    
    def _get_connection(self):
        """Get database connection"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def _create_tables(self):
        """Create necessary database tables"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Chat history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                is_user_message BOOLEAN NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_user_id 
            ON chat_history(user_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON chat_history(timestamp)
        ''')
        
        conn.commit()
        conn.close()
    
    # ========== USER MANAGEMENT ==========
    
    def create_user(self, username, email, password):
        """
        Create a new user account
        
        Args:
            username (str): Username
            email (str): Email address
            password (str): Plain text password (will be hashed)
            
        Returns:
            dict: Success/error message
        """
        # Validate inputs
        if not username or not email or not password:
            return {'success': False, 'message': 'All fields are required'}
        
        if len(username) < 3:
            return {'success': False, 'message': 'Username must be at least 3 characters'}
        
        if len(password) < 6:
            return {'success': False, 'message': 'Password must be at least 6 characters'}
        
        if '@' not in email:
            return {'success': False, 'message': 'Please provide a valid email'}
        
        try:
            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            ''', (username.lower(), email.lower(), password_hash))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            
            return {
                'success': True,
                'message': 'Account created successfully! 🎉',
                'user_id': user_id
            }
        
        except sqlite3.IntegrityError:
            return {
                'success': False,
                'message': 'Username or email already exists'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'An error occurred: {str(e)}'
            }
    
    def authenticate_user(self, username, password):
        """
        Authenticate user login
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            dict: User info if successful, None otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, username, email, password_hash
                FROM users
                WHERE username = ?
            ''', (username.lower(),))
            
            user = cursor.fetchone()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
                # Update last login
                cursor.execute('''
                    UPDATE users
                    SET last_login = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (user['id'],))
                conn.commit()
                conn.close()
                
                return {
                    'success': True,
                    'user_id': user['id'],
                    'username': user['username'],
                    'email': user['email']
                }
            
            conn.close()
            return {'success': False, 'message': 'Invalid username or password'}
        
        except Exception as e:
            return {'success': False, 'message': f'Login error: {str(e)}'}
    
    def get_user_by_id(self, user_id):
        """Get user information by ID"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, username, email, created_at, last_login
                FROM users
                WHERE id = ?
            ''', (user_id,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return dict(user)
            return None
        
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
    
    # ========== CHAT HISTORY MANAGEMENT ==========
    
    def save_message(self, user_id, message, is_user_message=True):
        """
        Save a chat message
        
        Args:
            user_id (int): User ID
            message (str): Message content
            is_user_message (bool): True if from user, False if from bot
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO chat_history (user_id, message, is_user_message)
                VALUES (?, ?, ?)
            ''', (user_id, message, is_user_message))
            
            conn.commit()
            
            # Clean up old messages if exceeding limit
            cursor.execute('''
                SELECT COUNT(*) as count FROM chat_history WHERE user_id = ?
            ''', (user_id,))
            
            count = cursor.fetchone()['count']
            
            if count > Config.MAX_CHAT_HISTORY:
                # Delete oldest messages
                cursor.execute('''
                    DELETE FROM chat_history
                    WHERE id IN (
                        SELECT id FROM chat_history
                        WHERE user_id = ?
                        ORDER BY timestamp ASC
                        LIMIT ?
                    )
                ''', (user_id, count - Config.MAX_CHAT_HISTORY))
                conn.commit()
            
            conn.close()
            return True
        
        except Exception as e:
            print(f"Error saving message: {e}")
            return False
    
    def get_chat_history(self, user_id, limit=50):
        """
        Get chat history for a user
        
        Args:
            user_id (int): User ID
            limit (int): Maximum number of messages to retrieve
            
        Returns:
            list: List of messages
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT message, is_user_message, timestamp
                FROM chat_history
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
            
            messages = cursor.fetchall()
            conn.close()
            
            # Reverse to get chronological order
            return [dict(msg) for msg in reversed(messages)]
        
        except Exception as e:
            print(f"Error fetching chat history: {e}")
            return []
    
    def clear_chat_history(self, user_id):
        """Clear all chat history for a user"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM chat_history WHERE user_id = ?
            ''', (user_id,))
            
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            print(f"Error clearing chat history: {e}")
            return False
    
    def get_user_stats(self, user_id):
        """Get user statistics"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_messages,
                    SUM(CASE WHEN is_user_message = 1 THEN 1 ELSE 0 END) as user_messages,
                    MIN(timestamp) as first_message,
                    MAX(timestamp) as last_message
                FROM chat_history
                WHERE user_id = ?
            ''', (user_id,))
            
            stats = cursor.fetchone()
            conn.close()
            
            return dict(stats) if stats else None
        
        except Exception as e:
            print(f"Error fetching stats: {e}")
            return None


# Example usage and testing
if __name__ == "__main__":
    db = Database()
    
    print("=== Database Test ===\n")
    
    # Test user creation
    result = db.create_user("testuser", "test@example.com", "password123")
    print(f"Create user: {result}")
    
    # Test authentication
    auth = db.authenticate_user("testuser", "password123")
    print(f"Authenticate: {auth}")
    
    if auth['success']:
        user_id = auth['user_id']
        
        # Test message saving
        db.save_message(user_id, "Hello!", True)
        db.save_message(user_id, "Hi! How can I help?", False)
        
        # Test history retrieval
        history = db.get_chat_history(user_id)
        print(f"Chat history: {history}")
        
        # Test stats
        stats = db.get_user_stats(user_id)
        print(f"User stats: {stats}")
