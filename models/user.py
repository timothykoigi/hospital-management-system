import bcrypt
import json
import os

SPECIALITIES = [
    "General",
    "Cardiology",
    "Dermatology",
    "Pediatrics",
    "Dentistry",
    "Orthopedics",
]


class User:
    def __init__(self,user_id,name,username,password,role,password_is_hashed=False):
        self._user_id = user_id
        self._name = name
        self._username = username
        self._role = role

        if password_is_hashed:
            self._password = password
        else:
            self._password = self.hash_password(password)

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

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
        return self._role

    def check_password(self, attempt):
        return bcrypt.checkpw(attempt.encode("utf-8"),self._password.encode("utf-8"))

    def to_dict(self):
        return {
            "user_id": self._user_id,
            "name": self._name,
            "username": self._username,
            "password": self._password,
            "role": self._role,
        }


class Patient(User):
    def __init__(self,user_id,name,username,password,password_is_hashed=False,):
        super().__init__(user_id,name,username,password,role="patient",password_is_hashed=password_is_hashed,)


class Doctor(User):
    def __init__(self,user_id,name,username,password,speciality,password_is_hashed=False,):
        super().__init__(user_id,name,username,password,role="doctor",password_is_hashed=password_is_hashed,)

        self._speciality = speciality

    def get_speciality(self):
        return self._speciality

    def to_dict(self):
        data = super().to_dict()
        data["speciality"] = self._speciality
        return data


class Admin(User):
    def __init__(self,user_id,name,username,password,password_is_hashed=False,):
        super().__init__(user_id,name,username,password,role="admin",password_is_hashed=password_is_hashed,)





class UserManager:
    def __init__(self, filename="data/users.json"):
        self._filename = filename
        self._users = []
        self._load()

        if not self._users:
            self._create_demo_users()

    def _load(self):
        if os.path.exists(self._filename):
            with open(self._filename, "r", encoding="utf-8") as file:
                data = json.load(file)

                for item in data:
                    if item["role"] == "doctor":
                        user = Doctor(
                            item["user_id"],
                            item["name"],
                            item["username"],
                            item["password"],
                            item["speciality"],
                            password_is_hashed=True,
                        )
                    elif item["role"] == "admin":
                        user = Admin(
                            item["user_id"],
                            item["name"],
                            item["username"],
                            item["password"],
                            password_is_hashed=True,
                        )
                    else:
                        user = Patient(
                            item["user_id"],
                            item["name"],
                            item["username"],
                            item["password"],
                            password_is_hashed=True,
                        )

                    self._users.append(user)

    def _save(self):
        data = [user.to_dict() for user in self._users]

        parent = os.path.dirname(self._filename)

        if parent:
            os.makedirs(parent, exist_ok=True)

        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)


    def _generate_id(self, role):
        prefix = {
            "patient": "P",
            "doctor": "D",
            "admin": "A",
        }[role]

        count = len([user for user in self._users if user.get_role() == role])
        return prefix + str(count + 1)
    

    def _create_demo_users(self):
        self._users.append(Doctor(self._generate_id("doctor"),"Dr. Ben Otieno","botieno","doc123","Dentistry"))
        self._users.append(Patient(self._generate_id("patient"),"Jane Doe","jdoe","pat123"))
        self._users.append(Admin(self._generate_id("admin"),"System Admin","admin","admin123"))

        self._save()

    def register(self,name,username,password,role,speciality=None,):
        if self.find_by_username(username) is not None:
            print("That username is already taken.")
            return None

        user_id = self._generate_id(role)

        if role == "doctor":
            if speciality not in SPECIALITIES:
                print("That speciality does not exist. ")
                return None
            new_user = Doctor(user_id,name,username,password,speciality)
        elif role == "admin":
            new_user = Admin(user_id,name,username,password)
        else:
            new_user = Patient(user_id,name,username,password)

        self._users.append(new_user)
        self._save()
        return new_user

    def login(self, username, password):
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
        return [user for user in self._users if user.get_role() == "doctor"]

    def get_doctors_by_speciality(self, speciality):
        return [user for user in self.get_all_doctors() if user.get_speciality() == speciality]
