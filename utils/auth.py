```python
"""
auth.py

Authentication helper functions for the
Hospital Management System.
"""

from models.user import User


def hash_password(password):
    """Hash a password using bcrypt."""
    return User.hash_password(password)


def verify_password(password, password_hash):
    """Verify a password against a bcrypt hash."""
    import bcrypt

    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )


def authenticate(user_manager, username, password):
    """
    Authenticate a user through UserManager.

    Returns the user if login is successful.
    Returns None if the credentials are incorrect.
    """
    return user_manager.login(username, password)
```
