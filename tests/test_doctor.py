from models.user import Doctor, UserManager


def test_doctor_creation():
    doctor = Doctor(
        "D1",
        "Dr. Kamau",
        "kamau",
        "doc123",
        "Cardiology"
    )

    assert doctor.get_id() == "D1"
    assert doctor.get_name() == "Dr. Kamau"
    assert doctor.get_username() == "kamau"
    assert doctor.get_role() == "doctor"
    assert doctor.get_speciality() == "Cardiology"


def test_doctor_role_property():
    doctor = Doctor(
        "D1",
        "Dr. Kamau",
        "kamau",
        "doc123",
        "Cardiology"
    )

    assert doctor.role == "doctor"


def test_doctor_password():
    doctor = Doctor(
        "D1",
        "Dr. Kamau",
        "kamau",
        "doc123",
        "Cardiology"
    )

    assert doctor.check_password("doc123") is True
    assert doctor.check_password("wrongpassword") is False


def test_register_doctor(tmp_path):
    file_path = tmp_path / "users.json"

    manager = UserManager(str(file_path))

    doctor = manager.register(
        "Dr. Kamau",
        "kamau",
        "doc123",
        "doctor",
        "Cardiology"
    )

    assert doctor is not None
    assert doctor.get_name() == "Dr. Kamau"
    assert doctor.get_role() == "doctor"
    assert doctor.get_speciality() == "Cardiology"


def test_get_all_doctors(tmp_path):
    file_path = tmp_path / "users.json"

    manager = UserManager(str(file_path))

    doctor = manager.register(
        "Dr. Kamau",
        "kamau",
        "doc123",
        "doctor",
        "Cardiology"
    )

    doctors = manager.get_all_doctors()

    assert doctor in doctors
    assert len(doctors) == 1


def test_get_doctors_by_speciality(tmp_path):
    file_path = tmp_path / "users.json"

    manager = UserManager(str(file_path))

    manager.register(
        "Dr. Kamau",
        "kamau",
        "doc123",
        "doctor",
        "Cardiology"
    )

    manager.register(
        "Dr. Otieno",
        "otieno",
        "doc456",
        "doctor",
        "Dentistry"
    )

    doctors = manager.get_doctors_by_speciality("Cardiology")

    assert len(doctors) == 1
    assert doctors[0].get_name() == "Dr. Kamau"


def test_doctor_invalid_speciality(tmp_path):
    file_path = tmp_path / "users.json"

    manager = UserManager(str(file_path))

    doctor = manager.register(
        "Dr. Wrong",
        "wrong",
        "doc123",
        "doctor",
        "WrongSpeciality"
    )

    assert doctor is None