from utils.decorators import login_required, admin_required


class FakeUser:
    def __init__(self, role):
        self.role = role

    def get_role(self):
        return self.role


@login_required
def protected_function(user):
    return "success"


@admin_required
def admin_function(user):
    return "admin success"


def test_login_required_allows_logged_in_user():
    user = FakeUser("patient")

    result = protected_function(user)

    assert result == "success"


def test_login_required_blocks_logged_out_user():
    result = protected_function(None)

    assert result is None


def test_admin_required_allows_admin():
    user = FakeUser("admin")

    result = admin_function(user)

    assert result == "admin success"


def test_admin_required_blocks_patient():
    user = FakeUser("patient")

    result = admin_function(user)

    assert result is None


def test_admin_required_blocks_logged_out_user():
    result = admin_function(None)

    assert result is None