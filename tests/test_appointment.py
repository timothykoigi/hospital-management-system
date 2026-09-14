from models.appointment import (
    Appointment,
    AppointmentManager,
)


def test_appointment_creation():
    appointment = Appointment(
        "A1",
        "P1",
        "D1",
        "Cardiology",
        "Monday",
        "morning",
    )

    assert appointment.get_id() == "A1"
    assert appointment.get_patient_id() == "P1"
    assert appointment.get_doctor_id() == "D1"
    assert appointment.get_speciality() == "Cardiology"
    assert appointment.get_day() == "Monday"
    assert appointment.get_period() == "morning"


def test_new_appointment_starts_as_waiting():
    appointment = Appointment(
        "A1",
        "P1",
        "D1",
        "Cardiology",
        "Monday",
        "morning",
    )

    assert appointment.get_status() == "waiting"


def test_mark_attended():
    appointment = Appointment(
        "A1",
        "P1",
        "D1",
        "Cardiology",
        "Monday",
        "morning",
    )

    appointment.mark_attended()

    assert appointment.get_status() == "attended"


def test_appointment_to_dict():
    appointment = Appointment(
        "A1",
        "P1",
        "D1",
        "Cardiology",
        "Monday",
        "morning",
    )

    data = appointment.to_dict()

    assert data["appointment_id"] == "A1"
    assert data["patient_id"] == "P1"
    assert data["doctor_id"] == "D1"
    assert data["speciality"] == "Cardiology"
    assert data["day"] == "Monday"
    assert data["period"] == "morning"
    assert data["status"] == "waiting"


def test_appointment_from_dict():
    data = {
        "appointment_id": "A1",
        "patient_id": "P1",
        "doctor_id": "D1",
        "speciality": "Cardiology",
        "day": "Monday",
        "period": "morning",
        "status": "attended",
    }

    appointment = Appointment.from_dict(data)

    assert appointment.get_id() == "A1"
    assert appointment.get_patient_id() == "P1"
    assert appointment.get_doctor_id() == "D1"
    assert appointment.get_speciality() == "Cardiology"
    assert appointment.get_day() == "Monday"
    assert appointment.get_period() == "morning"
    assert appointment.get_status() == "attended"


def test_book_appointment(tmp_path):
    file_path = tmp_path / "appointments.json"

    manager = AppointmentManager(str(file_path))

    appointment = manager.book_appointment(
        "P1",
        "D1",
        "Cardiology",
        "Monday",
        "morning",
    )

    assert appointment is not None
    assert appointment.get_id() == "A1"
    assert appointment.get_patient_id() == "P1"
    assert appointment.get_doctor_id() == "D1"
    assert appointment.get_speciality() == "Cardiology"


def test_book_appointment_saves_to_json(tmp_path):
    file_path = tmp_path / "appointments.json"

    manager = AppointmentManager(str(file_path))

    manager.book_appointment(
        "P1",
        "D1",
        "Cardiology",
        "Monday",
        "morning",
    )

    assert file_path.exists()

    manager2 = AppointmentManager(str(file_path))

    appointments = manager2.get_all_appointments()

    assert len(appointments) == 1
    assert appointments[0].get_patient_id() == "P1"
    assert appointments[0].get_doctor_id() == "D1"


def test_invalid_speciality(tmp_path):
    file_path = tmp_path / "appointments.json"

    manager = AppointmentManager(str(file_path))

    appointment = manager.book_appointment(
        "P1",
        "D1",
        "Invalid Speciality",
        "Monday",
        "morning",
    )

    assert appointment is None
    assert manager.get_all_appointments() == []


def test_invalid_period(tmp_path):
    file_path = tmp_path / "appointments.json"

    manager = AppointmentManager(str(file_path))

    appointment = manager.book_appointment(
        "P1",
        "D1",
        "Cardiology",
        "Monday",
        "midnight",
    )

    assert appointment is None
    assert manager.get_all_appointments() == []


def test_get_appointments_by_patient(tmp_path):
    file_path = tmp_path / "appointments.json"

    manager = AppointmentManager(str(file_path))

    manager.book_appointment(
        "P1",
        "D1",
        "Cardiology",
        "Monday",
        "morning",
    )

    manager.book_appointment(
        "P2",
        "D2",
        "Dentistry",
        "Tuesday",
        "afternoon",
    )

    appointments = manager.get_appointments_by_patient("P1")

    assert len(appointments) == 1
    assert appointments[0].get_patient_id() == "P1"


def test_get_appointments_by_doctor(tmp_path):
    file_path = tmp_path / "appointments.json"

    manager = AppointmentManager(str(file_path))

    manager.book_appointment(
        "P1",
        "D1",
        "Cardiology",
        "Monday",
        "morning",
    )

    manager.book_appointment(
        "P2",
        "D1",
        "Cardiology",
        "Tuesday",
        "afternoon",
    )

    appointments = manager.get_appointments_by_doctor("D1")

    assert len(appointments) == 2

    for appointment in appointments:
        assert appointment.get_doctor_id() == "D1"


def test_get_waiting_appointments(tmp_path):
    file_path = tmp_path / "appointments.json"

    manager = AppointmentManager(str(file_path))

    appointment = manager.book_appointment(
        "P1",
        "D1",
        "Cardiology",
        "Monday",
        "morning",
    )

    waiting = manager.get_waiting_appointments()

    assert len(waiting) == 1
    assert waiting[0].get_id() == appointment.get_id()


def test_get_attended_appointments(tmp_path):
    file_path = tmp_path / "appointments.json"

    manager = AppointmentManager(str(file_path))

    appointment = manager.book_appointment(
        "P1",
        "D1",
        "Cardiology",
        "Monday",
        "morning",
    )

    manager.mark_attended(appointment.get_id())

    attended = manager.get_attended_appointments()

    assert len(attended) == 1
    assert attended[0].get_id() == appointment.get_id()


def test_mark_attended_existing_appointment(tmp_path):
    file_path = tmp_path / "appointments.json"

    manager = AppointmentManager(str(file_path))

    appointment = manager.book_appointment(
        "P1",
        "D1",
        "Cardiology",
        "Monday",
        "morning",
    )

    result = manager.mark_attended(appointment.get_id())

    assert result is True
    assert appointment.get_status() == "attended"


def test_mark_attended_nonexistent_appointment(tmp_path):
    file_path = tmp_path / "appointments.json"

    manager = AppointmentManager(str(file_path))

    result = manager.mark_attended("A999")

    assert result is False


def test_appointment_ids_increment(tmp_path):
    file_path = tmp_path / "appointments.json"

    manager = AppointmentManager(str(file_path))

    first = manager.book_appointment(
        "P1",
        "D1",
        "Cardiology",
        "Monday",
        "morning",
    )

    second = manager.book_appointment(
        "P2",
        "D2",
        "Dentistry",
        "Tuesday",
        "afternoon",
    )

    assert first.get_id() == "A1"
    assert second.get_id() == "A2"