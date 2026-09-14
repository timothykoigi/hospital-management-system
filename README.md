# Hospital Management System

A Python 3 command-line Hospital Management System built using **Object-Oriented Programming (OOP)**, **JSON storage**, **authentication**, **password hashing**, **input validation**, **role-based access control**, and **Pytest**.

The system allows administrators, doctors, and patients to manage basic hospital information and appointments through a command-line interface.

---

## Features

* User authentication and login
* Role-based access for Admins, Doctors, and Patients
* Patient registration
* Doctor registration
* View doctors and patients
* Search doctors by speciality
* Appointment booking
* Appointment cancellation
* Appointment status management
* Password hashing with bcrypt
* Input validation
* JSON-based data storage
* Automated testing with Pytest
* Git and GitHub version control

---

## User Roles

### Admin

Admins can:

* Register doctors
* View doctors
* View patients
* View all appointments
* Logout

### Doctor

Doctors can:

* View their appointments
* View their patients
* Mark appointments as attended
* Logout

### Patient

Patients can:

* Register an account
* View available doctors
* Search doctors by speciality
* Book appointments
* View their appointments
* Cancel appointments
* Logout

---

## Technology Stack

* **Python 3** — Application development
* **OOP** — Application structure and object-oriented design
* **JSON** — Local data storage
* **bcrypt** — Password hashing
* **Pytest** — Automated testing
* **Git/GitHub** — Version control

---

## Project Structure

```text
hospital-management-system/
│
├── main.py
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── appointment.py
│
├── utils/
│   ├── __init__.py
│   ├── auth.py
│   ├── storage.py
│   └── decorators.py
│
├── data/
│   ├── users.json
│   └── appointments.json
│
├── tests/
│   ├── __init__.py
│   ├── test_patient.py
│   ├── test_doctor.py
│   ├── test_admin.py
│   ├── test_auth.py
│   ├── test_appointment.py
│   └── test_decorators.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Data Storage

The application uses JSON files for local data storage instead of a relational database.

### `users.json`

The `users.json` file stores users with their roles.

Users can be:

* Admins
* Doctors
* Patients

Example structure:

```json
[
    {
        "user_id": "D1",
        "name": "Dr. Alice Smith",
        "username": "asmith",
        "password": "hashed_password",
        "role": "doctor",
        "speciality": "Cardiology"
    }
]
```

Passwords are stored as bcrypt hashes rather than plain-text passwords.

### `appointments.json`

Appointments are stored as a JSON list.

Example structure:

```json
[
    {
        "appointment_id": "A1",
        "patient_id": "P1",
        "doctor_id": "D1",
        "speciality": "Cardiology",
        "day": "Monday",
        "period": "morning",
        "status": "waiting"
    }
]
```

Appointments connect patients and doctors using their unique IDs.

Example relationship:

```text
Patient P1
    ↓
Appointment A1
    ↓
Doctor D1
```

When data is added, updated, or removed through the application, the corresponding JSON file is updated automatically.

---

## Authentication & Security

Users log in using a username and password.

```text
Username + Password
        ↓
Authentication
        ↓
Password Verification
        ↓
Identify User Role
        ↓
Display Role Menu
```

Passwords are hashed using **bcrypt** and are not stored as plain-text passwords.

The project also uses decorators for access control:

* `login_required` — restricts functionality to logged-in users
* `admin_required` — restricts functionality to administrators

---

## OOP Concepts

The project demonstrates several Object-Oriented Programming concepts:

* Classes and objects
* Encapsulation
* Inheritance
* Object relationships
* Static methods
* Class methods
* Properties
* Modular Python programming

The main user classes are:

```text
User
├── Admin
├── Doctor
└── Patient
```

The project also contains an:

```text
Appointment
```

class for managing hospital appointments.

---

## Validation & Testing

The application validates user input before saving data.

Examples of validation include:

* Required registration fields
* Unique usernames
* Valid doctor specialities
* Valid appointment periods
* Valid appointment information
* User role restrictions

Automated tests are written using **Pytest**.

Run the tests with:

```bash
pytest
```

The project currently contains tests covering:

* Admin functionality
* Doctor functionality
* Patient functionality
* Authentication
* Appointment management
* Access-control decorators

---

## Installation

Clone the repository and enter the project directory:

```bash
git clone git@github.com:YOUR_USERNAME/hospital-management-system.git

cd hospital-management-system
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the application with:

```bash
python3 main.py
```

The main menu provides:

```text
=== Hospital Management System ===

1. Login
2. Register as Patient
3. Exit
```

After login, the system identifies the user's role and displays the appropriate menu.

---

## Demo Accounts

The application automatically creates demo users when the user data file is empty.

### Admin

```text
Username: admin
Password: admin123
```

### Doctor

```text
Username: asmith
Password: doc123
```

### Doctor

```text
Username: botieno
Password: doc123
```

### Patient

```text
Username: jdoe
Password: pat123
```

These accounts are intended for demonstration and testing purposes.

---

## Project Flow

```text
Python 3
    ↓
OOP Models
    ↓
Application Logic
    ↓
Authentication + Validation
    ↓
Role-Based Access
    ↓
JSON Storage
    ↓
users.json / appointments.json
    ↓
Pytest
```

### User Flow

```text
User
  ↓
Login / Patient Registration
  ↓
Authentication
  ↓
Role Identification
  ↓
Admin / Doctor / Patient Menu
  ↓
Hospital Operations
  ↓
JSON Data Storage
```

---

## Current Scope

The current version focuses on:

* Python 3
* Object-Oriented Programming
* JSON storage
* Authentication
* bcrypt password hashing
* Role-based access control
* Input validation
* Appointment management
* Automated testing with Pytest

The project does **not** currently use:

* React
* Flask
* MySQL
* PostgreSQL
* REST APIs
* Payment integration
* Email or SMS services

These technologies may be considered for future versions.

---

## Future Improvements

Possible future additions include:

* Medical records
* Prescriptions
* Medications
* Billing
* Nurses and receptionists
* MySQL/PostgreSQL database
* Flask REST API
* React frontend
* Online deployment
* Email/SMS notifications
* More advanced appointment scheduling

---

## Git Workflow

Git and GitHub are used for version control and collaboration.

Common Git commands:

```bash
git status
git add .
git commit -m "Describe your changes"
git push origin main
```

The repository is hosted on GitHub.

---

## Testing

Run the complete test suite with:

```bash
pytest
```

The current test suite covers:

```text
Admin
Doctor
Patient
Authentication
Appointments
Decorators
```

---

## Security Notice

This is an educational project using local JSON storage.

It should **not** be used to store real patient or medical information.

A production hospital management system would require stronger security measures, including:

* Secure database infrastructure
* Strong access controls
* Encryption
* Audit logging
* Secure backups
* Monitoring
* Data privacy controls
* Appropriate healthcare data protection measures
