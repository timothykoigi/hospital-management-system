
import bcrypt
from models.user import User


def hash_password(password):
    return User.hash_password(password)


def verify_password(password, password_hash):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )


def authenticate(user_manager, username, password):
    return user_manager.login(username, password)