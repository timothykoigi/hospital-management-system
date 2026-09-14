"""
appointment.py

This file handles everything about appointments:
- the Appointment class (one single appointment)
- the AppointmentManager class (keeps track of all appointments,
  saves/loads them from a JSON file, and lets patients book doctors)
"""

import json
import os

# Only these 6 specialities are allowed in this system.
SPECIALITIES = [
    "General",
    "Cardiology",
    "Dermatology",
    "Pediatrics",
    "Dentistry",
    "Orthopedics",
]

# Only these 3 periods are allowed instead of exact times.
PERIODS = ["morning", "afternoon", "evening"]


class Appointment:
    """
    Represents one appointment between a patient and a doctor.

    Encapsulation: the attributes below start with an underscore (_status,
    _day, etc). This is a signal that other code should not change them
    directly. Instead, other code should use the get/set methods provided,
    which keeps control over how the data is changed.
    """

    def __init__(self, appointment_id, patient_name, doctor_name, speciality, day, period):
        self._appointment_id = appointment_id
        self._patient_name = patient_name
        self._doctor_name = doctor_name
        self._speciality = speciality
        self._day = day
        self._period = period
        self._status = "waiting"  # every new appointment starts as "waiting"

    # Getter methods, used to safely read the private attributes.
    def get_id(self):
        return self._appointment_id

    def get_patient_name(self):
        return self._patient_name

    def get_doctor_name(self):
        return self._doctor_name

    def get_speciality(self):
        return self._speciality

    def get_day(self):
        return self._day

    def get_period(self):
        return self._period

    def get_status(self):
        return self._status

    # The only way to change the status from outside this class.
    def mark_attended(self):
        self._status = "attended"

    def to_dict(self):
        """Turns this appointment into a plain dictionary, so it can be saved as JSON."""
        return {
            "appointment_id": self._appointment_id,
            "patient_name": self._patient_name,
            "doctor_name": self._doctor_name,
            "speciality": self._speciality,
            "day": self._day,
            "period": self._period,
            "status": self._status,
        }

    @classmethod
    def from_dict(cls, data):
        """Rebuilds an Appointment object from a dictionary (used when loading JSON)."""
        appointment = cls(
            data["appointment_id"],
            data["patient_name"],
            data["doctor_name"],
            data["speciality"],
            data["day"],
            data["period"],
        )
        appointment._status = data["status"]
        return appointment

    def __str__(self):
        return (
            f"ID: {self._appointment_id} | Patient: {self._patient_name} | "
            f"Doctor: {self._doctor_name} ({self._speciality}) | "
            f"{self._day} {self._period} | Status: {self._status}"
        )


class AppointmentManager:
    """
    Keeps the list of all appointments and handles saving/loading them
    to a JSON file so the data is not lost when the program closes.
    """

    def __init__(self, filename="data/appointments.json"):
        self._filename = filename
        self._appointments = []
        self._load()

    def _load(self):
        """Reads appointments from the JSON file, if it exists."""
        if os.path.exists(self._filename):
            with open(self._filename, "r") as file:
                data = json.load(file)
                self._appointments = [Appointment.from_dict(item) for item in data]

    def _save(self):
        """Writes all appointments to the JSON file."""
        with open(self._filename, "w") as file:
            data = [appointment.to_dict() for appointment in self._appointments]
            json.dump(data, file, indent=4)

    def _generate_id(self):
        """Creates a new appointment ID like A1, A2, A3..."""
        return "A" + str(len(self._appointments) + 1)

    def book_appointment(self, patient_name, doctor_name, speciality, day, period):
        """Creates a new appointment and saves it. A patient can book any doctor,
        for any day/period, no restrictions."""
        if speciality not in SPECIALITIES:
            print("That speciality does not exist. Choose from:", SPECIALITIES)
            return None

        if period not in PERIODS:
            print("Period must be one of:", PERIODS)
            return None

        new_appointment = Appointment(
            self._generate_id(), patient_name, doctor_name, speciality, day, period
        )
        self._appointments.append(new_appointment)
        self._save()
        return new_appointment

    def mark_attended(self, appointment_id):
        """Used by a doctor or admin to mark an appointment as attended."""
        for appointment in self._appointments:
            if appointment.get_id() == appointment_id:
                appointment.mark_attended()
                self._save()
                return True
        print("Appointment not found.")
        return False

    def get_all_appointments(self):
        return self._appointments

    def get_appointments_by_patient(self, patient_name):
        return [a for a in self._appointments if a.get_patient_name() == patient_name]

    def get_appointments_by_doctor(self, doctor_name):
        return [a for a in self._appointments if a.get_doctor_name() == doctor_name]

    def get_waiting_appointments(self):
        """Used by the admin to see who is still in the queue."""
        return [a for a in self._appointments if a.get_status() == "waiting"]

    def get_attended_appointments(self):
        """Used by the admin to see who has already been attended to."""
        return [a for a in self._appointments if a.get_status() == "attended"]