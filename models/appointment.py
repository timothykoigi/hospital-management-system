
from utils.storage import load_json, save_json


# Only these 6 specialities are allowed.
SPECIALITIES = [
    "General",
    "Cardiology",
    "Dermatology",
    "Pediatrics",
    "Dentistry",
    "Orthopedics",
]


# Only these 3 periods are allowed.
PERIODS = [
    "morning",
    "afternoon",
    "evening",
]


class Appointment:
    """
    Represents one appointment between a patient and a doctor.

    Encapsulation:
    Appointment information is stored using attributes
    beginning with an underscore.
    """

    def __init__(
        self,
        appointment_id,
        patient_id,
        doctor_id,
        speciality,
        day,
        period,
    ):
        self._appointment_id = appointment_id
        self._patient_id = patient_id
        self._doctor_id = doctor_id
        self._speciality = speciality
        self._day = day
        self._period = period
        self._status = "waiting"

    def get_id(self):
        """Return the appointment ID."""
        return self._appointment_id

    def get_patient_id(self):
        """Return the patient ID."""
        return self._patient_id

    def get_doctor_id(self):
        """Return the doctor ID."""
        return self._doctor_id

    def get_speciality(self):
        """Return the appointment speciality."""
        return self._speciality

    def get_day(self):
        """Return the appointment day."""
        return self._day

    def get_period(self):
        """Return the appointment period."""
        return self._period

    def get_status(self):
        """Return the appointment status."""
        return self._status

    def mark_attended(self):
        """Change the appointment status to attended."""
        self._status = "attended"

    def to_dict(self):
        """
        Convert the appointment into a dictionary
        so it can be stored in JSON.
        """
        return {
            "appointment_id": self._appointment_id,
            "patient_id": self._patient_id,
            "doctor_id": self._doctor_id,
            "speciality": self._speciality,
            "day": self._day,
            "period": self._period,
            "status": self._status,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Rebuild an Appointment object from JSON data.
        """

        appointment = cls(
            data["appointment_id"],
            data["patient_id"],
            data["doctor_id"],
            data["speciality"],
            data["day"],
            data["period"],
        )

        appointment._status = data["status"]

        return appointment

    def __str__(self):
        return (
            f"ID: {self._appointment_id} | "
            f"Patient ID: {self._patient_id} | "
            f"Doctor ID: {self._doctor_id} | "
            f"Speciality: {self._speciality} | "
            f"{self._day} {self._period} | "
            f"Status: {self._status}"
        )


class AppointmentManager:
    """
    Manages appointments.

    Handles:
    - Loading appointments from JSON.
    - Saving appointments to JSON.
    - Booking appointments.
    - Finding appointments.
    - Marking appointments as attended.
    """

    def __init__(self, filename="data/appointments.json"):
        self._filename = filename
        self._appointments = []

        self._load()

    def _load(self):
        """Load appointments from the JSON file."""

        data = load_json(self._filename)

        self._appointments = [
            Appointment.from_dict(item)
            for item in data
        ]

    def _save(self):
        """Save appointments to the JSON file."""

        data = [
            appointment.to_dict()
            for appointment in self._appointments
        ]

        save_json(self._filename, data)

    def _generate_id(self):
        """Create a new appointment ID such as A1, A2, A3."""

        return "A" + str(len(self._appointments) + 1)

    def book_appointment(
        self,
        patient_id,
        doctor_id,
        speciality,
        day,
        period,
    ):
        """
        Create and save a new appointment.
        """

        if speciality not in SPECIALITIES:
            print(
                "That speciality does not exist. "
                "Choose from:",
                SPECIALITIES,
            )
            return None

        if period not in PERIODS:
            print(
                "Period must be one of:",
                PERIODS,
            )
            return None

        new_appointment = Appointment(
            self._generate_id(),
            patient_id,
            doctor_id,
            speciality,
            day,
            period,
        )

        self._appointments.append(new_appointment)

        self._save()

        return new_appointment

    def mark_attended(self, appointment_id):
        """
        Mark an appointment as attended.
        """

        for appointment in self._appointments:

            if appointment.get_id() == appointment_id:

                appointment.mark_attended()

                self._save()

                return True

        print("Appointment not found.")

        return False

    def get_all_appointments(self):
        """Return all appointments."""
        return self._appointments

    def get_appointments_by_patient(self, patient_id):
        """Return appointments belonging to a patient."""

        return [
            appointment
            for appointment in self._appointments
            if appointment.get_patient_id() == patient_id
        ]

    def get_appointments_by_doctor(self, doctor_id):
        """Return appointments belonging to a doctor."""

        return [
            appointment
            for appointment in self._appointments
            if appointment.get_doctor_id() == doctor_id
        ]

    def get_waiting_appointments(self):
        """Return appointments that are still waiting."""

        return [
            appointment
            for appointment in self._appointments
            if appointment.get_status() == "waiting"
        ]

    def get_attended_appointments(self):
        """Return appointments that have been attended."""

        return [
            appointment
            for appointment in self._appointments
            if appointment.get_status() == "attended"
        ]