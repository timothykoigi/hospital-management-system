"""
auth.py

Authentication helper functions for the
Hospital Management System.
"""

from models.user import UserManager

try:
    import bcrypt  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover - handled at runtime when dependency is missing
    bcrypt = None


def hash_password(password):
    """Hash a password using bcrypt."""
    if bcrypt is None:
        raise RuntimeError("The 'bcrypt' package is required to hash passwords.")
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password, password_hash):
    """Verify a password against a bcrypt hash."""
    if bcrypt is None:
        raise RuntimeError("The 'bcrypt' package is required to verify passwords.")

    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8"),
    )


def login(manager=None, username=None, password=None):
    """Prompt for and validate a username/password against a UserManager."""
    if manager is None:
        manager = UserManager()

    username = username if username is not None else input("Username: ").strip()
    password = password if password is not None else input("Password: ").strip()
    return manager.login(username, password)


def register(manager=None, role="patient", name=None, username=None, password=None):
    """Prompt for a new account and register it through UserManager."""
    if manager is None:
        manager = UserManager()

    name = name if name is not None else input("Full name: ").strip()
    username = username if username is not None else input("Username: ").strip()
    password = password if password is not None else input("Password: ").strip()

    if role == "doctor":
        speciality = input("Speciality: ").strip()
        return manager.register(name, username, password, role, speciality)

    return manager.register(name, username, password, role)


def authenticate(user_manager, username, password):
    """
    Authenticate a user through UserManager.

    Returns the user if login is successful.
    Returns None if the credentials are incorrect.
    """
    return user_manager.login(username, password)

