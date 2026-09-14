from utils.decorators import login_required, admin_required


class FakeApp:
    def __init__(self, current_user=None):
        self.current_user = current_user

    @login_required
    def protected_function(self):
        return "success"

    @admin_required
    def admin_function(self):
        return "admin success"


class FakeUser:
    def __init__(self, role):
        self.role = role


def test_login_required_allows_logged_in_user():
    app = FakeApp(FakeUser("patient"))

    result = app.protected_function()

    assert result == "success"


def test_login_required_blocks_logged_out_user():
    app = FakeApp()

    result = app.protected_function()

    assert result is None


def test_admin_required_allows_admin():
    app = FakeApp(FakeUser("admin"))

    result = app.admin_function()

    assert result == "admin success"


def test_admin_required_blocks_patient():
    app = FakeApp(FakeUser("patient"))

    result = app.admin_function()

    assert result is None


def test_admin_required_blocks_logged_out_user():
    app = FakeApp()

    result = app.admin_function()

    assert result is None