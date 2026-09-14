
import json
import os

# Same 6 specialities used in appointment.py, so a doctor's speciality
# always matches one that a patient can search for.
SPECIALITIES = [
    "General",
    "Cardiology",
    "Dermatology",
    "Pediatrics",
    "Dentistry",
    "Orthopedics",
]


class User:
    """
    Base class for every account in the system.

    Encapsulation: attributes start with an underscore and are only
    read/changed through the methods below, instead of being accessed
    directly from outside the class.
    """

    def __init__(self, user_id, name, username, password, role):
        self._user_id = user_id
        self._name = name
        self._username = username
        self._password = password
        self._role = role

    def get_id(self):
        return self._user_id

    def get_name(self):
        return self._name

    def get_username(self):
        return self._username

    def get_role(self):
        return self._role

    @property
    def role(self):
        """
        Same value as get_role(), but as a property instead of a method.
        This exists because utils/decorators.py checks 'current_user.role'
        directly (no parentheses), so we need both styles to work.
        """
        return self._role

    def check_password(self, attempt):
        """Returns True if the given password matches this user's password."""
        return self._password == attempt

    def to_dict(self):
        return {
            "user_id": self._user_id,
            "name": self._name,
            "username": self._username,
            "password": self._password,
            "role": self._role,
        }


class Patient(User):
    """A Patient is a User with role 'patient'. Inherits everything from User."""

    def __init__(self, user_id, name, username, password):
        super().__init__(user_id, name, username, password, role="patient")


class Doctor(User):
    """A Doctor is a User with role 'doctor', and also has a speciality."""

    def __init__(self, user_id, name, username, password, speciality):
        super().__init__(user_id, name, username, password, role="doctor")
        self._speciality = speciality

    def get_speciality(self):
        return self._speciality

    def to_dict(self):
        data = super().to_dict()
        data["speciality"] = self._speciality
        return data


class Admin(User):
    """An Admin is a User with role 'admin'. Inherits everything from User."""

    def __init__(self, user_id, name, username, password):
        super().__init__(user_id, name, username, password, role="admin")


class UserManager:
    """
    Keeps the list of all users and handles saving/loading them to a
    JSON file, plus registration and login.
    """

    def __init__(self, filename="data/users.json"):
        self._filename = filename
        self._users = []
        self._load()
        if not self._users:
            self._create_demo_users()

    def _deserialize_user(self, item):
        """Build a User object from a JSON record, compatible with both list and dict storage."""
        role = item.get("role")
        if role == "doctor":
            return Doctor(
                item["user_id"],
                item["name"],
                item["username"],
                item["password"],
                item["speciality"],
            )
        if role == "admin":
            return Admin(item["user_id"], item["name"], item["username"], item["password"])
        return Patient(item["user_id"], item["name"], item["username"], item["password"])

    def _load(self):
        """Reads users from the JSON file, if it exists."""
        if os.path.exists(self._filename):
            with open(self._filename, "r") as file:
                data = json.load(file)
                for item in data:
                    if item["role"] == "doctor":
                        user = Doctor(
                            item["user_id"], item["name"], item["username"],
                            item["password"], item["speciality"],
                        )
                    elif item["role"] == "admin":
                        user = Admin(item["user_id"], item["name"], item["username"], item["password"])
                    else:
                        user = Patient(item["user_id"], item["name"], item["username"], item["password"])
                    self._users.append(user)

    def _save(self):
        """Writes all users to the JSON file."""
        with open(self._filename, "w") as file:
            data = [user.to_dict() for user in self._users]
            json.dump(data, file, indent=4)

    def _generate_id(self, role):
        """Creates a new user ID like P1, D1, A1 depending on the role."""
        prefix = {"patient": "P", "doctor": "D", "admin": "A"}[role]
        count = len([u for u in self._users if u.get_role() == role])
        return prefix + str(count + 1)

    def _create_demo_users(self):
        """Adds a few starter accounts so the program is usable right away."""
        self._users.append(Doctor(self._generate_id("doctor"), "Dr. Alice Smith", "asmith", "doc123", "Cardiology"))
        self._users.append(Doctor(self._generate_id("doctor"), "Dr. Ben Otieno", "botieno", "doc123", "Dentistry"))
        self._users.append(Patient(self._generate_id("patient"), "Jane Doe", "jdoe", "pat123"))
        self._users.append(Admin(self._generate_id("admin"), "System Admin", "admin", "admin123"))
        self._save()

    def register(self, name, username, password, role, speciality=None):
        """Creates a new account. Returns the new user, or None if the username is taken."""
        if self.find_by_username(username) is not None:
            print("That username is already taken.")
            return None

        user_id = self._generate_id(role)

        if role == "doctor":
            if speciality not in SPECIALITIES:
                print("That speciality does not exist. Choose from:", SPECIALITIES)
                return None
            new_user = Doctor(user_id, name, username, password, speciality)
        elif role == "admin":
            new_user = Admin(user_id, name, username, password)
        else:
            new_user = Patient(user_id, name, username, password)

        self._users.append(new_user)
        self._save()
        return new_user

    def login(self, username, password):
        """Returns the matching user if the username/password are correct, else None."""
        user = self.find_by_username(username)
        if user is not None and user.check_password(password):
            return user
        return None

    def find_by_username(self, username):
        for user in self._users:
            if user.get_username() == username:
                return user
        return None

    def get_all_doctors(self):
        return [u for u in self._users if u.get_role() == "doctor"]

    def get_doctors_by_speciality(self, speciality):
        return [u for u in self.get_all_doctors() if u.get_speciality() == speciality]