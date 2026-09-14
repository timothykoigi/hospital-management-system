from models.user import UserManager
from utils.auth import (
    hash_password,
    verify_password,
    authenticate,
)


def test_hash_password():
    password = "test123"

    password_hash = hash_password(password)

    assert password_hash != password
    assert isinstance(password_hash, str)


def test_verify_password():
    password = "test123"

    password_hash = hash_password(password)

    assert verify_password(password, password_hash) is True


def test_verify_wrong_password():
    password = "test123"

    password_hash = hash_password(password)

    assert verify_password("wrongpassword", password_hash) is False


def test_authenticate_user(tmp_path):
    file_path = tmp_path / "users.json"

    manager = UserManager(str(file_path))

    manager.register(
        "Kevin Otieno",
        "kevin",
        "kevin123",
        "patient",
    )

    user = authenticate(
        manager,
        "kevin",
        "kevin123",
    )

    assert user is not None
    assert user.get_username() == "kevin"
    assert user.get_role() == "patient"


def test_authenticate_wrong_password(tmp_path):
    file_path = tmp_path / "users.json"

    manager = UserManager(str(file_path))

    manager.register(
        "Kevin Otieno",
        "kevin",
        "kevin123",
        "patient",
    )

    user = authenticate(
        manager,
        "kevin",
        "wrongpassword",
    )

    assert user is None


def test_authenticate_unknown_user(tmp_path):
    file_path = tmp_path / "users.json"

    manager = UserManager(str(file_path))

    user = authenticate(
        manager,
        "unknown",
        "password123",
    )

    assert user is None