from models.appointment import AppointmentManager
from models.user import UserManager
from utils.decorators import login_required, admin_required


def list_users_by_role(manager, role):
    return [
        user
        for user in manager._users
        if user.get_role() == role
    ]


def remove_user_by_username(manager, username, role=None):
    users = manager._users
    updated_users = []
    removed = None

    for user in users:
        if (
            user.get_username() == username
            and (role is None or user.get_role() == role)
        ):
            removed = user
        else:
            updated_users.append(user)

    if removed is not None:
        manager._users = updated_users
        manager._save()

    return removed


def list_appointments_by_patient(patient_id):
    manager = AppointmentManager()
    return manager.get_appointments_by_patient(patient_id)


def cancel_appointment(appointment_id):
    manager = AppointmentManager()

    for appointment in manager.get_all_appointments():
        if appointment.get_id() == appointment_id:
            manager._appointments.remove(appointment)
            manager._save()
            return True

    return False


def welcome_screen(manager=None):
    manager = manager or UserManager()

    while True:
        print("\n=== Hospital Management System ===")
        print("1. Login")
        print("2. Register as Patient")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            username = input("Username: ").strip()
            password = input("Password: ")

            user = manager.login(username, password)

            if user:
                print(f"\nWelcome, {user.get_name()}!")
                route_to_menu(user)
            else:
                print("Invalid username or password.")

        elif choice == "2":
            register_patient(manager)

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1, 2, or 3.")


def register_patient(manager):
    print("\n--- Patient Registration ---")

    name = input("Full name: ").strip()
    username = input("Username: ").strip()
    password = input("Password: ")

    if not name or not username or not password:
        print("All fields are required.")
        return None

    patient = manager.register(
        name,
        username,
        password,
        "patient",
    )

    if patient:
        print(
            f"Patient registered successfully. "
            f"Your patient ID is {patient.get_id()}."
        )

    return patient


def route_to_menu(user):
    if user.get_role() == "admin":
        admin_menu(user)

    elif user.get_role() == "doctor":
        doctor_menu(user)

    elif user.get_role() == "patient":
        patient_menu(user)

    else:
        print("Unknown user role.")


