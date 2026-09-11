# Hospital Management System

A Python 3 command-line Hospital Management System built using **Object-Oriented Programming (OOP)**, **JSON storage**, **authentication**, **password hashing**, **input validation**, and **Pytest**.

The system allows administrators, doctors, and patients to manage basic hospital information and appointments.

---

## Features

* User authentication and login
* Role-based access for Admins, Doctors, and Patients
* Patient registration and management
* Doctor registration and management
* Appointment creation and management
* Password hashing with bcrypt
* Input validation
* JSON-based data storage
* Automated testing with Pytest
* Git and GitHub version control

---

## User Roles

### Admin

* Register doctors
* Register patients
* View doctors
* View patients
* View appointments

### Doctor

* View appointments
* View patients

### Patient

* View profile
* View appointments

---

## Technology Stack

* **Python 3** — Application development
* **OOP** — Application structure
* **JSON** — Data storage
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
│   ├── patient.py
│   ├── doctor.py
│   ├── admin.py
│   └── appointment.py
│
├── utils/
│   ├── __init__.py
│   ├── auth.py
│   ├── storage.py
│   ├── validators.py
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

The application uses JSON files instead of a relational database.

### `users.json`

Stores:

* Admins
* Doctors
* Patients

```json
{
    "admins": [],
    "doctors": [],
    "patients": []
}
```

### `appointments.json`

Stores hospital appointments.

```json
{
    "appointments": []
}
```

Appointments connect patients and doctors using their IDs.

```text
Patient P001
     ↓
Appointment AP001
     ↓
Doctor D001
```

When data is added or updated through the application, the corresponding JSON file is automatically updated.

---

## Authentication & Security

Users log in using a username and password.

```text
Username + Password
        ↓
Authentication
        ↓
Verify Password
        ↓
Identify Role
        ↓
Display Role Menu
```

Passwords are hashed using **bcrypt** and are not stored as plain text.

---

## OOP Concepts

The project demonstrates:

* Classes and objects
* Encapsulation
* Object relationships
* Inheritance where appropriate
* Static methods
* Modular Python programming

The main models are:

```text
Patient
Doctor
Admin
Appointment
```

---

## Validation & Testing

User input is validated before data is stored.

Examples include:

* Required fields
* Valid ages
* Unique usernames
* Valid phone numbers
* Valid appointment information

Automated tests are written using **Pytest**.

Run the tests with:

```bash
pytest
```

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

Activate it:

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

The application provides a command-line interface for authentication and hospital management.

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
JSON Storage
   ↓
users.json / appointments.json
   ↓
Pytest
```

User flow:

```text
User
 ↓
Login
 ↓
Authentication
 ↓
Role Identification
 ↓
Admin / Doctor / Patient Menu
 ↓
Hospital Operations
 ↓
JSON Data
```

---

## Current Scope

The current version focuses on Python, OOP, JSON storage, authentication, validation, and testing.

The project does **not** currently use:

* React
* Flask
* MySQL
* PostgreSQL
* REST APIs
* Payment integration

These may be considered for future versions.

---

## Future Improvements

Possible future additions include:

* Medical records
* Prescriptions
* Medications
* Billing
* Nurses and receptionists
* MySQL/PostgreSQL
* Flask REST API
* React frontend
* Online deployment

---

## Git Workflow

```bash
git status
git add .
git commit -m "Describe your changes"
git push
```

Git and GitHub are used to track development and collaborate on the project.

---

## Security Notice

This is an educational project using local JSON storage. It should not be used to store real patient or medical information.

A production system would require stronger security, a secure database, access controls, encryption, auditing, backups, and appropriate healthcare data protection measures.
