# utils/auth_db.py
"""
Persistent User Authentication Database
Stores registered users in a local JSON database (users_db.json)
to support persistent User Signup and Login workflows.
"""

import os
import json

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "users_db.json")

def init_user_db():
    """
    Initializes the user database JSON file with default credentials if missing.
    """
    if not os.path.exists(DB_PATH):
        default_users = {
            "admin@saas.com": {
                "name": "Platform Administrator",
                "password": "admin123"
            },
            "kamalidevarasetty@gmail.com": {
                "name": "Kamali Devarasetty",
                "password": "admin123"
            },
            "user@demo.com": {
                "name": "Demo User",
                "password": "user123"
            }
        }
        try:
            with open(DB_PATH, "w", encoding="utf-8") as f:
                json.dump(default_users, f, indent=4)
        except Exception as e:
            print(f"Error initializing auth database: {e}")


def load_users():
    """
    Loads all registered users from the JSON database.
    """
    init_user_db()
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading auth database: {e}")
        return {}


def register_user(name, email, password):
    """
    Registers a new user inside the local JSON database.
    Returns:
        tuple: (bool, str) representing (success_status, message)
    """
    email_clean = email.strip().lower()
    users = load_users()
    
    if email_clean in users:
        return False, "An account is already linked to this email address."
        
    # Append new user credentials
    users[email_clean] = {
        "name": name.strip(),
        "password": password.strip()
    }
    
    try:
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)
        return True, "Account registered successfully!"
    except Exception as e:
        return False, f"Database write error: {str(e)}"


def verify_user(email, password):
    """
    Validates user credentials against the persistent database.
    """
    email_clean = email.strip().lower()
    users = load_users()
    
    if email_clean not in users:
        return False, None
        
    user_record = users[email_clean]
    if user_record["password"] == password.strip():
        return True, user_record["name"]
        
    return False, None