@admin_required
def admin_menu(user):
    manager = UserManager()

    while True:
        print("\n--- Admin Menu ---")
        print("1. Register Doctor")
        print("2. View Doctors")
        print("3. View Patients")
        print("4. View All Appointments")
        print("5. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            print("\n--- Register Doctor ---")

            name = input("Doctor name: ").strip()
            username = input("Username: ").strip()
            password = input("Password: ")

            print(
                "Available specialities:",
                ", ".join([
                    "General",
                    "Cardiology",
                    "Dermatology",
                    "Pediatrics",
                    "Dentistry",
                    "Orthopedics",
                ])
            )

            speciality = input("Speciality: ").strip()

            doctor = manager.register(
                name,
                username,
                password,
                "doctor",
                speciality,
            )

            if doctor:
                print(
                    f"Doctor registered successfully. "
                    f"Doctor ID: {doctor.get_id()}"
                )

        elif choice == "2":
            doctors = manager.get_all_doctors()

            if not doctors:
                print("No doctors found.")

            else:
                print("\n--- Doctors ---")

                for doctor in doctors:
                    print(
                        f"ID: {doctor.get_id()} | "
                        f"Name: {doctor.get_name()} | "
                        f"Username: {doctor.get_username()} | "
                        f"Speciality: {doctor.get_speciality()}"
                    )

        elif choice == "3":
            patients = list_users_by_role(manager, "patient")

            if not patients:
                print("No patients found.")

            else:
                print("\n--- Patients ---")

                for patient in patients:
                    print(
                        f"ID: {patient.get_id()} | "
                        f"Name: {patient.get_name()} | "
                        f"Username: {patient.get_username()}"
                    )

        elif choice == "4":
            appointment_manager = AppointmentManager()
            appointments = appointment_manager.get_all_appointments()

            if not appointments:
                print("No appointments found.")

            else:
                print("\n--- All Appointments ---")

                for appointment in appointments:
                    print(appointment)

        elif choice == "5":
            print("Logging out...")
            break

        else:
            print("Invalid option. Please try again.")


@login_required
def doctor_menu(user):
    if user.get_role() != "doctor":
        print("Doctor access required.")
        return

    appointment_manager = AppointmentManager()

    while True:
        print("\n--- Doctor Menu ---")
        print("1. View My Appointments")
        print("2. View My Patients")
        print("3. Mark Appointment as Attended")
        print("4. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            appointments = appointment_manager.get_appointments_by_doctor(
                user.get_id()
            )

            if not appointments:
                print("You have no appointments.")

            else:
                for appointment in appointments:
                    print(appointment)

        elif choice == "2":
            appointments = appointment_manager.get_appointments_by_doctor(
                user.get_id()
            )

            if not appointments:
                print("You have no patients.")

            else:
                user_manager = UserManager()

                patient_ids = {
                    appointment.get_patient_id()
                    for appointment in appointments
                }

                for patient in user_manager._users:
                    if (
                        patient.get_id() in patient_ids
                        and patient.get_role() == "patient"
                    ):
                        print(
                            f"ID: {patient.get_id()} | "
                            f"Name: {patient.get_name()} | "
                            f"Username: {patient.get_username()}"
                        )

        elif choice == "3":
            appointments = appointment_manager.get_appointments_by_doctor(
                user.get_id()
            )

            if not appointments:
                print("You have no appointments.")
                continue

            for appointment in appointments:
                print(
                    f"{appointment.get_id()} | "
                    f"Status: {appointment.get_status()}"
                )

            appointment_id = input(
                "Enter appointment ID to mark as attended: "
            ).strip()

            appointment = None

            for item in appointments:
                if item.get_id() == appointment_id:
                    appointment = item
                    break

            if appointment is None:
                print("Appointment not found.")
                continue

            if appointment_manager.mark_attended(appointment_id):
                print(
                    f"Appointment {appointment_id} "
                    "marked as attended."
                )

        elif choice == "4":
            print("Logging out...")
            break

        else:
            print("Invalid option. Please try again.")


@login_required
def patient_menu(user):
    if user.get_role() != "patient":
        print("Patient access required.")
        return

    appointment_manager = AppointmentManager()
    user_manager = UserManager()

    while True:
        print("\n--- Patient Menu ---")
        print("1. View Doctors")
        print("2. Search Doctors by Speciality")
        print("3. Book Appointment")
        print("4. View My Appointments")
        print("5. Cancel Appointment")
        print("6. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            doctors = user_manager.get_all_doctors()

            if not doctors:
                print("No doctors available.")

            else:
                for doctor in doctors:
                    print(
                        f"ID: {doctor.get_id()} | "
                        f"Name: {doctor.get_name()} | "
                        f"Speciality: {doctor.get_speciality()}"
                    )

        elif choice == "2":
            speciality = input(
                "Enter speciality: "
            ).strip()

            doctors = user_manager.get_doctors_by_speciality(
                speciality
            )

            if not doctors:
                print("No doctors found for that speciality.")

            else:
                for doctor in doctors:
                    print(
                        f"ID: {doctor.get_id()} | "
                        f"Name: {doctor.get_name()} | "
                        f"Speciality: {doctor.get_speciality()}"
                    )

        elif choice == "3":
            speciality = input(
                "Doctor speciality: "
            ).strip()

            doctors = user_manager.get_doctors_by_speciality(
                speciality
            )

            if not doctors:
                print("No doctors available for that speciality.")
                continue

            for doctor in doctors:
                print(
                    f"ID: {doctor.get_id()} | "
                    f"Name: {doctor.get_name()} | "
                    f"Speciality: {doctor.get_speciality()}"
                )

            doctor_id = input(
                "Enter doctor ID: "
            ).strip()

            doctor = None

            for item in doctors:
                if item.get_id() == doctor_id:
                    doctor = item
                    break

            if doctor is None:
                print("Doctor not found.")
                continue

            day = input(
                "Appointment day: "
            ).strip()

            period = input(
                "Period (morning/afternoon/evening): "
            ).strip().lower()

            appointment = appointment_manager.book_appointment(
                user.get_id(),
                doctor.get_id(),
                speciality,
                day,
                period,
            )

            if appointment:
                print("\nAppointment booked successfully!")
                print(appointment)

        elif choice == "4":
            appointments = appointment_manager.get_appointments_by_patient(
                user.get_id()
            )

            if not appointments:
                print("You have no appointments.")

            else:
                for appointment in appointments:
                    print(appointment)

        elif choice == "5":
            appointments = appointment_manager.get_appointments_by_patient(
                user.get_id()
            )

            if not appointments:
                print("You have no appointments to cancel.")
                continue

            for appointment in appointments:
                print(appointment)

            appointment_id = input(
                "Enter appointment ID to cancel: "
            ).strip()

            appointment = None

            for item in appointments:
                if item.get_id() == appointment_id:
                    appointment = item
                    break

            if appointment is None:
                print("Appointment not found.")
                continue

            if cancel_appointment(appointment_id):
                print(
                    f"Appointment {appointment_id} "
                    "cancelled successfully."
                )

        elif choice == "6":
            print("Logging out...")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    try:
        welcome_screen()
    except KeyboardInterrupt:
        print("\nGoodbye!")