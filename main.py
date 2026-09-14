
from models.appointment import AppointmentManager
from models.user import UserManager
from utils.auth import login, register
from utils.decorators import role_required


def list_users_by_role(manager, role):
    return [user for user in getattr(manager, "_users", []) if user.get_role() == role]


def remove_user_by_username(manager, username, role=None):
    users = list(getattr(manager, "_users", []))
    updated = []
    removed = None

    for user in users:
        if user.get_username() == username and (role is None or user.get_role() == role):
            removed = user
            continue
        updated.append(user)

    if removed is not None:
        manager._users = updated
        manager._save()

    return removed


def list_appointments_by_patient(patient_name):
    manager = AppointmentManager()
    return manager.get_appointments_by_patient(patient_name)


def cancel_appointment(appointment_id):
    manager = AppointmentManager()
    for index, appointment in enumerate(manager._appointments):
        if appointment.get_id() == appointment_id:
            del manager._appointments[index]
            manager._save()
            return True
    return False


def welcome_screen(manager=None):
    """Show the login/register menu until the user exits."""
    manager = manager or UserManager()

    while True:
        print("\n=== Hospital Appointment CLI ===")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            user = login(manager)
            if user:
                print(f"\nWelcome, {user.get_name()}!")
                route_to_menu(user)
            else:
                print("Login failed. Check your username/password and try again.")

        elif choice == "2":
            register(manager, role="patient")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option, please choose 1, 2, or 3.")


def route_to_menu(user):
    """Send a logged-in user to the menu for their role."""
    if user.role == "admin":
        admin_menu(user)
    elif user.role == "doctor":
        doctor_menu(user)
    elif user.role == "patient":
        patient_menu(user)
    else:
        print(f"Unknown role '{user.role}' — cannot open a menu.")


# ADMIN MENU

@role_required("admin")
def admin_menu(user):
    manager = UserManager()

    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Doctor")
        print("2. Remove Doctor")
        print("3. View All Appointments")
        print("4. View All Patients")
        print("5. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            new_doctor = register(manager, role="doctor")
            if new_doctor:
                print(f"Doctor {new_doctor.get_name()} was added successfully.")
        elif choice == "2":
            username = input("Doctor username to remove: ").strip()
            removed = remove_user_by_username(manager, username, role="doctor")
            if removed:
                print(f"Removed doctor: {removed.get_name()} ({removed.get_username()})")
            else:
                print("No doctor found with that username.")
        elif choice == "3":
            appointments = AppointmentManager().get_all_appointments()
            if not appointments:
                print("No appointments found.")
            else:
                for appointment in appointments:
                    print(appointment)
        elif choice == "4":
            patients = list_users_by_role(manager, "patient")
            if not patients:
                print("No patients found.")
            else:
                for patient in patients:
                    print(f"{patient.get_id()} | {patient.get_name()} | {patient.get_username()}")
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid option, try again.")


# DOCTOR MENU

@role_required("doctor")
def doctor_menu(user):
    appointment_manager = AppointmentManager()

    while True:
        print("\n--- Doctor Menu ---")
        print("1. View My Schedule")
        print("2. Set Availability")
        print("3. Mark Appointment Completed / No-show")
        print("4. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            appointments = appointment_manager.get_appointments_by_doctor(user.get_name())
            if not appointments:
                print("You have no scheduled appointments.")
            else:
                for appointment in appointments:
                    print(appointment)
        elif choice == "2":
            print("Availability is managed by appointment slots in this system.")
            print("Your current booked appointments are:")
            for appointment in appointment_manager.get_appointments_by_doctor(user.get_name()):
                print(appointment)
        elif choice == "3":
            appointments = appointment_manager.get_appointments_by_doctor(user.get_name())
            if not appointments:
                print("No appointments to update.")
            else:
                for appointment in appointments:
                    print(f"{appointment.get_id()} | {appointment.get_status()}")
                appointment_id = input("Enter appointment ID to mark as attended: ").strip()
                if appointment_manager.mark_attended(appointment_id):
                    print(f"Appointment {appointment_id} marked as attended.")
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid option, try again.")


# PATIENT MENU

@role_required("patient")
def patient_menu(user):
    while True:
        print("\n--- Patient Menu ---")
        print("1. Search Doctors by Specialty")
        print("2. Book Appointment")
        print("3. Cancel / Reschedule Appointment")
        print("4. View My Appointment History")
        print("5. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            speciality = input("Enter speciality: ").strip()
            doctors = UserManager().get_doctors_by_speciality(speciality)
            if not doctors:
                print("No doctors found for that speciality.")
            else:
                for doctor in doctors:
                    print(f"{doctor.get_name()} | {doctor.get_username()} | {doctor.get_speciality()}")
        elif choice == "2":
            speciality = input("Doctor speciality: ").strip()
            doctors = UserManager().get_doctors_by_speciality(speciality)
            if not doctors:
                print("No doctors available for that speciality.")
                continue

            print("Available doctors:")
            for doctor in doctors:
                print(f"{doctor.get_name()} | {doctor.get_username()}")

            doctor_username = input("Choose doctor username: ").strip()
            doctor = UserManager().find_by_username(doctor_username)
            if doctor is None or doctor.get_role() != "doctor":
                print("Doctor not found.")
                continue

            day = input("Appointment day: ").strip()
            period = input("Period (morning/afternoon/evening): ").strip().lower()
            appointment = AppointmentManager().book_appointment(
                user.get_name(), doctor.get_name(), speciality, day, period
            )
            if appointment:
                print(f"Appointment booked: {appointment}")
        elif choice == "3":
            appointments = list_appointments_by_patient(user.get_name())
            if not appointments:
                print("You have no appointments to cancel.")
                continue

            for appointment in appointments:
                print(f"{appointment.get_id()} | {appointment}")

            appointment_id = input("Enter appointment ID to cancel: ").strip()
            if cancel_appointment(appointment_id):
                print(f"Appointment {appointment_id} cancelled.")
            else:
                print("Appointment not found.")
        elif choice == "4":
            appointments = list_appointments_by_patient(user.get_name())
            if not appointments:
                print("You have no appointment history.")
            else:
                for appointment in appointments:
                    print(appointment)
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid option, try again.")


# ENTRY POINT

if __name__ == "__main__":
    try:
        welcome_screen()
    except KeyboardInterrupt:
        print("\nGoodbye!")