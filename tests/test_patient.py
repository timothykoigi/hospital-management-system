from models.user import Patient, UserManager


def test_patient_creation():
    patient = Patient(
        "P1",
        "Jane Doe",
        "jdoe",
        "pat123"
    )

    assert patient.get_id() == "P1"
    assert patient.get_name() == "Jane Doe"
    assert patient.get_username() == "jdoe"
    assert patient.get_role() == "patient"


def test_patient_role_property():
    patient = Patient(
        "P1",
        "Jane Doe",
        "jdoe",
        "pat123"
    )

    assert patient.role == "patient"


def test_patient_password():
    patient = Patient(
        "P1",
        "Jane Doe",
        "jdoe",
        "pat123"
    )

    assert patient.check_password("pat123") is True
    assert patient.check_password("wrongpassword") is False


def test_register_patient(tmp_path):
    file_path = tmp_path / "users.json"

    manager = UserManager(str(file_path))

    patient = manager.register(
        "Kevin Otieno",
        "kevin",
        "kevin123",
        "patient"
    )

    assert patient is not None
    assert patient.get_name() == "Kevin Otieno"
    assert patient.get_username() == "kevin"
    assert patient.get_role() == "patient"


def test_find_patient_by_username(tmp_path):
    file_path = tmp_path / "users.json"

    manager = UserManager(str(file_path))

    manager.register(
        "Kevin Otieno",
        "kevin",
        "kevin123",
        "patient"
    )

    patient = manager.find_by_username("kevin")

    assert patient is not None
    assert patient.get_name() == "Kevin Otieno"


def test_patient_login(tmp_path):
    file_path = tmp_path / "users.json"

    manager = UserManager(str(file_path))

    manager.register(
        "Kevin Otieno",
        "kevin",
        "kevin123",
        "patient"
    )

    patient = manager.login("kevin", "kevin123")

    assert patient is not None
    assert patient.get_role() == "patient"


def test_patient_login_wrong_password(tmp_path):
    file_path = tmp_path / "users.json"

    manager = UserManager(str(file_path))

    manager.register(
        "Kevin Otieno",
        "kevin",
        "kevin123",
        "patient"
    )

    patient = manager.login("kevin", "wrongpassword")

    assert patient is None