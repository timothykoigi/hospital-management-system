from models.user import Admin, UserManager


def test_admin_creation():
    admin = Admin(
        "A1",
        "System Admin",
        "admin",
        "admin123"
    )

    assert admin.get_id() == "A1"
    assert admin.get_name() == "System Admin"
    assert admin.get_username() == "admin"
    assert admin.get_role() == "admin"


def test_admin_role_property():
    admin = Admin(
        "A1",
        "System Admin",
        "admin",
        "admin123"
    )

    assert admin.role == "admin"


def test_admin_password():
    admin = Admin(
        "A1",
        "System Admin",
        "admin",
        "admin123"
    )

    assert admin.check_password("admin123") is True
    assert admin.check_password("wrongpassword") is False


def test_register_admin(tmp_path):
    file_path = tmp_path / "users.json"

    manager = UserManager(str(file_path))

    admin = manager.register(
        "New Admin",
        "newadmin",
        "admin123",
        "admin"
    )

    assert admin is not None
    assert admin.get_name() == "New Admin"
    assert admin.get_role() == "admin"


def test_admin_login(tmp_path):
    file_path = tmp_path / "users.json"

    manager = UserManager(str(file_path))

    manager.register(
        "New Admin",
        "newadmin",
        "admin123",
        "admin"
    )

    admin = manager.login("newadmin", "admin123")

    assert admin is not None
    assert admin.get_role() == "admin"