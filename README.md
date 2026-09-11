# Hospital Management System

A Python 3 Hospital Management System built using **Object-Oriented Programming (OOP)**, **JSON file storage**, **authentication**, **password hashing**, **input validation**, and **automated testing with Pytest**.

The project is a command-line application designed to demonstrate how Python and OOP concepts can be applied to a practical hospital management system.

The current version focuses on three types of users:

* Administrators
* Doctors
* Patients

The system also manages hospital appointments.

The project does not use React, Flask, MySQL, or any other relational database in the current version. Data is stored locally using JSON files.

---

# Table of Contents

* [Project Overview](#-project-overview)
* [Project Objectives](#-project-objectives)
* [Current Scope](#-current-scope)
* [Features](#-features)
* [User Roles](#-user-roles)
* [Technology Stack](#-technology-stack)
* [Project Architecture](#-project-architecture)
* [Project Structure](#-project-structure)
* [JSON Data Storage](#-json-data-storage)
* [Models](#-models)
* [Model Relationships](#-model-relationships)
* [Authentication](#-authentication)
* [Password Security](#-password-security)
* [Validation](#-validation)
* [Object-Oriented Programming Concepts](#-object-oriented-programming-concepts)
* [Installation](#-installation)
* [Running the Application](#-running-the-application)
* [Testing](#-testing)
* [Git and Version Control](#-git-and-version-control)
* [Development Guidelines](#-development-guidelines)
* [Project Development Stages](#-project-development-stages)
* [Future Improvements](#-future-improvements)
* [Security Notice](#-security-notice)
* [Contributing](#-contributing)

---

# Project Overview

The Hospital Management System is a Python-based command-line application designed to demonstrate how Object-Oriented Programming can be used to build a real-world management system.

The system allows different types of hospital users to log in and perform actions according to their roles.

The current system contains:

* Administrators
* Doctors
* Patients
* Appointments

Each user type has its own Python model.

The application uses JSON files as a simple local data store.

The project is intentionally kept simple so that the main focus remains on Python programming, OOP, application logic, authentication, validation, data storage, and testing.

---

# Project Objectives

The main objectives of this project are:

1. Practice Python 3 programming.
2. Apply Object-Oriented Programming concepts.
3. Build well-defined Python classes.
4. Understand classes and instances.
5. Understand relationships between objects.
6. Implement one-to-many relationships.
7. Practice encapsulation.
8. Use inheritance where appropriate.
9. Use static methods where appropriate.
10. Implement user authentication.
11. Protect passwords using password hashing.
12. Validate user input.
13. Store application data using JSON.
14. Read and write JSON files using Python.
15. Separate application responsibilities into modules.
16. Practice error handling.
17. Write automated tests using Pytest.
18. Practice Git and GitHub workflows.
19. Build a complete command-line Python application.
20. Create a foundation that can later be expanded into a web-based application.

---

# Current Scope

The current version focuses on **Python and Object-Oriented Programming**.

The system includes four main models:

* `Patient`
* `Doctor`
* `Admin`
* `Appointment`

The system supports:

* User authentication
* Role-based access
* Password hashing
* Patient registration
* Doctor registration
* Viewing patients
* Viewing doctors
* Creating appointments
* Viewing appointments
* JSON data storage
* Input validation
* Error handling
* Automated testing with Pytest

The project is intentionally built without:

* React
* Flask
* MySQL
* PostgreSQL
* REST APIs
* M-Pesa/payment integration
* Email/SMS notifications

These technologies and features can be introduced in future versions.

---

# Features

## Authentication

Users can log into the system using a username and password.

The system identifies the user's role and displays the appropriate menu.

## Role-Based Access

Different users have different permissions.

### Administrator

An administrator can:

* Register doctors
* Register patients
* View doctors
* View patients
* View appointments

### Doctor

A doctor can:

* Log in
* View their appointments
* View patients
* Log out

### Patient

A patient can:

* Log in
* View their profile
* View their appointments
* Log out

## Appointment Management

The system allows appointments to connect a patient with a doctor.

Each appointment contains:

* Appointment ID
* Patient ID
* Doctor ID
* Date
* Time

## JSON Storage

Application data is stored locally using JSON files.

The current project uses:

```text
data/
├── users.json
└── appointments.json
```

---

# User Roles

The system has three user roles.

```text
Admin
  │
  ├── Register Doctors
  ├── Register Patients
  ├── View Doctors
  ├── View Patients
  └── View Appointments


Doctor
  │
  ├── View Appointments
  └── View Patients


Patient
  │
  ├── View Profile
  └── View Appointments
```

---

# Technology Stack

The current project uses:

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python 3   | Main programming language |
| OOP        | Application design        |
| JSON       | Local data storage        |
| bcrypt     | Password hashing          |
| Pytest     | Automated testing         |
| Git        | Version control           |
| GitHub     | Code hosting              |

---

# Project Architecture

The project follows a simple layered structure.

```text
User
  ↓
main.py
  ↓
Services
  ↓
Models / Utilities
  ↓
JSON Storage
```

For example, registering a patient follows this flow:

```text
Admin
  ↓
main.py
  ↓
patient_service.py
  ↓
validation.py
  ↓
security.py
  ↓
storage.py
  ↓
users.json
```

The application is separated into different responsibilities so that each part of the project has a clear purpose.

---

# Project Structure

```text
hospital-management-system/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── patient.py
│   │   ├── doctor.py
│   │   ├── admin.py
│   │   └── appointment.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── patient_service.py
│   │   ├── doctor_service.py
│   │   └── appointment_service.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── storage.py
│       ├── security.py
│       └── validation.py
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
│   └── test_appointment.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# JSON Data Storage

The application uses two JSON files.

## users.json

`users.json` stores the three types of users:

```json
{
    "admins": [],
    "doctors": [],
    "patients": []
}
```

Each section contains the relevant users.

For example:

```text
users.json
    │
    ├── admins
    ├── doctors
    └── patients
```

## appointments.json

Appointments are stored separately:

```json
{
    "appointments": []
}
```

An appointment connects a patient and a doctor using their IDs.

For example:

```text
Patient P001
     ↓
Appointment AP001
     ↓
Doctor D001
```

When new information is added through the application, Python automatically updates the appropriate JSON file.

---

# Models

The project has four main models.

## Patient

The `Patient` model represents a hospital patient.

A patient contains information such as:

* Patient ID
* Name
* Username
* Password
* Age
* Gender
* Phone

## Doctor

The `Doctor` model represents a hospital doctor.

A doctor contains:

* Doctor ID
* Name
* Username
* Password
* Specialization

## Admin

The `Admin` model represents a hospital administrator.

An administrator contains:

* Admin ID
* Name
* Username
* Password

## Appointment

The `Appointment` model represents a scheduled meeting between a patient and doctor.

An appointment contains:

* Appointment ID
* Patient ID
* Doctor ID
* Date
* Time

---

# Model Relationships

The main relationship in the system is between patients, doctors, and appointments.

An appointment belongs to one patient and one doctor.

```text
Patient
   │
   │ patient_id
   ▼
Appointment
   ▲
   │ doctor_id
   │
Doctor
```

For example:

```text
Patient:
P001 - Kevin

Doctor:
D001 - Dr. Kamau

Appointment:
AP001
Patient ID: P001
Doctor ID: D001
Date: 2026-09-15
Time: 10:00
```

The IDs allow the system to connect the objects without duplicating all of their information.

---

# Authentication

Authentication allows users to log into the application.

The login process is:

```text
Username + Password
        ↓
Authentication Service
        ↓
Read users.json
        ↓
Find user
        ↓
Verify password
        ↓
Identify role
        ↓
Display correct menu
```

The system supports authentication for:

* Admins
* Doctors
* Patients

---

# Password Security

Passwords are not stored as plain text.

Instead, the project uses **bcrypt** to hash passwords.

The process is:

```text
User enters password
        ↓
bcrypt hashes password
        ↓
Hash is stored in users.json
```

During login:

```text
User enters password
        ↓
bcrypt verifies password
        ↓
Password correct?
        ↓
Login successful
```

This prevents the original password from being directly stored in the JSON file.

---

# Validation

The application validates user input before storing information.

Examples include:

* Required fields cannot be empty.
* Age must be a valid number.
* Usernames should be unique.
* Phone numbers should follow the expected format.
* Appointment information must be valid.
* Passwords must meet the application's requirements.

Validation helps prevent incorrect data from being stored.

---

# Object-Oriented Programming Concepts

The project demonstrates several OOP concepts.

## Classes

The system uses classes such as:

```text
Patient
Doctor
Admin
Appointment
```

## Instances

Objects are created from these classes.

For example:

```text
Patient class
      ↓
Kevin object
```

## Encapsulation

Data and behavior are organized inside classes.

## Inheritance

Inheritance can be used where it provides a clear benefit without unnecessarily complicating the project.

## Static Methods

Static methods can be used for operations that belong to a class but do not require a specific object instance.

## Object Relationships

Appointments demonstrate relationships between different objects.

---

# Installation

Clone the project repository and enter the project directory.

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

# Running the Application

Start the application with:

```bash
python3 app/main.py
```

The application will display the main menu:

```text
================================
     HOSPITAL MANAGEMENT SYSTEM
================================

1. Login
2. Exit
```

---

# Testing

The project uses **Pytest** for automated testing.

Run all tests with:

```bash
pytest
```

Tests cover areas such as:

* Patient creation
* Doctor creation
* Admin creation
* Authentication
* Password hashing
* Appointment creation

Successful tests should produce a result similar to:

```text
10 passed
```

The exact number of tests may change as the project grows.

---

# Git and Version Control

Git is used to track changes to the project.

Basic workflow:

```bash
git status
git add .
git commit -m "Add patient model"
git push
```

The project is hosted on GitHub so that team members can collaborate and the development history can be maintained.

---

# Development Guidelines

The project follows these principles:

1. Keep each class focused on its responsibility.
2. Keep services responsible for application logic.
3. Keep utility functions reusable.
4. Do not store plain-text passwords.
5. Validate user input before saving it.
6. Keep JSON data organized.
7. Write tests for important functionality.
8. Use meaningful variable and function names.
9. Make small Git commits.
10. Keep the project simple and understandable.

---

# Project Development Stages

The project is developed in stages.

## Stage 1 — Project Setup

* Create project structure
* Create virtual environment
* Install dependencies
* Configure Git
* Create JSON files

## Stage 2 — Models

Create:

* Patient
* Doctor
* Admin
* Appointment

## Stage 3 — Storage

Implement:

* Reading JSON
* Writing JSON
* Updating JSON data

## Stage 4 — Security

Implement:

* Password hashing
* Password verification

## Stage 5 — Authentication

Implement:

* Login
* User identification
* Role-based access

## Stage 6 — Services

Implement:

* Patient management
* Doctor management
* Appointment management

## Stage 7 — Validation

Add input validation and error handling.

## Stage 8 — CLI

Connect everything through the command-line interface.

## Stage 9 — Testing

Write and run Pytest tests.

## Stage 10 — GitHub

Commit and push the completed project to GitHub.

---

# Future Improvements

Future versions may introduce:

* Nurses
* Receptionists
* Medical records
* Medications
* Prescriptions
* Billing
* MySQL or PostgreSQL
* Flask backend
* REST APIs
* React frontend
* Online deployment
* Email notifications
* SMS notifications
* M-Pesa/payment integration
* Advanced user permissions

These features are outside the scope of the current Python OOP version.

---

# Security Notice

This project is an educational application using local JSON files.

It should not be used to store real patient information or sensitive medical data in its current form.

A production hospital system would require stronger security, access controls, encryption, auditing, secure databases, backups, and compliance with applicable healthcare and privacy requirements.

---

# Contributing

Contributions are welcome.

When contributing:

1. Create a new branch.
2. Make your changes.
3. Test the application.
4. Run Pytest.
5. Commit your changes with a clear message.
6. Push the branch to GitHub.
7. Create a pull request.

---

# Project Development Flow

The core development flow of the current project is:

```text
Python 3
    ↓
OOP Classes
    ↓
Models
    ↓
Services / Application Logic
    ↓
Validation + Security
    ↓
JSON Storage
    ↓
users.json / appointments.json
    ↓
Pytest
    ↓
Working CLI Application
```

The overall application flow is:

```text
User
  ↓
main.py
  ↓
Login
  ↓
Authentication
  ↓
Identify Role
  ↓
Admin / Doctor / Patient Menu
  ↓
Services
  ↓
Models + Utilities
  ↓
JSON Files
```

The goal is to build a complete, understandable Python application while developing a strong foundation in Object-Oriented Programming and software development.
